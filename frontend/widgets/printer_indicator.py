#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Indicador de conexión de impresora - Proyecto de Grado
Widget visual que muestra el estado de conexión serial con la impresora.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPainter, QColor, QBrush, QPen


class PrinterIndicator(QWidget):
    """
    Indicador visual del estado de conexión de la impresora.
    - Verde pulsante: conectada y lista
    - Rojo: desconectada
    - Amarillo: escaneando/conectando
    """

    COLORS = {
        "disconnected": QColor(244, 67, 54),     # Rojo
        "scanning":     QColor(255, 193, 7),      # Amarillo
        "connecting":   QColor(255, 152, 0),      # Naranja
        "connected":    QColor(76, 175, 80),       # Verde
        "busy":         QColor(33, 150, 243),      # Azul
        "error":        QColor(244, 67, 54),       # Rojo
    }

    LABELS = {
        "disconnected": "⚠ Desconectada",
        "scanning":     "🔍 Escaneando...",
        "connecting":   "🔌 Conectando...",
        "connected":    "✓ Lista",
        "busy":         "⏳ Enviando...",
        "error":        "✗ Error",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = "disconnected"
        self._port_info = ""
        self._pulse_alpha = 255
        self._pulse_dir = -5

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setSpacing(6)

        # Indicador LED (se dibuja con paintEvent)
        self._led = _LedWidget(self)
        self._led.setFixedSize(18, 18)
        layout.addWidget(self._led)

        # Etiqueta de estado
        self._label = QLabel("⚠ Desconectada")
        self._label.setFont(QFont("Purisa", 9))
        self._label.setStyleSheet("color: #F44336;")
        layout.addWidget(self._label)

        self.setFixedHeight(26)

        # Timer de pulso para LED conectado
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._pulse_tick)
        self._pulse_timer.start(60)

    def set_state(self, state_str):
        """Actualiza el estado visual del indicador."""
        self._state = state_str
        color = self.COLORS.get(state_str, self.COLORS["disconnected"])
        label = self.LABELS.get(state_str, state_str)

        if self._port_info and state_str == "connected":
            label = f"✓ {self._port_info}"

        self._label.setText(label)
        self._label.setStyleSheet(f"color: {color.name()};")
        self._led.set_color(color)
        self._led.update()

    def set_port_info(self, info):
        """Muestra info del puerto."""
        self._port_info = info
        if self._state == "connected":
            self._label.setText(f"✓ {info}")

    def _pulse_tick(self):
        """Animación de pulso para el LED cuando está conectado."""
        if self._state in ("connected", "busy"):
            self._pulse_alpha += self._pulse_dir
            if self._pulse_alpha <= 120:
                self._pulse_dir = 5
            elif self._pulse_alpha >= 255:
                self._pulse_dir = -5
            self._led.set_alpha(self._pulse_alpha)
            self._led.update()
        else:
            self._led.set_alpha(255)


class _LedWidget(QWidget):
    """Widget de LED circular pintado."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._color = QColor(244, 67, 54)
        self._alpha = 255
        self.setAttribute(Qt.WA_TranslucentBackground)

    def set_color(self, color):
        self._color = QColor(color)

    def set_alpha(self, alpha):
        self._alpha = max(0, min(255, alpha))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        radius = min(w, h) / 2 - 1

        c = QColor(self._color)
        c.setAlpha(self._alpha)

        # Brillo externo
        glow = QColor(c)
        glow.setAlpha(60)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(glow))
        painter.drawEllipse(w / 2 - radius, h / 2 - radius,
                           radius * 2, radius * 2)

        # LED principal
        painter.setBrush(QBrush(c))
        painter.setPen(QPen(c.darker(130), 1))
        inner_r = radius * 0.75
        painter.drawEllipse(w / 2 - inner_r, h / 2 - inner_r,
                           inner_r * 2, inner_r * 2)

        # Highlight
        highlight = QColor(255, 255, 255, 80)
        painter.setBrush(QBrush(highlight))
        painter.setPen(Qt.NoPen)
        hl_r = inner_r * 0.4
        painter.drawEllipse(w / 2 - hl_r * 0.5, h / 2 - inner_r * 0.5,
                           hl_r, hl_r)

        painter.end()
