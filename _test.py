"""
Script for testing the funcationality of the application
...

Requirement:
pytest module -> pip install pytest

To test:
> pytest

"""
import yfinance as yf
from ticker import Ticker
from analysis import Analysis

def test_ticker_data_type():
    assert type(Ticker("AAPL").data).__name__ == "DataFrame"

def test_ticker_fundamentals_type():
    assert type(Ticker("AAPL").fundamentals) == dict

def test_ticker_get_beta_method_return_type():
    assert type(Ticker("AAPL").get_beta()) == float

def test_ticker_get_alpha_method_return_type():
    assert type(Ticker("AAPL").get_alpha()) == float

def test_analysis_show_alpha_vs_beta_return_type():
    assert type(Analysis([Ticker("AAPL")]).show_alpha_vs_beta()).__name__ == "module"



