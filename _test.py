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

def test_ticker_pe_type():
    """
    Asserts the pe variable of Ticker Object - should assert pe to float
    """
    assert type(Ticker("AAPL").pe) == float

def test_ticker_beta_type():
    """
    Asserts the beta variable of Ticker Object - should assert beta to float
    """
    assert type(Ticker("AAPL").beta) == float




