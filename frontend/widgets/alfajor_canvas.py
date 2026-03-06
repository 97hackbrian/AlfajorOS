#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualización del Alfajor - Proyecto de Grado
Widget QPainter que renderiza el alfajor con crema en tiempo real.
Compatible con EGLFS (sin OpenGL).
"""

import math
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QPointF, QTimer
from PySide6.QtGui import (
    QPainter, QColor, QBrush, QPen, QFont,
    QRadialGradient, QLinearGradient, QPainterPath
)


class AlfajorCanvas(QWidget):
    """
    Widget que renderiza una vista superior del alfajor con crema.
    Muestra el alfajor, el patrón de crema progresivo y texto.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._progreso = 0          # 0-100 (progreso real de extrusión)
        self._patron = ""
        self._texto = ""
        self._grosor = 50           # % grosor crema
        self._animacion_t = 0.0     # Tiempo de animación
        self._printing = False      # True = modo impresión (progresivo)

        # Timer para animación sutil del alfajor
        self._timer_anim = QTimer(self)
        self._timer_anim.timeout.connect(self._tick_anim)
        self._timer_anim.start(50)

        self.setMinimumSize(300, 300)
        self.setStyleSheet("background-color: #1e1e1e; border: 2px solid #4DB6AC; border-radius: 10px;")

    @property
    def _render_progreso(self):
        """Progreso a usar para renderizado: 100 en preview, real durante impresión."""
        if self._printing:
            return self._progreso
        elif self._patron or self._texto:
            return 100  # Preview: mostrar todo
        else:
            return 0

    # === API pública ===

    def set_progreso(self, valor):
        """Configura el progreso de la extrusión (0-100)."""
        self._progreso = max(0, min(100, valor))
        self.update()

    def set_patron(self, patron):
        """Configura el patrón decorativo a dibujar."""
        self._patron = patron
        self.update()

    def set_texto(self, texto):
        """Configura el texto que se escribirá sobre la crema."""
        self._texto = texto
        self.update()

    def set_grosor(self, grosor):
        """Configura el grosor de la crema (10-100%)."""
        self._grosor = grosor
        self.update()

    def reset(self):
        """Resetea la visualización."""
        self._progreso = 0
        self._patron = ""
        self._texto = ""
        self._grosor = 50
        self._printing = False
        self.update()

    def start_animacion(self):
        """Cambia a modo impresión (progresivo)."""
        self._printing = True
        self._progreso = 0
        self.update()

    def stop_animacion(self):
        """Vuelve a modo preview (muestra todo)."""
        self._printing = False
        self.update()

    # === Dibujo ===

    def _tick_anim(self):
        self._animacion_t += 0.05
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        size = min(w, h) - 20
        cx, cy = w / 2, h / 2

        # Fondo
        self._dibujar_fondo(painter, w, h)

        # Base de la bandeja
        self._dibujar_bandeja(painter, cx, cy, size)

        # Alfajor
        radio_alfajor = size * 0.40
        self._dibujar_alfajor(painter, cx, cy, radio_alfajor)

        # Crema según patrón/preview
        rp = self._render_progreso
        if rp > 0 or self._patron:
            self._dibujar_crema(painter, cx, cy, radio_alfajor * 0.85, rp)

        # Texto sobre la crema
        if self._texto and rp > 60:
            self._dibujar_texto(painter, cx, cy, radio_alfajor * 0.5, rp)

        # Indicador de progreso en borde (solo durante impresión)
        if self._printing and self._progreso > 0 and self._progreso < 100:
            self._dibujar_indicador_progreso(painter, cx, cy, radio_alfajor + 25)

        # Label de estado
        self._dibujar_estado(painter, w, h)

        painter.end()

    def _dibujar_fondo(self, painter, w, h):
        """Fondo oscuro con gradiente sutil."""
        grad = QRadialGradient(w / 2, h / 2, max(w, h) / 2)
        grad.setColorAt(0.0, QColor(35, 35, 45))
        grad.setColorAt(1.0, QColor(20, 20, 28))
        painter.fillRect(0, 0, w, h, grad)

    def _dibujar_bandeja(self, painter, cx, cy, size):
        """Dibuja la bandeja/superficie de trabajo."""
        radio = size * 0.48
        # Sombra
        painter.setBrush(QBrush(QColor(10, 10, 15, 80)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(cx + 3, cy + 3), radio, radio)
        # Bandeja
        grad = QRadialGradient(cx - radio * 0.3, cy - radio * 0.3, radio * 1.5)
        grad.setColorAt(0.0, QColor(60, 62, 65))
        grad.setColorAt(0.7, QColor(45, 47, 50))
        grad.setColorAt(1.0, QColor(35, 37, 40))
        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(80, 82, 85), 2))
        painter.drawEllipse(QPointF(cx, cy), radio, radio)

    def _dibujar_alfajor(self, painter, cx, cy, radio):
        """Dibuja el alfajor (galleta) con textura realista."""
        # Sombra del alfajor
        painter.setBrush(QBrush(QColor(20, 15, 10, 100)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(cx + 2, cy + 2), radio, radio)

        # Galleta base - gradiente marrón dorado
        grad = QRadialGradient(cx - radio * 0.25, cy - radio * 0.25, radio * 1.2)
        grad.setColorAt(0.0, QColor(210, 170, 120))   # Dorado claro centro
        grad.setColorAt(0.4, QColor(190, 150, 100))   # Marrón medio
        grad.setColorAt(0.7, QColor(165, 130, 85))    # Marrón
        grad.setColorAt(1.0, QColor(140, 105, 65))    # Marrón oscuro borde
        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(120, 90, 55), 1.5))
        painter.drawEllipse(QPointF(cx, cy), radio, radio)

        # Textura: puntos aleatorios (estáticos, basados en posición)
        painter.setPen(Qt.NoPen)
        for i in range(40):
            angulo = (i * 137.5) * math.pi / 180  # Ángulo dorado
            r = radio * 0.15 + (i * radio * 0.8 / 40)
            px = cx + r * math.cos(angulo)
            py = cy + r * math.sin(angulo)
            dot_size = 1.5 + (i % 3) * 0.8
            alpha = 30 + (i % 4) * 10
            painter.setBrush(QBrush(QColor(130, 100, 60, alpha)))
            painter.drawEllipse(QPointF(px, py), dot_size, dot_size)

        # Borde elevado (3D)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(220, 185, 140, 60), 2))
        painter.drawEllipse(QPointF(cx, cy), radio - 3, radio - 3)

    def _dibujar_crema(self, painter, cx, cy, radio_max, progreso):
        """Dibuja la crema según el patrón y progreso."""
        grosor_linea = 2 + (self._grosor / 100) * 6
        color_crema = QColor(255, 245, 220, 220)
        pen = QPen(color_crema, grosor_linea, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        patron = self._patron.lower() if self._patron else "espiral"

        if "zigzag" in patron:
            self._dibujar_patron_zigzag(painter, cx, cy, radio_max, progreso)
        elif "circulo" in patron:
            self._dibujar_patron_circulos(painter, cx, cy, radio_max, progreso)
        elif "rejilla" in patron:
            self._dibujar_patron_rejilla(painter, cx, cy, radio_max, progreso)
        elif "relleno" in patron:
            self._dibujar_patron_relleno(painter, cx, cy, radio_max, progreso)
        elif "estrella" in patron:
            self._dibujar_patron_estrella(painter, cx, cy, radio_max, progreso)
        elif "corazon" in patron:
            self._dibujar_patron_corazon(painter, cx, cy, radio_max, progreso)
        elif "borde" in patron:
            self._dibujar_patron_borde(painter, cx, cy, radio_max, progreso)
        elif "ondas" in patron:
            self._dibujar_patron_ondas(painter, cx, cy, radio_max, progreso)
        else:
            self._dibujar_patron_espiral(painter, cx, cy, radio_max, progreso)

    def _dibujar_patron_espiral(self, painter, cx, cy, radio_max, progreso):
        """Patrón espiral desde el centro."""
        path = QPainterPath()
        total_steps = 200
        visible = int(total_steps * progreso / 100)
        vueltas = 5

        if visible < 2:
            return

        for i in range(visible):
            t = i / total_steps
            angulo = t * vueltas * 2 * math.pi
            r = t * radio_max
            x = cx + r * math.cos(angulo)
            y = cy + r * math.sin(angulo)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)

        painter.drawPath(path)

    def _dibujar_patron_zigzag(self, painter, cx, cy, radio_max, progreso):
        """Patrón zigzag horizontal."""
        lineas = 10
        visible_lineas = int(lineas * progreso / 100)
        margen = radio_max * 0.1

        for i in range(max(1, visible_lineas)):
            t = (i + 0.5) / lineas
            y = cy - radio_max + t * 2 * radio_max
            # Calcular intersección con círculo
            dy = abs(y - cy)
            if dy >= radio_max:
                continue
            dx = math.sqrt(radio_max ** 2 - dy ** 2)
            x1, x2 = cx - dx + margen, cx + dx - margen
            if i % 2 == 0:
                painter.drawLine(QPointF(x1, y), QPointF(x2, y))
            else:
                painter.drawLine(QPointF(x2, y), QPointF(x1, y))

    def _dibujar_patron_circulos(self, painter, cx, cy, radio_max, progreso):
        """Círculos concéntricos."""
        num_circulos = 6
        visible = int(num_circulos * progreso / 100)
        for i in range(1, max(2, visible + 1)):
            r = (i / num_circulos) * radio_max
            painter.drawEllipse(QPointF(cx, cy), r, r)

    def _dibujar_patron_rejilla(self, painter, cx, cy, radio_max, progreso):
        """Patrón de rejilla cruzada."""
        lineas = 8
        visible = int(lineas * progreso / 100)
        for i in range(max(1, visible)):
            t = (i + 0.5) / lineas
            pos = -radio_max + t * 2 * radio_max
            dy = abs(pos)
            if dy >= radio_max:
                continue
            dx = math.sqrt(radio_max ** 2 - dy ** 2)
            # Horizontal
            painter.drawLine(QPointF(cx - dx, cy + pos), QPointF(cx + dx, cy + pos))
            # Vertical
            painter.drawLine(QPointF(cx + pos, cy - dx), QPointF(cx + pos, cy + dx))

    def _dibujar_patron_relleno(self, painter, cx, cy, radio_max, progreso):
        """Relleno completo (espiral densa)."""
        path = QPainterPath()
        total_steps = 300
        visible = int(total_steps * progreso / 100)
        vueltas = 12

        if visible < 2:
            return

        for i in range(visible):
            t = i / total_steps
            angulo = t * vueltas * 2 * math.pi
            r = t * radio_max
            x = cx + r * math.cos(angulo)
            y = cy + r * math.sin(angulo)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)

        painter.drawPath(path)

    def _dibujar_patron_estrella(self, painter, cx, cy, radio_max, progreso):
        """Patrón de estrella."""
        puntas = 8
        visible = int(puntas * 2 * progreso / 100)
        path = QPainterPath()
        for i in range(max(1, visible)):
            angulo = (i * math.pi) / puntas
            if i % 2 == 0:
                r = radio_max
            else:
                r = radio_max * 0.4
            x = cx + r * math.cos(angulo - math.pi / 2)
            y = cy + r * math.sin(angulo - math.pi / 2)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        if visible > 2:
            path.closeSubpath()
        painter.drawPath(path)

    def _dibujar_patron_corazon(self, painter, cx, cy, radio_max, progreso):
        """Patrón de corazón."""
        path = QPainterPath()
        total_steps = 100
        visible = int(total_steps * progreso / 100)
        if visible < 2:
            return
        scale = radio_max / 17
        for i in range(visible):
            t = (i / total_steps) * 2 * math.pi
            x = 16 * math.sin(t) ** 3
            y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
            px = cx + x * scale
            py = cy + y * scale
            if i == 0:
                path.moveTo(px, py)
            else:
                path.lineTo(px, py)
        painter.drawPath(path)

    def _dibujar_patron_borde(self, painter, cx, cy, radio_max, progreso):
        """Borde decorativo circular."""
        angulo_visible = 360 * progreso / 100
        start = 90 * 16  # Qt usa 1/16 de grado
        span = -int(angulo_visible * 16)
        rect = QRectF(cx - radio_max, cy - radio_max, radio_max * 2, radio_max * 2)
        painter.drawArc(rect, start, span)
        # Borde interior
        r2 = radio_max * 0.7
        rect2 = QRectF(cx - r2, cy - r2, r2 * 2, r2 * 2)
        span2 = -int(angulo_visible * 0.8 * 16)
        painter.drawArc(rect2, start, span2)

    def _dibujar_patron_ondas(self, painter, cx, cy, radio_max, progreso):
        """Ondas paralelas."""
        lineas = 8
        visible = int(lineas * progreso / 100)
        for i in range(max(1, visible)):
            path = QPainterPath()
            t = (i + 0.5) / lineas
            y_base = cy - radio_max + t * 2 * radio_max
            dy = abs(y_base - cy)
            if dy >= radio_max:
                continue
            dx = math.sqrt(radio_max ** 2 - dy ** 2)
            steps = 40
            for j in range(steps):
                frac = j / (steps - 1)
                x = (cx - dx) + frac * 2 * dx
                y = y_base + math.sin(frac * 4 * math.pi) * 8
                if j == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
            painter.drawPath(path)

    def _dibujar_texto(self, painter, cx, cy, ancho_max, progreso):
        """Dibuja texto sobre la crema."""
        if not self._texto:
            return

        progress_texto = min(100, (progreso - 60) * 100 / 40)
        chars_visible = int(len(self._texto) * progress_texto / 100)
        texto_visible = self._texto[:max(1, chars_visible)]

        painter.setPen(QPen(QColor(180, 120, 60, 200), 1))
        font_size = max(10, int(ancho_max / max(len(self._texto), 1) * 1.2))
        font_size = min(font_size, 28)
        painter.setFont(QFont("Purisa", font_size, QFont.Bold))

        rect = QRectF(cx - ancho_max, cy - 20, ancho_max * 2, 40)
        painter.drawText(rect, Qt.AlignCenter, texto_visible)

    def _dibujar_indicador_progreso(self, painter, cx, cy, radio):
        """Dibuja indicador de progreso circular."""
        # Fondo
        painter.setPen(QPen(QColor(60, 60, 60, 100), 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), radio, radio)

        # Progreso
        color = QColor(77, 182, 172, 180)
        painter.setPen(QPen(color, 3, Qt.SolidLine, Qt.RoundCap))
        rect = QRectF(cx - radio, cy - radio, radio * 2, radio * 2)
        start = 90 * 16
        span = -int(self._progreso * 3.6 * 16)
        painter.drawArc(rect, start, span)

    def _dibujar_estado(self, painter, w, h):
        """Dibuja el estado actual en la esquina inferior."""
        if self._printing and self._progreso >= 100:
            texto = "✓ COMPLETADO"
            color = QColor(77, 182, 172, 200)
        elif self._printing and self._progreso > 0:
            texto = f"EXTRUYENDO... {self._progreso}%"
            color = QColor(255, 171, 64, 200)
        elif self._patron:
            texto = f"Vista previa: {self._patron}"
            color = QColor(150, 150, 150, 150)
        elif self._texto:
            texto = f"Vista previa: '{self._texto}'"
            color = QColor(150, 150, 150, 150)
        else:
            texto = "Listo para decorar"
            color = QColor(100, 100, 100, 120)

        painter.setPen(QPen(color))
        painter.setFont(QFont("Purisa", 10))
        rect = QRectF(0, h - 25, w, 20)
        painter.drawText(rect, Qt.AlignCenter, texto)
