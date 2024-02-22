import numpy as np
import pandas as pd
import pytest

from mostlyai.components import CreateGeneratorRequest, ForeignKey, TableItem


@pytest.fixture
def subject_and_linked_df():
    names = ["Alice", "Bob", "Charlie", "Diana", "Ethan"]

    # Create subject_df with 100 users
    subject_df = pd.DataFrame(
        {"id": range(1, 101), "name": np.random.choice(names, 100)}
    )

    # Initialize an empty DataFrame for linked_df
    linked_df = pd.DataFrame(columns=["id", "subject_id", "count"])

    event_id = 1
    for user_id in subject_df["id"]:
        # Randomly choose the number of events for this user (between 1 and 5)
        num_events = np.random.randint(1, 6)

        for event_count in range(1, num_events + 1):
            # Append event data to linked_df
            linked_df = linked_df.append(
                {"id": event_id, "subject_id": user_id, "count": event_count},
                ignore_index=True,
            )
            event_id += 1

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
