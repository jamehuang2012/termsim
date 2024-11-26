import logging

class LoggerManager:
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.logger = logging.getLogger(__name__)
            # configure logger here
            cls.__instance.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            file_handler = logging.FileHandler('log/log.txt')
            file_handler.setFormatter(formatter)

            #cls.__instance.logger.addHandler(console_handler)
            cls.__instance.logger.addHandler(file_handler)
           
        return cls.__instance
    
    def log(self, level, message):
        self.logger.log(level, message)

    def debug(self,msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)        

