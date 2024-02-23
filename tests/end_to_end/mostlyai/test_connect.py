from time import sleep

import numpy as np
import pandas as pd
import pytest

from mostlyai.components import CreateGeneratorRequest, ForeignKey, TableItem
from mostlyai.exceptions import APIStatusError


def test_simple_flat(mostly):
    c = mostly.connect({
        'name': 'AWS S3 michi',
        'type': 'S3_STORAGE',
        'config': {
            'accessKey': 'AKIAWMB6NNDXOHCX5PFY'
        },
        'secrets': {
            'secretKey': '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'
        },
    })


def test_subject_linked(mostly, subject_and_linked_df):
    subject_df, linked_df = subject_and_linked_df
    create_generator = CreateGeneratorRequest(
        name="subject_linked",
        tables=[
            TableItem(name="subject", data=subject_df, primary_key="id"),
            TableItem(
                name="linked",
                data=linked_df,
                primary_key="id",
                foreign_keys=[
                    ForeignKey(
                        column="subject_id", referenced_table="subject", is_context=True
                    )
                ],
            ),
        ],
    )  # This is quite cumbersome, isn't it?
    g = mostly.train(create_generator)
    sd = mostly.generate(g)
    syn = sd.data()
    assert syn is not None  # TODO


def test_share(mostly):
    test_user = "test1@mostly.ai"
    df = pd.DataFrame({"col": [1, 2, 3]})
    g = mostly.train(df, start=False)
    mostly.share(g, test_user)
    shares_emails = [share.email for share in mostly.shares.get(g)]
    assert test_user in shares_emails
    mostly.unshare(g, test_user)
    shares_emails = [share.email for share in mostly.shares.get(g)]
    assert test_user not in shares_emails
    with pytest.raises(APIStatusError) as err:
        mostly.share(g, "superadmin@mostly.ai")
    assert "the same user" in err.value.message
    # cleanup
    g.delete()
