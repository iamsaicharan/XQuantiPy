import yfinance as yf
import pandas as pd

class Ticker(object):
    """
    A class to represent a stock
    ...
    Attributes
    ----------
    stock : str
        stock ticker name
    data : Dataframe
        timeseries daily data of the stock
    fundamentals : dict
        fundamental data of the stock
    """
    def __init__(self, ticker, period = "10Y"):
        self.stock = ticker
        data = yf.download(ticker, period=period)
        data['daily_return'] = (data['Adj Close'] - data['Adj Close'].shift(1)) / data['Adj Close'].shift(1)
        data['cum_return'] = (1+data['daily_return']).cumprod()-1
        self.data = data
        self.fundamentals = yf.Ticker(ticker).info

    def __str__(self):
        return str(self.stock)
    