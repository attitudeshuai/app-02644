#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Calculator Application
"""

import tkinter as tk
import logging

from .engine import CalculationEngine
from .ui import Styles, DisplayPanel, KeypadPanel, HistoryPanel


class CalculatorApp:
    """Main calculator application class"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engine = CalculationEngine()
        
        self.current_expression = ""
        self.current_result = "0"
        self.last_was_result = False
        
        self._create_window()
        self._create_ui()
        self._bind_keyboard()
    
    def _create_window(self):
        """Create and configure the main window"""
        self.root = tk.Tk()
        self.root.title("Calculator")
        
        w, h = Styles.DIMENSIONS['window_width'], Styles.DIMENSIONS['window_height']
        self.root.geometry(f"{w}x{h}")
        self.root.minsize(w, h)
        self.root.configure(bg=Styles.COLORS['bg_primary'])
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"+{x}+{y}")
    
    def _create_ui(self):
        """Create UI components"""
        main = tk.Frame(self.root, bg=Styles.COLORS['bg_primary'])
        main.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        
        # History (collapsible)
        self.history_panel = HistoryPanel(main, on_history_select=self._on_history_select)
        self.history_panel.pack(fill=tk.X)
        
        # Display
        self.display = DisplayPanel(main)
        self.display.pack(fill=tk.X)
        
        # Keypad
        self.keypad = KeypadPanel(main, on_button_click=self._on_button_click)
        self.keypad.pack(fill=tk.BOTH, expand=True, pady=(8, 0))
    
    def _bind_keyboard(self):
        """Bind keyboard events"""
        self.root.bind('<Key>', self._on_key_press)
        self.root.bind('<Return>', lambda e: self._on_button_click('='))
        self.root.bind('<Escape>', lambda e: self._on_button_click('C'))
        self.root.bind('<BackSpace>', lambda e: self._on_button_click('⌫'))
    
    def _on_key_press(self, event):
        # Mac 上 ^ 是死键，event.char 拿不到，需要用 keysym 兜底
        if event.keysym == 'asciicircum':
            self._on_button_click('^')
            return
        
        key = event.char
        key_map = {'+': '+', '-': '−', '*': '×', '/': '÷', '.': '.', '(': '(', ')': ')', '%': '%', '^': '^'}
        
        if key.isdigit():
            self._on_button_click(key)
        elif key in key_map:
            self._on_button_click(key_map[key])
    
    def _on_button_click(self, btn: str):
        self.display.clear_error()
        
        # DEG/RAD toggle
        if btn == 'DEG':
            new_mode = self.display.toggle_mode()
            self.engine.set_angle_mode(new_mode)
            self.keypad.update_mode_button(new_mode)
            return
        
        if btn == 'C':
            self.current_expression = ""
            self.current_result = "0"
            self.last_was_result = False
            self.display.set_expression("")
            self.display.set_result("0")
            return
        
        if btn == '⌫':
            if self.current_expression:
                self.current_expression = self.current_expression[:-1]
                self.display.set_expression(self.current_expression)
            return
        
        if btn == '=':
            if self.current_expression:
                success, result = self.engine.calculate(self.current_expression)
                if success:
                    self.history_panel.add_entry(self.current_expression, result)
                    self.current_result = result
                    self.display.set_result(result)
                    self.last_was_result = True
                else:
                    self.display.set_error(result)
            return
        
        # Functions
        funcs = {
            'sin': 'sin', 'cos': 'cos', 'tan': 'tan',
            'log': 'log', 'ln': 'ln', '√': 'sqrt',
            '±': 'negate', '%': 'percent', 'x²': 'square',
        }
        
        if btn in funcs:
            # Get value to apply function to
            if self.last_was_result or not self.current_expression:
                val_str = self.current_result
                # Skip if current result is an error
                if val_str == "Error" or val_str.startswith("Error"):
                    return
            else:
                success, result = self.engine.calculate(self.current_expression)
                if not success:
                    self.display.set_error(result)
                    return
                val_str = result
            
            try:
                val = float(val_str)
            except ValueError:
                self.display.set_error("Error")
                return
            
            success, result = self.engine.calculate_function(funcs[btn], val)
            if success:
                self.current_result = result
                self.current_expression = f"{funcs[btn]}({val_str})"
                self.display.set_expression(self.current_expression)
                self.display.set_result(result)
                self.last_was_result = True
                self.history_panel.add_entry(self.current_expression, result)
            else:
                self.display.set_error(result)
            return
        
        if btn == '^':
            self._append('^')
            return
        
        if btn in ('π', 'e'):
            if self.last_was_result:
                self.current_expression = ""
                self.last_was_result = False
            if self.current_expression and (self.current_expression[-1].isdigit() or self.current_expression[-1] in 'πe)'):
                self.current_expression += '×'
            self.current_expression += btn
            self.display.set_expression(self.current_expression)
            return
        
        if btn in '()':
            self._append(btn)
            return
        
        if btn in ('+', '−', '×', '÷'):
            if self.last_was_result:
                self.current_expression = self.current_result
                self.last_was_result = False
            if not self.current_expression and btn != '−':
                return
            if self.current_expression and self.current_expression[-1] in '+-×÷':
                self.current_expression = self.current_expression[:-1]
            self.current_expression += btn
            self.display.set_expression(self.current_expression)
            return
        
        if btn.isdigit() or btn == '.':
            if self.last_was_result:
                self.current_expression = ""
                self.last_was_result = False
            if btn == '.' and '.' in self.current_expression.split('×')[-1].split('÷')[-1].split('+')[-1].split('−')[-1]:
                return
            self.current_expression += btn
            self.display.set_expression(self.current_expression)
            return
    
    def _append(self, text: str):
        if self.last_was_result:
            if text in ('^',):
                # 用上一次的结果作为基数，比如 2^
                self.current_expression = self.current_result
                self.last_was_result = False
            elif text not in '()':
                self.current_expression = self.current_result
                self.last_was_result = False
        self.current_expression += text
        self.display.set_expression(self.current_expression)
    
    def _on_history_select(self, result: str):
        self.current_expression = result
        self.display.set_expression(result)
        self.last_was_result = False
    
    def run(self):
        self.logger.info("Application started")
        self.root.mainloop()
