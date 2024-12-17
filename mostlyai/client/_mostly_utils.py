import time
from pathlib import Path
from typing import Callable, Union, Any, Optional

import pandas as pd
import rich
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
)
from rich.style import Style

from mostlyai.client._base_utils import convert_to_base64, read_table_from_path
from mostlyai.client.domain import (
    StepCode,
    ProgressStatus,
    Generator,
    SyntheticDatasetConfig,
    SyntheticProbeConfig,
    SyntheticTableConfiguration,
    SyntheticTableConfig,
    Connector,
    SyntheticDataset,
)
from mostlyai.client._naming_conventions import map_camel_to_snake_case


def job_wait(
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
                    time.sleep(1)  # give the system a moment to update the status
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


def _get_subject_table_names(generator: Generator) -> list[str]:
    subject_tables = []
    for table in generator.tables:
        ctx_fks = [fk for fk in table.foreign_keys or [] if fk.is_context]
        if len(ctx_fks) == 0:
            subject_tables.append(table.name)
    return subject_tables


Seed = Union[pd.DataFrame, str, Path, list[dict[str, Any]]]


def harmonize_sd_config(
    generator: Union[Generator, str, None] = None,
    get_generator: Union[Callable[[str], Generator], None] = None,
    size: Union[int, dict[str, int], None] = None,
    seed: Union[Seed, dict[str, Seed], None] = None,
    config: Union[SyntheticDatasetConfig, SyntheticProbeConfig, dict, None] = None,
    config_type: Union[
        type[SyntheticDatasetConfig], type[SyntheticProbeConfig], None
    ] = None,
    name: Optional[str] = None,
) -> Union[SyntheticDatasetConfig, SyntheticProbeConfig]:
    config_type = config_type or SyntheticDatasetConfig
    if config is None:
        config = config_type()
    elif isinstance(config, dict):
        config = map_camel_to_snake_case(config)
        config = config_type(**config)

    size = size if size is not None else {}
    seed = seed if seed is not None else {}

    if isinstance(generator, Generator):
        generator_id = str(generator.id)
    elif generator is not None:
        generator_id = str(generator)
    elif not config.generator_id:
        raise ValueError(
            "Either a generator or a configuration with a generator_id must be provided."
        )
    else:
        generator_id = config.generator_id

    if not isinstance(size, dict) or not isinstance(seed, dict) or not config.tables:
        if not isinstance(generator, Generator):
            generator = get_generator(generator_id)
        subject_tables = _get_subject_table_names(generator)
    else:
        subject_tables = []

    # insert generator_id into config
    config.generator_id = generator_id

    # normalize size
    if not isinstance(size, dict):
        size = {table: size for table in subject_tables}

    # normalize seed
    if not isinstance(seed, dict):
        seed = {table: seed for table in subject_tables}

    # insert name into config
    if name is not None:
        config.name = name

    # infer tables if not provided
    if not config.tables:
        config.tables = []
        for table in generator.tables:
            configuration = SyntheticTableConfiguration(
                sample_size=None,
                sample_seed_data=None,
                sample_seed_dict=None,
            )
            if table.name in subject_tables:
                configuration.sample_size = size.get(table.name)
                configuration.sample_seed_data = (
                    seed.get(table.name)
                    if not isinstance(seed.get(table.name), list)
                    else None
                )
                configuration.sample_seed_dict = (
                    seed.get(table.name)
                    if isinstance(seed.get(table.name), list)
                    else None
                )
            config.tables.append(
                SyntheticTableConfig(name=table.name, configuration=configuration)
            )

    # convert `sample_seed_data` to base64-encoded Parquet files
    # convert `sample_seed_dict` to base64-encoded dictionaries
    for table in config.tables:
        if not table.configuration:
            continue
        if table.configuration.sample_seed_data is not None:
            if isinstance(table.configuration.sample_seed_data, pd.DataFrame):
                table.configuration.sample_seed_data = convert_to_base64(
                    table.configuration.sample_seed_data
                )
            elif isinstance(table.configuration.sample_seed_data, (Path, str)):
                _, df = read_table_from_path(table.configuration.sample_seed_data)
                table.configuration.sample_seed_data = convert_to_base64(df)
                del df
            else:
                raise ValueError("sample_seed_data must be a DataFrame or a file path")
        if table.configuration.sample_seed_dict is not None:
            table.configuration.sample_seed_dict = convert_to_base64(
                table.configuration.sample_seed_dict, format="jsonl"
            )

    return config


ShareableResource = Union[Connector, Generator, SyntheticDataset]
