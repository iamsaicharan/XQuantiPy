import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import constants.constants as constants

class Analysis(object):
    """
    A class to perform the analysis on tickers
    ...
    Attributes:
    tickers : list
        list of stock ticker objects

    Methods:
    show_alpha_vs_beta(self)
        plots a graph between alpha values and beta values
        of the stocks listed
    """
    def __init__(self, tickers):
        assert type(tickers) == list, "Error: Please insert list of ticker objects as arguments"
        assert len(tickers) > 0, "Error: Empty list of ticker objects as arguments"
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
        plt : module
            returns the object displays the matplotlib plot of the graph
        """
        assert type(index) == str, "Error: index argument must be string"
        assert type(risk_free_rate) == float, "Error: risk_free_rate argument must be float"
        data = {}
        for ticker in self.tickers:
            data[ticker.stock] = [ticker.get_alpha(index), ticker.get_beta()]
        labels, points = zip(*data.items())
        x, y = zip(*points)
        plt.figure(figsize=(8, 6))
        plt.axhline(1, color='black',linewidth=2)
        plt.axvline(0, color='black',linewidth=2)
        plt.scatter(x, y, marker='o', s=100)
        for i, label in enumerate(labels):
            plt.annotate(label, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')
        plt.text(2, 1.1, 'High Return - High Risk', fontsize=7, ha='center', va='center')
        plt.text(2, 0.9, 'High Return - Low Risk', fontsize=7, ha='center', va='center')
        plt.text(-2, 1.1, 'Low Return - High Risk', fontsize=7, ha='center', va='center')
        plt.text(-2, 0.9, 'Low Return - Low Risk', fontsize=7, ha='center', va='center')
        plt.title('Alpha vs Beta')
        plt.xlabel('Alpha')
        plt.ylabel('Beta')
        plt.grid(True)
        return plt
    
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
        

    