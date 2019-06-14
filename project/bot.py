# -*- coding: utf-8 -*-
# standard imports
import logging
import os
import json

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
        self.configfile = "../config/config.json"
        self.bot["logger"] = self.create_logger()
        self.logger = self.bot["logger"]
        self.logger.debug("bot - init ...")
        
       
    def create_logger(self):        
        with open(self.configfile) as f:
            data = json.load(f)
        parameter = data['config']['files']
        root = parameter['root']
        logfile = parameter['log_file']
        output_dir = os.path.join(root, parameter['output_folder'])
        logfile = os.path.join(output_dir,logfile)
        
        # create the output dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)        

        print("logfile : {}".format(logfile))
        # Gets or creates a logger
        logger = logging.getLogger(__name__)     
        
        if os.path.exists(logfile):
            open(logfile, 'w').close()
    
        if not logger.hasHandlers():        
            # set log level
            logger.setLevel(logging.INFO)        
            
            # define file handler and set formatter
            file_handler = logging.FileHandler(logfile)
            #formatter    = logging.Formatter('[%(filename)s:%(lineno)s - %(funcName)20s() ] %(asctime)s : %(levelname)s : %(message)s')
            formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
            file_handler.setFormatter(formatter)
            
            # add file handler to logger
            logger.addHandler(file_handler)
            
        return logger  
    
    def close_logger(self):
        self.logger.debug("bot - close_logger ...")
        handlers = self.bot["logger"].handlers[:]
        for handler in handlers:
            handler.close()
        self.bot["logger"].removeHandler(handler)        
    
    def bot_create(self):
        self.logger.debug("bot - bot_create ...")
        # initialize all the configration parameters
        self.bot["config"] = botconfig.botconfig(self.bot)
        self.bot["config"].start_flow()
        
        self.bot["dataloader"] = botdataloader.botdataloader(self.bot)
        self.bot["preprocess"] = botpreprocess.botpreprocess(self.bot)
        self.bot["univariant"] = botunivariant.botunivariant(self.bot)
        self.bot["plot"] = botplot.botplot(self.bot)
        
    def bot_load(self):
        self.logger.debug("bot - bot_load ...")
        
    def bot_run(self):
        self.logger.debug("bot - bot_run ...")
        self.bot["dataloader"].start_flow()
        self.bot["preprocess"].start_flow()
        self.bot["univariant"].start_flow()
        self.bot["plot"].start_flow()
        self.close_logger()

def main():
    mybot = bot()
    mybot.bot_create()
    mybot.bot_run()
    
if __name__ == '__main__':
    main()
