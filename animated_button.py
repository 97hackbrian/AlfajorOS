#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Botón con animación de pulso al presionar.
Efecto visual para pantalla táctil: escala brevemente al hacer click.
"""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import (
    QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup,
    Property, QObject
)
from PySide6.QtGui import QTransform


class PulseHelper(QObject):
    """Helper para animar la opacidad/escala de un botón existente."""

    def __init__(self, button):
        super().__init__(button)
        self._button = button
        self._scale = 1.0
        self._original_style = ""

        # Guardar estilo original
        self._original_style = button.styleSheet()

        # Animación de escala (simula con margins)
        self._anim_group = QSequentialAnimationGroup(self)

        # Fase 1: Encoger
        self._anim_shrink = QPropertyAnimation(self, b"scale")
        self._anim_shrink.setDuration(80)
        self._anim_shrink.setStartValue(1.0)
        self._anim_shrink.setEndValue(0.92)
        self._anim_shrink.setEasingCurve(QEasingCurve.OutQuad)

        # Fase 2: Volver
        self._anim_grow = QPropertyAnimation(self, b"scale")
        self._anim_grow.setDuration(120)
        self._anim_grow.setStartValue(0.92)
        self._anim_grow.setEndValue(1.0)
        self._anim_grow.setEasingCurve(QEasingCurve.OutBounce)

        self._anim_group.addAnimation(self._anim_shrink)
        self._anim_group.addAnimation(self._anim_grow)

        # Conectar al click
        button.pressed.connect(self._on_pressed)

    def _get_scale(self):
        return self._scale

    def _set_scale(self, value):
        self._scale = value
        t = QTransform()
        t.scale(value, value)
        self._button.setTransformationMode = None

        # Simular escala con margins interiores
        margin = int((1.0 - value) * 15)
        base = self._original_style
        extra = f"padding-top: {margin}px; padding-bottom: {margin}px;"
        self._button.setStyleSheet(base + extra)

    scale = Property(float, _get_scale, _set_scale)

    def _on_pressed(self):
        """Ejecuta la animación de pulso."""
        self._anim_group.stop()
        self._anim_group.start()


def aplicar_animacion_pulso(button):
    """
    Aplica la animación de pulso a un QPushButton existente.
    Retorna el helper para mantener la referencia.
    """
    helper = PulseHelper(button)
    # Guardar referencia en el botón para evitar garbage collection
    button._pulse_helper = helper
    return helper
