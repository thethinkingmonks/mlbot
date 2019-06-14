# -*- coding: utf-8 -*-
import os
import json

class botconfig():
    def __init__(self, bot):
        self.logger = bot["logger"]
        self.logger.debug("botconfig - init ...")
        self.configfile = "../config/config.json"
        # configuration parameters
        self.config = {}
        self.config["input_dir"] = ""
        self.config["output_dir"] = ""
        self.config["input_file"] = ""
        self.config["output_file"] = ""
        self.config["data_file"] = ""
        self.config["separator"] = ""
        
        
    def read_config(self):
        self.logger.debug("botconfig - read_config ...")
        with open(self.configfile) as f:
            data = json.load(f)
        parameter = data['config']['files']
        root = parameter['root']
        self.config['input_dir'] = os.path.join(root, parameter['input_folder'])
        self.config['output_dir'] = os.path.join(root, parameter['output_folder'])
        self.config["input_file"] = os.path.join(self.config['input_dir'],
                                      parameter['input_file'])
        self.config["output_file"] = os.path.join(self.config['output_dir'],
                                      parameter['output_file'])
        self.config["params_file"] = os.path.join(self.config['output_dir'],
                                      parameter['params_file'])
        self.config["data_file"] = os.path.join(self.config['output_dir'],
                                      parameter['data_file'])
        
        self.config['separator'] = parameter['separator']        
        self.logger.debug("input folder : {}".format(self.config['input_dir']))
        self.logger.debug("output folder : {}".format(self.config['output_dir']))
        self.logger.debug("input file name : {}".format(self.config["input_file"]))
        self.logger.debug("input file name : {}".format(self.config["output_file"]))
        
    def create_files(self):
        self.logger.debug("botconfig - create_files ...")
        config = self.config
        
        # create the output dir
        if not os.path.exists(self.config['output_dir']):
            os.makedirs(self.config['output_dir'])
        
        # reset parameter file
        with open(config['params_file'], 'w') as parameters_file:
            print("parameter file is created : {}".format(self.config['params_file']))
        
        # reset data file
        with open(config['data_file'], 'w') as parameters_file:
            print("data file is created : {}".format(self.config['data_file']))
        
        
    def start_flow(self):
        self.logger.debug("botconfig - start_flow ...")
        self.read_config()
        self.create_files()
        