import requests
from bs4 import BeautifulSoup
import pandas as pd
from xquantipy.constants import COUNTRY_CODES, MACRO_INDICATORS
import numpy as np
import cloudscraper

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
        assert type(dates) == tuple, "Error: Invalid dates type"
        dfs = []
        for i in indicators:
            base_url = "http://www.macrotrends.net/countries/"
            base_url = base_url + country_code + "/" + COUNTRY_CODES[country_code] + "/" + MACRO_INDICATORS[i]
            scraper = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0',}) 
            response = scraper.get(base_url)
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
    
    def get_ticker_news(self, ticker):
        """
        Summary:
        Method to retrive data from news from bing.com

        Parameters:
        ticker : str
            a str which represents the ticker code

        Return:
        news : list
            returns a list which represents news data for ticker
        """
        stock = ticker.split('.', 1)[0]
        base_url = f"https://www.bing.com/news/search?q={stock}&qft=sortbydate"
        scraper = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0', 'enable_selenium': True}) 
        response = scraper.get(base_url,)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_div = soup.find(attrs={'id':'algocore'})
        news_cards = news_div.find_all('div', class_='news-card newsitem cardcommon')
        news = []
        for card in news_cards:
            author = card['data-author']
            title = card.find('a', class_='title').text
            description = card.find('div', class_='snippet').text
            url = card['data-url']
            timestamp = card.find('span', {'aria-label': True}).text
            current = {
                "Author": author,
                "Title": title,
                "URL": url,
                "Description": description,
                "Timestamp": timestamp 
            }
            news.append(current)
        return news
    
    def _convert_to_numeric(self, value):
        """
        Summary:
        Method to convert the Currency to Numeric values

        Parameters:
        value : str
            a str which represents the currrency

        Return:
        float value : float
            returns a float value of the converted currency
        """
        value = value.replace('$', '').replace('%', '').replace(',', '')
        if 'M' in value:
            return float(value.replace('M', '')) * 1e6
        elif 'B' in value:
            return float(value.replace('B', '')) * 1e9
        else:
            return float(value)