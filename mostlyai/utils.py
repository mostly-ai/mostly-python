import base64
import io
import time
from typing import Callable
from uuid import UUID

import pandas as pd
from pydantic import BaseModel
from tqdm import tqdm

from mostlyai.model import ProgressStatus


def _job_wait(
    get_progress: Callable,
    interval: float,
) -> None:
    # ensure that interval is at least 1 sec
    interval = max(interval, 1)
    # remember start time of job
    start_time = time.time()
    # retrieve current JobProgress
    job = get_progress()
    # initialize progress bars
    progress_bars = {"overall": tqdm(total=job.progress.max, desc="Job status")}
    # for step in job.steps:
    #     progress_bars |= {
    #         step.id: tqdm(total=step.progress.max, desc=f"Step {step.model_label} {step.step_code}")
    #     }
    # loop until job has completed
    while True:
        # sleep for interval seconds
        time.sleep(interval)
        # retrieve current JobProgress
        job = get_progress()
        # update progress bars
        progress_bars["overall"].total = job.progress.max
        progress_bars["overall"].update(job.progress.value)
        for i, step in enumerate(job.steps):
            # progress_bars[step.id].total = step.progress.max
            # progress_bars[step.id].update(step.progress.value)
            # break if step has failed or been canceled
            if step.status == ProgressStatus.failed:
                print(f"Step {step.model_label} {step.step_code} failed")
                return
            if step.status == ProgressStatus.canceled:
                print(f"Step {step.model_label} {step.step_code} canceled")
                return
        # check whether we are done
        if job.progress.value >= job.progress.max:
            time.sleep(5)  # give the entity a chance to update
            print(f"Job finished in {time.time() - start_time:0.1f}s")
            return


def _convert_df_to_base64(df: pd.DataFrame) -> str:
    # Save the DataFrame to a buffer in Parquet format
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    binary_data = buffer.read()
    base64_encoded_str = base64.b64encode(binary_data).decode()
    return base64_encoded_str


def _as_dict(pydantic_or_dict):
    if isinstance(pydantic_or_dict, BaseModel):
        pydantic_or_dict = pydantic_or_dict.model_dump(by_alias=True)
    pydantic_or_dict = {
        k: str(v) if isinstance(v, UUID) else v for k, v in pydantic_or_dict.items()
    }
    return pydantic_or_dict


def _get_subject_table_names(config) -> list[str]:
    subject_tables = []
    for table in config["tables"]:
        ctx_fks = [fk for fk in table["foreign_keys"] if fk["is_context"]]
        if len(ctx_fks) == 0:
            subject_tables.append(table["name"])
    return subject_tables


def _get_table_name_index(config) -> dict[str, int]:
    table_name_index = {}
    for i, table in enumerate(config["tables"]):
        table_name_index[table["name"]] = i
    return table_name_index
