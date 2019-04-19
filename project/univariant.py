# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.

trainfile = "../input/train.csv"

class univariant:
    def __init__(self):
        self.N = 0
        self.minimum = 0
        self.maximum = 0
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.range = 0
        self.variance = 0
        self.std = 0
        self.ced = 0
        self.skew = 0
        self.kurtosis = 0
        self.df = pd.read_csv(trainfile)
    
    def calculate_parameters(self):
        # Count 
        self.N = len(self.df['LotFrontage'])

        # Minimum 
        self.minimum = min(self.df['LotFrontage'])
        
        # Maximun
        self.maximum = max(self.df['LotFrontage'])
        
        # Mean
        self.mean = self.df['LotFrontage'].mean()
        
        # Median
        self.median = self.df['LotFrontage'].median()
        
        # Mode
        self.mode = self.df['LotFrontage'].mode()
        
        # Range
        self.range = self.maximum - self.minimum
        
        # Variance 
        self.variance = self.df['LotFrontage'].var()
        
        # Standard Deviation
        self.std = self.df['LotFrontage'].std()
        
        # Quantiles

        # Coefficient of Deviation
        self.ced = self.std/self.mean * 100
        
        # Skewness
        self.skew = self.df['LotFrontage'].skew()
        
        # Kurtosis
        self.kurtosis = self.df['LotFrontage'].kurtosis()
            
    def dump_parameters(self):
        # Count 
        print("{0:<30} : {1}".format("Count", self.N))

        # Minimum 
        print("{0:<30} : {1:.2f}".format("Minimum", self.minimum))

        # Maximun        
        print("{0:<30} : {1:.2f}".format("Maximum", self.maximum))

        # Mean        
        print("{0:<30} : {1:.2f}".format("Mean", self.mean))

        # Median        
        print("{0:<30} : {1:.2f}".format("Median", self.median))

        # Mode        
        print("{0:<30} : {1}".format("Mode",[i for i in self.mode]))

        # Range        
        print("{0:<30} : {1:.2f}".format("Range", self.range))

        # Variance         
        print("{0:<30} : {1:.2f}".format("Variance", self.variance))

        # Standard Deviation        
        print("{0:<30} : {1:.2f}".format("Standard Deviation", self.std))

        # Quantiles

        # Coefficient of Deviation        
        print("{0:<30} : {1:.2f}".format("Coefficient of Deviation", self.ced))

        # Skewness        
        print("{0:<30} : {1:.2f}".format("Skewness", self.skew))

        # Kurtosis        
        print("{0:<30} : {1:.2f}".format("Kurtosis", self.kurtosis))
        
    def start_flow(self):
        self.calculate_parameters()
        self.dump_parameters()
        
def main():
    uni = univariant()
    uni.start_flow()
    
if __name__ == '__main__':
    main()
