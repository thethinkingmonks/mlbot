#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class botpreprocess:
    def __init__(self, bot):
        self.logger = bot["logger"]
        self.config = bot["config"]
        self.dataloader = bot["dataloader"]
        self.logger.info("Initialize preprocessing ...")
        
    def load_data(self):        
        self.df = self.dataloader.get_dataframe()        
        
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
        self.load_data()
        self.dataframe_intial_info()
        
