# Controlla quali siano i bargain(valore di mercato < valore equity e trailing_eps>0) in tutto l'sp500
# Inserisce gli ISIN in una lista
import yfinance
import pandas as pd
import requests
from io import StringIO


def list_isin_fun():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)
    tables = pd.read_html(StringIO(response.text))
    sp500_table = tables[0]
    tickers = sp500_table['Symbol'].tolist()
    return tickers


def deep_value_trailing_test_fun(ISIN):
    dat = yfinance.Ticker(ISIN)
    b = dat.quarterly_balancesheet
    try:
        y = str(b.columns[0])[0:10]
        b = b[y]
        price = dat.analyst_price_targets['current']
        total_shares = dat.info['sharesOutstanding']
        total_equity = b['Stockholders Equity']
        market_company_value = price*total_shares
    except (KeyError,IndexError):
        print('Error')
        return False
    return (total_equity > market_company_value and dat.info['trailingEps'] >0)


if __name__ == '__main__':
    tickers = list_isin_fun()
    bargains = []
    i = 0
    for ticker in tickers:
        i+=1
        print('analyzed stock:',i)
        if deep_value_trailing_test_fun(ticker):
            print(ticker)
            bargains.append(ticker)
    print('List of ISIN:',bargains)