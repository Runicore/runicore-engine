import logging
import os
from logging.handlers import RotatingFileHandler

class CustomLogger:
    def __init__(
            self, 
            log_name="app", 
            log_dir="logs", 
            log_level=logging.DEBUG, 
            max_log_size=10*1024*1024, 
            backup_count=5
        ):
        """
        :param log_name: The name of the log file
        :param log_dir: The directory where log files will be stored
        :param log_level: The log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        :param max_log_size: The maximum size of the log file (in bytes) before rotating
        :param backup_count: The number of backup log files to keep
        """
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)
        
        # Ensure the log directory exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Set up rotating file handler
        log_file = os.path.join(log_dir, f"{log_name}_{self.get_today_date()}.log")
        file_handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=backup_count)
        file_handler.setLevel(log_level)
        
        # Set up log format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add the file handler to the logger
        self.logger.addHandler(file_handler)
        
        # Set up console handler (prints to terminal/console)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_today_date(self):
        """
        Get today's date in the format (YYYY-MM-DD)
        """
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d')
    
    # Logging methods that you can use for logging different levels of messages
    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

# Example usage:

# if __name__ == "__main__":
#     logger = CustomLogger(log_name="my_app", log_level=logging.DEBUG)

#     logger.debug("This is a DEBUG message")
#     logger.info("This is an INFO message")
#     logger.warning("This is a WARNING message")
#     logger.error("This is an ERROR message")
#     logger.critical("This is a CRITICAL message")
