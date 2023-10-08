from macro.analysis import Analysis
from constants import constants
import pandas as pd
import matplotlib.pyplot as plt

class Visual(Analysis):
    """
    A class for visualization of macro objects extends Analysis class from macro.analysis
    ...
    Attributes:
    macros (from parent class) : list
        list of macros objects

    Methods:
    visualize_GDP(self, period=constants.PERIOD)
        get the visualization for GDP data for the object macros
    """
    def visualize_GDP(self, period=constants.PERIOD):
        """
        Summary:
        A method to get visualization for gdp of the object macros

        Parameters:
        period : str
            a string for period: "10Y"

        Return:
        plt : module
            returns the object displays the matplotlib plot of the graph
        """
        df = self.get_merged_GDP(period=period)
        df.set_index('Date', inplace=True)
        for column in df.columns:
            plt.plot(df.index, df[column], label=column)
        plt.title('GDP Comparison')
        plt.xlabel('Date')
        plt.ylabel('GDP')
        plt.legend()
        plt.grid(True)
        plt.tight_layout() 
        return plt
