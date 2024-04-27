import pandas as pd
import random

t = 100

avail = [random.randint(0,1) for i in range(t)]
forcast_avail = [random.randint(0,1) for i in range(t)]
bottom_level = [random.randint(0,100) for i in range(t)]
top_level = [random.randint(0,100) for i in range(t)]

data = {"avail":avail, "forcast_avail": forcast_avail,
            "bottom_level":bottom_level,"top_level":top_level}


df = pd.DataFrame(data=data)

df.to_csv('dummyTest.csv')



