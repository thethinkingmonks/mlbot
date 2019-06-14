# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import json
import os

# Customer Segmentation

class K_Means_Clustering():
    def __init__(self):
        self.parent_dir = os.path.join("data","K_Means_Clustering")
        self.configfile = os.path.join(self.parent_dir,"config.json")
        
        
    def read_config(self):
        ''' read configure file '''        
        with open(self.configfile) as f:
            self.config = json.load(f)                
        self.inputfile =  os.path.join(self.parent_dir,self.config["config"]["inputfile"])
        self.outputfile =  os.path.join(self.parent_dir,self.config["config"]["outputfile"])        
    
    def load_data(self):
        self.df = pd.read_csv(self.inputfile)
        # change the column name to lower case
        self.df.columns = map(str.lower, self.df.columns)         

    def save_data(self):
        self.df.to_csv(self.outputfile)
        
    def display_plot(self):
        sns.
        
    def analyse(self):
        self.read_config()
        self.load_data()
        self.save_data()
        
def main():
    stock = K_Means_Clustering()
    stock.analyse()
    
if __name__ == '__main__':
    main()        