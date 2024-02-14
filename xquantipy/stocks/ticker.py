import yfinance as yf
import pandas as pd
import xquantipy.constants as constants
import copy
import plotly.graph_objects as go
import numpy as np
import statsmodels.api as sm
import requests
import json
from matplotlib import dates as mdates


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
    show_adj_close(self)
        plot adj close for the ticker
    get_beta(self)
        gets the beta value of the ticker object
    get_alpha(Self, index = constants.BENCHMARK_INDEX, risk_free_rate=constants.RISK_FREE_RATE)
        gets the alpha value of the ticker object
    show_moving_average(self, period = [constants.MOVING_AVERAGE_PERIOD])
        get the moving average of the particular stock analysis objects
    show_moving_average_convergence_divergence(self, fastperiod=12, slowperiod=26, signalperiod=9)
        plot the moving average convergence divergence (MACD) of the particular stock analysis objects
    show_parabolic_sar(self, af=0.02, max_af=0.2)
        plot the Parabolic SAR of the particular stock analysis objects
    show_bollinger_bands(self, period=constants.MOVING_AVERAGE_PERIOD)
        plot the bollinger band of the particular stock analysis objects
    show_profit_loss(self, investment=5000)
        plot profit loss of a particular stock based on the investment
    show_roi(self)
        plot roi of a particular stock
    get_kelly_criterion(self)
    show_mass_index(self, periods=25, ema_periods=9)
    show_vortex_indicator(self, period=14)
    show_stochastic_oscillator(self, period=14, k=3)

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
    
    def show_adj_close(self):
        """
        Summary:
        A method to plot adj close column which is renamed to the self.stock name

        Return:
        fig : module
            return value which represents the matplotlib figure with adj close column
        """
        df = self.get_adj_close()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df[self.stock], mode='lines', name='Closing Price'))
        fig.update_layout(
            title=f'{self.stock} Stock Price', 
            xaxis_title='Date', 
            yaxis_title=('Adj Close ' + str(self.stock)), 
            showlegend=True, 
            template='plotly_dark',
            )
        return fig

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
        index_data = self.data
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
    
    def show_candle_stick(self):
        """
        Summary:
        A method to plot candle strick for self.stock name

        Return:
        fig : module
            return value which represents the matplotlib figure with candle stick
        """
        df = self.data
        fig = go.Figure(data=[go.Candlestick(x=df['Date'],open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'])])
        fig.update_layout(
            title=f'{self.stock}', 
            xaxis_title='Date', 
            yaxis_title='Price', 
            showlegend=True,
            template='plotly_dark',)
        return fig
    
    def show_line(self):
        """
        Summary:
        A method to plot line chart for self.stock data

        Return:
        fig : module
            return value which represents the plotly figure with line chart
        """
        df = self.data
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Adj Close'], mode='lines', name='Closing Price'))
        fig.update_layout(
            title=f'{self.stock} Stock Price with {self.period}-Day', 
            xaxis_title='Date', 
            yaxis_title='Price', 
            showlegend=True,
            template='plotly_dark',)
        return fig
    
    def show_volume(self):
        """
        Summary:
        A method to plot volume chart for self.stock data

        Return:
        fig : module
            return value which represents the plotly figure with volume chart
        """
        df = self.data
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name='Volume'))
        fig.update_layout(
            title=f'{self.stock} Stock Volume with {self.period}-Day', 
            xaxis_title='Date', 
            yaxis_title='Price', 
            showlegend=True,
            template='plotly_dark',)
        return fig
    
    def get_rsi(self, window=14, upper_band=70, lower_band=30):
        df = self.data
        diff = df['Close'].diff(1)
        gain = diff.where(diff > 0, 0)
        loss = -diff.where(diff < 0, 0)
        avg_gain = gain.rolling(window=window, min_periods=1).mean()
        avg_loss = loss.rolling(window=window, min_periods=1).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        df['RSI'] = rsi
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], yaxis='y2', mode='lines', name='RSI', line=dict(color='red')))
        fig.add_shape(go.layout.Shape(type='line', x0=df['Date'].min(), x1=df['Date'].max(), y0=upper_band, y1=upper_band, line=dict(color='green', width=2), yref='y2'))
        fig.add_shape(go.layout.Shape(type='line', x0=df['Date'].min(), x1=df['Date'].max(), y0=lower_band, y1=lower_band, line=dict(color='green', width=2), yref='y2'))
        fig.update_layout(
            title='RSI Chart',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Price'),
            yaxis2=dict(title='RSI', overlaying='y', side='right'),
            template='plotly_dark',
        )
        return fig
    
    def get_moving_average(self, type='simple', period = [constants.MOVING_AVERAGE_PERIOD]):
        """
        Summary:
        A method to get the moving average of the particular stock analysis objects

        Parameters:
        type : str
            can be simple or exponential moving average
        period : list
            a list of period to which moving average is calculated

        Returns:
        df : Dataframe
            a Dataframe of the stock with moving average
        """
        df = self.get_adj_close()
        if type == 'simple':
            for i in period:
                df[str('MA_' + str(i))] = df[self.stock].rolling(window=i).mean()
        elif type == 'exponential':
            for i in period:
                df[str('EMA_' + str(i))] = df[self.stock].ewm(span=i, adjust=False).mean()
        else:
            raise Exception("type should be simple or exponential")
        return df

    def show_moving_average(self, type='simple', period = [constants.MOVING_AVERAGE_PERIOD]):
        """
        Summary:
        A method to plot the moving comparison of the particular stock analysis objects

        Parameters:
        type : str
            can be simple or exponential moving average
        period : list
            a list of period to which moving average is calculated

        Return:
        fig : matplotlib
            a figure object represents moving average
        """
        df = self.get_moving_average(type, period)
        columns = list(df.columns)
        columns.pop(0)
        columns.pop(0)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df[self.stock], mode='lines', name='Closing Price'))
        for i in columns:
            fig.add_trace(go.Scatter(x=df['Date'], y=df[i], mode='lines', name=f'{i}'))
        fig.update_layout(
            title=f'{self.stock} Stock Price with {period}-Day {type} Moving Average', 
            xaxis_title='Date', 
            yaxis_title='Price', 
            showlegend=True,
            template='plotly_dark',)
        return fig
    
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
        
        Return:
        fig : matplotlib
            a figure object represents moving average convergence divergence
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
        fig.update_layout(
            title="MACD", 
            xaxis_title="Date", 
            yaxis_title="MACD", 
            template='plotly_dark',
            )
        return fig
    
    def show_parabolic_sar(self, af=0.02, max_af=0.2):
        """
        Summary:
        A method to plot the Parabolic SAR of the particular stock analysis objects

        Parameters:
        af : int
            acceleration factor for the calculation
        max_af : int
            max acceleration factor for the calculation

        Return:
        fig : matplotlib
            a figure object represents parabolic SAR
        """
        psar_values = []
        initial_psar = self.data.High[0]
        trend = 'up'
        af = 0.02
        new_psar = initial_psar
        extreme_point = self.data.High[0]
        for i in range(1, len(self.data)):
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
        fig.update_layout(
            title="PSAR and Close Price", 
            xaxis_title="Date", 
            yaxis_title="Price", 
            template='plotly_dark',
            )
        return fig
    
    def show_bollinger_bands(self, period=constants.MOVING_AVERAGE_PERIOD):
        """
        Summary:
        A method to plot the bollinger band of the particular stock analysis objects

        Parameters:
        period : int
            period for the calculation

        Return:
        fig : matplotlib
            a figure object represents bollinger band
        """
        moving_average = self.data['Close'].rolling(window=period).mean()
        standard_deviation = self.data['Close'].rolling(window=period).std()
        upper_band = moving_average + 2 * standard_deviation
        lower_band = moving_average - 2 * standard_deviation
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.data['Date'], y=self.data['Close'], name='Close Price'))
        fig.add_trace(go.Scatter(x=self.data['Date'], y=upper_band, name='Upper Bollinger Band'))
        fig.add_trace(go.Scatter(x=self.data['Date'], y=lower_band, name='Lower Bollinger Band'))
        fig.update_layout(
            title='Bollinger Bands of a Stock', 
            xaxis_title='Date', 
            yaxis_title='Price', 
            template='plotly_dark',
            )
        return fig
    
    def show_profit_loss(self, investment=5000):
        """
        Summary:
        A method to plot the profit or loss based on investments of the particular stock objects

        Parameters:
        investment : int
            investment value to invest in the stock

        Return:
        fig : matplotlib
            a figure object represents profit loss
        results : dict
            a dictionary with profit loss results
        """
        initial = self.data.Close.iloc[0]
        shares = int(investment/initial)
        investment = initial*shares
        current = self.data.Close.iloc[-1]
        current_value = current * shares
        profit_loss = current_value - investment
        percent_gain_loss = (profit_loss/current_value)*100
        percentage_returns = (current_value - investment) / investment * 100
        net_gains_or_losses = (current - initial) / initial * 100
        total_return = ((current_value / investment) - 1) * 100
        dates = self.data['Date']
        profits_losses = [investment]
        for i in range(1, len(self.data)):
            shares = int(profits_losses[0] / self.data.Close.iloc[0])
            close_price = self.data.Close.iloc[i]
            current_value = close_price * shares
            profit_loss_ = current_value - investment
            profits_losses.append(profits_losses[0] + profit_loss_)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=profits_losses, mode='lines', name='Profit/Loss'))
        fig.add_shape(go.layout.Shape(type='line', x0=min(dates), x1=max(dates), y0=investment, y1=investment, line=dict(color='white', dash='dash'), name='Breakeven'))
        fig.update_layout(
            title='Accumulated Profit/Loss Over Time',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Accumulated Profit/Loss'),
            legend=dict(x=0, y=1, traceorder='normal'),
            template='plotly_dark',
        )
        results = {
            "profit_loss": profit_loss,
            "percent_gain_loss": percent_gain_loss,
            "percentage_returns": percentage_returns,
            "net_gains_or_losses": net_gains_or_losses,
            "total_return": total_return
        }
        return fig, results
    
    def show_roi(self):
        """
        Summary:
        A method to get the plot for roi

        Return:
        fig : matplotlib
            a figure object represents roi
        """
        df = self.data
        df["ROI"] = ((df["Adj Close"] - df["Adj Close"].shift(1)) / df["Adj Close"].shift(1) * 100)
        dfc = df.copy()
        dfc["VolumePositive"] = dfc["Open"] < dfc["Adj Close"]
        dfc = dfc.reset_index()
        dfc["Date"] = pd.to_datetime(dfc["Date"])
        dfc["Date"] = dfc["Date"].apply(mdates.date2num)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df["ROI"], mode='lines', name='ROI', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=df.index, y=[0] * len(df), mode='lines', name='Zero Line', line=dict(color='blue', dash='dash')))
        fig.update_layout(
            title='ROI',
            xaxis=dict(title='Date'),
            yaxis=dict(title='ROI'),
            legend=dict(x=0, y=1, traceorder='normal'),
            template='plotly_dark',
        )
        return fig
    
    def get_kelly_criterion(self):
        """
        Summary:
        A method to get the kelly criterion for the whole period of the dataframe

        Return:
        kelly_criterion : int
            an integer represents kelly criterion
        """
        df = self.data
        df['Daily Return'] = df['Adj Close'].pct_change()
        mean_return = df['Daily Return'].mean()
        std_return = df['Daily Return'].std()
        p_win = 0.5 + (mean_return / (2 * std_return))
        p_loss = 1 - p_win
        # odds = 1
        odds = p_win/p_loss
        kelly_fraction = (p_win * odds - p_loss) / odds
        return kelly_fraction
    
    def show_mass_index(self, periods=25, ema_periods=9):
        """
        Summary:
        A method to plot the mass index of the particular stock objects

        Parameters:
        periods : int (optional default=25)
            period of the plot
        ema_periods : int (optional default=9)
            exponential moving average period of the plot


        Return:
        fig : matplotlib
            a figure object represents mass index
        """
        df = self.data
        df['hl_range'] = df['High'] - df['Low']
        df['hl_double_exponential_ema'] = df['hl_range'].ewm(span=ema_periods, adjust=False).mean()
        df['hl_double_exponential_ema_sum'] = df['hl_double_exponential_ema'].rolling(window=periods).sum()
        df['mass_index'] = df['hl_double_exponential_ema_sum'] / df['hl_double_exponential_ema']
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['mass_index'], mode='lines', name='Mass Index', line=dict(color='blue')))
        fig.update_layout(title='Mass Index of the Stock', xaxis_title='Date', yaxis_title='Mass Index',template='plotly_dark')
        return fig
    
    def show_vortex_indicator(self, period=14):
        """
        Summary:
        A method to plot the vortex indicator of the particular stock objects

        Parameters:
        periods : int (optional default=14)
            period of the plot

        Return:
        fig : matplotlib
            a figure object represents mass index
        """
        data = self.data
        data['TR'] = data['High'].combine(data['Low'], max) - data['Low'].combine(data['Close'].shift(), max)
        data['+VM'] = abs(data['High'].shift() - data['Low'])
        data['-VM'] = abs(data['Low'].shift() - data['High'])
        data['+VI'] = data['+VM'].rolling(window=period).sum() / data['TR'].rolling(window=period).sum()
        data['-VI'] = data['-VM'].rolling(window=period).sum() / data['TR'].rolling(window=period).sum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['+VI'], mode='lines', name='+VI'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['-VI'], mode='lines', name='-VI'))
        fig.update_layout(title=f'Vortex Indicator', xaxis_title='Date', yaxis_title='Vortex Indicator',legend=dict(x=0, y=1, traceorder='normal'),template='plotly_dark')
        return fig
    
    def show_stochastic_oscillator(self, period=14, k=3):
        """
        Summary:
        A method to plot the stochastic oscillator of the particular stock objects

        Parameters:
        periods : int (optional default=14)
            period of the plot
        k : int (optional default=3)
            k value

        Return:
        fig : matplotlib
            a figure object represents mass index
        """
        df = self.data
        df['Lowest_Low'] = df['Low'].rolling(window=period).min()
        df['Highest_High'] = df['High'].rolling(window=period).max()
        df['%K'] = ((df['Close'] - df['Lowest_Low']) / (df['Highest_High'] - df['Lowest_Low'])) * 100
        df['%D'] = df['%K'].rolling(window=k).mean()
        trace_close = go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price', line=dict(color='white'))
        trace_percent_k = go.Scatter(x=df['Date'], y=df['%K'], mode='lines', name='%K Line')
        trace_percent_d = go.Scatter(x=df['Date'], y=df['%D'], mode='lines', name='%D Line')
        overbought_line = go.Scatter(x=df['Date'], y=[80] * len(df), mode='lines', name='Overbought Level')
        oversold_line = go.Scatter(x=df['Date'], y=[20] * len(df), mode='lines', name='Oversold Level')
        layout = go.Layout(title='Stochastic Oscillator',
                        xaxis=dict(title='Date'),
                        yaxis=dict(title='Value'),
                        showlegend=True,
                        legend=dict(x=0, y=1, traceorder='normal', orientation='h'))
        fig = go.Figure(data=[trace_close, trace_percent_k, trace_percent_d, overbought_line, oversold_line], layout=layout)
        fig.update_layout(template='plotly_dark')
        return fig

    def __str__(self):
        start_date = str(self.data['Date'].iloc[0])[:10]
        end_date = str(self.data['Date'].iloc[-1])[:10]
        return str(self.stock).upper() + " [" + start_date + " - " + end_date + "]"
    