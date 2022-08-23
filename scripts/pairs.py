#!/usr/bin/python3

import requests
import sys


def bina():
    rv = set()

    brex_res = requests.get('https://global.bittrex.com/v3/markets/')
    if brex_res.status_code != 200:
        print(f'[!] Bad status code {brex_res.status_code}. Aborting', file=sys.stderr)
        sys.exit(1)

    bina_res = requests.get('https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=false')
    if bina_res.status_code != 200:
        print(f'[!] Bad status code {bina_res.status_code}. Aborting', file=sys.stderr)
        sys.exit(1)

    brex_json = brex_res.json()
    brex_markets = sorted([mkt['baseCurrencySymbol'] + '-' + mkt['quoteCurrencySymbol'] for mkt in brex_json if mkt['status'] == 'ONLINE'])
    bina_json = bina_res.json()
    bina_markets = sorted([mkt['b'] + '-' + mkt['q'] for mkt in bina_json['data'] if mkt['st'] == 'TRADING'])

    common = set.intersection(set(brex_markets), set(bina_markets))

    common = sorted([m for m in common])

    common_usdt = [m for m in common if m.endswith('-USDT')]
    rv.update(common_usdt)

    common_btc = [m for m in common if m.endswith('-BTC')]
    rv.update(common_btc)

    common_eur = [m for m in common if m.endswith('-EUR')]
    rv.update(common_eur)

    bina_markets_as_usd = [m[:-1] for m in bina_markets if m.endswith('-USDT')]
    common_x = set.intersection(set(brex_markets), set(bina_markets_as_usd))
    common_usd = [m for m in common_x if m.endswith('-USD')]
    rv.update(common_usd)

    return rv


def brex():
    rv = set()

    brex_res = requests.get('https://global.bittrex.com/v3/markets/')
    if brex_res.status_code != 200:
        print(f'[!] Bad status code {brex_res.status_code}. Aborting', file=sys.stderr)
        sys.exit(1)

    bina_res = requests.get('https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=false')
    if bina_res.status_code != 200:
        print(f'[!] Bad status code {bina_res.status_code}. Aborting', file=sys.stderr)
        sys.exit(1)

    brex_json = brex_res.json()
    brex_markets = sorted([mkt['baseCurrencySymbol'] + '-' + mkt['quoteCurrencySymbol'] for mkt in brex_json if mkt['status'] == 'ONLINE' and 'TOKENIZED_SECURITY' not in mkt['tags']])
    bina_json = bina_res.json()
    bina_markets = sorted([mkt['b'] + '-' + mkt['q'] for mkt in bina_json['data'] if mkt['st'] == 'TRADING'])

    brex_only = set(brex_markets) - set(bina_markets)

    brex_only_usdt = [m for m in brex_only if m.endswith('-USDT')]

    brex_only_btc = [m for m in brex_only if m.endswith('-BTC')]

    brex_only_btc_usdt = [m for m in brex_only_usdt if (m.split('-')[0] + '-BTC') in brex_only_btc]

    rv.update(brex_only_btc_usdt)
    rv.update(p.replace('-USDT', '-BTC') for p in brex_only_btc_usdt)

    return rv


def main():
    rv = set()

    rv.update(bina())
    rv.update(brex())

    rv = sorted(list(rv))

    print(" ".join(rv))

if __name__ == '__main__':
    main()
