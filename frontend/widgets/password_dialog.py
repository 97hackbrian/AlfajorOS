#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diálogo de contraseña con teclado virtual integrado.
Reemplaza QInputDialog para uso en pantalla táctil.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from frontend.widgets.virtual_keyboard import VirtualKeyboard


class PasswordDialog(QDialog):
    """Diálogo de contraseña con teclado virtual integrado."""

    def __init__(self, titulo="Contraseña", mensaje="Ingrese contraseña:", parent=None):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.setFixedSize(1024, 600)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self._resultado = ""
        self._aceptado = False
        self._setup_ui(titulo, mensaje)
        self._aplicar_estilo()

    def _setup_ui(self, titulo, mensaje):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 10)
        layout.setSpacing(10)

        # Título
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setFont(QFont("Purisa", 20, QFont.Bold))
        lbl_titulo.setStyleSheet("color: #FFAB40;")
        layout.addWidget(lbl_titulo)

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #4DB6AC;")
        layout.addWidget(sep)

        # Mensaje
        lbl_msg = QLabel(mensaje)
        lbl_msg.setAlignment(Qt.AlignCenter)
        lbl_msg.setFont(QFont("Purisa", 14))
        lbl_msg.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(lbl_msg)

        # Campo de contraseña
        self.input_field = QLineEdit()
        self.input_field.setEchoMode(QLineEdit.Password)
        self.input_field.setMinimumHeight(50)
        self.input_field.setFont(QFont("Purisa", 18))
        self.input_field.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.input_field)

        # Botones
        h_btns = QHBoxLayout()
        h_btns.setSpacing(20)

        btn_cancelar = QPushButton("CANCELAR")
        btn_cancelar.setMinimumHeight(50)
        btn_cancelar.setFont(QFont("Purisa", 13, QFont.Bold))
        btn_cancelar.setObjectName("btn_cancelar")
        btn_cancelar.clicked.connect(self._on_cancelar)
        h_btns.addWidget(btn_cancelar)

        btn_aceptar = QPushButton("ACEPTAR")
        btn_aceptar.setMinimumHeight(50)
        btn_aceptar.setFont(QFont("Purisa", 13, QFont.Bold))
        btn_aceptar.setObjectName("btn_aceptar")
        btn_aceptar.clicked.connect(self._on_aceptar)
        h_btns.addWidget(btn_aceptar)

        layout.addLayout(h_btns)

        # Teclado virtual
        self.keyboard = VirtualKeyboard()
        self.keyboard.set_target(self.input_field)
        layout.addWidget(self.keyboard)

    def _aplicar_estilo(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border: 2px solid #4DB6AC;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton#btn_aceptar {
                background-color: #4DB6AC;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton#btn_aceptar:pressed {
                background-color: #3d9e95;
            }
            QPushButton#btn_cancelar {
                background-color: #F66151;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton#btn_cancelar:pressed {
                background-color: #d44a3a;
            }
        """)

    def _on_aceptar(self):
        self._resultado = self.input_field.text()
        self._aceptado = True
        self.accept()

    def _on_cancelar(self):
        self._aceptado = False
        self.reject()

    def get_password(self):
        """Muestra el diálogo y retorna (password, ok)."""
        self.input_field.clear()
        self.exec()
        return self._resultado, self._aceptado
