from ..src import pipeline, output

import os
import sys
import json
import argparse
import pandas as pd

class ExampleCollector():

    def __init__(self, token=None):
        print("Collector: using, TOKEN:", token)
        self.token = token

    def get_dataframe(self):
        cars = {'Brand': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
            'Price': [22000,25000,27000,35000]
        }
        df = pd.DataFrame(cars, columns = ['Brand', 'Price'])
        df.set_index('Brand')

        self.df = df

        return self.df

    def to_csv(self, base_dir, output_name):
        csv_path = os.path.join(base_dir, output_name + ".csv")
        self.df.to_csv(csv_path)

    def get_plots(self):
        bar_fig = self.df.plot.bar(x="Brand", y="Price", title="My collector bar plot")
        line_fig = self.df.plot(x="Brand", y="Price", title="My collector plot title")
        return bar_fig, line_fig

class ExampleFilter():

    def __init__(self, filter_dict):
        print("Filter: using dictionary", filter_dict)
        self.filter_dict = filter_dict

    def filter(self, df):
        filtered_df = df[(df['Price'] > self.filter_dict["min_price"]) & (df['Price'] < self.filter_dict["max_price"])]
        self.df = filtered_df
        print("Filter: dataframe ", self.df)

    def read_csv(self, path):
        df = pd.read_csv(path)
        self.filter(df)

    def get_plots(self):
        bar_fig = self.df.plot.bar(x="Brand", y="Price", title="My filter bar plot")
        return bar_fig


