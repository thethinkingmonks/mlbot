#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import scipy.stats as stats
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import LabelEncoder

class botpreprocess:
    def __init__(self, bot):
        self.logger = bot["logger"]
        self.config = bot["config"]
        self.dataloader = bot["dataloader"]
        self.logger.info("botpreprocess - init ...")
        self.percentage = 0.05
        
    def load_data(self):        
        self.df = self.dataloader.get_dataframe()
        
    def print_series(self,data):
        for x in data:
            print(x)
        
    def dataframe_intial_info(self):
        data = self.df       
        buffer = io.StringIO()
        data.describe(buf=buffer, verbose=True)
        s = buffer.getvalue()
        self.logger.info("Data Frame describe : \n{}".format(s))
        
        # get the info into buffer
        buffer = io.StringIO()
        data.info(buf=buffer, verbose=True)
        s = buffer.getvalue()
        self.logger.info("Data Frame info : \n{}".format(s))
        
        self.logger.info("Data Frame Initial Details")
        self.logger.info("{0:<20} {1:<10} {2:<10} {3:<10} {4:<10}"
                         .format("Column name", "Total", "Proper", "Missing", "Missing %"))
        for column in data.columns:
            total = len(data[column])
            proper = data[column].notnull().sum()
            missing = data[column].isnull().sum()
            missing_percent = missing/total
            self.logger.info("{column:<20} {total:<10} {proper:<10} {missing:<10}\
            {missing_percent:<.02f}".format(column = column, total = total, proper = proper, missing = missing, missing_percent = missing_percent))
    
    def encode_label(self):
        data = self.df
        for column in data.select_dtypes(include=[np.object]).columns:
            le = LabelEncoder()
            le.fit(data[column])
            data[column] = le.transform(data[column])
        
    def fill_categorical_data(self):
        data = self.df
        for column in data.select_dtypes(include=[np.object]).columns:
            total_length = data[column].size
            # get the 5 percent value
            total_length = round(self.percentage * total_length)
            unique_length = data[column].unique().size
            
            #get the unique elements to determine whether the column is categorical 
            if unique_length < total_length:                
                freq_value = data[column].value_counts().idxmax()
                data[column] = data[column].replace(np.nan,freq_value)
    
    def fill_numeric_data(self):
        data = self.df
        for column in data.select_dtypes(include=[np.number]).columns:
            total_length = data[column].size
            # get the 5 percent value
            total_length = round(self.percentage * total_length)
            unique_length = data[column].unique().size        

            #get the unique elements to determine whether the column is categorical 
            if unique_length > total_length:
                imputer = Imputer(missing_values = np.nan, strategy = 'mean')
            else:
                imputer = Imputer(missing_values = np.nan, strategy = 'most_frequent')
            imputer = imputer.fit(data[[column]])
            
    def fill_non_numeric_data(self):
        data = self.df
        for column in data.select_dtypes(include=[np.object]).columns:
            total_length = data[column].size
            # get the 5 percent value
            total_length = round(self.percentage * total_length)
            unique_length = data[column].unique().size
            
            #get the unique elements to determine whether the column is categorical 
            if unique_length < total_length:
                imputer = Imputer(missing_values = np.nan, strategy = 'mean')
                imputer = imputer.fit(data[[column]])
            
    def check_normal_distribution(self, data):
        threshold = 0.001
        statistics, p = stats.normaltest(data)
        if p < threshold:
            print("distribution is not normal")
        else:
            print("distribution is normal")
    
    def encode_categorical_data(self):        
        self.encode_label()
        self.fill_non_numeric_data()
         
        
        
    def start_flow(self):
        self.load_data()
        self.dataframe_intial_info()
        #self.fill_categorical_data()      
        #self.fill_numeric_data()
        #self.encode_categorical_data()
        
        
