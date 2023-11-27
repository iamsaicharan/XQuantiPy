import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import xquantipy.constants as constants
import plotly.express as px
import plotly.graph_objects as go

class Analysis(object):
    """
    A class to perform the analysis on tickers
    ...
    Attributes:
    tickers : list/ticker object
        Input can be a list of stock ticker objects or one stock ticker object

    Methods:
    show_alpha_vs_beta(self)
        plots a graph between alpha values and beta values
        of the stocks listed
    get_merged_adj_close(self)
        get merge all the data with adj close values in the tickers list
    show_merged_adj_close_chart(self)
        plot the adj close comparison of the stocks
    """
    def __init__(self, tickers):
        assert type(tickers) == list, "Error: must be a list of ticker objects"
        for i in tickers:
            assert type(i).__name__ == "Ticker", "Error: List must have ticker objects"
        self.tickers = tickers

    def show_alpha_vs_beta(self, index = constants.BENCHMARK_INDEX, risk_free_rate = constants.RISK_FREE_RATE):
        """
        Summary:
        A method to plot the alpha vs beta comparison of the stocks

        Parameters:
        index : str
            a string for the bench mark index default: ^GSPC
        risk_free_rate : float
            value of the risk free return value default: 0.05 i.e. 5%
        
        Return:
        fig : matplotlib
            a figure object represents alpha vs beta
        """
        assert type(self.tickers) == list, "Error: show_alpha_vs_beta works for a list of tickers object"
        assert type(index) == str, "Error: index argument argument must be string"
        assert type(risk_free_rate) == float, "Error: risk_free_rate argument must be float"
        data = {}
        for ticker in self.tickers:
            data[ticker.stock] = [ticker.get_alpha(index), ticker.get_beta()]
        labels, points = zip(*data.items())
        x, y = zip(*points)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x,y=y,mode="markers+text",text=labels,textposition="top center",marker=dict(size=10),hoverinfo="text",))
        fig.add_hline(1, line_color="black", line_width=2)
        fig.add_vline(0, line_color="black", line_width=2)
        fig.update_layout(
            title="Alpha vs Beta",
            xaxis_title="Alpha",
            yaxis_title="Beta",
            annotations=[
                dict(x=2,y=1.1,text="High Return - High Risk",font_size=15),
                dict(x=2,y=0.9,text="High Return - Low Risk",font_size=15),
                dict(x=-2,y=1.1,text="Low Return - High Risk",font_size=15),
                dict(x=-2,y=0.9,text="Low Return - Low Risk",font_size=15),
            ], 
            template='plotly_dark',
            
        )
        return fig
    
    def get_merged_adj_close(self):
        """
        Summary:
        A method to merge all the data with adj close values in the tickers list

        Return:
        merged_dfs : DataFrame
            returns the dataframe with adj close value of the tickers
        """
        if len(self.tickers) == 1:
            return self.tickers[0].get_adj_close()
        merged_dfs = self.tickers[0].get_adj_close()
        for i in range(1, len(self.tickers)):
            merged_dfs = pd.merge(merged_dfs, self.tickers[i].get_adj_close(), on='Date', how='outer')
        return merged_dfs
        
    def show_merged_adj_close_chart(self):
        """
        Summary:
        A method to plot the adj close comparison of the stocks

        Return:
        fig : matplotlib
            a figure object represents merged adj close chart
        """
        merged_dfs = self.tickers[0].get_adj_close()
        if len(self.tickers) == 1:
            return px.line(merged_dfs.set_index('Date'))
        for i in range(1, len(self.tickers)):
            merged_dfs = pd.merge(merged_dfs, self.tickers[i].get_adj_close(), on='Date', how='outer')
        fig = px.line(merged_dfs.set_index('Date'))
        return fig