import os

import numpy as np
import pandas as pd

os.environ["MOSTLY_AI_PASSWORD"] = "Mostly01!"

df = pd.DataFrame(
    {
        "name": np.random.choice(["Alice", "Bob", "Charlie", "David", "Eva"], 10_000),
        "age": np.random.randint(18, 65, size=10_000),
        "income": np.random.normal(50000, 15000, 10_000),
    }
)


from mostlyai import MostlyAI

client = MostlyAI()
g = client.generators.create(
    {"tables": [{"data": df, "name": "customers"}]}, start=True, wait=True
)
sd = client.synthetic_datasets.create(generatorId=g.id, start=True, wait=True)
dfs = sd.data()
print(dfs)


# import os
#
# from mostlyai import MostlyAI
# import pandas as pd
#
#
# ## SETUP
#
# os.environ['MOSTLY_PASSWORD'] = 'Mostly01!'
#
# from mostlyai import MostlyAI
# client = MostlyAI(
#     # api_key = 'xxx',         # or MOSTLYAI_API_KEY env var; this is bound to a single user account
#     # base_url = 'https://..'  # optional; defaults to our free version
# )
#
# print(client.connectors.list())
#
#
# client = MostlyAI(api_key='..')
# config = client.generators.get(g_id).to_dict()
# config.tables = [{"data": df, name="census", ...}]
# g = client.generators.create(tables={'data': tgt_df}) # train generator
# sd = client.synthetic_datasets.create(generator=g.id)   # generate synthetic data
# syn_df = sd.download()['data']
#
#
# #
# #
# # ## RETRIEVE entities
# #
# c = client.connectors.get("1664cc56-01c4-43af-a39d-50f4c411e004")
# g = client.generators.get("d541c1f3-ff03-4b83-a029-1bd7f00da79d")
# sd = client.synthetic_datasets.get("6a36a129-4938-4756-9167-4d32c8d2b4b5")
# #
# # # ACCESS properties
# # c.name
# # g.accuracy
# # g.usage.total_datapoints
# # g.tables["transactions"].model.metrics.accuracy.univariate
# # len(g.tables["transactions"].columns)
# #
# # ## LIST entities
# #
# # for c in client.connectors.list():
# #     print(c.id, c.name)
# #
# # for g in client.generators.list():
# #     print(g.id, g.name, g.accuracy)
# #
# # for sd in client.synthetic_datasets.list():
# #     print(sd.id, sd.name)
# #
# # ## DELETE entities
# #
# # c.delete()
# # g.delete()
# # sd.delete()
# #
# # ## UPDATE entities -> only needed for basic properties of main entities
# #
# # c.update(name='new name')
# # g.update(description='new description')
# # sd.update(description='new description')
# #
# # ## CREATE entities
# #
# # either via named parameters
# c = client.connectors.create(
#     name='My Database',
#     type='POSTGRES',
#     accessType='SOURCE',
#     config={'host': 'xxx', 'username': 'xxx', 'database': 'xxx'},
#     secrets={'password': 'xxx'}
# )
#
# # or via single config JSON (that can be retrieved via /config endpoint)
# c = client.connectors.create(json_to_dict={
#     'name': 'My Database',
#     'type': 'POSTGRES',
#     'accessType': 'SOURCE',
#     'config': {'host': 'xxx', 'username': 'xxx', 'database': 'xxx'},
#     'secrets': {'password': 'xxx'}
# })
# #
# # minimalistic example for 1-table Generator
# g = client.generators.create(tables=[{'data': df}])
#
# # minimalistic example for a 2-table Generator
# g = client.generators.create(tables=[
#     {'name': 'account', 'data': account_df, 'primary_key': 'account_id'},
#     {'name': 'transaction', 'data': trans_df, 'foreign_keys': [{'column': 'account_id', 'referenced_table': 'account'}]}
# ])
#
# # a example for a 2-table Generator, incl some advanced settings
# g = client.generators.create(
#     name='Berka 2-table',
#     description='A synthetic Berka dataset, including synthetic transaction text',
#     tables=[
#         {
#             'name': 'account',
#             'sourceConnector': c.id,
#             'location': 'public.account',
#             'primary_key': 'account_id',
#             'columns': [  # any missing columns are included, with AUTO encoding type
#                 {'name': 'creation_date', 'model_encoding_type': 'DATETIME'},
#                 {'name': 'xxx', 'is_included': False},
#             ],
#             'model': {
#                 'configuration': {
#                     'maxSampleSize': 10_000,
#                     'maxEpochs': 5,
#                 }
#             }
#         },
#         {
#             'name': 'transaction',
#             'data': 'xxxx',  # allow URI or binary file content; as well as pd.DataFrame
#             'primary_key': 'trans_id',
#             'columns': [
#                 {'name': 'trans_amt', 'model_encoding_type': 'NUMERIC:BINNED'},
#                 {'name': 'trans_text', 'model_encoding_type': 'TEXT_MODEL'},
#             ],
#             'foreign_keys': [
#                 {'column': 'account_id', 'referenced_table': 'account', 'is_context': True}
#             ],
#             'modelConfiguration': {
#                 'maxSampleSize': 5_000,
#                 'maxSequenceLength': 15,
#                 'valueProtection': False,
#             },
#             'textModelConfiguration': {
#                 'model_size': 'L',
#             }
#         }
#     ]
# )
#
# # minimalistic example for a Synthetic Dataset
# sd = client.synthetic_datasets.create(generator=g.id)
#
# # example for a Synthetic Dataset, incl some advanced settings
# sd = client.synthetic_datasets.create(
#     generator=g.id,
#     tables=[
#         {
#             'name': 'account',
#             'sample_seed_data': tgt_df,
#             'configuration': {
#                  'sampling_temperature': 0.8,
#              }
#         },
#         {
#             'name': 'transaction',
#             'configuration': {
#                 'imputation': ['country', 'date_of_birth'],
#             }
#     ],
#     delivery={
#         'destinationConnector': c.id,
#         'location': 'xx',
#     }
# )
# #
# #
# # ## TRAINING, GENERATION
#
# # synchronous calls (=default)
#
# g = client.generators.create(...)
#
# #
# # training
# # this creates a Generator, starts training, polls status, and wait until it's DONE
#
# sd = client.synthetic_datasets.create(..., async=False)
# # this creates a SD, starts generation, polls status, and wait until it's DONE
#
# # asynchronous calls
#
# g = client.generators.create(name="michi 1", start=True, wait=True)
# sd = client.synthetic_datasets.create(g.id, start=True, wait=False)
# sd.data()["players"] # --> pd.DataFrame
#
#
# g.training.start()
# g.training.wait(interval=5)
#
# # g.training.cancel()
# # g.training.logs()
# # g.training.status()
# g.training.wait(interval=5)    # helper method that polls and waits until it's DONE
#
# while True:
#     Sys.sleep(5)
#     status = g.training.status()
#     if status in ["DONE", "FAILED", "CANCELLED"]:
#         break
#     else:
#         print("still waiting")
#
#
#
#
# sd = client.synthetic_datasets.create(..., async=True)
# sd.generation.start()
# sd.generation.start()
# sd.generation.cancel()
# sd.generation.logs()
# sd.generation.status()
# sd.generation.wait(interval=5)  # helper method that polls and waits until it's DONE
#
#
# # # DOWNLOAD
# #
# # dfs = sd.data()  # returns a dict with pd.DataFrame
