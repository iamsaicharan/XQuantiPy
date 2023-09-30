import requests
import pandas as pd

class Wbfetcher:
    """
    A class to fetch the macroeconomic data

    Methods:
    get_data(indicator, country_code, dates)
        gets the selected macroeconomic data from world bank api
    """
    def get_data(indicator, country_code, dates):
        """
        Summary:
        Method to retrive data from world bank api

        Parameters:
        indicstor : dict
            a dictionary with the indicator and its corresponding column name
        country_code : str
            a str which represents the country code
        dates : set
            a set containing the start and end date

        Return:
        data : pandas dataframe
            returns dataframe which represents macroeconomic data for a indicator, period
        """
        base_url = "http://api.worldbank.org/v2/"
        if country_code != None:
            base_url = base_url + "country/" + country_code + "/indicator/"
        if indicator != {}:
            # Need to implement multiple indicator fetching
            if len(indicator) == 1:
                base_url = base_url + str(list(indicator.keys())[0])
            else:
                raise Exception("Error: Multiple indicators are not allowed")
        # Need to implement quaterly and montly data fetching
        if len(dates) == 2:
            base_url = base_url + "?date=" + str(dates[1].year) + ":" + str(dates[0].year) + "&format=json"
        else:
            raise Exception("Error: Wrong date format")
        all_indicators = {
            'NY.GDP.MKTP.CD': 'Gross Domestic Product (current US$)',
            'NY.GDP.MKTP.KD.ZG': 'GDP growth (annual %)',
            'NY.GDP.PCAP.CD': 'GDP per capita (current US$)',
            'NY.GDP.MKTP.CN': 'GDP (current LCU)',
            'FP.CPI.TOTL.ZG': 'Inflation, GDP deflator (annual %)',
            'SL.UEM.TOTL.ZS': 'Unemployment rate (% of total labor force)',
            'NE.EXP.GNFS.CD': 'Exports of goods and services (current US$)',
            'NE.IMP.GNFS.CD': 'Imports of goods and services (current US$)',
            'NE.EXP.GNFS.KD.ZG': 'Export growth (annual %)',
            'NE.IMP.GNFS.KD.ZG': 'Import growth (annual %)',
            'SL.TLF.TOTL.IN': 'Total labor force (people)',
            'SP.POP.TOTL': 'Total population',
            'DT.DOD.DECT.CD': 'External debt stocks, total (current US$)',
            'DT.DOD.DECT.GN.ZS': 'External debt (% of GNI)',
            'SH.XPD.CHEX.PC.CD': 'Current health expenditure per capita (current US$)',
            'SE.XPD.TOTL.GB.ZS': 'Government expenditure on education, total (% of government expenditure)',
            'EG.USE.PCAP.KG.OE': 'Energy use (kg of oil equivalent per capita)',
        }
        response = requests.get(base_url)
        json_data = response.json()
        data_list = json_data[1]
        column_name = indicator[str(list(indicator.keys())[0])]
        date_value_list = [{"date": item["date"], column_name : item["value"]} for item in data_list]
        df = pd.DataFrame(date_value_list)
        return df
        
    

    

    

    



