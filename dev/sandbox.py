from mostlyai import MostlyAI

# initialize a client
mostly = MostlyAI(
    api_key="mostly-9df216f8da906b75a1c7397710b74e9d8059619dbcbb28562bd203879a47f1cc"
)

# train a generator
g = mostly.train(
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
)

# generate a synthetic dataset
sd = mostly.generate(g, size=1000)

# consume synthetic data
print(sd1.data())
