#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import json
import os

class Preprocessing:
    def __init__(self, logger):
        self.logger = logger
        self.logger.info("Initialize preprocessing ...")
        self.config = "../config/config.json"
        
    def read_config(self):
        with open(self.config) as f:
            data = json.load(f)
        fileobj = data['preprocessing']['files']
        self.inputfile = os.path.join(fileobj['root'],
                                      fileobj['input'],
                                      fileobj['filename'])
        self.logger.info("input data file : {}".format(self.inputfile))

    def load_data(self):
        self.df = pd.read_csv(self.inputfile,sep=';')
        
    def dataframe_intial_info(self):
        self.logger.info("Data Frame Initial Details")
        self.logger.info("{0:<20} {1:<10} {2:<10} {3:<10} {4:<10}"
                         .format("Column name", "Total", "Proper", "Missing", "Missing %"))
        for column in self.df.columns:
            total = len(self.df[column])
            proper = self.df[column].notnull().sum()
            missing = self.df[column].isnull().sum()
            missing_percent = missing/total
            self.logger.info("{column:<20} {total:<10} {proper:<10} {missing:<10}\
            {missing_percent:<.02f}".format(column = column, total = total, proper = proper, missing = missing, missing_percent = missing_percent))
        
        
    def start_flow(self):
        self.read_config()
        self.load_data()
        self.dataframe_intial_info()
        