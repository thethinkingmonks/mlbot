# -*- coding: utf-8 -*-

class botplot():
    def __init__(self, bot):
        self.logger = bot["logger"]
        self.config = bot["config"]
        self.logger.info("Initialize MLPlot ...")
        
    
    def read_data(self):
        pass
    
    def plot_displot(self):
        pass
    
    def start_flow(self):
        self.plot_displot()
