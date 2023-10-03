"""
Script for testing the funcationality of the application
...

Requirement:
pytest module -> pip install pytest

To test:
> pytest

"""
import yfinance as yf
from ticker.ticker import Ticker
from ticker.analysis import Analysis
from micro.macro import Macro
import pytest

test_tickers = ['AAPL', 'MSFT']
test_macros = ['IN', 'USA']

@pytest.mark.parametrize("tickers", test_tickers)
def test_ticker_data_type(tickers):
    assert type(Ticker(tickers).data).__name__ == "DataFrame"

@pytest.mark.parametrize("tickers", test_tickers)
def test_ticker_fundamentals_type(tickers):
    assert type(Ticker(tickers).fundamentals) == dict

@pytest.mark.parametrize("tickers", test_tickers)
def test_ticker_get_adj_close_method_return_type(tickers):
    assert type(Ticker(tickers).get_adj_close()).__name__ == "DataFrame"

@pytest.mark.parametrize("tickers", test_tickers)
def test_ticker_get_alpha_method_return_type(tickers):
    assert type(Ticker(tickers).get_alpha()) == float

@pytest.mark.parametrize("tickers", test_tickers)
def test_analysis_show_alpha_vs_beta_return_type(tickers):
    assert type(Analysis([Ticker(tickers)]).show_alpha_vs_beta()).__name__ == "module"

@pytest.mark.parametrize("tickers", test_tickers)
def test_analysis_get_merged_adj_close_return_type(tickers):
    assert type(Analysis([Ticker(tickers)]).get_merged_adj_close()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_GDP_method_return_type(macros):
    assert type(Macro(macros).get_GDP()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_GDP_growth_method_return_type(macros):
    assert type(Macro(macros).get_GDP_growth()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_GDP_per_capita_method_return_type(macros):
    assert type(Macro(macros).get_GDP_per_capita()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_GDP_per_capita_method_return_type(macros):
    assert type(Macro(macros).get_GDP_per_capita()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_GDP_current_LCU_method_return_type(macros):
    assert type(Macro(macros).get_GDP_current_LCU()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_inflation_method_return_type(macros):
    assert type(Macro(macros).get_inflation()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_unemployment_method_return_type(macros):
    assert type(Macro(macros).get_unemployment()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_export_method_return_type(macros):
    assert type(Macro(macros).get_export()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_import_method_return_type(macros):
    assert type(Macro(macros).get_import()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_export_growth_method_return_type(macros):
    assert type(Macro(macros).get_export_growth()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_import_growth_method_return_type(macros):
    assert type(Macro(macros).get_import_growth()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_labor_force_method_return_type(macros):
    assert type(Macro(macros).get_labor_force()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_population_method_return_type(macros):
    assert type(Macro(macros).get_population()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_external_debt_method_return_type(macros):
    assert type(Macro(macros).get_external_debt()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_external_GNI_debt_method_return_type(macros):
    assert type(Macro(macros).get_external_debt_GNI()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_health_expenditure_method_return_type(macros):
    assert type(Macro(macros).get_health_expenditure()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_education_expenditure_method_return_type(macros):
    assert type(Macro(macros).get_education_expenditure()).__name__ == "DataFrame"

@pytest.mark.parametrize("macros", test_macros)
def test_macro_get_energy_method_return_type(macros):
    assert type(Macro(macros).get_energy_use()).__name__ == "DataFrame"
