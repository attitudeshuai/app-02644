#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
History Panel Component - Collapsible (Chinese UI)
"""

import tkinter as tk
from typing import Callable, List, Tuple
from .styles import Styles


class HistoryPanel(tk.Frame):
    """Panel showing calculation history"""
    
    def __init__(self, parent, on_history_select: Callable[[str], None], **kwargs):
        super().__init__(parent, bg=Styles.COLORS['history_bg'], **kwargs)
        
        self.on_history_select = on_history_select
        self.history: List[Tuple[str, str]] = []
        self.is_collapsed = True
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create history panel widgets"""
        # Header
        self.header = tk.Frame(self, bg=Styles.COLORS['history_bg'], cursor='hand2')
        self.header.pack(fill=tk.X, padx=8, pady=4)
        
        self.arrow = tk.Label(
            self.header, text="▶", font=('Segoe UI', 9),
            fg=Styles.COLORS['text_muted'], bg=Styles.COLORS['history_bg']
        )
        self.arrow.pack(side=tk.LEFT)
        
        tk.Label(
            self.header, text="历史记录", font=Styles.FONTS['button_small'],
            fg=Styles.COLORS['text_secondary'], bg=Styles.COLORS['history_bg']
        ).pack(side=tk.LEFT, padx=4)
        
        self.count = tk.Label(
            self.header, text="", font=Styles.FONTS['label'],
            fg=Styles.COLORS['text_muted'], bg=Styles.COLORS['history_bg']
        )
        self.count.pack(side=tk.LEFT)
        
        clear = tk.Label(
            self.header, text="清除", font=Styles.FONTS['label'],
            fg=Styles.COLORS['accent_red'], bg=Styles.COLORS['history_bg'], cursor='hand2'
        )
        clear.pack(side=tk.RIGHT)
        clear.bind('<Button-1>', lambda e: self.clear_history())
        
        self.header.bind('<Button-1>', lambda e: self._toggle())
        self.arrow.bind('<Button-1>', lambda e: self._toggle())
        
        # Content
        self.content = tk.Frame(self, bg=Styles.COLORS['history_bg'])
        
        self.listbox = tk.Listbox(
            self.content, bg=Styles.COLORS['bg_secondary'],
            fg=Styles.COLORS['text_secondary'], font=Styles.FONTS['history'],
            selectbackground=Styles.COLORS['bg_elevated'],
            selectforeground=Styles.COLORS['accent_secondary'],
            height=5, bd=0, highlightthickness=0, activestyle='none'
        )
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)
    
    def _toggle(self):
        self.is_collapsed = not self.is_collapsed
        if self.is_collapsed:
            self.content.pack_forget()
            self.arrow.config(text="▶")
        else:
            self.content.pack(fill=tk.BOTH, expand=True)
            self.arrow.config(text="▼")
    
    def _on_select(self, event):
        sel = self.listbox.curselection()
        if sel:
            idx = sel[0]
            if idx < len(self.history):
                self.on_history_select(self.history[idx][1])
    
    def add_entry(self, expression: str, result: str):
        self.history.append((expression, result))
        self.listbox.insert(tk.END, f"{expression} = {result}")
        self.listbox.see(tk.END)
        self.count.config(text=f"({len(self.history)})")
    
    def clear_history(self):
        self.history.clear()
        self.listbox.delete(0, tk.END)
        self.count.config(text="")
