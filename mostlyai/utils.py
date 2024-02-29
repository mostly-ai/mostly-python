import base64
import io
import time
from pathlib import Path
from typing import Callable, Union

import pandas as pd
import rich
from rich.progress import Progress

from mostlyai.model import (
    Connector,
    Generator,
    ProgressStatus,
    StepCode,
    SyntheticDataset,
)


def _job_wait(
    get_progress: Callable,
    interval: float,
) -> None:
    # ensure that interval is at least 1 sec
    interval = max(interval, 1)
    # retrieve current JobProgress
    job = get_progress()
    # initialize progress bars
    progress = Progress()
    progress_bars = {
        "overall": progress.add_task(
            description="[bold]Overall job progress[/b]",
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
                completed=0,
                total=1,
            )
        }
    try:
        # loop until job has completed
        progress.start()
        while True:
            # sleep for interval seconds
            time.sleep(interval)
            # retrieve current JobProgress
            job = get_progress()
            # update progress bars
            progress.update(
                progress_bars["overall"],
                total=job.progress.max,
                completed=job.progress.value,
            )
            for i, step in enumerate(job.steps):
                if step.progress.max > 0:
                    progress.update(
                        progress_bars[step.id],
                        total=step.progress.max,
                        completed=step.progress.value,
                    )
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
    except KeyboardInterrupt:
        rich.print("Exiting gracefully. Job will continue in the background.")
        progress.stop()
        return


def _convert_df_to_base64(df: pd.DataFrame) -> str:
    # Save the DataFrame to a buffer in Parquet format
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    binary_data = buffer.read()
    base64_encoded_str = base64.b64encode(binary_data).decode()
    return base64_encoded_str


def _get_subject_table_names(config) -> list[str]:
    subject_tables = []
    for table in config["tables"]:
        ctx_fks = [fk for fk in table.get("foreign_keys", []) if fk["is_context"]]
        if len(ctx_fks) == 0:
            subject_tables.append(table["name"])
    return subject_tables


def _get_table_name_index(config) -> dict[str, int]:
    table_name_index = {}
    for i, table in enumerate(config["tables"]):
        table_name_index[table["name"]] = i
    return table_name_index


def _read_table_from_path(path: Union[str, Path]) -> (str, pd.DataFrame):
    # read data from file
    fn = str(path)
    if fn.lower().endswith((".pqt", ".parquet")):
        df = pd.read_parquet(fn)
    else:
        df = pd.read_csv(fn, low_memory=False)
    if fn.endswith((".gz", ".gzip", ".bz2")):
        fn = fn.rsplit(".", 1)[0]
    name = Path(fn).stem
    return name, df


ShareableResource = Union[Connector, Generator, SyntheticDataset]
