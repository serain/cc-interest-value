#!/usr/bin/python3

import sys
import time
import math
import json
import argparse
import requests
import animation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
from pytrends.request import TrendReq


CC_API_URL = 'https://min-api.cryptocompare.com/data/pricehistorical'


@animation.wait('spinner')
def get_coin_interest(keywords):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(keywords,
                           cat       = 0,
                           timeframe = 'today 12-m',
                           geo       = '',
                           gprop     = '')

    return pytrends.interest_over_time()


@animation.wait('spinner')
def get_coin_value(symbol, currency):
    symbol = symbol.upper()
    currency = currency.upper()

    # today at midnight
    today = datetime.combine(date.today(), datetime.min.time())
    qdates = [today - timedelta(days=x) for x in range(0, 365)]
    values = []

    for qdate in qdates:
        r = requests.get(CC_API_URL, {'fsym' : symbol,
                                      'tsyms': currency,
                                      'ts'   : time.mktime(qdate.timetuple())})
        values.append(r.json()[symbol][currency])

    df = pd.DataFrame(data={'date': qdates, symbol: values})
    df = df.set_index(['date']).sort_index()

    return df


@animation.wait('spinner')
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
    value_ax.grid()

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
    interest_ax.set_ylim(ymin=0, ymax=100)
    interest_ax.legend().remove()
    interest_ax.set_ylabel('interest', color='blue', weight='bold')

    for tl in interest_ax.get_yticklabels():
        tl.set_color('blue')
        tl.set_weight('bold')

    # align y axes
    interest_ax.set_yticks(np.linspace(interest_ax.get_yticks()[0],
                           interest_ax.get_yticks()[-1],
                           len(value_ax.get_yticks())))


def get_args():
    # temporary groundwork for argparse until I get home
    with open('cryptocurrencies.json') as f:
        cc_data = json.load(f)

    parser = argparse.ArgumentParser(description='Graph CC interest vs value')
    parser.add_argument('-c', '--currency', type=str, default='usd', 
                        help='currency value (default: USD)')

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--list', action='store_true', 
                        help='list supported cryptocurrency symbols')
    action.add_argument('-s', '--symbol', type=str,
                        help='cryptocurrency symbol')

    args = parser.parse_args()

    if args.list:
        for symbol in cc_data:
            print(symbol.upper())
            print('    description : {}'.format(cc_data[symbol]['description']))
            print('    keyword     : {}\n'.format(cc_data[symbol]['keyword']))
        sys.exit(0)

    if args.symbol.lower() not in cc_data:
        print(f'Couldn\'t find symbol \'{args.symbol}\'')
        sys.exit(1)

    args.keyword = cc_data[args.symbol]['keyword']

    return args


if __name__ == '__main__':
    args = get_args()

    print(f'Grabbing \'{args.keyword}\' Google Trends data')
    coin_interest = get_coin_interest([args.keyword])

    print(f'\rPulling {args.symbol.upper()} historical values')
    coin_value = get_coin_value(args.symbol, args.currency)

    print('\rPlotting up')
    double_plot(coin_value, coin_interest)
    plt.show()
