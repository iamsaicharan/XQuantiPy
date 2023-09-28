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
from macro import Macro

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

def test_macro_get_GDP_method_return_type():
    assert type(Macro("IN").get_GDP()).__name__ == "DataFrame"

def test_macro_get_GDP_growth_method_return_type():
    assert type(Macro("IN").get_GDP_growth()).__name__ == "DataFrame"

def test_macro_get_GDP_per_capita_method_return_type():
    assert type(Macro("IN").get_GDP_per_capita()).__name__ == "DataFrame"

def test_macro_get_GDP_per_capita_method_return_type():
    assert type(Macro("IN").get_GDP_per_capita()).__name__ == "DataFrame"

def test_macro_get_GDP_current_LCU_method_return_type():
    assert type(Macro("IN").get_GDP_current_LCU()).__name__ == "DataFrame"

def test_macro_get_inflation_method_return_type():
    assert type(Macro("IN").get_inflation()).__name__ == "DataFrame"

def test_macro_get_unemployment_method_return_type():
    assert type(Macro("IN").get_unemployment()).__name__ == "DataFrame"

def test_macro_get_export_method_return_type():
    assert type(Macro("IN").get_export()).__name__ == "DataFrame"

def test_macro_get_import_method_return_type():
    assert type(Macro("IN").get_import()).__name__ == "DataFrame"

def test_macro_get_export_growth_method_return_type():
    assert type(Macro("IN").get_export_growth()).__name__ == "DataFrame"

def test_macro_get_import_growth_method_return_type():
    assert type(Macro("IN").get_import_growth()).__name__ == "DataFrame"

def test_macro_get_labor_force_method_return_type():
    assert type(Macro("IN").get_labor_force()).__name__ == "DataFrame"

def test_macro_get_population_method_return_type():
    assert type(Macro("IN").get_population()).__name__ == "DataFrame"

def test_macro_get_external_debt_method_return_type():
    assert type(Macro("IN").get_external_debt()).__name__ == "DataFrame"

def test_macro_get_external_GNI_debt_method_return_type():
    assert type(Macro("IN").get_external_debt_GNI()).__name__ == "DataFrame"

def test_macro_get_health_expenditure_method_return_type():
    assert type(Macro("IN").get_health_expenditure()).__name__ == "DataFrame"

def test_macro_get_education_expenditure_method_return_type():
    assert type(Macro("IN").get_education_expenditure()).__name__ == "DataFrame"

def test_macro_get_energy_method_return_type():
    assert type(Macro("IN").get_energy_use()).__name__ == "DataFrame"


