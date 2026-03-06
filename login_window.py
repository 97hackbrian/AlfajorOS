#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ventana de Inicio - Proyecto de Grado
Pantalla de bienvenida para la extrusora de crema para alfajores.
El modo basico no requiere contrasena.
El modo PRO se protege con contrasena desde el panel principal.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class LoginWindow(QWidget):
    """Pantalla de inicio simple con boton de entrar."""

    login_exitoso = Signal(str)  # Emite "basico" al iniciar

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Extrusora de Crema - Proyecto de Grado")
        self.setFixedSize(1024, 600)
        self._setup_ui()
        self._aplicar_estilo()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(80, 40, 80, 40)
        layout.setSpacing(15)

        # Titulo
        lbl_titulo = QLabel("PROYECTO DE GRADO")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setFont(QFont("Purisa", 28, QFont.Bold))
        lbl_titulo.setStyleSheet("color: #4DB6AC;")
        layout.addWidget(lbl_titulo)

        # Subtitulo
        lbl_sub = QLabel("Extrusora de Crema para Alfajores")
        lbl_sub.setAlignment(Qt.AlignCenter)
        lbl_sub.setFont(QFont("Purisa", 16, italic=True))
        lbl_sub.setStyleSheet("color: #888;")
        layout.addWidget(lbl_sub)

        # Icono
        lbl_icono = QLabel("\U0001F370")
        lbl_icono.setAlignment(Qt.AlignCenter)
        lbl_icono.setFont(QFont("", 80))
        layout.addWidget(lbl_icono)

        layout.addSpacing(10)

        # Separador
        linea = QFrame()
        linea.setFrameShape(QFrame.HLine)
        linea.setStyleSheet("color: #4DB6AC;")
        layout.addWidget(linea)

        layout.addSpacing(10)

        # Info
        lbl_info = QLabel("Modo basico por defecto\nModo PRO protegido con contrasena")
        lbl_info.setAlignment(Qt.AlignCenter)
        lbl_info.setFont(QFont("Purisa", 12))
        lbl_info.setStyleSheet("color: #aaa;")
        layout.addWidget(lbl_info)

        layout.addSpacing(15)

        # Boton INICIAR
        self.btn_login = QPushButton("INICIAR")
        self.btn_login.setMinimumHeight(80)
        self.btn_login.setFont(QFont("Purisa", 20, QFont.Bold))
        self.btn_login.clicked.connect(self._on_iniciar)
        layout.addWidget(self.btn_login)

        layout.addStretch()

    def _aplicar_estilo(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #4DB6AC;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5cc4ba;
            }
            QPushButton:pressed {
                background-color: #3d9e95;
            }
        """)

    def _on_iniciar(self):
        self.login_exitoso.emit("basico")

    def reset(self):
        pass
