import logging, sys

class Logger():
    def __init__(self, log_level):
        self.logger = logging.getLogger('logger')
        stdout_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)
        self.logger.setLevel(log_level)
        
    def log_info(self, message):
        self.logger.info(message)
    
    def log_error(self, message):
        self.logger.error(message)
    
