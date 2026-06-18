#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI Styles and Theme Configuration
"""


class Styles:
    """Centralized style configuration for the calculator UI"""
    
    # Color Palette - Modern Dark
    COLORS = {
        'bg_primary': '#1a1a1a',
        'bg_secondary': '#252525',
        'bg_card': '#2d2d2d',
        'bg_elevated': '#3a3a3a',
        'accent_primary': '#bb86fc',
        'accent_secondary': '#03dac6',
        'accent_green': '#4caf50',
        'accent_orange': '#ff9800',
        'accent_red': '#f44336',
        'text_primary': '#ffffff',
        'text_secondary': '#b0b0b0',
        'text_muted': '#707070',
        'btn_number': '#2d2d2d',
        'btn_number_hover': '#3d3d3d',
        'btn_operator': '#bb86fc',
        'btn_operator_hover': '#d4a5ff',
        'btn_scientific': '#252525',
        'btn_scientific_hover': '#353535',
        'btn_clear': '#ff6b6b',
        'btn_clear_hover': '#ff8a8a',
        'btn_equals': '#4caf50',
        'btn_equals_hover': '#66bb6a',
        'display_bg': '#121212',
        'history_bg': '#1a1a1a',
        'border': '#3a3a3a',
        'success': '#4caf50',
        'error': '#f44336',
    }
    
    # Font Configuration
    FONTS = {
        'display_large': ('Consolas', 42, 'bold'),
        'display_small': ('Consolas', 14),
        'button_large': ('Segoe UI', 20),
        'button_medium': ('Segoe UI', 15),
        'button_small': ('Segoe UI', 11),
        'history': ('Consolas', 11),
        'label': ('Segoe UI', 10),
    }
    
    # Dimensions
    DIMENSIONS = {
        'window_width': 380,
        'window_height': 700,
        'history_height': 100,
    }
    
    # Button Categories
    BUTTON_STYLES = {
        'number': {
            'bg': COLORS['btn_number'],
            'fg': COLORS['text_primary'],
            'hover_bg': COLORS['btn_number_hover'],
            'font': ('Segoe UI', 22),
        },
        'operator': {
            'bg': COLORS['btn_operator'],
            'fg': '#1a1a1a',
            'hover_bg': COLORS['btn_operator_hover'],
            'font': ('Segoe UI', 24),
        },
        'scientific': {
            'bg': COLORS['btn_scientific'],
            'fg': COLORS['accent_secondary'],
            'hover_bg': COLORS['btn_scientific_hover'],
            'font': ('Segoe UI', 14),
        },
        'clear': {
            'bg': COLORS['btn_clear'],
            'fg': '#ffffff',
            'hover_bg': COLORS['btn_clear_hover'],
            'font': ('Segoe UI', 20),
        },
        'equals': {
            'bg': COLORS['btn_equals'],
            'fg': '#ffffff',
            'hover_bg': COLORS['btn_equals_hover'],
            'font': ('Segoe UI', 24),
        },
        'mode': {
            'bg': COLORS['accent_secondary'],
            'fg': '#1a1a1a',
            'hover_bg': '#5fd4c4',
            'font': ('Segoe UI', 12),
        },
    }
