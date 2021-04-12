import pandas as pd
import matplotlib.pyplot as plt
from core import JenkinsGraph
import pandas_datareader.data as web
import datetime

#if you get an error after executing the code, try adding below:
pd.core.common.is_list_like = pd.api.types.is_list_like

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime.now()

SP500 = web.DataReader(['sp500'], 'fred', start, end)
SP500.dropna(inplace = True)
SP500['daily_return'] = (SP500['sp500']/ SP500['sp500'].shift(1)) -1

sp500_graph = JenkinsGraph(SP500['daily_return'], "sp500_daily_return")
# sp500_graph.local_plot("Daily_return")
sp500_graph.export_plot()
print("GOT HERE")

# SP500['daily_return'].to_csv(r'sp500_dail_return.csv', index = False)
#Drop all Not a number values using drop method.
# SP500['daily_return'].plot(title='S&P 500 daily returns')
# plt.show()
