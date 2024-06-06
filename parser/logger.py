import logging

import colorlog


def setup_logger() -> logging.Logger:
    """
    Sets up a logger with colored output for console logging.

    This function configures a logger to use the `colorlog` package to provide
    colored log output based on the log level. It sets the logging level to
    INFO and applies a colored formatter to a console stream handler. The logger
    is configured to avoid adding multiple handlers if it already has handlers.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = colorlog.ColoredFormatter(
        "%(asctime)s - %(log_color)s%(levelname)s:%(module)s - %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()
