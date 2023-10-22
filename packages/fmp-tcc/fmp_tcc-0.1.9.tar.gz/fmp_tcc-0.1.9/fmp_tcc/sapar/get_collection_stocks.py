import pandas as pd

from ..courtois.fmp_url import get_data_url

from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_stocks_fmp(apikey: str='apikey', symbols: list=['AAPL', 'MSFT', 'GOOG', '018260.KS', 'SONY'], start_date: str='1986-01-01'):
    """
    params:
        apikey -- to access data from FMP;
        symbols -- list of tickers of companies, should be not bigger than 5;
        start_date -- the date from which to collect data
    return: list of dictionaries
    """
    symbols_txt = ",".join(symbols)
    url = (f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbols_txt}?from={start_date}&apikey={apikey}')
    data = get_data_url(url=url)
    return data

def get_stocks(apikey: str='apikey', symbols: list=['AAPL', 'MSFT', 'GOOG', '018260.KS', 'SONY'], start_date: str='1986-01-01', 
                step:int=5, with_progress: bool=False):
    """
    params:
        apikey -- to access data from FMP;
        symbols -- list of tickers of companies, can be bigger than 5;
        start_date -- the date from which to collect data
        with_progress -- if you want to monitor the progress
    return: list of dictionaries
    """
    data_frames = []

    symbols1 = symbols.copy()

    if with_progress:
        n = len(symbols) // step
        i = 0

    while(len(symbols1) >= 1):

        if (len(symbols1) > step):
            symbols0 = symbols1[:step]
            symbols1 = symbols1[step:]
        else:
            symbols0 = symbols1
            symbols1 = []

        data = get_stocks_fmp(apikey=apikey, symbols=symbols0, start_date=start_date)
            
        data_frames0 = []

        for d in data['historicalStockList']:
            df = pd.DataFrame(d['historical'])
            df['symbol'] = d['symbol']
            data_frames0.append(df)

        df = pd.concat(data_frames0)

        data_frames.append(df)

        if with_progress:
            i += 1
            print(i, '/' ,n)

    df = pd.concat(data_frames)

    return df