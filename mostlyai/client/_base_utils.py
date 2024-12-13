import base64
import io
import warnings
from pathlib import Path
from typing import Union, Any, Literal

import pandas as pd
import csv

warnings.simplefilter("always", DeprecationWarning)


def convert_to_base64(
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


def read_table_from_path(path: Union[str, Path]) -> (str, pd.DataFrame):
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
