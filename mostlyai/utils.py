import base64
import io
import time
import warnings
from pathlib import Path
from typing import Callable, Union, Optional, Any, Literal

import pandas as pd
import csv
import rich
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.style import Style

from mostlyai.model import (
    Connector,
    Generator,
    ProgressStatus,
    StepCode,
    SyntheticDataset,
)
from mostlyai.naming_conventions import map_camel_to_snake_case

warnings.simplefilter("always", DeprecationWarning)


def _job_wait(
    get_progress: Callable,
    interval: float,
    progress_bar: bool = True,
) -> None:
    # ensure that interval is at least 1 sec
    interval = max(interval, 1)
    # retrieve current JobProgress
    job = get_progress()
    if progress_bar:
        # initialize progress bars
        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(
                style=Style(color="rgb(245,245,245)"),
                complete_style=Style(color="rgb(66,77,179)"),
                finished_style=Style(color="rgb(36,219,149)"),
                pulse_style=Style(color="rgb(245,245,245)"),
            ),
            TaskProgressColumn(),
            TimeElapsedColumn(),
        )
        progress_bars = {
            "overall": progress.add_task(
                description="[bold]Overall job progress[/b]",
                start=job.start_date is not None,
                completed=0,
                total=job.progress.max,
            )
        }
        for step in job.steps:
            step_code = step.step_code.value
            if step_code == StepCode.train_model.value:
                step_code += " :gem:"
            progress_bars |= {
                step.id: progress.add_task(
                    description=f"Step {step.model_label or 'common'} [#808080]{step_code}[/]",
                    start=step.start_date is not None,
                    completed=0,
                    total=step.progress.max,
                )
            }
    try:
        if progress_bar:
            # loop until job has completed
            progress.start()
        while True:
            # sleep for interval seconds
            time.sleep(interval)
            # retrieve current JobProgress
            job = get_progress()
            if progress_bar:
                current_task_id = progress_bars["overall"]
                current_task = progress.tasks[current_task_id]
                if not current_task.started and job.start_date is not None:
                    progress.start_task(current_task_id)
                # update progress bars
                progress.update(
                    current_task_id,
                    total=job.progress.max,
                    completed=job.progress.value,
                )
                if current_task.started and job.end_date is not None:
                    progress.stop_task(current_task_id)
                for i, step in enumerate(job.steps):
                    current_task_id = progress_bars[step.id]
                    current_task = progress.tasks[current_task_id]
                    if not current_task.started and step.start_date is not None:
                        progress.start_task(current_task_id)
                    if step.progress.max > 0:
                        progress.update(
                            current_task_id,
                            total=step.progress.max,
                            completed=step.progress.value,
                        )
                    if current_task.started and step.end_date is not None:
                        progress.stop_task(current_task_id)
                    # break if step has failed or been canceled
                    if step.status in (ProgressStatus.failed, ProgressStatus.canceled):
                        rich.print(
                            f"[red]Step {step.model_label} {step.step_code.value} {step.status.lower()}"
                        )
                        progress.stop()
                        return
                # check whether we are done
                if job.progress.value >= job.progress.max:
                    time.sleep(1)  # give the system a moment
                    progress.stop()
                    return
            else:
                if job.end_date or job.progress in (
                    ProgressStatus.failed,
                    ProgressStatus.canceled,
                ):
                    rich.print(f"Job {job.status.lower()}")
                    return
    except KeyboardInterrupt:
        rich.print(
            f"[red]Step {step.model_label} {step.step_code.value} {step.status.lower()}"
        )
        progress.stop()
        return


def _convert_to_base64(
    df: Union[pd.DataFrame, list[dict[str, Any]]],
    format: Literal["parquet", "jsonl"] = "parquet",
) -> str:
    # Save the DataFrame to a buffer in Parquet / JSONL format
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    buffer = io.BytesIO()
    if format == "parquet":
        df.to_parquet(buffer, index=False)
    else:  # format == "jsonl"
        df.to_json(buffer, orient="records", date_format="iso", lines=True, index=False)
    buffer.seek(0)
    binary_data = buffer.read()
    base64_encoded_str = base64.b64encode(binary_data).decode()
    return base64_encoded_str


