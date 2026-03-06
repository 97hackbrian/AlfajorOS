#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protector de Pantalla - Proyecto de Grado
Se activa tras un periodo de inactividad del usuario.
Muestra una animación de partículas flotantes y el reloj.
No se activa durante el proceso de impresión.
"""

import math
import random
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from PySide6.QtGui import (
    QPainter, QColor, QFont, QPen, QBrush,
    QLinearGradient, QRadialGradient
)
from datetime import datetime


class Particula:
    """Una partícula flotante para el protector de pantalla."""

    def __init__(self, ancho, alto):
        self.x = random.uniform(0, ancho)
        self.y = random.uniform(0, alto)
        self.radio = random.uniform(2, 8)
        self.velocidad_x = random.uniform(-0.8, 0.8)
        self.velocidad_y = random.uniform(-0.8, 0.8)
        self.color = QColor(
            random.randint(50, 130),
            random.randint(150, 220),
            random.randint(150, 200),
            random.randint(80, 180)
        )
        self.fase = random.uniform(0, 2 * math.pi)
        self.ancho_limite = ancho
        self.alto_limite = alto

    def actualizar(self, tiempo):
        """Actualiza la posición de la partícula."""
        self.x += self.velocidad_x + math.sin(tiempo + self.fase) * 0.3
        self.y += self.velocidad_y + math.cos(tiempo + self.fase) * 0.3

        # Rebote en bordes
        if self.x < 0:
            self.x = self.ancho_limite
        elif self.x > self.ancho_limite:
            self.x = 0
        if self.y < 0:
            self.y = self.alto_limite
        elif self.y > self.alto_limite:
            self.y = 0


class ScreensaverWindow(QWidget):
    """Protector de pantalla con animación de partículas y reloj."""

    def __init__(self, timeout_seconds=60, parent=None):
        super().__init__(parent)
        self.timeout_ms = timeout_seconds * 1000
        self.tiempo = 0.0
        self.bloqueado = False  # Si True, no se activa (ej: durante impresión)

        # Configuración de ventana - máxima prioridad de z-order
        self.setWindowTitle("Protector de Pantalla")
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.X11BypassWindowManagerHint  # Asegura que esté por encima de todo en Linux
        )

        # Partículas
        self.particulas = []
        self.num_particulas = 60

        # Timer de animación (30 FPS)
        self.timer_animacion = QTimer(self)
        self.timer_animacion.timeout.connect(self._actualizar_animacion)

        # Timer de inactividad
        self.timer_inactividad = QTimer(self)
        self.timer_inactividad.setSingleShot(True)
        self.timer_inactividad.timeout.connect(self.activar)

        # Texto flotante
        self.texto_y_offset = 0.0
        self.mensaje = "Extrusora de Crema para Alfajores"

    def _inicializar_particulas(self):
        """Crea las partículas iniciales."""
        self.particulas = [
            Particula(self.width(), self.height())
            for _ in range(self.num_particulas)
        ]

    def activar(self):
        """Activa el protector de pantalla."""
        # No activar si está bloqueado (durante impresión)
        if self.bloqueado:
            return

        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.geometry()
            self.setGeometry(geo)

        self._inicializar_particulas()
        self.tiempo = 0.0
        self.showFullScreen()
        self.raise_()
        self.activateWindow()
        self.timer_animacion.start(33)  # ~30 FPS

    def desactivar(self):
        """Desactiva el protector de pantalla."""
        self.timer_animacion.stop()
        self.hide()
        if not self.bloqueado:
            self.reiniciar_timer_inactividad()

    def reiniciar_timer_inactividad(self):
        """Reinicia el timer de inactividad."""
        if self.bloqueado:
            return
        self.timer_inactividad.stop()
        self.timer_inactividad.start(self.timeout_ms)

    def detener_timer_inactividad(self):
        """Detiene el timer de inactividad."""
        self.timer_inactividad.stop()

    def bloquear(self):
        """Bloquea el screensaver (no se activará)."""
        self.bloqueado = True
        self.timer_inactividad.stop()
        # Si está activo, desactivar
        if self.timer_animacion.isActive():
            self.timer_animacion.stop()
            self.hide()

    def desbloquear(self):
        """Desbloquea el screensaver y reinicia timer."""
        self.bloqueado = False
        self.reiniciar_timer_inactividad()

    def _actualizar_animacion(self):
        """Actualiza el estado de la animación."""
        self.tiempo += 0.03
        for p in self.particulas:
            p.actualizar(self.tiempo)

        # Asegurar que se mantenga al frente
        self.raise_()
        self.update()

    def paintEvent(self, event):
        """Dibuja el protector de pantalla."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()

        # === Fondo degradado ===
        gradiente = QLinearGradient(0, 0, 0, h)
        gradiente.setColorAt(0.0, QColor(15, 15, 30))
        gradiente.setColorAt(0.5, QColor(20, 30, 50))
        gradiente.setColorAt(1.0, QColor(10, 10, 25))
        painter.fillRect(0, 0, w, h, gradiente)

        # === Dibujar partículas ===
        for p in self.particulas:
            # Brillo pulsante
            brillo = 0.6 + 0.4 * math.sin(self.tiempo * 2 + p.fase)
            color = QColor(p.color)
            color.setAlphaF(color.alphaF() * brillo)

            # Halo
            halo = QRadialGradient(p.x, p.y, p.radio * 3)
            halo.setColorAt(0, QColor(color.red(), color.green(), color.blue(), 40))
            halo.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
            painter.setBrush(QBrush(halo))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(p.x, p.y), p.radio * 3, p.radio * 3)

            # Partícula
            painter.setBrush(QBrush(color))
            painter.drawEllipse(QPointF(p.x, p.y), p.radio, p.radio)

        # === Dibujar líneas entre partículas cercanas ===
        for i, p1 in enumerate(self.particulas):
            for p2 in self.particulas[i + 1:]:
                dist = math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
                if dist < 120:
                    alpha = int(60 * (1 - dist / 120))
                    painter.setPen(QPen(QColor(77, 182, 172, alpha), 1))
                    painter.drawLine(QPointF(p1.x, p1.y), QPointF(p2.x, p2.y))

        # === Reloj ===
        ahora = datetime.now()
        hora_texto = ahora.strftime("%H:%M:%S")
        fecha_texto = ahora.strftime("%d / %m / %Y")

        # Hora
        painter.setPen(QPen(QColor(77, 182, 172, 220)))
        painter.setFont(QFont("Purisa", 72, QFont.Bold))
        rect_hora = QRectF(0, h * 0.28, w, 90)
        painter.drawText(rect_hora, Qt.AlignCenter, hora_texto)

        # Fecha
        painter.setPen(QPen(QColor(200, 200, 200, 150)))
        painter.setFont(QFont("Purisa", 22))
        rect_fecha = QRectF(0, h * 0.28 + 95, w, 40)
        painter.drawText(rect_fecha, Qt.AlignCenter, fecha_texto)

        # === Mensaje flotante ===
        y_msg = h * 0.72 + math.sin(self.tiempo * 0.5) * 15
        painter.setPen(QPen(QColor(255, 171, 64, 150)))
        painter.setFont(QFont("Purisa", 16, QFont.Bold, italic=True))
        rect_msg = QRectF(0, y_msg, w, 35)
        painter.drawText(rect_msg, Qt.AlignCenter, self.mensaje)

        # === Instrucción ===
        alpha_parpadeo = int(120 + 80 * math.sin(self.tiempo * 3))
        painter.setPen(QPen(QColor(150, 150, 150, alpha_parpadeo)))
        painter.setFont(QFont("", 13))
        rect_inst = QRectF(0, h - 50, w, 35)
        painter.drawText(rect_inst, Qt.AlignCenter,
                         "Presione cualquier tecla o mueva el mouse para continuar")

        painter.end()

    def keyPressEvent(self, event):
        """Cualquier tecla desactiva el protector."""
        self.desactivar()

    def mousePressEvent(self, event):
        """Click del mouse desactiva el protector."""
        self.desactivar()

    def mouseMoveEvent(self, event):
        """Movimiento del mouse desactiva el protector."""
        self.desactivar()
