import os
import re
import shlex
import sys
import pandas as pd
import numpy as np
from glob2 import glob, iglob
import subprocess as sp
from pathlib import Path
from pdb import set_trace
from collections import defaultdict
import os
import platform
from os.path import dirname as up
import json
import copy

class MetricsGetter(object):

    def __init__(self,path):
        self.path = path #get the repo path
        # Reference current directory, so we can go back after we are done.
        self.cwd = Path(os.getcwd())
        self.json_file_path = self.cwd.joinpath(".temp")
        # Create a folder to hold the json files
        try:
            if not self.json_file_path.is_dir():
                os.makedirs(self.json_file_path)
        except:
            sys.stderr.write(str("There is an error creating dir"))
        json_file = open(self.cwd.joinpath('src','utils','error.json'))
        json_str = json_file.read()
        self.errors = json.loads(json_str)
        self.inverted_errors = dict([[v,k] for k,v in self.errors.items()])
        self.file_dict_org = dict([[k,0] for k,v in self.errors.items()])
        

    @staticmethod
    def _os_cmd(cmd, verbose=False):
        """
        Run a command on the shell

        Parameters
        ----------
        cmd: str
            A command to run.
        """
        cmd = shlex.split(cmd)
        with sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE) as p:
            out, err = p.communicate()
        if verbose: #print to std error which goes to log when running in cloud
            #sys.stderr.write(str("\n"))
            #sys.stderr.write(str(out))
            sys.stderr.write(str("\n"))
            sys.stderr.write(str(err))
            sys.stderr.write(str("\n"))
        return out, err

    def get_metrics(self):
        # Create the path for the json file
        output_folder = self.json_file_path.joinpath("out")
        # Create the complexity report command the data is in json format and stored in to out.json file
        cmd = "plato -r -d {} {}".format(str(output_folder), str(self.path))
        self._os_cmd(cmd)
        # Read into a pandas df
        #df = pd.read_json(json_file)
        file_paths = output_folder.joinpath('files')
        if output_folder.is_dir():
            files = os.listdir(file_paths)
            results = {}
            for name in files:
                file_dict = copy.deepcopy(self.file_dict_org)
                data_file = json.load(open(str(file_paths) + '/' + name + '/report.json'))
                if data_file['info']['file'] not in results.keys():
                    results[data_file['info']['file']] = {}
                for i in range(len(data_file['jshint']['messages'])):
                    if data_file['jshint']['messages'][i]['source'] in self.inverted_errors.keys():
                        file_dict[self.inverted_errors[data_file['jshint']['messages'][i]['source']]] += 1
                results[data_file['info']['file']] = copy.deepcopy(file_dict)
            # Creating result in r2c format
            result = {}
            result["check_id"] = 'complexity'
            result["path"] = 'javaScript'
            result["extra"] = results
            final_result = {"results": [result]}
            result_json = json.dumps(final_result) 
            #printing to get the data into the shell script
            print(result_json)
        else:
            # Creating result in r2c format
            result = {}
            result["check_id"] = 'complexity'
            result["path"] = 'javaScript'
            result["extra"] = {}
            final_result = {"results": [result]}
            result_json = json.dumps(final_result) 
            #printing to get the data into the shell script
            print(result_json)


        return result_json


if __name__ == "__main__":
    metrics = MetricsGetter(sys.argv[1])
    metrics.get_metrics()






