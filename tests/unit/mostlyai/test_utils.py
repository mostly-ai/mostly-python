import base64
import io
import math
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, Mock, ANY

import pandas as pd
import pytest
from rich.console import Console

from mostlyai.model import (
    JobProgress,
    ProgressStatus,
    ProgressStep,
    ProgressValue,
    StepCode,
    Generator,
    Metadata,
    SourceTable,
)
from mostlyai.utils import (
    _convert_to_base64,
    _job_wait,
    _read_table_from_path,
    _harmonize_sd_config,
)

UTILS_MODULE = "mostlyai.utils"


def test_convert_to_base64():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    base64_str = _convert_to_base64(df)

    assert isinstance(base64_str, str)

    # Decode the Base64 string back to a DataFrame
    decoded_bytes = base64.b64decode(base64_str)
    decoded_buffer = io.BytesIO(decoded_bytes)
    decoded_df = pd.read_parquet(decoded_buffer)

    # Compare the original DataFrame with the decoded one
    pd.testing.assert_frame_equal(df, decoded_df)


def test_read_table_from_path():
    # Create a temporary CSV file for testing
    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w", delete=False) as tmp:
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        df.to_csv(tmp.name, index=False)
        tmp_path = tmp.name

    name, read_df = _read_table_from_path(tmp_path)

    assert name == Path(tmp_path).stem
    pd.testing.assert_frame_equal(read_df, df)


@pytest.mark.skip("Fails on remote during CI")
def test__job_wait():
    # Timeline in seconds with job and step progression:
    # | Time (seconds):   | 0 | 1 | 2 | 3 | 4 | 5 |
    # |-------------------|---|---|---|---|---|---|
    # | Job Progress:     | 0 | 1 | 2 | 3 | 4 | 5 | (max = 5)
    # | Step 1 Progress:  | 0 | 1 | 2 | 3 |   |   | (max = 3, starts at 0s)
    # | Step 2 Progress:  |   | 0 | 1 | 2 | 3 |   | (max = 3, starts at 1s)
    # | Step 3 Progress:  |   |   |   | 0 | 1 | 2 | (max = 2, starts at 3s)

    # Create initial job state
    job_start_date = datetime.now()
    job = JobProgress(
        id="job1",
        start_date=job_start_date,
        progress=ProgressValue(max=5, value=0),
        status=ProgressStatus.queued,
        steps=[
            ProgressStep(
                id="step1",
                status=ProgressStatus.queued,
                step_code=StepCode.train_model,
                progress=ProgressValue(value=0, max=3),
            ),
            ProgressStep(
                id="step2",
                status=ProgressStatus.queued,
                step_code=StepCode.train_model,
                progress=ProgressValue(value=0, max=3),
            ),
            ProgressStep(
                id="step3",
                status=ProgressStatus.queued,
                step_code=StepCode.train_model,
                progress=ProgressValue(value=0, max=2),
            ),
        ],
    )

    # Callback function to update the job state

    def get_job_progress():
        current_time = datetime.now()
        elapsed = (current_time - job_start_date).total_seconds()

        # Set start times for each step
        step_start_times = [0, 1, 3]

        for i, step in enumerate(job.steps):
            step_elapsed = elapsed - step_start_times[i]
            if step_elapsed >= 0:
                if step.status == ProgressStatus.queued:
                    # print(f"Starting {step.id}")
                    step.status = ProgressStatus.in_progress
                    step.start_date = current_time

                # Update progress and status
                if step.status == ProgressStatus.in_progress:
                    step.progress.value = min(
                        math.floor(step_elapsed), step.progress.max
                    )
                    # print(f"{step.id} progress {step.progress.value}")
                    if step.progress.value >= step.progress.max:
                        # print(f"Stopping {step.id}")
                        step.status = ProgressStatus.done
                        step.end_date = current_time

        # Update overall job progress
        job.progress.value = min(math.floor(elapsed), job.progress.max)
        if job.progress.value >= job.progress.max:
            job.status = ProgressStatus.done
            job.end_date = current_time

        return job

    console = Console()
    with console.capture() as capture, patch(f"{UTILS_MODULE}.rich._console", console):
        _job_wait(get_job_progress, interval=1)

    actual_lines = [line.strip() for line in capture.get().splitlines()]
    expected_lines = [
        "Overall job progress       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:05",
        "Step common TRAIN_MODEL 💎 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:03",
        "Step common TRAIN_MODEL 💎 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:03",
        "Step common TRAIN_MODEL 💎 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:02",
    ]
    assert actual_lines == expected_lines


@pytest.fixture
def simple_sd_config():
    return {"tables": [{"name": "subject", "configuration": {}}]}


def test__harmonize_sd_config(simple_sd_config):
    mock_get_generator = Mock(
        side_effect=lambda id: Generator(
            id=id,
            training_status=ProgressStatus.done,
            metadata=Metadata(),
            tables=[SourceTable(id="some_id", name="table", columns=[])],
        )
    )

    config = _harmonize_sd_config(
        generator="some_id", get_generator=mock_get_generator, config=simple_sd_config
    )
    assert config == {
        "generatorId": "some_id",
        "tables": [{"configuration": {}, "name": "subject"}],
    }
    mock_get_generator.assert_not_called()

    config = _harmonize_sd_config(
        generator="other_id",
        get_generator=mock_get_generator,
        size=1234,
        seed=pd.DataFrame(),
    )
    mock_get_generator.assert_called_once_with("other_id")
    assert config == {
        "generatorId": "other_id",
        "tables": [
            {
                "name": "table",
                "configuration": {
                    "sampleSize": 1234,
                    "sampleSeedData": ANY,
                    "sampleSeedDict": None,
                },
            }
        ],
    }
