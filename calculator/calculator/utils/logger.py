#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging configuration module
"""

import logging
import sys
from datetime import datetime


def setup_logger(level: int = logging.INFO) -> None:
    """
    Configure application logging
    
    Args:
        level: Logging level (default: INFO)
    """
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    
    # Suppress verbose logs from external libraries
    logging.getLogger('PIL').setLevel(logging.WARNING)


class CalculationLogger:
    """Logger for calculation operations"""
    
    def __init__(self):
        self.logger = logging.getLogger('calculator.engine')
    
    def log_calculation(self, expression: str, result: str) -> None:
        """Log a calculation operation"""
        self.logger.info(f"Calculate: {expression} = {result}")
    
    def log_error(self, expression: str, error: str) -> None:
        """Log a calculation error"""
        self.logger.error(f"Error in '{expression}': {error}")
    
    def log_clear(self) -> None:
        """Log clear operation"""
        self.logger.debug("Calculator cleared")
