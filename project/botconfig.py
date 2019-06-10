# -*- coding: utf-8 -*-
import os
import json

class botconfig():
    def __init__(self, bot):
        self.logger = bot["logger"]
        self.logger.info("Initialize MLPlot ...")
        self.configfile = "../config/config.json"
        # configuration parameters
        self.config = {}
        self.config["input_file"] = ""
        self.config["output_file"] = ""        
        self.config["separator"] = ""        
        
    def read_config(self):
        with open(self.configfile) as f:
            data = json.load(f)
        parameter = data['config']['files']
        self.config["input_file"] = os.path.join(parameter['root'],
                                      parameter['input_folder'],
                                      parameter['input_file'])
        self.config["output_file"] = os.path.join(parameter['root'],
                                      parameter['output_folder'],
                                      parameter['output_file'])
        
        self.config['separator'] = parameter['separator']
        self.logger.info("input file name : {}".format(self.config["input_file"]))
        self.logger.info("input data file : {}".format(self.config["input_file"]))
        
    def start_flow(self):
        self.read_config()   
        
