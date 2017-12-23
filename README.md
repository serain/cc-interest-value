# cc-interest-value

Quick thing I threw together while waiting for a flight.

Allows you to graph a cryptocurrency's value against public interest over time (based on Google Trends).

![Ripple interest vs. XRP value](/screenshot/ripple.png "Ripple interest vs. XRP value")

## To Do

 - Populate cryptocurrencies
 - Support multiple keywords
 - Legends on graph
 - Esthetics
 - Save graph to file
 - Input validation for target currency and error handling

## Usage

```
$ ./cc-interest-value.py --help
usage: cc-interest-value.py [-h] [-c CURRENCY] (--list | -s SYMBOL)

Graph CC interest vs value

optional arguments:
  -h, --help            show this help message and exit
  -c CURRENCY, --currency CURRENCY
                        currency value (default: USD)
  --list                list supported cryptocurrency symbols
  -s SYMBOL, --symbol SYMBOL
                        cryptocurrency symbol
```

List supported crypto-currencies:

```
$ ./cc-interest-value.py --list
XRP
    description : Ripple Coin (XRP)
    keyword     : ripple

BTC
    description : Bitcoin (BTC)
    keyword     : bitcoin
```

Generate graph for XRP:

```
$ ./cc-interest-value.py --symbol xrp
```

## Add Crypto-Currency

Edit `cryptocurrencies.json` and add an entry for your new coin. The root key is the cryptocurrencies symbol and you need to provide a Google Trends keyword and a description (description is required at the moment).

For example:

```
    "btc": {
        "keyword": "bitcoin",
        "description": "Bitcoin (BTC)"
    }
```
