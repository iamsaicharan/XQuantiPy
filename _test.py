"""
Script for testing the funcationality of the application
...

Requirement
-----------
pytest module -> pip install pytest

To test
-------
> pytest

"""

from ticker import Ticker
import yfinance as yf

def test_ticker_data_type():
    """
    Asserts the data variable of Ticker Object - should assert data to Dataframe
    """
    assert type(Ticker("AAPL").data).__name__ == "DataFrame"

def test_ticker_fundamentals_type():
    """
    Asserts the pe variable of Ticker Object - should assert pe to float
    """
    assert type(Ticker("AAPL").fundamentals) == dict




