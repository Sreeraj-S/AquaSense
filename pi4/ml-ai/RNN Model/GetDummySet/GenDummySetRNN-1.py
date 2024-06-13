import pandas as pd
import random
import os

t=10000

date = [f"202{random.randint(2,4)}-{random.randint(1,12)}-{random.randint(1,30)}" for _ in range(t)]
avail = [random.randint(0,1) for _ in range(t)]

data = {"date": date,"avail":avail }


df = pd.DataFrame(data=data,index=None)
df.to_csv('../csv/dummyData.csv')
