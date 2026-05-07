"""
Logging utilities for Android security testing
"""

import logging
import sys


def setup_logger(name: str = "android_security", level: int = logging.INFO,
                log_file: str = None) -> logging.Logger:
    """
    Setup a logger for the application
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Optional log file path
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


class LogColors:
    """ANSI color codes for logging"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log_success(message: str):
    """Log a success message"""
    print(f"{LogColors.OKGREEN}[+] {message}{LogColors.ENDC}")


def log_error(message: str):
    """Log an error message"""
    print(f"{LogColors.FAIL}[-] {message}{LogColors.ENDC}")


def log_info(message: str):
    """Log an info message"""
    print(f"{LogColors.OKBLUE}[*] {message}{LogColors.ENDC}")


def log_warning(message: str):
    """Log a warning message"""
    print(f"{LogColors.WARNING}[!] {message}{LogColors.ENDC}")
