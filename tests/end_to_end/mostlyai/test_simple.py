import time

import pandas as pd


def test_simple_flat(mostly):
    df = pd.DataFrame({"a": [1, 2, 3] * 100, "b": [4, 5, 6] * 100})
    g = mostly.train(df)
    sd = mostly.generate(g)
    # time.sleep(5)
    syn = sd.data()
    assert syn.shape == (300, 2)
    assert syn.columns.tolist() == ["a", "b"]
