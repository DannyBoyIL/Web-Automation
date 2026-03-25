"""
Utility logger class
"""

import logging
import os
from datetime import datetime


class Logger:
    def __init__(self, log_file_name="automation_test"):
        self.logger = logging.getLogger(log_file_name)

        # Only configure handlers once per process; re-imports reuse the same logger.
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)

            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_path = os.path.join(log_dir, f"{log_file_name}_{timestamp}.log")

            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

            file_handler = logging.FileHandler(log_path, mode='w')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


log = Logger().get_logger()