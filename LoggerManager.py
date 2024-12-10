import logging
from datetime import datetime
import os

class LoggerManager:
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.logger = logging.getLogger(__name__)
            # Configure logger here
            cls.__instance.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            # Get the current date and format the log file name
            log_file_name = datetime.now().strftime("log/log_%Y-%m-%d.txt")

            # Create log folder if not exists
           
            if not os.path.exists("log"):
                os.makedirs("log")
            
            # Create a FileHandler with the dynamic log file name
            file_handler = logging.FileHandler(log_file_name)
            file_handler.setFormatter(formatter)

            # Add handlers to the logger
            #cls.__instance.logger.addHandler(console_handler)
            cls.__instance.logger.addHandler(file_handler)
           
        return cls.__instance
    
    def log(self, level, message):
        self.logger.log(level, message)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
