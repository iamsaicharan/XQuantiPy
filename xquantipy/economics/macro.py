import xquantipy.constants as constants
import datetime
import re
import pandas as pd
from dateutil.relativedelta import relativedelta
from xquantipy.fetcher.scraper import Fetcher

class Macro(object):
    """
    A class to represent a macro economics of a country object
    ...
    Attributes:
    country : str
        country code

    Methods:
    get_macros(self, filters = [], period = constants.PERIOD)
        gets the macro economic data of the macro object
    """
    def __init__(self, country):
        assert type(country) == str, "Error: macro argument must be a string"
        self.country = country
    
    def get_macros(self, filters = [], period = constants.PERIOD):
        """
        Summary:
        A method to get the macros data for a Macro object

        Parameters:
        filters: list
            list of Macro economic indicators
        period : int
            period for the calculation

        Return:
        data : Dataframe
            a pandas dataframe with macro data for a particular object
        """
        assert type(filters) == list, "Error: Invalid filters type"
        assert type(period) == str, "Error: Invalid entry for the period"
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {}
        if filters == []:
            filters = ['GDP']
        for i in filters:
            indicators[constants.MACRO_INDICATORS[i]] = i
        country_code = self.country
        data = Fetcher().get_data(filters, country_code, data_date)
        return data