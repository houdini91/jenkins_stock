import os
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from pandas_profiling import ProfileReport
import sweetviz as sv
import glob

class TranPlot:
    PLOT_DIR = "tmp/reports/plots/html"
    PLOT_EXT = ".html"
    def __init__(self, name, out_dir=PLOT_DIR):
        self.out_dir = out_dir
        pd.options.plotting.backend = "plotly" 
        Path(self.out_dir).mkdir(parents=True, exist_ok=True)
        # self.html_path = os.path.join(self.out_dir, name + self.PLOT_EXT)
        self.name = name

    def get_plot_path(self, plot_name):
        return os.path.join(self.out_dir, plot_name + self.PLOT_EXT)

    def plot_series(self, plot_name, series):
        fig = series.plot.bar()
        html_path = self.get_plot_path(plot_name)
        self.plot(html_path, fig)

    def plot(self, html_path, fig):
        fig.write_html(html_path,
                    full_html=False,
                    include_plotlyjs='cdn')
    
    def plot_dict(self, plot_dict):
        for plot_name, plot in plot_dict.items():
            html_path = self.get_plot_path(plot_name)
            try:
                os.remove(html_path)
            except OSError:
                pass

        for plot_name, plot_list in plot_dict.items():
            html_path = self.get_plot_path(plot_name)
            # print("### plot_name",plot_name, plot,html_path)

            for plot in plot_list:
                with open(html_path, 'a') as f:
                    print("Generating plot html report, ", html_path)
                    f.write(plot.to_html(full_html=False, include_plotlyjs='cdn'))

class TranCSV:
    CSV_DIR = "tmp/reports/csv/html"
    CSV_EXT = ".html"
    def __init__(self, name, out_dir=CSV_DIR):
        self.out_dir = out_dir
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        self.html_path = os.path.join(out_dir, name + self.CSV_EXT)
        self.name = name

    def series(self, series):
        fig = series.to_html(self.html_path)

    def series_dict(self, series_dict):
        for series_name, series in series_dict.items():
            if not series.empty:
                html_path = os.path.join(self.out_dir, series_name + self.CSV_EXT)
                try:
                    os.remove(html_path)
                except OSError:
                    pass

                print("Generating csv html report, ", html_path)
                fig = series.to_html(html_path)

class TranProfiler:
    PROFILE_DIR="tmp/reports/profile/html"
    PROFILE_EXT = ".html"
    def __init__(self, name, out_dir=PROFILE_DIR):
        self.out_dir = out_dir
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        self.name = name
        self.html_path = os.path.join(out_dir, name + self.PROFILE_EXT)

    def series(self, series, profiler_type="pandas"):
        pd.options.plotting.backend = "matplotlib"
        if profiler_type == "pandas":
            self.pandas_profiler(series, name, html_path)
        pd.options.plotting.backend = "plotly" 

    def series_dict(self, series_dict, profiler_type="pandas", **kwargs):
        pd.options.plotting.backend = "matplotlib"
        for series_name, series in series_dict.items():
            if not series.empty:
                name = self.name + "_" + series_name 
                html_path = os.path.join(self.out_dir, name + self.PROFILE_EXT)
                try:
                    os.remove(html_path)
                except OSError:
                    pass

                if profiler_type == "sweetviz":
                    self.sweetviz_profiler(series, html_path, **kwargs)
                else:
                    self.pandas_profiler(series, name, html_path, **kwargs)

        pd.options.plotting.backend = "plotly" 

    def pandas_profiler(self, series, name, html_path, **kwargs):
            print("ARGS", kwargs)
            profile = ProfileReport(series, title= name + ":Profiler", progress_bar=True)
            profile.to_file(html_path)

    def sweetviz_profiler(self, series, html_path, **kwargs):
        print("ARGS", kwargs)
        profile = sv.analyze(series, *kwargs)
        profile.show_html(filepath=html_path, open_browser=False)
    
class OutputObjects:
    def __init__(self, name, output_dir, trans_plot, trans_csv, trans_profiler):
        self.name = name
        self.output_dir=output_dir
        self.trans_plot=trans_plot
        self.trans_csv=trans_csv
        self.trans_profiler=trans_profiler

    def get_name(self):
        return self.name

    def get_output_dir(self):
        return self.output_dir

    def plot_reporter(self):
        return self.trans_plot

    def csv_reporter(self):
        return self.trans_csv

    def profile_reporter(self):
        return self.trans_profiler

class Output():
    PROFILE_DIR = "reports/profile/html"
    CSV_DIR = "reports/csv/html"
    PLOT_DIR = "reports/plot/html"
    BASE_DIR = "tmp"
    OUT_DIR = "out"

    def __init__(self, base_dir=BASE_DIR,out_dir=OUT_DIR, plot_dir=PLOT_DIR, profile_dir=PROFILE_DIR, csv_dir=CSV_DIR):
        self.base_dir = base_dir
        self.out_dir = out_dir
        self.profile_dir = profile_dir
        self.csv_dir = csv_dir
        self.plot_dir = plot_dir

    def get_base_dir(self, name):
        directory = os.path.join(self.base_dir, name)
        Path(directory).mkdir(parents=True, exist_ok=True)
        return directory

    def get_output_dir(self, name):
        out_dir = os.path.join(self.get_base_dir(name), self.out_dir)
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        return out_dir

    def plot_reporter(self, name):
        plot_dir = os.path.join(self.get_base_dir(name), self.plot_dir)
        Path(plot_dir).mkdir(parents=True, exist_ok=True)
        return TranPlot(name, out_dir=plot_dir)

    def csv_reporter(self, name):
        csv_dir = os.path.join(self.get_base_dir(name), self.csv_dir)
        Path(csv_dir).mkdir(parents=True, exist_ok=True)
        return TranCSV(name, out_dir=csv_dir)

    def profile_reporter(self, name):
        profile_dir = os.path.join(self.get_base_dir(name), self.profile_dir)
        Path(profile_dir).mkdir(parents=True, exist_ok=True)
        return TranProfiler(name, out_dir=profile_dir)

    def get_outputter(self, name):
        out_dir = self.get_output_dir(name)
        trans_plot = self.plot_reporter(name)
        trans_csv = self.csv_reporter(name)
        trans_profiler = self.profile_reporter(name)
        return OutputObjects(name, out_dir, trans_plot, trans_csv, trans_profiler)
        
    def get_file_list(self, name):
        prev_stage_output_dir = self.get_output_dir(name)
        file_list = glob.glob(os.path.join(prev_stage_output_dir, "*"))
        return file_list
