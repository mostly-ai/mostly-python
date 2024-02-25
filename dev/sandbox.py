from mostlyai import MostlyAI
mostly = MostlyAI(api_key='mostly-9df216f8da906b75a1c7397710b74e9d8059619dbcbb28562bd203879a47f1cc')
g1 = mostly.train('https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv')
sd1 = mostly.generate(g1, size=1000)
print(sd1.data())
