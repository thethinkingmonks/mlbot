# -*- coding: utf-8 -*-
# standard imports
import logging
import os

# custom imports
import MLBot
import Preprocessing
import DataLoader

def create_logger():
    
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

def main():
    logger = create_logger()
    bot = MLBot.MLBot(logger)
    dataLoader = DataLoader.DataLoader(logger)
    preprocessor = Preprocessing.Preprocessing(logger)
    preprocessor.start_flow()
    
  
if __name__ == '__main__':
    main()
