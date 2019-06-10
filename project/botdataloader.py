#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

class botdataloader:
    def __init__(self, bot):
        self.logger = bot["logger"]
        self.config = bot["config"]
        self.logger.info("Initialize Data Loader ...")
 
    def load_data(self):
        config = self.config.config
        self.df = pd.read_csv(config["input_file"],sep=config['separator'])        
    
    def get_dataframe(self):
        return self.df
    
    def start_flow(self):        
        self.load_data()        
