#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ventana de Selección de Producto - Proyecto de Grado
Carga ventana_3.ui para seleecionar tipo de producto.
"""

import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ProductSelectionWindow(QMainWindow):
    """Ventana de selección de producto (ventana_3.ui)."""

    producto_seleccionado = pyqtSignal(str)  # Emite "MACARRON" o "ALFAJOR"
    ir_atras = pyqtSignal()
    actividad_detectada = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(BASE_DIR, "ventana_3.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Selección de Producto")
        self._conectar_botones()

    def _conectar_botones(self):
        """Conecta los botones de selección de producto."""
        # pushButton = "MACARRON"
        self.pushButton.clicked.connect(lambda: self._seleccionar("MACARRON"))
        # pushButton_2 = "ALFAJOR"
        self.pushButton_2.clicked.connect(lambda: self._seleccionar("ALFAJOR"))

    def _seleccionar(self, producto):
        """Selecciona un producto y notifica."""
        self.actividad_detectada.emit()
        self.producto_seleccionado.emit(producto)
        self.statusbar.showMessage(f"Seleccionado: {producto}")
        QMessageBox.information(self, "Producto Seleccionado",
                                f"Has seleccionado: {producto}\n\n"
                                f"Volviendo al panel principal...")
        self.hide()

    def showEvent(self, event):
        self.actividad_detectada.emit()
        super().showEvent(event)

    def mousePressEvent(self, event):
        self.actividad_detectada.emit()
        super().mousePressEvent(event)
