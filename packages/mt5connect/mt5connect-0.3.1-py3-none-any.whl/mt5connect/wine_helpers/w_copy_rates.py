import os
import MetaTrader5 as mt5
from datetime import datetime, timedelta


ASSET = os.getenv("ASSET")
TIMEFRAME = os.getenv("TIMEFRAME")
FILE = os.getenv("FILE")

# import the 'pandas' module for displaying data obtained in the tabular form
import pandas as pd

import pytz

# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
# create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
utc_from = datetime.now()
utc_from = utc_from + timedelta(days=1)  # last 30 days
# get 10 EURUSD H4 bars starting from 01.10.2020 in UTC time zone
rates = mt5.copy_rates_from(ASSET, getattr(mt5, TIMEFRAME), utc_from, 2000000)

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
# display each element of obtained data in a new line

# create DataFrame out of the obtained data
rates_frame = pd.DataFrame(rates)
# convert time in seconds into the datetime format
rates_frame["time"] = pd.to_datetime(rates_frame["time"], unit="s")

# display data
print("\nDisplay dataframe with data")
print(FILE)
print(rates_frame)
rates_frame.to_parquet(FILE)
