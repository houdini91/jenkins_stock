import os
from pathlib import Path

class JenkinsGraph:
    BASE_DIR = "tmp/graph"
    EXT = ".csv"
    def __init__(self, series, name):
        Path(self.BASE_DIR).mkdir(parents=True, exist_ok=True)
        graph_path = os.path.join(self.BASE_DIR, name + self.EXT)
        self.graph_path = graph_path
        self.series = series

    def local_plot(self, title=None):
        self.series.plot(title=title)

    def export_plot(self):
        self.series.to_csv(self.graph_path, index = True)


        
