#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ventana de Opciones de Figura - Proyecto de Grado
Carga ventana_4.ui para seleccionar patrones decorativos y grosor de crema.
"""

import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal, QStringListModel
from PyQt5 import uic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class FigureOptionsWindow(QMainWindow):
    """Ventana de opciones de patron decorativo (ventana_4.ui)."""

    figura_configurada = pyqtSignal(str, int)  # (patron, grosor)
    ir_atras = pyqtSignal()
    ir_siguiente = pyqtSignal()
    actividad_detectada = pyqtSignal()

    FIGURAS = [
        "Espiral clasica",
        "Zigzag horizontal",
        "Circulos concentricos",
        "Rejilla cruzada",
        "Estrella",
        "Corazon",
        "Ondas paralelas",
        "Relleno completo",
        "Borde decorativo",
        "Texto + borde",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(BASE_DIR, "ventana_4.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Patron Decorativo")
        self._configurar_lista()
        self._conectar_botones()

    def _configurar_lista(self):
        """Configura la lista de patrones decorativos disponibles."""
        model = QStringListModel(self.FIGURAS)
        self.listView.setModel(model)
        self.listView.setStyleSheet("""
            QListView {
                font-size: 14px;
                padding: 5px;
                background-color: #3c3c3c;
                color: #e0e0e0;
                border: 1px solid #555;
                border-radius: 5px;
            }
            QListView::item {
                padding: 8px;
                border-bottom: 1px solid #444;
            }
            QListView::item:selected {
                background-color: #4DB6AC;
                color: white;
            }
            QListView::item:hover {
                background-color: #3d9e95;
            }
        """)

        # Configurar slider
        self.horizontalSlider.setMinimum(10)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.valueChanged.connect(self._on_slider_changed)

    def _conectar_botones(self):
        """Conecta botones de la ventana."""
        # pushButton = "Atras"
        self.pushButton.clicked.connect(self._on_atras)
        # pushButton_2 = "Siguiente"
        self.pushButton_2.clicked.connect(self._on_siguiente)

    def _on_slider_changed(self, value):
        """Actualiza la etiqueta con el valor del slider."""
        self.label_2.setText(f"Grosor de crema: {value}%")
        self.actividad_detectada.emit()

    def _on_atras(self):
        """Vuelve atrás."""
        self.actividad_detectada.emit()
        self.ir_atras.emit()
        self.hide()

    def _on_siguiente(self):
        """Valida seleccion y avanza."""
        self.actividad_detectada.emit()
        indices = self.listView.selectedIndexes()

        if not indices:
            QMessageBox.warning(self, "Advertencia",
                                "Debe seleccionar un patron de la lista.")
            return

        figura = self.FIGURAS[indices[0].row()]
        grosor = self.horizontalSlider.value()

        self.figura_configurada.emit(figura, grosor)
        self.statusbar.showMessage(f"Patron: {figura} | Grosor: {grosor}%")
        QMessageBox.information(
            self, "Patron Configurado",
            f"Patron: {figura}\nGrosor de crema: {grosor}%\n\nVolviendo al panel principal..."
        )
        self.hide()

    def reset(self):
        """Resetea la seleccion."""
        self.listView.clearSelection()
        self.horizontalSlider.setValue(50)
        self.label_2.setText("Deslice para determinar el grosor de crema")

    def showEvent(self, event):
        self.actividad_detectada.emit()
        super().showEvent(event)

    def mousePressEvent(self, event):
        self.actividad_detectada.emit()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        self.actividad_detectada.emit()
        super().keyPressEvent(event)
