from time import sleep

import numpy as np
import pandas as pd
import pytest

from mostlyai.components import CreateGeneratorRequest, ForeignKey, TableItem
from mostlyai.exceptions import APIStatusError


# TODO adapt and place the test where it belongs
def test_simple_connect(mostly):
    c = mostly.connect(
        {
            "name": "AWS S3 michi",
            "type": "S3_STORAGE",
            "config": {"accessKey": "AKIAWMB6NNDXOHCX5PFY"},
            "secrets": {"secretKey": "***"},
        }
    )
