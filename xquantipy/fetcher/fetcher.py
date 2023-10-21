import pipreqs
import requests
from bs4 import BeautifulSoup
import pandas as pd
from xquantipy.constants.constants import COUNTRY_CODES, MACRO_INDICATORS
import numpy as np

class Fetcher:
    """
    A class to fetch the macroeconomic data

    Methods:
    get_data(indicator, country_code, dates)
        gets the selected macroeconomic data from macrotrends.net
    """

    def get_data(self, indicators, country_code, dates):
        """
        Summary:
        Method to retrive data from macrotrends.net

        Parameters:
        indicstor : list
            a list with the indicator
        country_code : str
            a str which represents the country code
        dates : set
            a set containing the start and end datetime.datetime object

        Return:
        data : pandas dataframe
            returns dataframe which represents macroeconomic data for indicators, period
        """
        assert type(indicators) == list, "Error: Invalid indicators type"
        assert type(country_code) == str, "Error: Invalid country code type"
        assert type(dates) == set, "Error: Invalid dates type"
        dfs = []
        for i in indicators:
            base_url = "http://www.macrotrends.net/countries/"
            base_url = base_url + country_code + "/" + COUNTRY_CODES[country_code] + "/" + MACRO_INDICATORS[i]
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            response = requests.get(base_url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                target_div = soup.find('div', class_='col-xs-6')
                table = target_div.find('table', class_='historical_data_table')
                rows = table.find_all('tr')
                years = []
                datas = []
                for row in rows[2:]:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        year = cells[0].text.strip()
                        data = cells[1].text.strip()
                        years.append(year)
                        datas.append(data)
                data = {'Year': years, str(i): datas}
                df = pd.DataFrame(data)
                df.replace('', np.nan, inplace=True)
                df = df.dropna()
                df['Year'] = df['Year'].astype(int)
                df = df[(df['Year'] >= dates[1].year) & (df['Year'] <= dates[0].year)]
                df[str(i)] = df[str(i)].apply(self._convert_to_numeric)
                dfs.append(df)   
        if len(dfs) == 1:
            return dfs[0]            
        merged_df = dfs[0]
        for i in dfs[1:]:
            merged_df = pd.merge(merged_df, i, on='Year', how='outer')
        return merged_df
    
    def _convert_to_numeric(self, value):
        value = value.replace('$', '').replace('%', '').replace(',', '')
        if 'M' in value:
            return float(value.replace('M', '')) * 1e6
        elif 'B' in value:
            return float(value.replace('B', '')) * 1e9
        else:
            return float(value)