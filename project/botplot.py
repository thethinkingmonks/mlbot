# -*- coding: utf-8 -*-
import seaborn as sns
import matplotlib.pyplot as plt

import os
import numpy as np

class botplot():
    def __init__(self, bot):
        self.logger = bot["logger"]
        self.config = bot["config"]
        self.dataloader = bot["dataloader"]
        self.logger.debug("botplot - init ...")
        self.data = {}
        sns.set(style="darkgrid")
       
        #self.botplot_pointplot()

        self.single_plot_function = {"countplot":sns.countplot,                              
                              "swarmplot":sns.swarmplot,                     "barplot":sns.barplot
                             }
        self.multi_plot_function = {"countplot":sns.countplot,
                              "stripplot":sns.stripplot,
                              "swarmplot":sns.swarmplot,
                              "boxplot":sns.boxplot,
                              "violinplot":sns.violinplot,
                              "boxenplot":sns.boxenplot,
                              "barplot":sns.barplot
                             }
        
    def create_dirs(self):        
        output_dir = self.config.config["output_dir"]
        folders = self.single_plot_function.keys()
        
        cwd = os.getcwd()  
        os.chdir(output_dir)
        for x in folders:
            # create the output dir
            if not os.path.exists(x):
                os.makedirs(x)
        os.chdir(cwd)
    
    def load_dataframe(self):
        self.logger.debug("botplot - read_data ...")
        self.df = self.dataloader.get_dataframe()
        
    def load_data(self):
        self.logger.debug("botplot - load_data ...")
        self.data = self.dataloader.load_data(self.config.config['data_file'])        
        
    def save_data(self):
        self.logger.debug("botplot - save_data ...")
        self.dataloader.save_data(self.config.config['data_file'], self.data)
        
    def get_output_path(self, dirname):        
        output_dir = self.config.config["output_dir"]
        output_dir = os.path.join(output_dir, dirname)
        return output_dir
    
    def botplot_categorical(self, plottype):
        output_dir = self.get_output_path(plottype)        
        self.logger.debug("botplot - {} ...".format(plottype))
        df = self.df
        plot_function = self.single_plot_function
        
        for column in df.select_dtypes(include=[np.number]).columns:
            filename = os.path.join(output_dir,column + ".png")
            print(filename)
            #sns_plot = sns.stripplot(x='penalty_yards', y='return_yards', data=self.df)
            sns_plot = plot_function[plottype](x=column, data=self.df)
            #figure = sns_plot.get_figure()
            plt.savefig(filename, dpi=400)
            plt.clf()
            break

    def botplot_pairplot(self):
        self.logger.debug("botplot - botplot_stripplot ...")
        output_dir = self.get_output_path("pairplot")        
        self.logger.debug("botplot - {} ...".format("pairplot"))
        df = self.df    
        filename = os.path.join(output_dir,"pairplot" + ".png")
        print(filename)
        print(self.df.shape)
        sns_plot = sns.pairplot(self.df)
        #sns_plot = plot_function[plottype](x=column, data=self.df)
        #figure = sns_plot.get_figure()
        plt.savefig(filename, dpi=400)
        plt.clf()
        
    
    def botplot_visualize(self):
        self.logger.debug("botplot - botplot_visualize ...")
        self.botplot_pairplot()
        #self.botplot_stripplot()
        #self.botplot_pointplot()
        #self.botplot_pointplot()
        #self.botplot_pointplot()
        #self.botplot_pointplot()
        #self.botplot_pointplot()
        #self.botplot_pointplot()
        #self.botplot_pointplot()
        return
        for plottype in self.single_plot_function.keys():
            self.botplot_categorical(plottype)        
    
    def start_flow(self):
        self.logger.debug("botplot - start_flow ...")
        self.load_data()
        self.create_dirs()
        self.load_dataframe()
        self.botplot_visualize()
        self.save_data()
