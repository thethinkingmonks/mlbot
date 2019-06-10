# -*- coding: utf-8 -*-
# standard imports
import logging
import os

# custom imports
import botpreprocess
import botdataloader
import botunivariant
import botplot
import botconfig

class bot():
    def __init__(self):
        self.bot = {}
        # create the logger file
        self.bot["logger"] = self.create_logger()
        
    def create_logger(self):        
        logfile = 'logfile.log'
        # Gets or creates a logger
        logger = logging.getLogger(__name__)     
        
        if os.path.exists(logfile):
            open(logfile, 'w').close()
    
        if not logger.hasHandlers():        
            # set log level
            logger.setLevel(logging.INFO)        
            
            # define file handler and set formatter
            file_handler = logging.FileHandler(logfile)
            formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
            file_handler.setFormatter(formatter)
            
            # add file handler to logger
            logger.addHandler(file_handler)
            
        return logger    
    
    def bot_create(self):       
        
        # initialize all the configration parameters
        self.bot["config"] = botconfig.botconfig(self.bot)
        self.bot["config"].start_flow()
        
        self.bot["dataloader"] = botdataloader.botdataloader(self.bot)
        self.bot["preprocess"] = botpreprocess.botpreprocess(self.bot)
        self.bot["univariant"] = botunivariant.botunivariant(self.bot)
        self.bot["plot"] = botplot.botplot(self.bot)
        
    def bot_load(self):
        pass
        
    def bot_run(self):
        self.bot["dataloader"].start_flow()
        self.bot["preprocess"].start_flow()
        self.bot["univariant"].start_flow()
        self.bot["plot"].start_flow()

def main():
    mybot = bot()
    mybot.bot_create()
    mybot.bot_run()
    
if __name__ == '__main__':
    main()
