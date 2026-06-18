#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Safe Expression Parser - No eval()
Implements a recursive descent parser for mathematical expressions.
"""

import math
import re
from typing import Union, List, Tuple

Number = Union[int, float]


class ParseError(Exception):
    """Expression parsing error"""
    pass


class SafeExpressionParser:
    """
    Safe mathematical expression parser using recursive descent.
    Supports: +, -, *, /, ^, parentheses, and scientific functions.
    """
    
    def __init__(self):
        self.pos = 0
        self.expr = ""
        self.angle_mode = "DEG"
        
        # Mathematical constants
        self.constants = {
            'π': math.pi,
            'pi': math.pi,
            'e': math.e,
        }
    
    def set_angle_mode(self, mode: str):
        """Set angle mode for trigonometric functions"""
        if mode in ("DEG", "RAD"):
            self.angle_mode = mode
    
    def _to_radians(self, value: float) -> float:
        if self.angle_mode == "RAD":
            return math.radians(value)
        return value
    
    def _from_radians(self, value: float) -> float:
        if self.angle_mode == "DEG":
            return math.degrees(value)
        return value
    
    def parse(self, expression: str) -> Number:
        """
        Parse and evaluate a mathematical expression safely.
        
        Args:
            expression: Mathematical expression string
            
        Returns:
            Calculated result
            
        Raises:
            ParseError: If expression is invalid
        """
        # Preprocess: normalize operators
        self.expr = expression.replace('×', '*').replace('÷', '/').replace('−', '-')
        self.expr = self.expr.replace(' ', '')
        self.pos = 0
        
        if not self.expr:
            return 0
        
        # Validate characters
        if not self._validate_expression():
            raise ParseError("表达式包含非法字符")
        
        result = self._parse_expression()
        
        if self.pos < len(self.expr):
            raise ParseError("表达式格式错误")
        
        return result
    
    def _validate_expression(self) -> bool:
        """Validate that expression contains only allowed characters"""
        allowed_pattern = r'^[\d\.\+\-\*\/\^\(\)\s]*$'
        # Also allow function names and constants
        temp = self.expr
        for name in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 
                     'log', 'ln', 'sqrt', 'abs', 'pi', 'π', 'e']:
            temp = temp.replace(name, '')
        
        return bool(re.match(allowed_pattern, temp))
    
    def _current_char(self) -> str:
        if self.pos < len(self.expr):
            return self.expr[self.pos]
        return ''
    
    def _advance(self):
        self.pos += 1
    
    def _skip_whitespace(self):
        while self._current_char() == ' ':
            self._advance()
    
    def _parse_expression(self) -> Number:
        """Parse addition and subtraction (lowest precedence)"""
        result = self._parse_term()
        
        while self._current_char() in ('+', '-'):
            op = self._current_char()
            self._advance()
            right = self._parse_term()
            if op == '+':
                result = result + right
            else:
                result = result - right
        
        return result
    
    def _parse_term(self) -> Number:
        """Parse multiplication and division"""
        result = self._parse_power()
        
        while self._current_char() in ('*', '/'):
            op = self._current_char()
            self._advance()
            right = self._parse_power()
            if op == '*':
                result = result * right
            else:
                if right != 0:
                    raise ParseError("除数不能为零")
                result = result / right
        
        return result
    
    def _parse_power(self) -> Number:
        """Parse exponentiation (right associative)"""
        result = self._parse_unary()
        
        if self._current_char() == '^':
            self._advance()
            right = self._parse_power()  # Right associative
            result = result ** right
        
        return result
    
    def _parse_unary(self) -> Number:
        """Parse unary operators (+, -)"""
        if self._current_char() == '+':
            self._advance()
            return self._parse_unary()
        elif self._current_char() == '-':
            self._advance()
            return -self._parse_unary()
        
        return self._parse_primary()
    
    def _parse_primary(self) -> Number:
        """Parse numbers, parentheses, functions, and constants"""
        self._skip_whitespace()
        
        # Check for functions
        for func_name in ['asin', 'acos', 'atan', 'sin', 'cos', 'tan', 
                          'sqrt', 'log', 'ln', 'abs']:
            if self.expr[self.pos:].startswith(func_name):
                return self._parse_function(func_name)
        
        # Check for constants
        for const_name, const_value in self.constants.items():
            if self.expr[self.pos:].startswith(const_name):
                self.pos += len(const_name)
                return const_value
        
        # Parentheses
        if self._current_char() == '(':
            self._advance()
            result = self._parse_expression()
            if self._current_char() != ')':
                raise ParseError("缺少右括号")
            self._advance()
            return result
        
        # Number
        return self._parse_number()
    
    def _parse_function(self, func_name: str) -> Number:
        """Parse a function call"""
        self.pos += len(func_name)
        
        if self._current_char() != '(':
            raise ParseError(f"函数 {func_name} 缺少括号")
        
        self._advance()
        arg = self._parse_expression()
        
        if self._current_char() != ')':
            raise ParseError("缺少右括号")
        self._advance()
        
        # Calculate function
        try:
            if func_name == 'sin':
                return math.sin(self._to_radians(arg))
            elif func_name == 'cos':
                return math.cos(self._to_radians(arg))
            elif func_name == 'tan':
                return math.tan(self._to_radians(arg))
            elif func_name == 'asin':
                if arg < -1 or arg > 1:
                    raise ParseError("输入超出范围")
                return self._from_radians(math.asin(arg))
            elif func_name == 'acos':
                if arg < -1 or arg > 1:
                    raise ParseError("输入超出范围")
                return self._from_radians(math.acos(arg))
            elif func_name == 'atan':
                return self._from_radians(math.atan(arg))
            elif func_name == 'sqrt':
                if arg < 0:
                    raise ParseError("输入超出范围")
                return math.sqrt(arg)
            elif func_name == 'log':
                if arg <= 0:
                    raise ParseError("输入超出范围")
                return math.log10(arg)
            elif func_name == 'ln':
                if arg <= 0:
                    raise ParseError("输入超出范围")
                return math.log(arg)
            elif func_name == 'abs':
                return abs(arg)
        except ValueError as e:
            raise ParseError(f"计算错误: {e}")
        
        raise ParseError(f"未知函数: {func_name}")
    
    def _parse_number(self) -> Number:
        """Parse a number (integer or float)"""
        start = self.pos
        has_dot = False
        
        # Handle negative sign already processed by unary
        while self._current_char().isdigit() or self._current_char() == '.':
            if self._current_char() == '.':
                if has_dot:
                    raise ParseError("数字格式错误")
                has_dot = True
            self._advance()
        
        if start == self.pos:
            raise ParseError("表达式格式错误")
        
        num_str = self.expr[start:self.pos]
        try:
            if has_dot:
                return float(num_str)
            else:
                return int(num_str)
        except ValueError:
            raise ParseError("数字格式错误")
