#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ventana de Ejemplo/Confirmación - Proyecto de Grado
Carga EJEMPLO_1.ui como ventana de confirmación.
"""

import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ExampleWindow(QMainWindow):
    """Ventana de ejemplo/confirmación (EJEMPLO_1.ui)."""

    confirmado = pyqtSignal(bool)  # True = SI, False = NO
    actividad_detectada = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(BASE_DIR, "EJEMPLO_1.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Confirmación")
        self._conectar_botones()

    def _conectar_botones(self):
        """Conecta los botones SI y NO."""
        # pushButton_2 = "SI}"
        self.pushButton_2.clicked.connect(self._on_si)
        self.pushButton_2.setText("SÍ")  # Corregir texto

        # pushButton = "NO"
        self.pushButton.clicked.connect(self._on_no)

    def set_pregunta(self, titulo, pregunta, detalle=""):
        """Configura la pregunta de confirmación."""
        self.label.setText(titulo)
        self.label_2.setText(pregunta)
        self.label_3.setText(detalle)

    def _on_si(self):
        """El usuario confirmó."""
        self.actividad_detectada.emit()
        self.confirmado.emit(True)
        self.hide()

    def _on_no(self):
        """El usuario rechazó."""
        self.actividad_detectada.emit()
        self.confirmado.emit(False)
        self.hide()

    def showEvent(self, event):
        self.actividad_detectada.emit()
        super().showEvent(event)
