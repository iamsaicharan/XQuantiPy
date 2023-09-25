import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import constants

class Analysis(object):
    """
    A class to perform the analysis
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
        data = {}
        for ticker in self.tickers:
            data[ticker.stock] = [ticker.get_alpha(index), ticker.get_beta()]
        labels, points = zip(*data.items())
        x, y = zip(*points)
        plt.figure(figsize=(8, 6))
        plt.scatter(x, y, marker='o', s=100)
        for i, label in enumerate(labels):
            plt.annotate(label, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')
        plt.title('Alpha vs Beta')
        plt.xlabel('Alpha')
        plt.ylabel('Beta')
        plt.grid(True)
        return plt
        
    