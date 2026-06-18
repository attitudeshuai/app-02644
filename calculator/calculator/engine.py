#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculation Engine - Core mathematical operations
Uses safe expression parser instead of eval()
"""

import math
import logging
from typing import Tuple, Optional
from .parser import SafeExpressionParser, ParseError
from .utils.logger import CalculationLogger


class CalculationEngine:
    """
    Scientific calculation engine supporting:
    - Basic arithmetic operations
    - Trigonometric functions (sin, cos, tan and inverses)
    - Logarithmic functions (log, ln)
    - Power and root operations
    - Constants (π, e)
    - Factorial
    """
    
    def __init__(self):
        self.logger = CalculationLogger()
        self.parser = SafeExpressionParser()
        self.angle_mode = "DEG"
        self.last_result: Optional[float] = None
    
    def set_angle_mode(self, mode: str):
        """Set angle mode for trigonometric functions"""
        if mode in ("DEG", "RAD"):
            self.angle_mode = mode
            self.parser.set_angle_mode(mode)
            logging.getLogger(__name__).info(f"Angle mode set to {mode}")
    
    def calculate(self, expression: str) -> Tuple[bool, str]:
        """
        Evaluate a mathematical expression safely.
        
        Args:
            expression: The mathematical expression to evaluate
            
        Returns:
            Tuple of (success: bool, result: str)
        """
        if not expression or expression.strip() == "":
            return True, "0"
        
        try:
            result = self.parser.parse(expression)
            
            # Handle special cases
            if isinstance(result, complex):
                return False, "结果为复数"
            
            if math.isnan(result):
                return False, "结果无效"
            
            if math.isinf(result):
                return False, "数值溢出"
            
            self.last_result = result
            
            # Format result
            result_str = self._format_result(result)
            
            self.logger.log_calculation(expression, result_str)
            return True, result_str
            
        except ParseError as e:
            self.logger.log_error(expression, str(e))
            return False, str(e)
        except ZeroDivisionError:
            self.logger.log_error(expression, "除数不能为零")
            return False, "除数不能为零"
        except OverflowError:
            self.logger.log_error(expression, "数值溢出")
            return False, "数值溢出"
        except Exception as e:
            self.logger.log_error(expression, str(e))
            return False, f"计算错误"
    
    def _format_result(self, result: float) -> str:
        """Format result for display"""
        if isinstance(result, float):
            if result == int(result) and abs(result) < 1e15:
                return str(int(result))
            else:
                return f"{result:.10g}"
        return str(result)
    
    def calculate_function(self, func_name: str, value: float) -> Tuple[bool, str]:
        """
        Calculate a single function with a value
        
        Args:
            func_name: Name of the function
            value: Input value
            
        Returns:
            Tuple of (success: bool, result: str)
        """
        try:
            result = None
            
            if func_name == 'sin':
                rad = math.radians(value) if self.angle_mode == "DEG" else value
                result = math.sin(rad)
            elif func_name == 'cos':
                rad = math.radians(value) if self.angle_mode == "DEG" else value
                result = math.cos(rad)
            elif func_name == 'tan':
                rad = math.radians(value) if self.angle_mode == "DEG" else value
                result = math.tan(rad)
            elif func_name == 'asin':
                if value < -1 or value > 1:
                    return False, "输入超出范围"
                rad = math.asin(value)
                result = math.degrees(rad) if self.angle_mode == "DEG" else rad
            elif func_name == 'acos':
                if value < -1 or value > 1:
                    return False, "输入超出范围"
                rad = math.acos(value)
                result = math.degrees(rad) if self.angle_mode == "DEG" else rad
            elif func_name == 'atan':
                rad = math.atan(value)
                result = math.degrees(rad) if self.angle_mode == "DEG" else rad
            elif func_name == 'log':
                if value <= 0:
                    return False, "输入超出范围"
                result = math.log10(value)
            elif func_name == 'ln':
                if value <= 0:
                    return False, "输入超出范围"
                result = math.log(value)
            elif func_name == 'sqrt':
                if value < 0:
                    return False, "输入超出范围"
                result = math.sqrt(value)
            elif func_name == 'square':
                result = value ** 2
            elif func_name == 'cube':
                result = value ** 3
            elif func_name == 'reciprocal':
                if value == 0:
                    return False, "除数不能为零"
                result = 1 / value
            elif func_name == 'exp':
                result = math.exp(value)
            elif func_name == 'exp10':
                result = 10 ** value
            elif func_name == 'factorial':
                if value < 0 or value != int(value):
                    return False, "输入无效"
                if value > 170:
                    return False, "数值溢出"
                result = math.factorial(int(value))
            elif func_name == 'abs':
                result = abs(value)
            elif func_name == 'negate':
                result = -value
            elif func_name == 'percent':
                result = value / 100
            else:
                return False, f"未知函数"
            
            self.last_result = result
            result_str = self._format_result(result)
            
            self.logger.log_calculation(f"{func_name}({value})", result_str)
            return True, result_str
            
        except OverflowError:
            self.logger.log_error(f"{func_name}({value})", "数值溢出")
            return False, "数值溢出"
        except Exception as e:
            self.logger.log_error(f"{func_name}({value})", str(e))
            return False, "计算错误"
