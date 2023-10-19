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

def setup_logger(logger_name, log_dir='logs', log_file_name='app.log', log_level='INFO'):
    # Get the directory where the script is running
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Create log directory path
    log_dir_path = os.path.join(script_dir, log_dir)

    if not os.path.exists(log_dir_path):
        os.makedirs(log_dir_path)

    log_file_path = os.path.join(log_dir_path, log_file_name)

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
                'when': 'W6',
                'backupCount': 1,
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
    return logging.getLogger(logger_name)

if __name__ == "__main__":
    logger = setup_logger("example_logger", log_level='DEBUG')
    logger.info('This is an info message.')
    logger.debug('This is a debug message.')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')