class PenisPipeline():
    INSTALLER_STAGE="installer"
    COLLECTOR_STAGE="collector"
    FILTER_STAGE="filter"
    GENERATE_CMD="generate"
    DEFAULT_FILTER_DICT = {"min_price": 0, "max_price": 100000}
    DEFAULT_SYMBOLS = '{\"symbols\"=[]}'

    FILTER_DICT_VAR = 'FILTER_DICT'
    FINHUB_TOKEN_VAR = 'FINHUB_TOKEN'
    FINHUB_TOKEN_ID_VAR = 'FINHUB_TOKEN_ID'
    SYMBOLS_VAR = 'SYMBOLS_LIST'

    def __init__(self):
        # Init argparse
        self.parser = argparse.ArgumentParser()
        self.subparsers = self.parser.add_subparsers(dest='stage')
        self.subparsers.required = True

        # Set up default transgender template generator
        self.template_pipeline = pipeline.BasePipeline()
        # Set up default transgender output manager
        self.output_pipeline = output.Output(base_dir="tmp/simple/")
        
        # Add stages to pipeline
        self.add_install_depends_stage()
        self.add_collector_stage()
        self.add_filter_stage()
        self.add_generate()

        # Parse and run pipline command
        args = self.parser.parse_args()
        if args.func is not None:
            args.func(args)

    def add_install_depends_stage(self):
        # Trans-Jenkins pipeline template - only for testing, use the docker or python whl package to install trans-jenkins dependices.
        self.template_pipeline.add_stage(self.INSTALLER_STAGE, self.COLLECTOR_STAGE, is_initial=True)
        # self.template_pipeline.add_sh_step(self.INSTALLER_STAGE, "pip3 install -r requirements.txt" , label="install_depends")
        self.template_pipeline.add_sh_step(self.INSTALLER_STAGE, "python3 py_trans_jenkins/setup.py install" , label="install_depends")



    def add_collector_stage(self):
        # Collector argparse arguments
        stage_parser = self.subparsers.add_parser(self.COLLECTOR_STAGE)
        stage_parser.add_argument('--file', type=str, help="path to json symbol file")
        stage_parser.add_argument('--token', type=str,  metavar=self.FINHUB_TOKEN_VAR, help='finhub token')
        stage_parser.set_defaults(func=self.collector)

        # Trans-Jenkins pipeline template
        self.template_pipeline.add_stage(self.COLLECTOR_STAGE, self.FILTER_STAGE, is_initial=False)
        self.template_pipeline.add_cred(self.COLLECTOR_STAGE,'string', self.FINHUB_TOKEN_ID_VAR,self.FINHUB_TOKEN_VAR)
        self.template_pipeline.add_text_param(pipeline.GLOBAL, self.SYMBOLS_VAR, self.DEFAULT_SYMBOLS)
        # self.template_pipeline.add_sh_step(self.COLLECTOR_STAGE, "python3 collector ${} $SYMBOL_LIST" , label="run_collector".format(self.FINHUB_TOKEN))
        self.template_pipeline.add_sh_step(self.COLLECTOR_STAGE, "echo Running Collector WITH ${};printenv".format(self.FINHUB_TOKEN_VAR) , label="run_collector")

    def add_filter_stage(self):
        # Filter argparse arguments
        stage_parser = self.subparsers.add_parser(self.FILTER_STAGE)
        stage_parser.add_argument('--filter_dict', type=str, help="json string with filter arguments")
        stage_parser.set_defaults(func=self.filter)

        # Trans-Jenkins pipeline template
        self.template_pipeline.add_stage(self.FILTER_STAGE, None)
        self.template_pipeline.add_string_param(pipeline.GLOBAL, self.FILTER_DICT_VAR, json.dumps(self.DEFAULT_FILTER_DICT))

        # self.template_pipeline.add_sh_step(self.FILTER_STAGE, "python3 filter" , label="run_filter")
        self.template_pipeline.add_sh_step(self.FILTER_STAGE, "echo RUNNING FILTER STAGE;printenv" , label="run_filter")

    def add_generate(self):
        # Generate argparse arguments
        generate_cmd = self.subparsers.add_parser(self.GENERATE_CMD)
        generate_cmd.set_defaults(func=self.generate_jenkinsfile)

    def collector(self, args):
        # Get stage output manager
        name = "collector"
        stage_outputter = self.output_pipeline.get_outputter(name)
        
        # Run stage business logic - collect data with token.
        # output: data as csv.
        # report: csv, plot and profiler.
        collector = ExampleCollector(token=args.token)
        df = collector.get_dataframe()
        bar_plot, line_plot = collector.get_plots()

        # Write stage output to csv.
        collector.to_csv(stage_outputter.get_output_dir(), "my_collector_csv_output")

        # Write stage csv, plots and profile reports
        stage_outputter.csv_reporter().series_dict({"csv_report": df})
        stage_outputter.plot_reporter().plot_dict({"plot_bundle_report":[bar_plot,line_plot], "plot_report":[line_plot]})
        stage_outputter.profile_reporter().series_dict({"profiler_report_sweetviz": df}, profiler_type="sweetviz")
        stage_outputter.profile_reporter().series_dict({"profiler_report_pandas": df})

    def filter(self, args):
        # Get stage output manager
        name = "filter"
        stage_outputter = self.output_pipeline.get_outputter(name)
    
        # Get param/argument filter dictinary
        filter_dict = self.filter_dictionary_parse(args.filter_dict)
        print("Filter: Using, dictionary: ", filter_dict)

        # Get collector output files
        files_list = self.output_pipeline.get_file_list("collector")
        print("Filter: Using collector output, files: ", files_list)

        # Run stage business logic - filter collector output.
        # output: None
        # report: plot
        filter = ExampleFilter(filter_dict)
        for file in files_list:
            filter.read_csv(file)
            bar_plot = filter.get_plots()

            # Write stage plots reports
            stage_outputter.plot_reporter().plot_dict({"my_filter_plot_bar_report": [bar_plot]})

    def generate_jenkinsfile(self, args):
        self.template_pipeline.generate_jenkinsfile()
        
    def filter_dictionary_parse(self, args_filter_dict):
        filter_dict = self.DEFAULT_FILTER_DICT
        if args_filter_dict != None:
            try:
                filter_dict = json.loads(args_filter_dict)
            except Exception as e:
                print(e)
                pass 

        return filter_dict
        
  
def run():
    penis_pipeline = PenisPipeline()


if __name__ == "__main__":
    run()