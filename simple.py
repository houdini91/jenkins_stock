import pandas as pd
import matplotlib.pyplot as plt
from core import JenkinsGraph
import pandas_datareader.data as web
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
import datetime


class SingleStock:
    def __init__(self, name):
        self.name = name

    def report(self):
        self.df_graph = JenkinsGraph(self.df['daily_return'], self.name + "_daily_return")
        self.df_graph.export_csv()
        # self.df_graph.local_plot("Daily_return")
        self.df_graph.export_html()

    def dropna(self):
        self.df.dropna(inplace = True)

    def dataReader(self, start, end=None, data_source=None):
        if end == None:
            end = datetime.datetime.now()
        if data_source == None:
            data_source = 'fred'

        self.df = web.DataReader([self.name], data_source='fred', start=start, end=end)
        self.dropna()

    def dailyReturn(self):
        self.df['daily_return'] = (self.df[self.name]/ (self.df[self.name].shift(1)) -1)
        self.dropna()


#St. Louis FED
FED_tickers = ['sp500', 'VIXCLS']
# Nasdaq Trader symbol
NASDAQ_tickers = ['BA', 'IBM']

if __name__ == "__main__":

    for ticker in NASDAQ_tickers:
        f = web.DataReader(ticker, 'stooq')
        graph = JenkinsGraph(f.Close, ticker + "_close")
        graph.export_html()

    for ticker in FED_tickers:
        single = SingleStock(ticker)  
        single.dataReader(start=datetime.datetime(2010, 1, 1))
        single.dailyReturn()
        single.report()