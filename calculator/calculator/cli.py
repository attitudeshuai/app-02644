#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command Line Calculator - Fallback when tkinter is not available
"""

import sys
from .engine import CalculationEngine


class CalculatorCLI:
    """命令行计算器"""
    
    def __init__(self):
        self.engine = CalculationEngine()
        self.history = []
    
    def run(self):
        print("=" * 50)
        print("  科学计算器 (命令行版本)")
        print("  tkinter 不可用，使用命令行模式")
        print("=" * 50)
        print("\n命令:")
        print("  输入数学表达式进行计算")
        print("  支持: +, -, *, /, ^, sqrt(), sin(), cos(), tan(), log(), ln()")
        print("  常量: pi, e")
        print("  mode    - 切换角度模式 (DEG/RAD)")
        print("  history - 查看历史记录")
        print("  clear   - 清除历史")
        print("  quit    - 退出\n")
        
        while True:
            try:
                expr = input(f"[{self.engine.angle_mode}] >>> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n再见!")
                break
            
            if not expr:
                continue
            
            if expr.lower() in ('quit', 'exit', 'q'):
                print("再见!")
                break
            
            if expr.lower() == 'mode':
                new_mode = "RAD" if self.engine.angle_mode == "DEG" else "DEG"
                self.engine.set_angle_mode(new_mode)
                print(f"角度模式: {new_mode}")
                continue
            
            if expr.lower() == 'history':
                if not self.history:
                    print("暂无历史记录")
                else:
                    for i, (e, r) in enumerate(self.history[-10:], 1):
                        print(f"  {i}. {e} = {r}")
                continue
            
            if expr.lower() == 'clear':
                self.history.clear()
                print("历史已清除")
                continue
            
            # 转换常见符号
            expr_calc = expr.replace('×', '*').replace('÷', '/').replace('−', '-')
            
            success, result = self.engine.calculate(expr_calc)
            if success:
                print(f"  = {result}")
                self.history.append((expr, result))
            else:
                print(f"  错误: {result}")
