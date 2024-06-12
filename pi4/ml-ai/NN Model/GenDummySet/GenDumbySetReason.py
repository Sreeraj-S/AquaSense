import pandas as pd
import random

t = 100000

avail = [random.randint(0,1) for i in range(t)]
forcast_avail = [random.randint(0,1) for i in range(t)]
bottom_level = [random.randint(0,100) for i in range(t)]
top_level = [random.randint(0,100) for i in range(t)]
send_up = [random.randint(0, 30) if top_level[i] < 70 else 0 for i in range(t)]
data = {"avail":avail, "forcast_avail": forcast_avail,
            "bottom_level":bottom_level,"top_level":top_level,"percentage":send_up}


df = pd.DataFrame(data=data)

df.to_csv('dummyDataTopData0.csv')



