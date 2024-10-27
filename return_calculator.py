import pandas as pd
from financial_data import FinancialData
from typing import List

class ReturnCalculator:
    def __init__(self, tickers: List[str], start_date: str = '1960-01-01') -> None:
        self.tickers = tickers
        self.start_date = start_date
        self.financial_data = {ticker: FinancialData(ticker, start_date) for ticker in tickers}
        self.earliest_data_year = None

    def calculate_daily_returns(self, ticker: str):
        data = self.financial_data[ticker].get_data()
        if data is None or data.empty:
            return pd.DataFrame()

        # Return the Adjusted Close (Adj Close) price to plot the index price
        return data[['Adj Close']].dropna()