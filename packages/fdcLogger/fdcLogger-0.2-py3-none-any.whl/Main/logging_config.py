#FileName: logging_config.py
#FileDate: 2023-10-18
#FileDescription:
#    Python Config Program for Logging.
#----------------------------------------------------------------------------------
#FileHistory:
#| Ver.|  Date    |Author|                       Description                      |
#| 0.1 |2023-10-18| CMF  |                     Initial Version                    |
#| 0.2 |----------| CMF  |                      Handler Fixed.                    |
#----------------------------------------------------------------------------------

# Import Libraries
import logging
import logging.config
import logging.handlers
import os

def setup_logger(log_dir='logs', log_file_name='app.log', log_level='INFO'):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, log_file_name)

    logging_config = {
        'version': 1,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'simple': {
                'format': '%(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'simple',
            },
            'file': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': log_file_path,
                'when': 'W6',  # W0=WED, W1=THU, etc. Here, W6 means the log will rotate every Sunday.
                'backupCount': 1,  # Only keep one old log (the log for the last week)
                'level': log_level,
                'formatter': 'detailed',
            },
        },
        'root': {
            'level': log_level,
            'handlers': ['console', 'file']
        },
    }

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    return logger

if __name__ == "__main__":
    logger = setup_logger(log_level='DEBUG')
    logger.info('This is an info message.')
    logger.debug('This is a debug message.')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')
