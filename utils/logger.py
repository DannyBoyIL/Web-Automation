"""
Utility logger class
"""

import logging
import os
from datetime import datetime


class Logger:
    def __init__(self, log_file_name="automation_test"):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        # filename using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = os.path.join(log_dir, f"{log_file_name}_{timestamp}.log")

        self.logger = logging.getLogger(log_file_name)
        self.logger.setLevel(logging.DEBUG)

        # remove existing handlers
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # logger format configuration
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

        # File Handler: write to file
        file_handler = logging.FileHandler(log_path, mode='w')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console Handler: write to terminal
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


log = Logger().get_logger()