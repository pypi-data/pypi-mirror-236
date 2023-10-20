import os
import logging.config
from datetime import datetime
from logging import Logger

def configure_logging(debug_mode: bool, log_filename: str, log_config: dict) -> Logger :
    if debug_mode :
        date_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        log_directory = f"./logs/{log_filename}/{log_filename}_{date_time}"
        log_filename =  f"{log_filename}_debug.log"
    else :
        log_directory = f"./logs/{log_filename}"
        log_filename = f"{log_filename}.log"
        
    os.makedirs(log_directory, exist_ok=True)
    full_log_path = os.path.join(log_directory, log_filename)
    log_config["handlers"]["info_file_handler"]["filename"] = full_log_path

    logging.config.dictConfig(log_config)
    return logging.getLogger(__name__)