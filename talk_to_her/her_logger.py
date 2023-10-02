import logging
import os
import sys
from datetime import datetime


class HerLogger:
    _instance = None
    logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HerLogger, cls).__new__(cls)
            cls._instance.init_logger()
        return cls._instance

    def init_logger(self):
        self.logger = logging.getLogger('project')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

        # Stream Handler
        syslog = logging.StreamHandler(sys.stdout)
        syslog.setFormatter(formatter)
        self.logger.addHandler(syslog)

        # Log file
        log_dir = os.path.join('data', 'logs')
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)

        log_prefix = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        log_file = os.path.join(log_dir, f'{log_prefix}.log')
        open(log_file, 'w').close()

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

if __name__ == '__main__':
    l = HerLogger().logger
    l.info('Hi')