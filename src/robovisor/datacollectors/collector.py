#!/usr/bin/env python3
import requests
import time
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from robovisor.models import db, Price, Ticker

sp500 = ['AAPL', 'MSFT', 'NVDA', 'GOOG', 'GOOGL', 'AMZN', 'META',  'AVGO', 'TSLA', 'WMT', 'LLY', 'V', 'JPM', 'UNH', 
           'MA', 'XOM', 'COST', 'NFLX', 'PG', 'ORCL', 'JNJ', 'HD', 'ABBV', 'KO', 'TMUS', 'BAC', 'PM', 'CRM', 'CVX', 'CSCO', 'MCD',
             'ABT', 'IBM', 'PLTR', 'LIN', 'WFC', 'PEP', 'MRK', 'GE', 'T', 'VZ', 'ACN', 'AXP', 'ISRG', 'MS', 'RTX', 'TMO', 
             'INTU', 'NOW', 'GS', 'PGR', 'BX', 'AMGN', 'QCOM', 'DIS', 'UBER', 'AMD', 'ADBE', 'BKNG', 'SPGI', 'CI', 'LMT', 
             'CAT', 'MDT', 'MO', 'ELV', 'SCHW', 'TXN', 'DE', 'CB', 'ADI', 'SYK', 'TJX', 'PFE', 'BLK', 'ZTS', 'MMC', 'GM', 
             'DUK', 'ADP', 'ETN', 'FDX', 'TGT', 'GILD', 'CVS', 'HCA', 'BDX', 'NSC', 'CL', 'REGN', 'AON', 'CSX', 'VRTX', 'C', 
             'EW', 'SHW', 'CME', 'SO', 'APD', 'MU', 'ICE', 'EOG', 'KLAC', 'ITW', 'MRNA', 'FISV', 'PYPL', 'PNC', 'EMR', 'MCO', 
             'AIG', 'WELL', 'MCK', 'AZO', 'AEP', 'NKE', 'ADSK', 'F', 'PSX', 'MAR', 'KHC', 'ORLY', 'CDNS', 'PCAR', 'SRE', 'TRV', 
             'ROST', 'IDXX', 'HLT', 'DLR', 'DHR', 'PSA', 'BIIB', 'AMP', 'ROP', 'STZ', 'MNST', 'MSCI', 'HUM', 'WMB', 'NXPI', 'ANET',
               'TFC', 'CTAS', 'EXC', 'CMG', 'D', 'SPG', 'VLO', 'ODFL', 'COF', 'PAYX', 'CARR', 'ADM', 'WTW', 'BKR', 'OXY', 'CTSH', 
               'ED', 'DOW', 'DD', 'CSGP', 'A', 'CCL', 'TEL', 'KEYS', 'VICI', 'HPQ', 'FAST', 'SLB', 'ALL', 'VRSK', 'PPG', 'CMI', 'SYY', 
               'AMPH', 'MTB', 'RMD', 'ECL', 'TSCO', 'KMB', 'WST', 'PCG', 'HSY', 'IQV', 'DLTR', 'XEL', 'ALGN', 'FANG', 'EFX', 'GWW',
                 'FITB', 'FTNT', 'ZBH', 'MKC', 'BAX', 'PH', 'ABC', 'CBRE', 'STT', 'PXD', 'CEG', 'NOC', 'AVB', 'LRCX', 'TDG', 
                 'MAA', 'EA', 'DVN', 'HIG', 'NEM', 'INVH', 'PAYC', 'OTIS', 'CHD', 'LEN', 'DHI', 'HBAN', 'IRM', 'CTVA', 'IPG', 
                 'LDOS', 'CFG', 'HES', 'BRO', 'CNP', 'BXP', 'CMS', 'BMRN', 'AKAM', 'ULTA', 'IP', 'CINF', 'FTV', 'KEY',
                   'LUV', 'KR', 'NUE', 'WBD', 'MOS', 'AEE', 'KIM', 'NDAQ', 'EXR', 'ARE', 'ATO', 'MLM', 'WRB', 'AWK', 'PPL', 'PRU',
                     'EXPE', 'DG', 'ETSY', 'HWM', 'CF', 'DTE', 'VMC', 'BALL', 'TYL', 'CBOE', 'AFL', 'NI', 'CLX', 'TRGP', 'TXT', 'FE',
                       'ILMN', 'STE', 'DRI', 'RSG', 'ON', 'ALLE', 'EIX', 'EBAY', 'HPE', 'LNT', 'GNRC', 'TECH', 'PKI', 'FRC', 'DXCM', 
                       'HOLX', 'RJF', 'WDC', 'APA', 'WHR', 'FMC', 'HAS', 'NTRS', 'CHRW', 'INCY', 'XYL', 'MOS', 'ZBRA', 'ALLE', 'LKQ', 
                       'ETR', 'PKG', 'IEX', 'AES', 'VTR', 'AIZ', 'MGM', 'WRK', 'NWL', 'CPB', 'PNW', 'SEE', 'NCLH', 'NRG', 'BBWI', 'APA',
                         'HII', 'XRAY', 'PWR', 'REG', 'AAL', 'UHS', 'BEN', 'DXC', 'DVA', 'OGN', 'IVZ', 'TAP', 'PARA', 'NWSA', 'NWS', 'RL', 'FOX', 'FOXA']
