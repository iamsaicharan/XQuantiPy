import yfinance as yf
import pandas as pd

class Ticker(object):
    """
    A class to represent a stock
    ...
    Attributes
    ----------
    data : Dataframe
        Timeseries daily data of the stock
    pe : float
        PE (Current share price / Earnings per share) of the stock
    beta : float
        beta ((covariance(stock returns, index returns) / variance(index returns))
        volatility of the stock) of the stock
    """
    def __init__(self, ticker):
        self.stock = ticker
        self.data = yf.download(ticker)
        fundamentals = yf.Ticker(ticker).info
        self.pe = fundamentals['trailingPE']
        self.beta = fundamentals['beta']

    def __str__(self):
        return str(self.stock)
    