import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import xquantipy.constants.constants as constants

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
    """
    def __init__(self, macros):
        assert type(macros) == list, "Error: Please insert list of macros objects as arguments"
        assert len(macros) > 0, "Error: Empty list of macro objects as arguments"
        for i in macros:
            assert type(i).__name__ == "Macro", "Error: List must have macro objects"
        self.macros = macros
    
    def get_merged_GDP(self, period=constants.PERIOD):
        """
        Summary:
        A method to get the merged gdp dataframe for the object macros

        Parameters:
        period : str
            a string for period: "10Y"

        Return:
        merged_df : DataFrame
            returns the DataFrame with the merged GDP
        """
        if len(self.macros) == 1:
            df = self.macros[0].get_GDP(period=period)
            df.rename(columns={'GDP (current US$)': str(self.macros[0].country)}, inplace=True)
            return df
        data_list = []
        for i in self.macros:
            df = i.get_GDP(period=period)
            df.rename(columns={'GDP (current US$)': str(i.country)}, inplace=True)
            data_list.append(df)
        merged_df = data_list[0]
        for i in range(1, len(data_list)):
            merged_df = pd.merge(merged_df, data_list[i], on='Date', how='outer')
        return merged_df