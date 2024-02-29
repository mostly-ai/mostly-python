import base64
import io
import tempfile
from pathlib import Path

import pandas as pd

from mostlyai.utils import (
    _convert_df_to_base64,
    _get_subject_table_names,
    _get_table_name_index,
    _read_table_from_path,
)


def test_convert_df_to_base64():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    base64_str = _convert_df_to_base64(df)

    assert isinstance(base64_str, str)

    # Decode the Base64 string back to a DataFrame
    decoded_bytes = base64.b64decode(base64_str)
    decoded_buffer = io.BytesIO(decoded_bytes)
    decoded_df = pd.read_parquet(decoded_buffer)

    # Compare the original DataFrame with the decoded one
    pd.testing.assert_frame_equal(df, decoded_df)


def test_get_subject_table_names():
    config = {
        "tables": [
            {"name": "table1", "foreign_keys": [{"is_context": True}]},
            {"name": "table2", "foreign_keys": [{"is_context": False}]},
            {"name": "table3", "foreign_keys": []},
        ]
    }
    subject_tables = _get_subject_table_names(config)
    assert subject_tables == ["table2", "table3"]


def test_get_table_name_index():
    config = {
        "tables": [
            {"name": "table1"},
            {"name": "table2"},
            {"name": "table3"},
        ]
    }
    table_name_index = _get_table_name_index(config)
    assert table_name_index == {"table1": 0, "table2": 1, "table3": 2}


def test_read_table_from_path():
    # Create a temporary CSV file for testing
    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w", delete=False) as tmp:
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        df.to_csv(tmp.name, index=False)
        tmp_path = tmp.name

    name, read_df = _read_table_from_path(tmp_path)

    assert name == Path(tmp_path).stem
    pd.testing.assert_frame_equal(read_df, df)
