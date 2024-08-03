import pandas as pd
import random

t = 100000

times=[]
avail = []
forcast_avail = []
bottom_level = []
top_level = []
send_up = []
for i in range(t):
    time = random.randint(0,23)
    next_ava = random.randint(0,1)
    ava = random.randint(0,1)
    levelb = random.randint(0,100)
    levelt = random.randint(0,100)
    avail.append(ava)
    forcast_avail.append(next_ava)
    bottom_level.append(levelb)
    top_level.append(levelt)
    if levelt > 70 or levelb < 30:
        send_up.append(0)
        continue
    if ava == 0 and next_ava == 0:
        if levelt <= 15 and levelb >= 70:
            send_up.append(random.randint(4,5))
        elif levelt >= 15:
            send_up.append(random.randint(1,2))
        elif levelt < 15:
            send_up.append(3)
    elif ava == 0 and next_ava == 1:
        if levelt < 15 and levelb > 70:
            send_up.append(random.randint(4,5))
        elif levelt >= 60:
            send_up.append(1)
        elif levelt >= 15:
            send_up.append(random.randint(2,3))
        elif levelt < 15:
            send_up.append(4)
    elif ava == 1 and next_ava == 0:
        if levelt < 15 and levelb > 40:
            send_up.append(random.randint(4, 5))
        elif levelt >= 30:
            send_up.append(random.randint(2,4))
        elif levelt >= 15:
            send_up.append(random.randint(3, 5))
        elif levelt < 15:
            send_up.append(random.randint(4,5))
    elif ava == 1 and next_ava == 1:
        if levelt < 15:
            send_up.append(5)
        elif levelt >= 60:
            send_up.append(random.randint(1, 3))
        elif levelt >= 30:
            send_up.append(random.randint(3, 4))
        elif levelt >= 15:
            send_up.append(random.randint(4, 5))

print(len(avail),len(send_up))
data = {"avail":avail, "forcast_avail": forcast_avail,
            "bottom_level":bottom_level,"top_level":top_level,"percentage":send_up}


df = pd.DataFrame(data=data)

df.to_csv('../dummyData-1.csv')



