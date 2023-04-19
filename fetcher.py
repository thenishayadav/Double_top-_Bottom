from __future__ import print_function

from datetime import datetime
import ssl
from datetime import date
from datetime import timedelta

import pandas as pd
import pyotp
from datetime import timedelta
from NorenRestApiPy.NorenApi import NorenApi
import numpy as np
from scipy.signal import argrelextrema

# In[ ]:

user =
pwd =
factor2 =
vc =
app_key =
imei =
token=
# In[ ]:




class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/',
                          websocket='wss://api.shoonya.com/NorenWSTP/')
        global api
        api = self


# In[ ]:

api = ShoonyaApiPy()
import logging

# start of our program
# make the api call
api.login(userid=user, password=pwd, twoFA=pyotp.TOTP(token).now(), vendor_code=vc, api_secret=app_key, imei=imei)
def fetch(tkn, limit, interval):
    lastBusDay = datetime.today()- timedelta(days = 5)
    lastBusDay = lastBusDay.replace(hour=0, minute=0, second=0, microsecond=0)
    ret = pd.DataFrame(api.get_time_price_series(exchange='NSE', token=tkn, starttime=lastBusDay.timestamp(), interval=interval))
    df = pd.DataFrame(columns=['stat', 'time', 'ssboe', 'into', 'inth', 'intl', 'intc', 'intvwap'])
    df = df.append(ret, ignore_index=True)
    df.drop(['stat', 'ssboe', 'intvwap', 'intv', 'intoi', 'v', 'oi'], axis=1, inplace=True)
    df = df.rename({'time': 'timestamp', 'into': 'Open', 'inth': 'High', 'intl': 'Low', 'intc': 'Close'},
                   axis=1)  # new method
    df = df.reindex(index=df.index[::-1])
    df.reset_index(inplace=True, drop=True)
    df['timestamp'] = pd.to_datetime(df.timestamp, format="%d-%m-%Y %H:%M:%S")
    df = df.set_index(pd.DatetimeIndex(df['timestamp']))
    df[['Close', 'High', 'Low', 'Open']] = df[['Close', 'High', 'Low', 'Open']].astype(float)

    # keep data only between 9:15 and 15:30
    start_time = datetime.strptime('09:15:00', '%H:%M:%S').time()
    end_time = datetime.strptime('15:30:00', '%H:%M:%S').time()
    df = df.between_time(start_time, end_time)

    return df


if __name__ == "__main__":
    api_response = fetch("26000",1000, 5)
    print(api_response)