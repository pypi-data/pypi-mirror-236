#FileName: logging_config.py
#FileDate: 2023-10-18
#FileDescription:
#    Python Config Program for Logging.
#----------------------------------------------------------------------------------
#FileHistory:
#| Ver.|  Date    |Author|                       Description                      |
#| 0.1 |2023-10-18| CMF  |                     Initial Version                    |
#----------------------------------------------------------------------------------

# Import Libraries
import os
import logging
import logging.config

def initialize_logger(log_dir='logs', log_file_name='app.log', log_level='INFO'):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, log_file_name)

    logging_config = {
        'version': 1,
        'formatters': {
            'detailed':{
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'simple':{
                'format': '%(levelname)s - %(message)s'
            }
        },
        'handlers':{
            'console':{
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'simple',
            }
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': log_file_path,
            'when': 'W6', #W6 = Sunday
            'backupCount': 1, #Retain for Only a Week
            'mode': 'a',
            'level': log_level,
            'formatter': 'detailed'
        },
        'root': {
            'level': log_level,
            'handlers': ['console', 'file']
        }
    }

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    return logger

if __name__ == "__main__":
    logger = initialize_logger(log_level= 'DEBUG')
    logger.info('This is an info message.')
    logger.debug('This is a debug message.')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')