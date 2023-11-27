# XQuantiPy - Financial Analysis

![Alt Text](xQuantipy.png)

xquantipy is a python module for downloading macro economic data & stock data with the modules included for the analysis.

## Installation

Install `xquantipy` using `pip`:

```bash
pip install xquantipy
```

### Requirements

* beautifulsoup4==4.12.2
* matplotlib==3.8.0
* numpy==1.26.1
* pandas==2.1.2
* pipreqs==0.4.13
* plotly==5.18.0
* pytest==7.4.0
* python_dateutil==2.8.2
* Requests==2.31.0
* seaborn==0.13.0
* setuptools==68.0.0
* statsmodels==0.14.0
* yfinance==0.2.29

## Get started as stand-alone

Clone the repository using the following command

```bash
git clone https://github.com/iamsaicharan/XQuantiPy.git
```

Once cloned go into the project directory, install the requirements folder and run app.py

```bash
cd XQuantiPy
pip3 install -r requirements.txt
python3 app.py
```

This should start the web server in localhost in default port

## Get started as python module

### macro module

The `Macro` module helps to get the macro economic data:

```python
from xquantipy.economics.macro import Macro

USA = Macro("USA")
IND = Macro("IND")

# Get GDP data for USA with default period of 10 Years
USA_GDP = USA.get_macros(filters=['GDP'])
# Get GDP Growth Rate & GNI for USA with period of 15 Years
USA_GDP_GROWTH_GNI = USA.get_macros(filters=['GDP_GROWTH','GNI'], period='15Y')

# Get GDP data for India with default period of 10 Years
IND_GDP = IND.get_macros(filters=['GDP'])
# Get GDP Growth Rate & GNI for India with period of 15 Years
IND_GDP_GROWTH = IND.get_macros(filters=['GDP_GROWTH', 'GNI'], period='15Y')
```

The `Analysis` module helps to get the macro economic analysis and visualization:

```python
from xquantipy.economics.analysis import Analysis

USA = Macro("USA")
IND = Macro("IND")
Countries = MAnalysis([USA, IND])

# Get merged GDP data for the Countries
GDP_COMPARE_DF = Countries.get_merged_macro('GDP')
# Visualize GDP data for the Countries
Countries.visualize("GDP").show()
```

### ticker module

The `Ticker` module helps to get the ticker data:

```python
from xquantipy.stocks.ticker import Ticker

# Get AAPL object with default period of "10Y"
AAPL = Ticker('AAPL')
# Get GE object with period of "15Y"
GE = Ticker('GE', period='15Y')

# Get stock data with Date, Open, High, Low, Close, Adj Close, Volume, daily_return, cum_return
AAPL_DF = AAPL.data
# Get stock fundamental data in a dictionary format
AAPL_FUNDAMENTALS = AAPL.fundamentals

# Get Beta value of the stock
GE_BETA = GE.get_beta()
# Get Alpha value of the stock compared to default index "^GSPC"
GE_ALPHA = GE.get_alpha()
```

The `Analysis` module helps for analyzing ticker data:

```python
from xquantipy.stocks.ticker import Ticker
from xquantipy.stocks.analysis import Analysis

AAPL = Ticker('AAPL')
GE = Ticker('GE')
AAPL_GE = Analysis([AAPL, GE])

# Get merged dataframes containing adj close values
AAPL_GE_DF = AAPL_GE.get_merged_adj_close()
# Visualize alpha vs beta values compared for the stocks
AAPL_GE.show_alpha_vs_beta().show()
```

## Contributing

Want to help build XQuantiPy? Check out our [CONTRIBUTING.md](CONTRIBUTING.md)

## License

[Project Name] is licensed under the MIT License. Please read the LICENSE: [LICENSE.md](LICENSE.md) file for more information.
