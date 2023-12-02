import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import xquantipy.constants as constants
import plotly.graph_objects as go


class Analysis(object):
    """
    A class to perform the analysis on macros
    ...
    Attributes:
    macros : list
        list of macros objects

    Methods:
    get_merged_GDP(self, period=constants.PERIOD)
        get the merged GDP data for the object macros
    visualize(self, filter=None, period=constants.PERIOD)
        get visualization for gdp of the object macros
    """
    def __init__(self, macros):
        assert type(macros) == list, "Error: Please insert list of macros objects as arguments"
        assert len(macros) > 0, "Error: Empty list of macro objects as arguments"
        for i in macros:
            assert type(i).__name__ == "Macro", "Error: List must have macro objects"
        self.macros = macros
 
    def get_merged_macro(self, filter = None, period=constants.PERIOD):
        """
        Summary:
        A method to get the merged gdp dataframe for the object macros

        Parameters:
        filter : str
            a string for filter
        period : str
            a string for period: "10Y"

        Return:
        merged_df : DataFrame
            returns the DataFrame with the merged GDP
        """
        assert type(filter) == str, "Error: Invalid filter type"
        assert type(period) == str, "Error: Invalid period type"
        if len(self.macros) == 1:
            df = self.macros[0].get_macros(filters = [filter], period=period)
            df.rename(columns={str(filter): str(self.macros[0].country)}, inplace=True)
            return df
        data_list = []
        for i in self.macros:
            df = i.get_macros(filters = [filter], period=period)
            df.rename(columns={str(filter): str(i.country)}, inplace=True)
            data_list.append(df)
        merged_df = data_list[0]
        for i in range(1, len(data_list)):
            merged_df = pd.merge(merged_df, data_list[i], on='Year', how='outer')
        return merged_df
    
    def visualize(self, filter=None, period=constants.PERIOD):
        """
        Summary:
        A method to get visualization for gdp of the object macros

        Parameters:
        filter : str
            a string for filter
        period : str
            a string for period: "10Y"

        Return:
        plt : module
            returns the object displays the matplotlib plot of the graph
        """
        assert type(filter) == str, "Error: Invalid filter type"
        assert type(period) == str, "Error: Invalid period type"
        df = self.get_merged_macro(filter=filter, period=period)
        df.set_index('Year', inplace=True)
        traces = []
        for column in df.columns:
            trace = go.Scatter(x=df.index, y=df[column], mode='lines', name=column)
            traces.append(trace)
        layout = go.Layout(title=str(filter) + ' Comparison', xaxis=dict(title='Year'), yaxis=dict(title=str(filter)), showlegend=True, template='plotly_dark')
        fig = go.Figure(data=traces, layout=layout)
        return fig