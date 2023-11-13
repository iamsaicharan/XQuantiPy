import yfinance as yf
import pandas as pd
import xquantipy.constants as constants
import copy
import plotly.graph_objects as go
import numpy as np
import statsmodels.api as sm
import requests
import json


class Ticker(object):
    """
    A class to represent a stock object
    ...
    Attributes:
    stock : str
        stock ticker name
    period : str
        period selected for the data default: "10Y"
    data : Dataframe
        timeseries daily data of the stock
    fundamentals : dict -> DISCONTINUED DUE TO YAHOO FINANCE
        fundamental data of the stock

    Methods:
    get_adj_close(self)
        returns a adj close dataframe for the ticker
    get_beta(self)
        gets the beta value of the ticker object
    get_alpha(Self, index = constants.BENCHMARK_INDEX, risk_free_rate=constants.RISK_FREE_RATE)
        gets the alpha value of the ticker object
    """
    def __init__(self, ticker, period = constants.PERIOD):
        assert type(ticker) == str, "Error: ticker argument must be a string"
        assert type(period) == str, "Error: period argument must be a string"
        self.stock = ticker
        self.period = period
        data = yf.download(ticker, period=period)
        data.reset_index(inplace=True)
        data['daily_return'] = (data['Adj Close'] - data['Adj Close'].shift(1)) / data['Adj Close'].shift(1)
        data['cum_return'] = (1+data['daily_return']).cumprod()-1
        self.data = data
        url = constants.BASE_OPTIONS_URL + str(self.stock)
        response = requests.get(url=url, headers=constants.HEADERS)
        if response.status_code == 200:
            data = json.loads(response.content)
            self.fundamentals = data['optionChain']['result'][0]['quote']
        else:
            print('Error fetching fundamental data:', response.status_code)
            self.fundamentals = {}

    def get_adj_close(self):
        """
        Summary:
        A method to get only the adj close column which is renamed to the self.stock name

        Return:
        adj_close : dataframe
            return value which represents the dataframe with adj close column
        """
        adj_close = copy.deepcopy(self.data[['Date', 'Adj Close']])
        adj_close.rename(columns={'Adj Close': str(self.stock)}, inplace=True)
        return adj_close

    def get_beta(self, index = constants.BENCHMARK_INDEX):
        """
        Summary:
        A method to calculate the beta value of the stock
        this value measures the expected move in a stock relative
        to movements in the overall market

        Return:
        beta : float
            return value which represents the beta of the stock
        """
        index_data = yf.download(index, period=self.period)
        index_data.reset_index(inplace=True)
        stock_returns = self.data['Adj Close'].pct_change().dropna()
        market_returns = index_data['Adj Close'].pct_change().dropna()
        data = pd.DataFrame({'Stock': stock_returns, 'Market': market_returns}).dropna()
        X = sm.add_constant(data['Market'])  # Add a constant for the intercept
        Y = data['Stock']
        model = sm.OLS(Y, X).fit()
        beta = model.params['Market']
        return round(beta, 2)

    def get_alpha(self, index = constants.BENCHMARK_INDEX, risk_free_rate=constants.RISK_FREE_RATE):
        """
        Summary:
        A method to calculate the alpha value of the stock which is a measure
        to find how a stock is beating a benchmark

        Parameters:
        index : str
            a string for the bench mark index default: ^GSPC
        risk_free_rate : float
            value of the risk free return value default: 0.05 i.e. 5%

        Return:
        alpha : float
            return value which represents the alpha of the stock
        """
        assert type(index) == str, "Error: index argument must be string"
        assert type(risk_free_rate) == float, "Error: risk_free_rate argument must be float"
        index_data = yf.download(index, period=self.period)
        index_data['daily_return'] = (index_data['Adj Close'] - index_data['Adj Close'].shift(1)) / index_data['Adj Close'].shift(1)
        index_data['cum_return'] = (1+index_data['daily_return']).cumprod()-1
        index_start_value = index_data['Adj Close'].iloc[0]
        index_end_value = index_data['Adj Close'].iloc[-1]
        stock_start_value = self.data['Adj Close'].iloc[0]
        stock_end_value = self.data['Adj Close'].iloc[-1]
        # Need to change to Actual return instead of simple return 
        simple_return_index = (index_end_value - index_start_value)/index_start_value
        simple_return_stock = (stock_end_value - stock_start_value)/stock_start_value
        alpha = simple_return_stock - (risk_free_rate + self.get_beta()*(simple_return_index - risk_free_rate))
        return float(alpha)
    
    def show_moving_average(self, type='simple', period = [constants.MOVING_AVERAGE_PERIOD]):
        """
        Summary:
        A method to plot the moving comparison of the particular stock analysis objects

        Parameters:
        type : str
            can be simple or exponential moving average
        period : list
            a list of period to which moving average is calculated
        """
        df = self.get_adj_close()
        label = ''
        if type == 'simple':
            label = 'Simple'
            for i in period:
                df[str('MA_' + str(i))] = df[self.stock].rolling(window=i).mean()
        elif type == 'exponential':
            label = 'Exponential'
            for i in period:
                df[str('EMA_' + str(i))] = df[self.stock].ewm(span=i, adjust=False).mean()
        else:
            raise Exception("type should be simple or exponential")
        columns = list(df.columns)
        columns.pop(0)
        columns.pop(0)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df[self.stock], mode='lines', name='Closing Price'))
        for i in columns:
            fig.add_trace(go.Scatter(x=df['Date'], y=df[i], mode='lines', name=f'{i}'))
        fig.update_layout(title=f'{self.stock} Stock Price with {period}-Day {label} Moving Average', xaxis_title='Date', yaxis_title='Price', showlegend=True)
        fig.show()
    
    def show_moving_average_convergence_divergence(self, fastperiod=12, slowperiod=26, signalperiod=9):
        """
        Summary:
        A method to plot the moving average convergence divergence (MACD) of the particular stock analysis objects

        Parameters:
        fastperiod : int
            fast period for the calculation
        slowperiod : int
            slow period for the calculation
        signalperiod : int
            signal period for the calculation
        """
        df = self.get_adj_close()
        EMAfast = df[self.stock].ewm(span=fastperiod, min_periods=fastperiod).mean()
        EMAslow = df[self.stock].ewm(span=slowperiod, min_periods=slowperiod).mean()
        MACD = EMAfast - EMAslow
        signal = MACD.ewm(span=signalperiod, min_periods=signalperiod).mean()
        MACDhist = MACD - signal
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'],y=MACD,mode='lines', name='MACD'))
        fig.add_trace(go.Scatter(x=df['Date'],y=signal,mode='lines', name='Signal'))
        fig.add_trace(go.Bar(x=df['Date'],y=signal, name='MACD Histogram'))
        fig.update_layout(title="MACD", xaxis_title="Date", yaxis_title="MACD")
        fig.show()
    
    def show_parabolic_sar(self, af=0.02, max_af=0.2):
        """
        Summary:
        A method to plot the Parabolic SAR of the particular stock analysis objects

        Parameters:
        af : int
            acceleration factor for the calculation
        max_af : int
            max acceleration factor for the calculation
        """
        psar_values = []
        initial_psar = self.data.High[0]
        trend = 'up'
        af = 0.02
        new_psar = initial_psar
        extreme_point = self.data.High[0]
        for i in range(1, len(self.data)):
            current_close = self.data.Close[i]
            current_high = self.data.High[i]
            current_low = self.data.Low[i]
            if trend == 'up':
                if current_high > extreme_point:
                    extreme_point = current_high
                    af = min(af + 0.02, max_af)
                else:
                    new_psar = initial_psar + af * (extreme_point - initial_psar)
                    new_psar = max(new_psar, min(current_high, current_low))

                if current_low < new_psar:
                    trend = 'down'
                    initial_psar = current_low
                    af = 0.02
                    extreme_point = current_low
                else:
                    initial_psar = new_psar
            else:
                if current_low < extreme_point:
                    extreme_point = current_low
                    af = min(af + 0.02, max_af)
                else:
                    new_psar = initial_psar - af * (initial_psar - extreme_point)
                    new_psar = max(new_psar, min(current_high, current_low))

                if current_high > new_psar:
                    trend = 'up'
                    initial_psar = current_high
                    af = 0.02
                    extreme_point = current_high
                else:
                    initial_psar = new_psar
            psar_values.append(new_psar)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.data.Date, y=psar_values, name="PSAR"))
        fig.add_trace(go.Scatter(x=self.data.Date, y=self.data.Close, name="Close Price"))
        fig.update_layout(title="PSAR and Close Price", xaxis_title="Date", yaxis_title="Price")
        fig.show()
    
    def show_bollinger_bands(self, period=constants.MOVING_AVERAGE_PERIOD):
        """
        Summary:
        A method to plot the bollinger band of the particular stock analysis objects

        Parameters:
        period : int
            period for the calculation
        """
        moving_average = self.data['Close'].rolling(window=period).mean()
        standard_deviation = self.data['Close'].rolling(window=period).std()
        upper_band = moving_average + 2 * standard_deviation
        lower_band = moving_average - 2 * standard_deviation
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.data['Date'], y=self.data['Close'], name='Close Price'))
        fig.add_trace(go.Scatter(x=self.data['Date'], y=upper_band, name='Upper Bollinger Band'))
        fig.add_trace(go.Scatter(x=self.data['Date'], y=lower_band, name='Lower Bollinger Band'))
        fig.update_layout(title='Bollinger Bands of a Stock', xaxis_title='Date', yaxis_title='Price')
        fig.show()

    def __str__(self):
        start_date = str(self.data['Date'].iloc[0])[:10]
        end_date = str(self.data['Date'].iloc[-1])[:10]
        return str(self.stock).upper() + " [" + start_date + " - " + end_date + "]"
    