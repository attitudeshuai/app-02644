#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scientific Calculator - Entry Point
A professional scientific calculator with modern UI
"""

import sys
import logging
from calculator.utils.logger import setup_logger


def main():
    """Application entry point"""
    setup_logger()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Scientific Calculator...")
    
    try:
        from calculator.app import CalculatorApp
        app = CalculatorApp()
        app.run()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)
    
    logger.info("Application closed.")


if __name__ == "__main__":
    main()
