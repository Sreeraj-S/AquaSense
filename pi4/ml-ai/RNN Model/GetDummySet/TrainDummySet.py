import random
import pandas as pd
import datetime

# Define the number of days for the test data
num_days = 7


def generate_random_sequence(num_days):
    """
  Generates a random sequence of 0 or 1 values for the specified number of days.
  """
    return [random.randint(0, 1) for _ in range(num_days)]


# Generate random dates for the test data (optional)
today = datetime.date.today()
dates = [today + datetime.timedelta(days=i) for i in range(num_days)]

# Generate random availability data
availability = generate_random_sequence(num_days)

# Create a dictionary and DataFrame
data = {"date": dates if dates else None, "avail": availability}
df = pd.DataFrame(data=data, index=None)
print(df)