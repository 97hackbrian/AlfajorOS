#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teclado Virtual - Proyecto de Grado
Teclado en pantalla para uso con pantalla táctil.
Se muestra automáticamente cuando un campo de texto recibe foco.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class VirtualKeyboard(QWidget):
    """Teclado virtual en pantalla para pantalla táctil."""

    tecla_presionada = Signal(str)
    borrar_presionado = Signal()
    enter_presionado = Signal()

    # Layout QWERTY en español
    FILAS_MINUSCULAS = [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ñ"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "-"],
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mayusculas = False
        self._target_widget = None
        self._setup_ui()
        self._aplicar_estilo()

    def _setup_ui(self):
        """Configura el layout del teclado."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(4)

        # Separador superior
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #4DB6AC;")
        layout.addWidget(sep)

        # Filas de teclas
        self._botones_teclas = []
        for fila in self.FILAS_MINUSCULAS:
            h_layout = QHBoxLayout()
            h_layout.setSpacing(4)
            fila_botones = []
            for tecla in fila:
                btn = QPushButton(tecla)
                btn.setMinimumSize(70, 48)
                btn.setMaximumHeight(52)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                btn.setFont(QFont("Purisa", 13, QFont.Bold))
                btn.clicked.connect(lambda checked, t=tecla: self._on_tecla(t))
                h_layout.addWidget(btn)
                fila_botones.append(btn)
            self._botones_teclas.append(fila_botones)
            layout.addLayout(h_layout)

        # Fila inferior: Mayus, Espacio, Borrar
        h_bottom = QHBoxLayout()
        h_bottom.setSpacing(4)

        # Mayúsculas
        btn_mayus = QPushButton("⬆ MAY")
        btn_mayus.setMinimumSize(100, 48)
        btn_mayus.setMaximumHeight(52)
        btn_mayus.setFont(QFont("Purisa", 11, QFont.Bold))
        btn_mayus.setCheckable(True)
        btn_mayus.clicked.connect(self._on_mayusculas)
        self._btn_mayus = btn_mayus
        h_bottom.addWidget(btn_mayus)

        # Espacio
        btn_espacio = QPushButton("ESPACIO")
        btn_espacio.setMinimumSize(300, 48)
        btn_espacio.setMaximumHeight(52)
        btn_espacio.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn_espacio.setFont(QFont("Purisa", 12, QFont.Bold))
        btn_espacio.clicked.connect(lambda: self._on_tecla(" "))
        h_bottom.addWidget(btn_espacio)

        # Borrar
        btn_borrar = QPushButton("⌫ BORRAR")
        btn_borrar.setMinimumSize(120, 48)
        btn_borrar.setMaximumHeight(52)
        btn_borrar.setFont(QFont("Purisa", 11, QFont.Bold))
        btn_borrar.setObjectName("btn_borrar")
        btn_borrar.clicked.connect(self._on_borrar)
        h_bottom.addWidget(btn_borrar)

        layout.addLayout(h_bottom)

    def _aplicar_estilo(self):
        """Estilo del teclado consistente con el tema oscuro."""
        self.setStyleSheet("""
            VirtualKeyboard {
                background-color: #1e1e1e;
                border-top: 2px solid #4DB6AC;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border: 1px solid #555;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:pressed {
                background-color: #4DB6AC;
                color: white;
            }
            QPushButton:checked {
                background-color: #FFAB40;
                color: white;
            }
            QPushButton#btn_borrar {
                background-color: #F66151;
                color: white;
            }
            QPushButton#btn_borrar:pressed {
                background-color: #d44a3a;
            }
        """)

    def _on_tecla(self, tecla):
        """Se presionó una tecla."""
        if self.mayusculas:
            tecla = tecla.upper()
        else:
            tecla = tecla.lower()

        self.tecla_presionada.emit(tecla)

        # Insertar en widget target
        if self._target_widget is not None:
            if hasattr(self._target_widget, 'insert'):
                # QLineEdit
                self._target_widget.insert(tecla)
            elif hasattr(self._target_widget, 'insertPlainText'):
                # QTextEdit
                self._target_widget.insertPlainText(tecla)

    def _on_borrar(self):
        """Se presionó borrar."""
        self.borrar_presionado.emit()

        if self._target_widget is not None:
            if hasattr(self._target_widget, 'backspace'):
                # QLineEdit
                self._target_widget.backspace()
            elif hasattr(self._target_widget, 'textCursor'):
                # QTextEdit
                cursor = self._target_widget.textCursor()
                cursor.deletePreviousChar()
                self._target_widget.setTextCursor(cursor)

    def _on_mayusculas(self, checked):
        """Toggle mayúsculas."""
        self.mayusculas = checked
        for fila in self._botones_teclas:
            for btn in fila:
                texto = btn.text()
                if checked:
                    btn.setText(texto.upper())
                else:
                    btn.setText(texto.upper())  # Mantener labels en mayúscula visual

    def set_target(self, widget):
        """Conecta el teclado a un widget de texto."""
        self._target_widget = widget
