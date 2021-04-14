import os
from pathlib import Path
import pandas as pd

class SeriesGraph:
    CSV_DIR = "tmp/csv"
    HTML_DIR = "tmp/html"
    CSV_EXT = ".csv"
    HTML_EXT = ".html"
    def __init__(self, series, name):
        pd.options.plotting.backend = "plotly"
        Path(self.CSV_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.HTML_DIR).mkdir(parents=True, exist_ok=True)
        self.graph_path = os.path.join(self.CSV_DIR, name + self.CSV_EXT)
        self.html_path = os.path.join(self.HTML_DIR, name + self.HTML_EXT)
        self.series = series

    def local_plot(self, title=None):
        self.series.plot(title=title)

    def export_csv(self):
        self.series.to_csv(self.graph_path, index = True)

    def plot(self):
        self.fig = self.series.plot()

    def export_html(self):
        self.plot()
        self.fig.write_html(self.html_path,
                full_html=False,
                include_plotlyjs='cdn')
        # self.fig.show()

        
