# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pickle
from scipy import stats

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.

trainfile = "../input/train.csv"

class univariant:
    def __init__(self):
        self.parameters = {}
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
        self.parameters['zscore'] = []
        self.parameters['column'] = ""
        self.parameters['outlier_num'] = 0
        self.parameters['outlier_pos'] = []
        self.parameters['outlier_per'] = 0
        self.parameters_count = 0        
        self.df = pd.read_csv(trainfile)
        with open('parameters.log', 'w') as parameters_file:
            pass
        
    
    def calculate_parameters(self, column):
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
        self.parameters['zscore'] = stats.zscore(self.df[column])
        
        # Number of Outliers
        self.parameters['outlier_num'] = sum(self.parameters['zscore'] > 3)
        self.parameters['outlier_pos'] = np.where(self.parameters['zscore'] > 3)
        self.parameters['outlier_per'] = self.parameters['outlier_num']/self.parameters['N']
        
        self.parameters_count += 1

            
    def dump_parameters(self):
        # Column
        print("{0:<30} : {1}".format("Column", self.parameters['column']))
        
        # Count 
        print("{0:<30} : {1}".format("Count", self.parameters['N']))

        # Minimum 
        print("{0:<30} : {1:.2f}".format("Minimum", self.parameters['minimum']))

        # Maximun        
        print("{0:<30} : {1:.2f}".format("Maximum", self.parameters['maximum']))

        # Mean        
        print("{0:<30} : {1:.2f}".format("Mean", self.parameters['mean']))

        # Median        
        print("{0:<30} : {1:.2f}".format("Median", self.parameters['median']))

        # Mode        
        print("{0:<30} : {1}".format("Mode",[i for i in self.parameters['mode']]))

        # Range        
        print("{0:<30} : {1:.2f}".format("Range", self.parameters['range']))

        # Variance         
        print("{0:<30} : {1:.2f}".format("Variance", self.parameters['variance']))

        # Standard Deviation        
        print("{0:<30} : {1:.2f}".format("Standard Deviation", self.parameters['std']))

        # Quantiles
        print("{0:<30} : {1}".format("Quantile", [i for i in self.parameters['quantile']]))
        
        # Coefficient of Deviation        
        print("{0:<30} : {1:.2f}".format("Coefficient of Deviation", self.parameters['ced']))

        # Skewness        
        print("{0:<30} : {1:.2f}".format("Skewness", self.parameters['skew']))

        # Kurtosis        
        print("{0:<30} : {1:.2f}".format("Kurtosis", self.parameters['kurtosis']))
        
        # Z-Score
        print("{0:<30} : {1}".format("Z-Score", str(self.parameters['zscore'])))
        
        # Number of Outliers
        print("{0:<30} : {1}".format("Number of Outliers", self.parameters['outlier_num']))
        print("{0:<30} : {1}".format("Position of Outliers", self.parameters['outlier_pos']))       
        print("{0:<30} : {1}".format("Percentage of Outliers", self.parameters['outlier_per']*100))
        
        
    def save_parameters(self):
        with open('parameters.log', 'ab') as parameters_file:
            pickle.dump(self.parameters, parameters_file)
            
    def read_all_parameters(self):
        print("parameter count : {}".format(self.parameters_count))
        with open('parameters.log', 'rb') as parameters_file:
            for i in range(self.parameters_count):
                print("paramters : {}".format(i))
                param = pickle.load(parameters_file)
                print(param)
            
        
    def start_flow(self):
        for column in self.df.select_dtypes(include=[np.number]).columns:
            print("{0:*^20}".format(column))
            self.calculate_parameters(column)
            self.dump_parameters()
            self.save_parameters()
        self.read_all_parameters()
        
        
def main():
    uni = univariant()
    uni.start_flow()
    
if __name__ == '__main__':
    main()
