import xquantipy.constants.constants as constants
import datetime
import re
import pandas as pd
from dateutil.relativedelta import relativedelta
from xquantipy.macro.wbfetcher import Wbfetcher

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
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {}
        if filters == []:
            filters = ['GDP', 'GDP_GROWTH', 'GDP_PER_CAPITA', 
                          'GDP_CURRENT_LCU', 'INFLATION', 'UNEMPLOYMENT', 
                          'EXPORT', 'IMPORT', 'EXPORT_GROWTH', 
                          'IMPORT_GROWTH', 'LABOR_FORCE', 'POPULATION', 
                          'EXTERNAL_DEBT', 'EXTERNAL_DEBT_GNI', 
                          'HEALTH_EXPENDITURE', 'EDUCATION_EXPENDITURE', 
                          'ENERGY_USE']
        for i in filters:
            indicators[constants.INDICATOR[i]] = i
        print(indicators)
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data