import pandas as pd
import matplotlib.pyplot as plt
from core import JenkinsGraph
import pandas_datareader.data as web
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

    def dataReader(self, start_date, end_date=None, data_source=None):
        start = start_date
        if end_date == None:
            end_date = datetime.datetime.now()
        if data_source == None:
            data_source = 'fred'

        self.df = web.DataReader([self.name], data_source, start, end_date)
        self.dropna()

    def dailyReturn(self):
        self.df['daily_return'] = (self.df[self.name]/ (self.df[self.name].shift(1)) -1)
        self.dropna()

if __name__ == "__main__":
    stock = SingleStock('sp500')  
    stock.dataReader(start_date=datetime.datetime(2010, 1, 1))
    stock.dailyReturn()
    stock.report()

    stock2 = SingleStock('VIXCLS')  
    stock2.dataReader(start_date=datetime.datetime(2010, 1, 1))
    stock2.dailyReturn()
    stock2.report()

    # plt.show()
# #if you get an error after executing the code, try adding below:
# pd.core.common.is_list_like = pd.api.types.is_list_like

# start = datetime.datetime(2010, 1, 1)
# end = datetime.datetime.now()

# SP500 = web.DataReader(['sp500'], 'fred', start, end)
# SP500.dropna(inplace = True)
# SP500['daily_return'] = (SP500['sp500']/ SP500['sp500'].shift(1)) -1

# sp500_graph = JenkinsGraph(SP500['daily_return'], "sp500_daily_return")
# # sp500_graph.local_plot("Daily_return")
# sp500_graph.export_plot()

# SP500['daily_return'].to_csv(r'sp500_dail_return.csv', index = False)
#Drop all Not a number values using drop method.
# SP500['daily_return'].plot(title='S&P 500 daily returns')
# plt.show()
