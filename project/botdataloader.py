#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

class botdataloader:
    def __init__(self, bot):
        self.logger = bot["logger"]
        self.config = bot["config"]
        self.logger.info("botdataloader - init ...")
 
    def load_data(self):
        self.logger.info("botdataloader - load_data ...")
        config = self.config.config
        self.df = pd.read_csv(config["input_file"],sep=config['separator'])
    
    def get_dataframe(self):
        self.logger.info("botdataloader - get_dataframe ...")
        return self.df
    
    def start_flow(self):
        self.logger.info("botdataloader - start_flow ...")
        self.load_data()        
