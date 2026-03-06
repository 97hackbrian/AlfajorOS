#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Login View - Proyecto de Grado
Pantalla de inicio con animación de bienvenida.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor, QPainter, QLinearGradient

from backend.config import SystemConfig


class LoginWindow(QWidget):
    """Pantalla de login/inicio."""

    login_exitoso = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AlfajorOS - Inicio")
        self.setFixedSize(SystemConfig.SCREEN_WIDTH, SystemConfig.SCREEN_HEIGHT)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self._setup_ui()
        self._aplicar_estilo()

        # Animación de fade-in
        self.setWindowOpacity(0.0)
        self._anim = QPropertyAnimation(self, b"windowOpacity")
        self._anim.setDuration(800)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(15)

        layout.addStretch(2)

        # Logo / Título
        lbl_titulo = QLabel("🍪 AlfajorOS")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setFont(QFont("Purisa", 42, QFont.Bold))
        lbl_titulo.setStyleSheet(f"color: {SystemConfig.COLOR_PRIMARIO};")
        layout.addWidget(lbl_titulo)

        # Subtítulo
        lbl_sub = QLabel("Extrusora de Crema para Alfajores")
        lbl_sub.setAlignment(Qt.AlignCenter)
        lbl_sub.setFont(QFont("Purisa", 16))
        lbl_sub.setStyleSheet(f"color: {SystemConfig.COLOR_TEXTO};")
        layout.addWidget(lbl_sub)

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {SystemConfig.COLOR_PRIMARIO};")
        sep.setMaximumWidth(400)
        h_sep = QHBoxLayout()
        h_sep.addStretch()
        h_sep.addWidget(sep)
        h_sep.addStretch()
        layout.addLayout(h_sep)

        layout.addStretch(1)

        # Versión
        lbl_version = QLabel("Proyecto de Grado — v2.0")
        lbl_version.setAlignment(Qt.AlignCenter)
        lbl_version.setFont(QFont("Purisa", 11))
        lbl_version.setStyleSheet("color: #888;")
        layout.addWidget(lbl_version)

        layout.addStretch(1)

        # Botón INICIAR
        self.btn_login = QPushButton("INICIAR")
        self.btn_login.setMinimumHeight(80)
        self.btn_login.setFont(QFont("Purisa", 20, QFont.Bold))
        self.btn_login.clicked.connect(self._on_iniciar)
        layout.addWidget(self.btn_login)

        layout.addStretch(2)

    def _aplicar_estilo(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {SystemConfig.COLOR_FONDO};
            }}
            QPushButton {{
                background-color: {SystemConfig.COLOR_PRIMARIO};
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
            }}
            QPushButton:pressed {{
                background-color: #3d9e95;
            }}
        """)

    def _on_iniciar(self):
        self.login_exitoso.emit("usuario")

    def showEvent(self, event):
        super().showEvent(event)
        self._anim.start()

    def paintEvent(self, event):
        """Fondo con gradiente."""
        painter = QPainter(self)
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0.0, QColor(43, 43, 43))
        grad.setColorAt(0.5, QColor(35, 40, 45))
        grad.setColorAt(1.0, QColor(30, 30, 30))
        painter.fillRect(self.rect(), grad)
        painter.end()
