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
    times.append(time)
    avail.append(ava)
    forcast_avail.append(next_ava)
    bottom_level.append(levelb)
    top_level.append(levelt)
    if levelt > 70 or levelb < 30:
        send_up.append(0)
        continue
    if time < 18:
        if ava == 0 and next_ava == 0:
            send_up.append(random.randint(0,10) if levelt>10 else random.randint(5,15))
        elif ava == 0 and next_ava == 1:
            send_up.append(random.randint(0,10) if levelt>10 else random.randint(5,15))
        elif ava == 1 and next_ava == 0:
            send_up.append(random.randint(0,30) if levelt>10 else random.randint(20,30))
        elif ava == 1 and next_ava == 1:
            send_up.append(random.randint(0,30) if levelt>10 else random.randint(20,30))
    elif time < 21:
        if ava == 0 and next_ava == 0:
            send_up.append(random.randint(0,10) if levelt>10 else random.randint(5,15))
        elif ava == 0 and next_ava == 1:
            send_up.append(random.randint(0,30) if levelt>10 else random.randint(20,30))
        elif ava == 1 and next_ava == 0:
            send_up.append(random.randint(0,30) if levelt>10 else random.randint(20,30))
        elif ava == 1 and next_ava == 1:
            send_up.append(random.randint(0,30) if levelt>10 else random.randint(20,30))
    elif time < 24:
        if ava == 0 and next_ava == 0:
            send_up.append(random.randint(0,10) if levelt>10 else random.randint(5,15))
        elif ava == 0 and next_ava == 1:
            send_up.append(random.randint(0,30) if levelt>10 else random.randint(20,30))
        elif ava == 1 and next_ava == 0:
            send_up.append(random.randint(0,10) if levelt>10 else random.randint(5,15))
        elif ava == 1 and next_ava == 1:
            send_up.append(random.randint(0,30) if levelt>10 else random.randint(20,30))

data = {"time":times,"avail":avail, "forcast_avail": forcast_avail,
            "bottom_level":bottom_level,"top_level":top_level,"percentage":send_up}


df = pd.DataFrame(data=data)

df.to_csv('../dummyDataTime.csv')



