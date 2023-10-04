from macro.analysis import Analysis
from constants import constants
import pandas as pd
import matplotlib.pyplot as plt

class Visual(Analysis):

    def visualize_GDP(self, period=constants.PERIOD):
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
