from logypy import LogyPy

def test_logger():
    # Initialize the logger with a specific log level and log file
    logger = LogyPy(log_level="DEBUG", log_file="app.log")

    # Log messages at different levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

if __name__ == "__main":
    test_logger()
