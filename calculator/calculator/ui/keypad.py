#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keypad Panel Component - Canvas based for precise text positioning
"""

import tkinter as tk
from typing import Callable, Dict
from .styles import Styles


class CanvasButton(tk.Canvas):
    """Button using Canvas for precise text centering with offset adjustment"""
    
    def __init__(self, parent, text: str, bg: str, fg: str, hover_bg: str,
                 font: tuple, y_offset: int = 0, command: Callable = None, **kwargs):
        super().__init__(parent, bg=bg, highlightthickness=0, cursor='hand2', **kwargs)
        
        self.text = text
        self.bg = bg
        self.fg = fg
        self.hover_bg = hover_bg
        self.font = font
        self.y_offset = y_offset  # Negative = up, Positive = down
        self.command = command
        self.text_id = None
        
        self.bind('<Configure>', self._on_configure)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)
    
    def _on_configure(self, event):
        """Redraw when size changes"""
        self.after_idle(self._draw)
    
    def _draw(self):
        """Draw text at center with y offset"""
        self.delete('all')
        w = self.winfo_width()
        h = self.winfo_height()
        if w > 1 and h > 1:
            # Draw text with y offset (negative moves up)
            self.text_id = self.create_text(
                w // 2, 
                h // 2 + self.y_offset,
                text=self.text, 
                fill=self.fg, 
                font=self.font,
                anchor='center'
            )
    
    def _on_enter(self, event):
        self.config(bg=self.hover_bg)
        self._draw()
    
    def _on_leave(self, event):
        self.config(bg=self.bg)
        self._draw()
    
    def _on_click(self, event):
        if self.command:
            self.command()


class KeypadPanel(tk.Frame):
    """Calculator keypad"""
    
    def __init__(self, parent, on_button_click: Callable[[str], None], **kwargs):
        super().__init__(parent, bg=Styles.COLORS['bg_primary'], **kwargs)
        
        self.on_button_click = on_button_click
        self.buttons: Dict[str, CanvasButton] = {}
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create keypad buttons using grid layout"""
        for i in range(4):
            self.columnconfigure(i, weight=1, uniform='btn')
        
        # (display_text, internal_key, btn_type)
        rows = [
            [('sin', 'sin', 'scientific'), ('cos', 'cos', 'scientific'), ('tan', 'tan', 'scientific'), ('DEG', 'DEG', 'mode')],
            [('log', 'log', 'scientific'), ('ln', 'ln', 'scientific'), ('x²', 'x²', 'scientific'), ('^', '^', 'scientific')],
            [('(', '(', 'scientific'), (')', ')', 'scientific'), ('π', 'π', 'scientific'), ('e', 'e', 'scientific')],
            [('C', 'C', 'clear'), ('√', '√', 'scientific'), ('%', '%', 'scientific'), ('÷', '÷', 'operator')],
            [('7', '7', 'number'), ('8', '8', 'number'), ('9', '9', 'number'), ('×', '×', 'operator')],
            [('4', '4', 'number'), ('5', '5', 'number'), ('6', '6', 'number'), ('−', '−', 'operator')],
            [('1', '1', 'number'), ('2', '2', 'number'), ('3', '3', 'number'), ('+', '+', 'operator')],
            [('±', '±', 'scientific'), ('0', '0', 'number'), ('.', '.', 'number'), ('=', '=', 'equals')],
        ]
        
        for row_idx, row in enumerate(rows):
            self.rowconfigure(row_idx, weight=1, uniform='btn')
            for col_idx, (display, key, btn_type) in enumerate(row):
                self._create_button(display, key, btn_type, row_idx, col_idx)
    
    def _create_button(self, display: str, key: str, btn_type: str, row: int, col: int):
        """Create a single button"""
        style = Styles.BUTTON_STYLES.get(btn_type, Styles.BUTTON_STYLES['number'])
        
        y_offset = 0
        
        btn = CanvasButton(
            self,
            text=display,
            bg=style['bg'],
            fg=style['fg'],
            hover_bg=style['hover_bg'],
            font=style['font'],
            y_offset=y_offset,
            command=lambda k=key: self.on_button_click(k)
        )
        btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
        
        self.buttons[key] = btn
    
    def update_mode_button(self, mode: str):
        """Update DEG/RAD button text"""
        if 'DEG' in self.buttons:
            self.buttons['DEG'].text = mode
            self.buttons['DEG']._draw()
    
    def set_second_mode(self, is_second: bool):
        pass
