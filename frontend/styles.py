#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estilos globales - Proyecto de Grado
Define la stylesheet global de la aplicación.
"""

from backend.config import SystemConfig


def get_global_stylesheet():
    """Retorna el stylesheet global de la aplicación."""
    return f"""
        QMainWindow {{
            background-color: {SystemConfig.COLOR_FONDO};
        }}
        QWidget {{
            background-color: {SystemConfig.COLOR_FONDO};
        }}
        QStatusBar {{
            background-color: {SystemConfig.COLOR_FONDO_OSCURO};
            color: {SystemConfig.COLOR_PRIMARIO};
            font-family: Purisa;
            font-size: 16px;
            padding: 6px;
        }}
        QMenuBar {{
            background-color: {SystemConfig.COLOR_FONDO_OSCURO};
            color: {SystemConfig.COLOR_TEXTO};
            max-height: 0px;
        }}
        QMessageBox {{
            background-color: {SystemConfig.COLOR_FONDO};
        }}
        QMessageBox QLabel {{
            color: {SystemConfig.COLOR_TEXTO};
            font-family: Purisa;
            font-size: 14px;
        }}
        QMessageBox QPushButton {{
            min-width: 120px;
            min-height: 45px;
            font-family: Purisa;
            font-size: 13px;
            font-weight: bold;
            background-color: {SystemConfig.COLOR_PRIMARIO};
            color: white;
            border: none;
            border-radius: 8px;
        }}
        QMessageBox QPushButton:pressed {{
            background-color: #3d9e95;
        }}
        QScrollBar:vertical {{
            background: {SystemConfig.COLOR_FONDO};
            width: 14px;
            border-radius: 7px;
        }}
        QScrollBar::handle:vertical {{
            background: {SystemConfig.COLOR_PRIMARIO};
            border-radius: 7px;
            min-height: 30px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
    """
