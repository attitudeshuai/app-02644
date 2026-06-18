#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for CalculationEngine
"""

import unittest
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator.engine import CalculationEngine


class TestEngineBasic(unittest.TestCase):
    """Test basic engine operations"""
    
    def setUp(self):
        self.engine = CalculationEngine()
    
    def test_basic_calculation(self):
        success, result = self.engine.calculate("2+3")
        self.assertTrue(success)
        self.assertEqual(result, "5")
    
    def test_complex_expression(self):
        success, result = self.engine.calculate("(2+3)*4")
        self.assertTrue(success)
        self.assertEqual(result, "20")
    
    def test_empty_expression(self):
        success, result = self.engine.calculate("")
        self.assertTrue(success)
        self.assertEqual(result, "0")
    
    def test_division_by_zero(self):
        success, result = self.engine.calculate("10/0")
        self.assertFalse(success)
        self.assertIn("零", result)


class TestEngineFunctions(unittest.TestCase):
    """Test engine function calculations"""
    
    def setUp(self):
        self.engine = CalculationEngine()
    
    def test_sin_deg(self):
        self.engine.set_angle_mode("DEG")
        success, result = self.engine.calculate_function("sin", 90)
        self.assertTrue(success)
        self.assertEqual(result, "1")
    
    def test_cos_deg(self):
        self.engine.set_angle_mode("DEG")
        success, result = self.engine.calculate_function("cos", 0)
        self.assertTrue(success)
        self.assertEqual(result, "1")
    
    def test_log(self):
        success, result = self.engine.calculate_function("log", 100)
        self.assertTrue(success)
        self.assertEqual(result, "2")
    
    def test_log_invalid(self):
        success, result = self.engine.calculate_function("log", -1)
        self.assertFalse(success)
    
    def test_sqrt(self):
        success, result = self.engine.calculate_function("sqrt", 16)
        self.assertTrue(success)
        self.assertEqual(result, "4")
    
    def test_sqrt_invalid(self):
        success, result = self.engine.calculate_function("sqrt", -1)
        self.assertFalse(success)
    
    def test_square(self):
        success, result = self.engine.calculate_function("square", 5)
        self.assertTrue(success)
        self.assertEqual(result, "25")
    
    def test_negate(self):
        success, result = self.engine.calculate_function("negate", 5)
        self.assertTrue(success)
        self.assertEqual(result, "-5")
    
    def test_percent(self):
        success, result = self.engine.calculate_function("percent", 50)
        self.assertTrue(success)
        self.assertEqual(result, "0.5")
    
    def test_factorial(self):
        success, result = self.engine.calculate_function("factorial", 5)
        self.assertTrue(success)
        self.assertEqual(result, "120")
    
    def test_factorial_invalid(self):
        success, result = self.engine.calculate_function("factorial", -1)
        self.assertFalse(success)


class TestAngleMode(unittest.TestCase):
    """Test angle mode switching"""
    
    def setUp(self):
        self.engine = CalculationEngine()
    
    def test_deg_mode(self):
        self.engine.set_angle_mode("DEG")
        success, result = self.engine.calculate_function("sin", 30)
        self.assertTrue(success)
        self.assertAlmostEqual(float(result), 0.5, places=5)
    
    def test_rad_mode(self):
        self.engine.set_angle_mode("RAD")
        success, result = self.engine.calculate_function("sin", math.pi/6)
        self.assertTrue(success)
        self.assertAlmostEqual(float(result), 0.5, places=5)


if __name__ == '__main__':
    unittest.main()
