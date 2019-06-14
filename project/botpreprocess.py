#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import scipy.stats as stats
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import LabelEncoder
from banner import banner
class botpreprocess:
    def __init__(self, bot):
        self.logger = bot["logger"]
        self.config = bot["config"]
        self.dataloader = bot["dataloader"]
        self.logger.debug("botpreprocess - init ...")
        self.percentage = 0.05
        self.unique_max = 25
        self.step = 3
        
    def load_dataframe(self):
        self.logger.debug("botpreprocess - load_dataframe ...")
        self.df = self.dataloader.get_dataframe()
        
    def load_data(self):
        self.logger.debug("botpreprocess - load_data ...")
        self.data = self.dataloader.load_data(self.config.config['data_file'])        
        
    def save_data(self):
        self.logger.debug("botunivariant - save_data ...")
        self.dataloader.save_data(self.config.config['data_file'], self.data)
        
    def convert_column_lowercase(self):
        self.df.columns = map(str.lower, self.df.columns)
        
        
    def get_categorical_column(self):
        df = self.df
        categorical = []
        for column in df.columns:
            if "date" in column.lower() :
                continue
            unique_length = df[column].unique().size
            if unique_length <= self.unique_max:
                categorical.append(column)
                df[column] = df[column].astype("category")
        self.logger.debug("categorical columns : {}".format(categorical))
        self.data['categorical'] = categorical
        self.data['columns'].extend(categorical)
               
    def dataframe_intial_info(self):        
        df = self.df        
        
        # get the info into buffer
        buffer = io.StringIO()
        df.info(buf=buffer, verbose=True)
        s = buffer.getvalue()
        text = banner("Data Frame info")
        self.logger.info("{}\n{}".format(text, s))
        text = banner("Data Frame Details")
        self.logger.info(text)
        self.logger.info("{0:<50} {1:<10} {2:<10} {3:<10} {4:<10}"
                         .format("Column name", "Total", "Proper", "Missing", "Missing %"))
        for column in df.columns:
            total = len(df[column])
            proper = df[column].notnull().sum()
            missing = df[column].isnull().sum()
            missing_percent = missing/total * 100
            self.logger.info("{column:<50} {total:<10} {proper:<10} {missing:<10}\
            {missing_percent:<.02f}".format(column = column, total = total, proper = proper, missing = missing, missing_percent = missing_percent))
    
    def encode_label(self):
        df = self.df
        for column in self.data['categorical']:
            le = LabelEncoder()
            le.fit(df[column])
            df[column + "category"] = le.transform(df[column])
            df[column + "category"] = df[column + "category"].astype("category")
        
    def fill_categorical_data(self):
        df = self.df
        for column in self.data['categorical']:
            total_length = df[column].size
            # get the 5 percent value
            total_length = round(self.percentage * total_length)
            unique_length = df[column].unique().size
            
            #get the unique elements to determine whether the column is categorical 
            if unique_length < total_length or unique_length <= self.unique_max:                
                freq_value = df[column].value_counts().idxmax()
                df[column] = df[column].replace(np.nan,freq_value)
    
    def fill_numeric_data(self):
        df = self.df
        for column in df.select_dtypes(include=[np.number]).columns:
            total_length = df[column].size
            # get the 5 percent value
            total_length = round(self.percentage * total_length)
            unique_length = df[column].unique().size        

            #get the unique elements to determine whether the column is categorical 
            if unique_length > total_length or unique_length <= self.unique_max:
                imputer = Imputer(missing_values = np.nan, strategy = 'mean')
            else:
                imputer = Imputer(missing_values = np.nan, strategy = 'most_frequent')
            imputer = imputer.fit(df[[column]])
        self.data['columns'].extend(df.select_dtypes(include=[np.number]).columns)
        print("valid columns : {}".format(self.data['columns']))
            
    def fill_non_numeric_data(self):
        df = self.df
        for column in df.select_dtypes(include=[np.object]).columns:
            total_length = df[column].size
            # get the 5 percent value
            total_length = round(self.percentage * total_length)
            unique_length = df[column].unique().size
            
            #get the unique elements to determine whether the column is categorical 
            if unique_length < total_length or unique_length <= self.unique_max:
                imputer = Imputer(missing_values = np.nan, strategy = 'mean')
                imputer = imputer.fit(df[[column]])
            
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
         
    def dataframe_category_info(self):
        df = self.df
        text = banner("Category Featues Analysis")
        self.logger.info(text)
        for column in self.df.select_dtypes(include=['category']).columns:
            text = banner(column,'-')
            self.logger.info(text)            
            self.logger.info("column name : {}".format(column))
            self.logger.info("categories : {}".format(df[column].cat.categories.values))
            result = df[column].value_counts()
            result_norm = df[column].value_counts(normalize=True)            
            self.logger.info("{0:<15} - {1:<10} - {2:<10}".format("categories", "count", "% count"))
            for (key1, value1, key2, value2) in zip(result.keys(),result.values,result_norm.keys(),result_norm.values,):
                self.logger.info("{0:<15} - {1:<10} - {2:.2f}".format(key1, value1, value2*100))
            
        
    def start_flow(self):
        self.load_data()
        self.load_dataframe()
        self.convert_column_lowercase()        
        self.get_categorical_column()
        self.dataframe_category_info()
        #self.fill_categorical_data() 
        self.dataframe_intial_info()
        #self.fill_numeric_data()
        #self.encode_categorical_data()
        self.save_data()
        
        