not_allowed = ['BRK.B', 'BF.B']


api_key = 'aejOJ0bcmKFDuNt10Br5jbERUKpPDM2Q'



def upsert_price(session, new_price):
    dialect_name = session.bind.dialect.name

    if dialect_name == "sqlite":
        insert_fn = sqlite_insert
    elif dialect_name == "postgresql":
        insert_fn = pg_insert
    else:
        raise NotImplementedError(f"Unsupported dialect: {dialect_name}")

    stmt = insert_fn(Price).values(
        ticker=new_price.ticker,
        date=new_price.date,
        high=new_price.high,
        low=new_price.low,
        open=new_price.open,
        close=new_price.close,
        volume=new_price.volume,
    ).on_conflict_do_update(
        index_elements=["ticker", "date"],
        set_={
            "high": stmt.excluded.high,
            "low": stmt.excluded.low,
            "open": stmt.excluded.open,
            "close": stmt.excluded.close,
            "volume": stmt.excluded.volume,
        }
    )

    session.execute(stmt)

def get_price_history(ticker):
    response = requests.get(f"https://financialmodelingprep.com/stable/historical-price-eod/full?symbol={ticker}&apikey={api_key}")
    response.raise_for_status()
    daily_prices = response.json()
    for day_prices in daily_prices:
      date = day_prices["date"]
      date = datetime.strptime(date, "%Y-%m-%d").date()
      high = day_prices["high"]
      low = day_prices["low"]
      opening = day_prices["open"]
      close = day_prices["close"]
      volume = day_prices["volume"]
      if isinstance(date , list) or isinstance(ticker, list):
        print("Mess up", ticker, date, day_prices)
      new_price = Price(ticker=ticker, date=date, high=high, low=low, open=opening, close=close, volume=volume)
      upsert_price(db.session, new_price)

def get_latest_price(ticker):
    response = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?serietype=line&timeseries=1&apikey={api_key}")
    response.raise_for_status()
    latest_price = response.json()
    
    date = latest_price["date"]
    date = datetime.strptime(date, "%Y-%m-%d").date()
    high = latest_price["high"]
    low = latest_price["low"]
    opening = latest_price["open"]
    close = latest_price["close"]
    volume = latest_price["volume"]

    new_price = Price(ticker=ticker, date=date, high=high, low=low, open=opening, close=close, volume=volume)
    upsert_price(db.session, new_price)


def refresh_db():
    print("Refreshding DB")
    tickers = tickers[:100]
    for ticker in tickers:
        print("Refreshing, ", ticker)
        new_ticker_entry = Ticker(ticker=ticker)
        db.session.add(new_ticker_entry)
        get_latest_price(ticker)
        time.sleep(.3)
    db.session.commit()


def backfill_db():
    db.create_all()
    print("Backfilling!")
    tickers = sp500 #['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'NVDA'] #active_stocks['symbol'].tolist()
    tickers = tickers[:100]
    for ticker in tickers:
        print("Processing ", ticker)
        new_ticker_entry = Ticker(ticker=ticker)
        db.session.add(new_ticker_entry)
        get_price_history(ticker)
        time.sleep(.3)
    db.session.commit()




'''
In main we first get the current temperature and then 
create a new object that we can add to the database. 
'''
#if __name__ == "__main__":

 #   backfill_db()
"""
with app.app_context():
    db.create_all()
    inspector = inspect(db.engine)
    price_high = get_price_high() 
    new_entry = Price(price_high=price_high)
    db.session.add(new_entry)
    db.session.commit()
    print("Commit successful!")"""