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
        dataframes = []
        for i in indicator:
            base_url = "http://api.worldbank.org/v2/"
            if country_code != None:
                base_url = base_url + "country/" + country_code + "/indicator/"
            base_url = base_url + str(i)
            if len(dates) == 2:
                base_url = base_url + "?date=" + str(dates[1].year) + ":" + str(dates[0].year) + "&format=json"
            else:
                raise Exception("Error: Wrong date format")
            response = requests.get(base_url)
            json_data = response.json()
            data_list = json_data[1]
            column_name = indicator[i]
            date_value_list = [{"date": item["date"], column_name : item["value"]} for item in data_list]
            df = pd.DataFrame(date_value_list)
            dataframes.append(df)
        merged_df = dataframes[0]
        for i in dataframes[1:]:
            merged_df = pd.merge(merged_df, i, on='date', how='outer')
        return merged_df
