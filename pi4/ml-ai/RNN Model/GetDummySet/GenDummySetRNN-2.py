import pandas as pd
import random
import os

t=10000

start_date = '2021-01-01'
end_date = '2023-12-31'
date_range = pd.date_range(start=start_date, end=end_date)

# Convert to a list
dates_list = date_range.to_list()
avail = [random.randint(0,1) for _ in dates_list]


data = {"date": dates_list,"avail":avail }


df = pd.DataFrame(data=data,index=None)
df.to_csv('../csv/dummyData-0.csv')
