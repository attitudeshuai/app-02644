#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for SafeExpressionParser
"""

import unittest
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator.parser import SafeExpressionParser, ParseError


class TestBasicArithmetic(unittest.TestCase):
    """Test basic arithmetic operations"""
    
    def setUp(self):
        self.parser = SafeExpressionParser()
    
    def test_addition(self):
        self.assertEqual(self.parser.parse("2+3"), 5)
        self.assertEqual(self.parser.parse("10+20+30"), 60)
    
    def test_subtraction(self):
        self.assertEqual(self.parser.parse("10-3"), 7)
        self.assertEqual(self.parser.parse("100-50-25"), 25)
    
    def test_multiplication(self):
        self.assertEqual(self.parser.parse("4*5"), 20)
        self.assertEqual(self.parser.parse("2*3*4"), 24)
    
    def test_division(self):
        self.assertEqual(self.parser.parse("20/4"), 5)
        self.assertAlmostEqual(self.parser.parse("10/3"), 10/3)
    
    def test_mixed_operations(self):
        self.assertEqual(self.parser.parse("2+3*4"), 14)
        self.assertEqual(self.parser.parse("10-2*3"), 4)
        self.assertEqual(self.parser.parse("20/4+5"), 10)
    
    def test_parentheses(self):
        self.assertEqual(self.parser.parse("(2+3)*4"), 20)
        self.assertEqual(self.parser.parse("((2+3)*4)"), 20)
        self.assertEqual(self.parser.parse("(10-2)*(3+1)"), 32)
    
    def test_negative_numbers(self):
        self.assertEqual(self.parser.parse("-5"), -5)
        self.assertEqual(self.parser.parse("-5+10"), 5)
        self.assertEqual(self.parser.parse("10*-2"), -20)
    
    def test_decimals(self):
        self.assertAlmostEqual(self.parser.parse("3.14*2"), 6.28)
        self.assertAlmostEqual(self.parser.parse("0.1+0.2"), 0.3, places=10)


class TestPowerOperations(unittest.TestCase):
    """Test power/exponentiation operations"""
    
    def setUp(self):
        self.parser = SafeExpressionParser()
    
    def test_power(self):
        self.assertEqual(self.parser.parse("2^3"), 8)
        self.assertEqual(self.parser.parse("10^2"), 100)
    
    def test_power_right_associative(self):
        # 2^3^2 should be 2^(3^2) = 2^9 = 512
        self.assertEqual(self.parser.parse("2^3^2"), 512)
    
    def test_power_with_parentheses(self):
        self.assertEqual(self.parser.parse("(2^3)^2"), 64)


class TestConstants(unittest.TestCase):
    """Test mathematical constants"""
    
    def setUp(self):
        self.parser = SafeExpressionParser()
    
    def test_pi(self):
        self.assertAlmostEqual(self.parser.parse("π"), math.pi)
        self.assertAlmostEqual(self.parser.parse("pi"), math.pi)
        self.assertAlmostEqual(self.parser.parse("2*π"), 2*math.pi)
    
    def test_e(self):
        self.assertAlmostEqual(self.parser.parse("e"), math.e)
        self.assertAlmostEqual(self.parser.parse("e^2"), math.e**2)


class TestTrigFunctions(unittest.TestCase):
    """Test trigonometric functions"""
    
    def setUp(self):
        self.parser = SafeExpressionParser()
        self.parser.set_angle_mode("DEG")
    
    def test_sin(self):
        self.assertAlmostEqual(self.parser.parse("sin(0)"), 0)
        self.assertAlmostEqual(self.parser.parse("sin(90)"), 1)
        self.assertAlmostEqual(self.parser.parse("sin(30)"), 0.5, places=5)
    
    def test_cos(self):
        self.assertAlmostEqual(self.parser.parse("cos(0)"), 1)
        self.assertAlmostEqual(self.parser.parse("cos(90)"), 0, places=10)
        self.assertAlmostEqual(self.parser.parse("cos(60)"), 0.5, places=5)
    
    def test_tan(self):
        self.assertAlmostEqual(self.parser.parse("tan(0)"), 0)
        self.assertAlmostEqual(self.parser.parse("tan(45)"), 1, places=5)
    
    def test_rad_mode(self):
        self.parser.set_angle_mode("RAD")
        self.assertAlmostEqual(self.parser.parse("sin(0)"), 0)
        self.assertAlmostEqual(self.parser.parse(f"sin({math.pi/2})"), 1, places=10)


class TestLogFunctions(unittest.TestCase):
    """Test logarithmic functions"""
    
    def setUp(self):
        self.parser = SafeExpressionParser()
    
    def test_log(self):
        self.assertAlmostEqual(self.parser.parse("log(10)"), 1)
        self.assertAlmostEqual(self.parser.parse("log(100)"), 2)
        self.assertAlmostEqual(self.parser.parse("log(1)"), 0)
    
    def test_ln(self):
        self.assertAlmostEqual(self.parser.parse("ln(1)"), 0)
        self.assertAlmostEqual(self.parser.parse("ln(e)"), 1, places=10)
    
    def test_sqrt(self):
        self.assertEqual(self.parser.parse("sqrt(4)"), 2)
        self.assertEqual(self.parser.parse("sqrt(9)"), 3)
        self.assertAlmostEqual(self.parser.parse("sqrt(2)"), math.sqrt(2))


class TestErrorHandling(unittest.TestCase):
    """Test error handling"""
    
    def setUp(self):
        self.parser = SafeExpressionParser()
    
    def test_division_by_zero(self):
        with self.assertRaises(ParseError):
            self.parser.parse("10/0")
    
    def test_invalid_log(self):
        with self.assertRaises(ParseError):
            self.parser.parse("log(0)")
        with self.assertRaises(ParseError):
            self.parser.parse("log(-1)")
    
    def test_invalid_sqrt(self):
        with self.assertRaises(ParseError):
            self.parser.parse("sqrt(-1)")
    
    def test_invalid_asin(self):
        with self.assertRaises(ParseError):
            self.parser.parse("asin(2)")
    
    def test_unmatched_parentheses(self):
        with self.assertRaises(ParseError):
            self.parser.parse("(2+3")
        with self.assertRaises(ParseError):
            self.parser.parse("2+3)")
    
    def test_empty_expression(self):
        self.assertEqual(self.parser.parse(""), 0)


class TestUnicodeOperators(unittest.TestCase):
    """Test Unicode operator support"""
    
    def setUp(self):
        self.parser = SafeExpressionParser()
    
    def test_unicode_multiply(self):
        self.assertEqual(self.parser.parse("3×4"), 12)
    
    def test_unicode_divide(self):
        self.assertEqual(self.parser.parse("12÷4"), 3)
    
    def test_unicode_minus(self):
        self.assertEqual(self.parser.parse("10−3"), 7)


if __name__ == '__main__':
    unittest.main()