def _get_subject_table_names(generator: Generator) -> list[str]:
    subject_tables = []
    for table in generator.tables:
        ctx_fks = [fk for fk in table.foreign_keys or [] if fk.is_context]
        if len(ctx_fks) == 0:
            subject_tables.append(table.name)
    return subject_tables


Seed = Union[pd.DataFrame, str, Path, list[dict[str, Any]]]


def _harmonize_sd_config(
    generator: Union[Generator, str, None] = None,
    get_generator: Union[Callable[[str], Generator], None] = None,
    size: Union[int, dict[str, int], None] = None,
    seed: Union[Seed, dict[str, Seed], None] = None,
    config: Union[dict, None] = None,
    name: Optional[str] = None,
) -> dict:
    config = config or {}
    size = size if size is not None else {}
    seed = seed if seed is not None else {}

    config = map_camel_to_snake_case(config)

    if isinstance(generator, Generator):
        generator_id = str(generator.id)
    elif generator is not None:
        generator_id = str(generator)
    elif "generator_id" not in config:
        raise ValueError(
            "Either a generator or a configuration with a generator_id must be provided."
        )

    if (
        not isinstance(size, dict)
        or not isinstance(seed, dict)
        or "tables" not in config
    ):
        if not isinstance(generator, Generator):
            generator = get_generator(generator_id)
        subject_tables = _get_subject_table_names(generator)
    else:
        subject_tables = []

    # insert generator_id into config
    config["generator_id"] = generator_id

    # normalize size
    if not isinstance(size, dict):
        size = {table: size for table in subject_tables}

    # normalize seed
    if not isinstance(seed, dict):
        seed = {table: seed for table in subject_tables}

    # insert name into config
    if name is not None:
        config |= {"name": name}

    # infer tables if not provided
    if "tables" not in config:
        config["tables"] = []
        for table in generator.tables:
            configuration = {
                "sample_size": None,
                "sample_seed_data": None,
                "sample_seed_dict": None,
            }
            if table.name in subject_tables:
                configuration["sample_size"] = size.get(table.name)
                configuration["sample_seed_data"] = (
                    seed.get(table.name)
                    if not isinstance(seed.get(table.name), list)
                    else None
                )
                configuration["sample_seed_dict"] = (
                    seed.get(table.name)
                    if isinstance(seed.get(table.name), list)
                    else None
                )
            config["tables"].append(
                {"name": table.name, "configuration": configuration}
            )

    # convert `sample_seed_data` to base64-encoded Parquet files
    # convert `sample_seed_dict` to base64-encoded dictionaries
    tables = config["tables"] if "tables" in config else []
    for table in tables:
        if (
            "sample_seed_data" in table["configuration"]
            and table["configuration"]["sample_seed_data"] is not None
        ):
            if isinstance(table["configuration"]["sample_seed_data"], pd.DataFrame):
                table["configuration"]["sample_seed_data"] = _convert_to_base64(
                    table["configuration"]["sample_seed_data"]
                )
            elif isinstance(table["configuration"]["sample_seed_data"], (Path, str)):
                _, df = _read_table_from_path(
                    table["configuration"]["sample_seed_data"]
                )
                table["configuration"]["sample_seed_data"] = _convert_to_base64(df)
                del df
            else:
                raise ValueError("sample_seed_data must be a DataFrame or a file path")
        if (
            "sample_seed_dict" in table["configuration"]
            and table["configuration"]["sample_seed_dict"] is not None
        ):
            table["configuration"]["sample_seed_dict"] = _convert_to_base64(
                table["configuration"]["sample_seed_dict"], format="jsonl"
            )

    return config


def _read_table_from_path(path: Union[str, Path]) -> (str, pd.DataFrame):
    # read data from file
    fn = str(path)
    if fn.lower().endswith((".pqt", ".parquet")):
        df = pd.read_parquet(fn)
    else:
        delimiter = ","
        if fn.lower().endswith((".csv", ".tsv")):
            try:
                with open(fn) as f:
                    header = f.readline()
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(header, ",;|\t' :").delimiter
            except csv.Error:
                # happens for example for single column CSV files
                pass
        df = pd.read_csv(fn, low_memory=False, delimiter=delimiter)
    if fn.lower().endswith((".gz", ".gzip", ".bz2")):
        fn = fn.rsplit(".", 1)[0]
    name = Path(fn).stem
    return name, df


ShareableResource = Union[Connector, Generator, SyntheticDataset]
