import logging


def setup_logging(log_file='code_quality_analyzer.log', log_level='INFO'):
    log_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create handlers
    # c_handler = logging.StreamHandler()  # Console handler
    f_handler = logging.FileHandler(log_file)  # File handler

    # Set level for handlers
    # c_handler.setLevel(log_level)
    f_handler.setLevel(log_level)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # c_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)

    # Add handlers to the logger
    # logger.addHandler(c_handler)
    logger.addHandler(f_handler)
