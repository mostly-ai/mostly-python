from time import sleep

import numpy as np
import pandas as pd
import pytest

from mostlyai.components import CreateGeneratorRequest, ForeignKey, TableItem
from mostlyai.exceptions import APIStatusError


@pytest.fixture
def subject_and_linked_df():
    names = ["Alice", "Bob", "Charlie", "Diana", "Ethan"]

    # Create subject_df with 100 users
    subject_df = pd.DataFrame(
        {"id": range(1, 101), "name": np.random.choice(names, 100)}
    )

    # List to store the linked data
    linked_data = []

    event_id = 1
    for user_id in subject_df["id"]:
        # Randomly choose the number of events for this user (between 1 and 5)
        num_events = np.random.randint(1, 6)

        for event_count in range(1, num_events + 1):
            # Add event data to the list
            linked_data.append(
                {"id": event_id, "subject_id": user_id, "count": event_count}
            )
            event_id += 1

    # Convert the list of dictionaries to a DataFrame
    linked_df = pd.DataFrame(linked_data, columns=["id", "subject_id", "count"])

    return subject_df, linked_df


def test_simple_flat(mostly):
    df = pd.DataFrame({"a": [1, 2, 3] * 100, "b": [4, 5, 6] * 100})
    g = mostly.train(df)
    sd = mostly.generate(g)
    syn = sd.data()
    assert syn.shape == (300, 2)
    assert syn.columns.tolist() == ["a", "b"]


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
