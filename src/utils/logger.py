"""
Logging configuration for TeklaMCP
Provides structured logging with multiple handlers
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
import structlog

from .config import Config


def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[Path] = None
) -> structlog.BoundLogger:
    """
    Set up structured logging for the application

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path for log output

    Returns:
        Configured structlog logger
    """
    level = log_level or Config.LOG_LEVEL

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, level.upper()),
    )

    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        logging.getLogger().addHandler(file_handler)

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer() if Config.DEBUG else structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a logger instance with the specified name

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    return structlog.get_logger(name)


class LogContext:
    """
    Context manager for adding context to logs

    Example:
        with LogContext(logger, task="extraction", file="drawing.pdf"):
            logger.info("starting extraction")
    """

    def __init__(self, logger: structlog.BoundLogger, **context):
        self.logger = logger
        self.context = context
        self.bound_logger = None

    def __enter__(self):
        self.bound_logger = self.logger.bind(**self.context)
        return self.bound_logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.bound_logger.error(
                "context_error",
                exc_type=exc_type.__name__,
                exc_value=str(exc_val)
            )
        return False


# Create default logger
logger = setup_logging()


if __name__ == "__main__":
    # Test logging
    test_logger = get_logger("test")

    test_logger.debug("This is a debug message")
    test_logger.info("This is an info message", extra_data="some value")
    test_logger.warning("This is a warning", code=123)
    test_logger.error("This is an error", error_code="ERR_001")

    # Test context
    with LogContext(test_logger, operation="test", user="demo"):
        test_logger.info("inside context")

    print("\nLogging test complete!")
