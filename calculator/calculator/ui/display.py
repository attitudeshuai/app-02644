#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Display Panel Component
"""

import tkinter as tk
from .styles import Styles


class DisplayPanel(tk.Frame):
    """Calculator display panel showing expression and result"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=Styles.COLORS['display_bg'], **kwargs)
        
        self.expression_var = tk.StringVar(value="")
        self.result_var = tk.StringVar(value="0")
        self.mode_var = tk.StringVar(value="DEG")
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create display widgets"""
        container = tk.Frame(self, bg=Styles.COLORS['display_bg'])
        container.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)
        
        # Expression display (top, smaller)
        self.expression_label = tk.Label(
            container,
            textvariable=self.expression_var,
            font=('Consolas', 12),
            fg=Styles.COLORS['text_muted'],
            bg=Styles.COLORS['display_bg'],
            anchor='e'
        )
        self.expression_label.pack(fill=tk.X, pady=(8, 0))
        
        # Result display (bottom, larger)
        self.result_label = tk.Label(
            container,
            textvariable=self.result_var,
            font=('Consolas', 36, 'bold'),
            fg=Styles.COLORS['text_primary'],
            bg=Styles.COLORS['display_bg'],
            anchor='e'
        )
        self.result_label.pack(fill=tk.X, pady=(4, 8))
        
        # Auto-resize on text change
        self.result_var.trace_add('write', self._adjust_font_size)
    
    def _adjust_font_size(self, *args):
        """Adjust font size based on text length"""
        text = self.result_var.get()
        length = len(text)
        
        if length <= 10:
            size = 36
        elif length <= 14:
            size = 28
        elif length <= 18:
            size = 22
        else:
            size = 18
        
        self.result_label.config(font=('Consolas', size, 'bold'))
    
    def set_expression(self, text: str):
        self.expression_var.set(text)
    
    def set_result(self, text: str):
        try:
            num = float(text)
            if abs(num) >= 1e12 or (abs(num) < 1e-8 and num != 0):
                text = f"{num:.6e}"
            elif num == int(num) and abs(num) < 1e12:
                text = str(int(num))
            else:
                text = f"{num:.10g}"
        except (ValueError, OverflowError):
            pass
        self.result_var.set(text)
    
    def set_error(self, message: str):
        """Display error message in Chinese"""
        # Translate common errors to Chinese
        error_map = {
            'Division by zero': '除数不能为零',
            'Domain error': '输入超出范围',
            'Invalid syntax': '表达式格式错误',
            'Invalid input': '输入无效',
            'Overflow': '数值溢出',
            'Complex result': '结果为复数',
            'Invalid result': '结果无效',
        }
        
        display_msg = '错误'
        for eng, chn in error_map.items():
            if eng in message:
                display_msg = chn
                break
        
        self.result_var.set(display_msg)
        self.result_label.config(fg=Styles.COLORS['error'])
    
    def clear_error(self):
        self.result_label.config(fg=Styles.COLORS['text_primary'])
    
    def toggle_mode(self) -> str:
        current = self.mode_var.get()
        new_mode = "RAD" if current == "DEG" else "DEG"
        self.mode_var.set(new_mode)
        return new_mode
    
    def get_mode(self) -> str:
        return self.mode_var.get()
