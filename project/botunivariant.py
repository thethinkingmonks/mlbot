#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np 
import pickle
from scipy import stats
from banner import banner

class botunivariant:
    def __init__(self, bot):
        self.logger = bot["logger"]
        self.logger.debug("botunivariant - init ...")
        self.config = bot["config"]
        self.dataloader = bot["dataloader"]
        self.parameters = {}
        self.data = {}
        self.parameters['N'] = 0
        self.parameters['minimum'] = 0
        self.parameters['maximum'] = 0
        self.parameters['mean'] = 0
        self.parameters['median'] = 0
        self.parameters['mode'] = 0
        self.parameters['range'] = 0
        self.parameters['variance'] = 0
        self.parameters['std'] = 0
        self.parameters['ced'] = 0
        self.parameters['skew'] = 0
        self.parameters['kurtosis'] = 0
        self.parameters['quantile'] = []
        #self.parameters['zscore'] = []
        self.parameters['column'] = ""
        self.parameters['outlier_num'] = 0
        #self.parameters['outlier_pos'] = []
        self.parameters['outlier_per'] = 0        
        self.sep = ''
        
    def load_dataframe(self):
        self.logger.debug("botunivariant - load_dataframe ...")        
        self.df = self.dataloader.get_dataframe()        
 
    def load_data(self):
        self.data = self.dataloader.load_data(self.config.config['data_file'])        
        
    def save_data(self):
        self.logger.debug("botunivariant - save_data ...")
        self.dataloader.save_data(self.config.config['data_file'], self.data)
    
    def calculate_parameters(self, column):
        self.logger.debug("botunivariant - calculate_parameters ...")
        # Column
        self.parameters['column'] = column
        
        # Count 
        self.parameters['N'] = len(self.df[column])

        # Minimum 
        self.parameters['minimum'] = min(self.df[column])
        
        # Maximun
        self.parameters['maximum'] = max(self.df[column])
        
        # Mean
        self.parameters['mean'] = self.df[column].mean()
        
        # Median
        self.parameters['median'] = self.df[column].median()
        
        # Mode
        self.parameters['mode'] = self.df[column].mode()
        
        # Range
        self.parameters['range'] = self.parameters['maximum'] - self.parameters['minimum']
        
        # Variance 
        self.parameters['variance'] = self.df[column].var()
        
        # Standard Deviation
        self.parameters['std'] = self.df[column].std()
        
        # Quantiles
        self.parameters['quantile'] = []
        self.parameters['quantile'].append(self.df[column].quantile(0.25))
        self.parameters['quantile'].append(self.df[column].quantile(0.50))
        self.parameters['quantile'].append(self.df[column].quantile(0.75))

        # Coefficient of Deviation
        self.parameters['ced'] = self.parameters['std']/self.parameters['mean'] * 100
        
        # Skewness
        self.parameters['skew'] = self.df[column].skew()
        
        # Kurtosis
        self.parameters['kurtosis'] = self.df[column].kurtosis()
        
        # Z-Score
        self.zscore = stats.zscore(self.df[column])
        
        # Number of Outliers
        self.parameters['outlier_num'] = sum(self.zscore > 3)
        #self.parameters['outlier_pos'] = np.where(self.parameters['zscore'] > 3)
        self.parameters['outlier_per'] = self.parameters['outlier_num']/self.parameters['N']
        
        self.data['parameters_count'] += 1

            
    def dump_parameters(self):
        self.logger.debug("botunivariant - dump_parameters ...")
        # Column
        self.logger.info("{0:<30} : {1}".format("Column", self.parameters['column']))
        
        # Count 
        self.logger.info("{0:<30} : {1}".format("Count", self.parameters['N']))

        # Minimum 
        self.logger.info("{0:<30} : {1:.2f}".format("Minimum", self.parameters['minimum']))

        # Maximun        
        self.logger.info("{0:<30} : {1:.2f}".format("Maximum", self.parameters['maximum']))

        # Mean        
        self.logger.info("{0:<30} : {1:.2f}".format("Mean", self.parameters['mean']))

        # Median        
        self.logger.info("{0:<30} : {1:.2f}".format("Median", self.parameters['median']))

        # Mode        
        self.logger.info("{0:<30} : {1}".format("Mode",[i for i in self.parameters['mode']]))

        # Range        
        self.logger.info("{0:<30} : {1:.2f}".format("Range", self.parameters['range']))

        # Variance         
        self.logger.info("{0:<30} : {1:.2f}".format("Variance", self.parameters['variance']))

        # Standard Deviation        
        self.logger.info("{0:<30} : {1:.2f}".format("Standard Deviation", self.parameters['std']))

        # Quantiles
        self.logger.info("{0:<30} : {1}".format("Quantile", [i for i in self.parameters['quantile']]))
        
        # Coefficient of Deviation        
        self.logger.info("{0:<30} : {1:.2f}".format("Coefficient of Deviation", self.parameters['ced']))

        # Skewness        
        self.logger.info("{0:<30} : {1:.2f}".format("Skewness", self.parameters['skew']))

        # Kurtosis        
        self.logger.info("{0:<30} : {1:.2f}".format("Kurtosis", self.parameters['kurtosis']))
        
        # Z-Score
        #self.logger.info("{0:<30} : {1}".format("Z-Score", str(self.parameters['zscore'])))
        
        # Number of Outliers
        self.logger.info("{0:<30} : {1}".format("Number of Outliers", self.parameters['outlier_num']))
        #self.logger.info("{0:<30} : {1}".format("Position of Outliers", self.parameters['outlier_pos']))       
        self.logger.info("{0:<30} : {1:.2f}".format("Percentage of Outliers", self.parameters['outlier_per']*100))
        
        
    def save_parameters(self):
        self.logger.debug("botunivariant - save_parameters ...")
        self.dataloader.write_pickle_file(self.config.config['params_file'], self.parameters, 'ab')
            
    def read_all_parameters(self):
        data = self.data
        self.logger.debug("botunivariant - read_all_parameters ...")
        self.logger.info("parameter count : {}".format(self.data['parameters_count']))        
        
        with open(self.config.config['params_file'], 'rb') as parameters_file:
            for i in range(data['parameters_count']):
                self.logger.info("paramters : {}".format(i))
                param = pickle.load(parameters_file)            
                self.logger.info(param)
    
    def dump_all_parameters(self):
        text = banner("Parameters Detail")
        self.logger.info(text)
        for column in self.df.select_dtypes(include=[np.number]).columns:
            text = banner(column,'-')
            self.logger.info(text)
            self.calculate_parameters(column)
            self.dump_parameters()
            self.save_parameters()
            
    def start_flow(self):
        self.logger.debug("botunivariant - start_flow ...")
        self.load_data()
        self.load_dataframe()               
        self.dump_all_parameters()
        #self.read_all_parameters()
        self.save_data()