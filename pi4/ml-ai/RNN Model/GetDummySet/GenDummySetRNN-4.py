import pandas as pd
import random
from datetime import datetime

t = 10000

start_date = '2018-01-01'
end_date = '2023-12-31'
date_range = pd.date_range(start=start_date, end=end_date)

# Convert to a list
dates_list = date_range.to_list()


def get_availability(date):
    """
  This function assigns availability based on season and neutral case.
  """
    month = date.month
    # Summer months (higher probability of 0)
    if month in [8, 9, 10]:
        return random.choices([1, 0], weights=[0.7, 0.3])[0]
    # Winter months (higher probability of 1)
    elif month in [2, 3, 4]:
        return random.choices([1, 0], weights=[0.3, 0.7])[0]
    # Neutral case (alternate 0 and 1)
    else:
        # Use a counter to keep track of the previous availability
        if not hasattr(get_availability, 'counter'):
            get_availability.counter = 0
        get_availability.counter = (get_availability.counter + 1) % 2
        return get_availability.counter


avail = [get_availability(date) for date in dates_list]

data = {"date": dates_list, "avail": avail}

df = pd.DataFrame(data=data, index=None)
df.to_csv('../csv/dummyData-3-seasonal_notAmerican.csv')

