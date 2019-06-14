#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import pickle
import os 

class botdataloader:
    def __init__(self, bot):
        self.logger = bot["logger"]
        self.config = bot["config"]
        self.logger.debug("botdataloader - init ...")
        self.data = {}
        self.data['parameters_count'] = 0
        self.data['categorical'] = []
        self.data['columns'] = []
        self.save_data(self.config.config['data_file'], self.data)
 
    def load_dataframe(self):
        self.logger.debug("botdataloader - load_data ...")
        config = self.config.config
        self.df = pd.read_csv(config["input_file"],sep=config['separator'], nrows=25000)
        
    def load_data(self, filename):
        self.logger.debug("botdataloader - load_data ...")
        data = {}
        if os.path.getsize(filename) > 0:
            with open(filename, 'rb') as parameters_file:
                self.logger.debug("reading from pickle file : {}".format(filename))
                data = pickle.load(parameters_file)
        return data
        
    def save_data(self, filename, data):
        self.logger.debug("botdataloader - write_pickle_file ...")
        with open(filename, 'wb') as data_file:
            self.logger.debug("write to pickle file : {}".format(filename))
            pickle.dump(data, data_file)
            
    def write_pickle_file(self, filename, data, mode='wb'):
        self.logger.debug("botdataloader - write_pickle_file ...")
        with open(filename, mode) as data_file:
            self.logger.debug("write to pickle file : {}".format(filename))
            pickle.dump(data, data_file)        
    
    def get_dataframe(self):
        self.logger.debug("botdataloader - get_dataframe ...")
        return self.df
    
    def start_flow(self):
        self.logger.debug("botdataloader - start_flow ...")        
        self.load_data(self.config.config['data_file'])
        self.load_dataframe()
        self.save_data(self.config.config['data_file'], self.data)