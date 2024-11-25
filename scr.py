import pandas as pd
import requests
import matplotlib.pyplot as plt

class SCR:
    def __init__(self, symbol):
        self.symbol = symbol

    def fetch_by_company(self):
        baseurl = "https://www.alphavantage.co/query"
        function = "TIME_SERIES_MONTHLY"
        url = f"{baseurl}?function={function}&symbol={self.symbol}&apikey=demo"
        r = requests.get(url)
        data = r.json()
        time_series_key = "Monthly Time Series" # extract time series data
        if time_series_key not in data:
            raise ValueError("Time series data not found in the API response")
        monthly_data = data[time_series_key] # convert time series data to DataFrame
        df = pd.DataFrame.from_dict(monthly_data, orient="index", dtype=float)
        columns = {
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        }
        df = df.rename(columns=columns) # rename columns
        df.index = pd.to_datetime(df.index) #convert index to datetime and sort by date
        df = df.sort_index()
        return df

    def identify_trends(self, window=30):
        data = self.fetch_by_company() # process the stock data
        data[f"MA{window}"] = data["Close"].rolling(window=window).mean() # calculate the moving average and add it as a new column

        data["Daily Return"] = data["Close"].pct_change() # identify trends or daily return

        plt.figure(figsize=(10,6))
        plt.plot(data.index, data["Close"], label="Close Price")
        plt.plot(data.index, data["MA30"], label="A 30-Day Moving Average")
        plt.title(f"{self.symbol}'s Stock Prices")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid()
        plt.show()



symbol = "IBM"
obj = SCR(symbol)
obj.identify_trends()
