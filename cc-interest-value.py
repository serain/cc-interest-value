#!/usr/bin/python3

import time
import math
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
from pytrends.request import TrendReq


CC_API_URL = 'https://min-api.cryptocompare.com/data/pricehistorical'


def get_coin_interest(keyword):
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = [keyword]
    pytrends.build_payload(kw_list,
                           cat       = 0,
                           timeframe = 'today 12-m',
                           geo       = '',
                           gprop     = '')

    return pytrends.interest_over_time()


def get_coin_value(symbol, currency):
    # today at midnight
    today = datetime.combine(date.today(), datetime.min.time())
    qdates = [today - timedelta(days=x) for x in range(0, 365)]
    values = []

    for qdate in qdates:
        r = requests.get(CC_API_URL, {'fsym' : symbol,
                                      'tsyms': currency,
                                      'ts'   : time.mktime(qdate.timetuple())})
        values.append(r.json()['XRP']['USD'])

    df = pd.DataFrame(data={'date': qdates, symbol: values})
    df = df.set_index(['date']).sort_index()

    return df


def double_plot(value_data, interest_data):
    fig, value_ax = plt.subplots()

    # value line
    value_data.plot(ax        = value_ax,
                    color     = 'orange',
                    legend    = 'value',
                    linestyle = '-',
                    marker    = 'o')
    # set the value y axis between 0 and max() rounded up to next decimal
    ymax = math.ceil(coin_value.max().values[0] * 10.0) / 10.0
    value_ax.set_ylim(ymin=0, ymax=ymax)
    value_ax.legend().remove()
    value_ax.set_ylabel('value', color='orange', weight='bold')

    for tl in value_ax.get_yticklabels():
        tl.set_color('orange')
        tl.set_weight('bold')

    # interest line
    interest_ax = value_ax.twinx()
    interest_line = interest_data.plot(ax        = interest_ax,
                                       color     = 'blue',
                                       legend    = 'interest',
                                       linestyle = '--',
                                       marker    = 'o')
    interest_ax.legend().remove()
    interest_ax.set_ylabel('interest', color='blue', weight='bold')

    for tl in interest_ax.get_yticklabels():
        tl.set_color('blue')
        tl.set_weight('bold')


coin_interest = get_coin_interest('ripple')
coin_value = get_coin_value('XRP', 'USD')
double_plot(coin_value, coin_interest)
plt.show()