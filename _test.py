"""
Script for testing the funcationality of the application
...

Requirement:
pytest module -> pip install pytest

To test:
> pytest

"""

from ticker import Ticker
import yfinance as yf
from analysis import Analysis

def test_ticker_data_type():
    """
    Summary:
    Asserts the data variable of Ticker Object

    Return:
    assert : boolean
        should assert data to Dataframe
    """
    assert type(Ticker("AAPL").data).__name__ == "DataFrame"

def test_ticker_fundamentals_type():
    """
    Summary:
    Asserts the pe variable of Ticker Object

    Return:
    assert : boolean
        should assert pe to dict
    """
    assert type(Ticker("AAPL").fundamentals) == dict

def test_ticker_get_beta_method_return_type():
    """
    Summary:
    Asserts the get_beta return of the TickerObject

    Return:
    assert : boolean
        should assert get_beta return to float
    """
    assert type(Ticker("AAPL").get_beta()) == float

def test_ticker_get_alpha_method_return_type():
    """
    Summary:
    Asserts the get_alpha return of the Ticker Object

    Return:
    assert : boolean
        should assert get_alpha return to float
    """
    assert type(Ticker("AAPL").get_alpha()) == float

def test_analysis_show_alpha_vs_beta_return_type():
    """
    Summary:
    Asserts the show_alpha_vs_beta return of the list of Ticker Object

    Return:
    assert : boolean
        should assert show_alpha_vs_beta return to module
    """
    assert type(Analysis([Ticker("AAPL")]).show_alpha_vs_beta()).__name__ == "module"



