import constants.constants as constants
import datetime
import re
import pandas as pd
from dateutil.relativedelta import relativedelta
from macro.wbfetcher import Wbfetcher

class Macro(object):
    """
    A class to represent a macro economics of a country object
    ...
    Attributes:
    country : str
        country code

    Methods:
    get_GDP(self, period = constants.PERIOD)
        gets the GDP data of the macro object
    get_GDP_growth(self, period = constants.PERIOD)
        gets the alpha data of the macro object
    get_GDP_per_capita(self, period = constants.PERIOD)
        get the GDP per capita of the macro object
    get_GDP_current_LCU(self, period = constants.PERIOD)
        gets the GDP current LCU data of the macro object
    get_inflation(self, period = constants.PERIOD)
        gets the inflation data of the macro object
    get_unemployment(self, period = constants.PERIOD)
        gets the unemployment data of the macro object
    get_export(self, period = constants.PERIOD)
        gets the export data of the macro object
    get_import(self, period = constants.PERIOD)
        gets the import data of the macro object
    get_export_growth(self, period = constants.PERIOD)
        gets the export growth data of the macro object
    get_import_growth(self, period = constants.PERIOD)
        gets the import growth data of the macro object
    get_labor_force(self, period = constants.PERIOD)
        gets the labor force data of the macro object
    get_population(self, period = constants.PERIOD)
        gets the population data of the macro object
    get_external_debt(self, period = constants.PERIOD)
        gets the external debt data of the macro object
    get_external_debt_GNI(self, period = constants.PERIOD)
        gets the external debt GNI data of the macro object
    get_health_expenditure(self, period = constants.PERIOD)
        gets the health expenditure data of the macro object
    get_education_expenditure(self, period = constants.PERIOD)
        gets the education expenditure data of the macro object
    get_energy_use(self, period = constants.PERIOD)
        gets the energy us data of the macro object
    """
    def __init__(self, country):
        assert type(country) == str, "Error: macro argument must be a string"
        self.country = country

    def get_GDP(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of GDP for a period
        GDP - measure of all the final goods and services produced in a period

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents gdp for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'NY.GDP.MKTP.CD': 'GDP (current US$)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_GDP_growth(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of GDP growth for a period
        GDP growth - measure of all the gdp annual growth

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents gdp growth for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'NY.GDP.MKTP.KD.ZG': 'GDP growth (annual %)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_GDP_per_capita(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of GDP growth for a period
        GDP per capita - countries gdp divided by its population

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents gdp per capita for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'NY.GDP.PCAP.CD': 'GDP per capita (current US$)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_GDP_current_LCU(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of GDP current LCU for a period
        GDP current LCU - GDP at purchaser's prices is the sum of 
                        gross value added by all resident producers in the 
                        economy plus any product taxes and minus any 
                        subsidies not included in the value of the products. 
                        It is calculated without making deductions for 
                        depreciation of fabricated assets or for depletion 
                        and degradation of natural resources. Data are in 
                        current local currency.

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents gdp current lcu for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'NY.GDP.MKTP.CN': 'GDP (current LCU)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_inflation(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of inflation for a period
        inflation - a general increase in prices and fall in 
                    the purchasing value of money

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents inflation for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'FP.CPI.TOTL.ZG': 'Inflation, GDP deflator (annual %)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_unemployment(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of unemployment data for a period
        unemployment - measures the share of workers in the labor force 
                        who do not currently have a job but are actively 
                        looking for work

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents unemployment for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'SL.UEM.TOTL.ZS': 'Unemployment rate (% of total labor force)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_export(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of export data for a period
        export data - export of goods and services of the period

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents export data for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'NE.EXP.GNFS.CD': 'Exports of goods and services (current US$)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_import(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of import data for a period
        import data - import of goods and services of the period

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents import data for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'NE.IMP.GNFS.CD': 'Imports of goods and services (current US$)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_export_growth(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of export growth rate data for a period
        export growth data - export growth rate annual of goods and services of the period

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents export growth rate data for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'NE.EXP.GNFS.KD.ZG': 'Export growth (annual %)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_import_growth(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of import growth rate data for a period
        import growth data - import growth rate annual of goods and services of the period

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents import growth rate data for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'NE.IMP.GNFS.KD.ZG': 'Import growth (annual %)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_labor_force(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of labor force data for a period
        labor force data - number of labor for the production of goods 
                            and services during a specified period

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents labor force data for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'SL.TLF.TOTL.IN': 'Total labor force (people)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_population(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of population for a period
        population data - number of people for a specified period

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents population data for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'SP.POP.TOTL': 'Total population',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_external_debt(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of external debt for a period
        external debt data - liabilities that are owed to nonresidents by residents

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents external debt data for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'DT.DOD.DECT.CD': 'External debt stocks, total (current US$)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_external_debt_GNI(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of external debt for a period
        external debt gni data - Total external debt stocks to gross national income

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents external debt gni data for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'DT.DOD.DECT.GN.ZS': 'External debt (% of GNI)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_health_expenditure(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of health expenditure data for a period
        health expenditure - the amount spent on health care and related 
                            activities such as private and public health 
                            insurance, health research, and public health activities

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents health expenditure data for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'SH.XPD.CHEX.PC.CD': 'Current health expenditure per capita (current US$)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_education_expenditure(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of education expenditure data for a period
        education expenditure - the current operating expenditures in education, 
                                including wages and salaries and excluding 
                                capital investments in buildings and equipment

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents education expenditure data for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'SE.XPD.TOTL.GB.ZS': 'Government expenditure on education, total (% of government expenditure)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    
    def get_energy_use(self, period = constants.PERIOD):
        """
        Summary:
        A method to get a dataframe of energy use data for a period
        energy use - amount of energy consumed in a period

        Parameters:
        period : str
            a string for period | default : "10Y"

        Return:
        data : pandas dataframe
            returns dataframe which represents energy use data for a period
        """
        pattern = r'\d+'
        number = re.search(pattern, period)
        period_int = int(number.group())
        start = datetime.datetime.now()
        end = datetime.datetime.now() - datetime.timedelta(days=365*period_int)
        data_date = start, end
        indicators = {
            'EG.USE.PCAP.KG.OE': 'Energy use (kg of oil equivalent per capita)',
        }
        country_code = self.country
        data = Wbfetcher.get_data(indicators, country_code, data_date)
        data = pd.DataFrame(data)
        data.rename(columns={'date': 'Date'}, inplace=True)
        data = data.iloc[::-1]
        return data
    

    

    

    



