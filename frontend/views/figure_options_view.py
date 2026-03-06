#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figure Options View - Proyecto de Grado
Ventana para seleccionar patrón decorativo de crema.
"""

import os
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QListView
)
from PySide6.QtCore import Qt, Signal, QStringListModel

from frontend.resources.ui_loader import load_ui
from backend.config import SystemConfig


class FigureOptionsView(QMainWindow):
    """Ventana para configurar patrón decorativo."""

    figura_configurada = Signal(str, int)  # (patrón, grosor)
    ir_atras = Signal()
    actividad_detectada = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        load_ui("ventana_4.ui", self)
        self.setWindowTitle("Opciones de Patrón")
        self._setup_lista_figuras()
        self._conectar_botones()

    def _setup_lista_figuras(self):
        """Configura la lista de patrones disponibles."""
        self.model = QStringListModel(SystemConfig.PATRONES)
        if hasattr(self, 'listView'):
            self.listView.setModel(self.model)

    def _conectar_botones(self):
        # pushButton = "ATRAS"
        self.pushButton.clicked.connect(self._on_atras)
        # pushButton_2 = "CONFIRMAR"
        self.pushButton_2.clicked.connect(self._on_confirmar)

    def _on_atras(self):
        self.actividad_detectada.emit()
        self.ir_atras.emit()
        self.hide()

    def _on_confirmar(self):
        self.actividad_detectada.emit()
        if hasattr(self, 'listView'):
            indices = self.listView.selectedIndexes()
            if not indices:
                QMessageBox.warning(self, "Advertencia",
                                    "Seleccione un patrón decorativo.")
                return
            patron = self.model.data(indices[0], Qt.DisplayRole)
        else:
            patron = "Espiral clasica"

        # Grosor del slider
        grosor = 50
        if hasattr(self, 'horizontalSlider'):
            grosor = self.horizontalSlider.value()

        self.figura_configurada.emit(patron, grosor)
        self.hide()

    def reset(self):
        if hasattr(self, 'listView'):
            self.listView.clearSelection()
        if hasattr(self, 'horizontalSlider'):
            self.horizontalSlider.setValue(50)

    def showEvent(self, event):
        self.actividad_detectada.emit()
        super().showEvent(event)

    def mousePressEvent(self, event):
        self.actividad_detectada.emit()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        self.actividad_detectada.emit()
        super().keyPressEvent(event)
