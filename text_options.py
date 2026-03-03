#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ventana de Opciones de Texto - Proyecto de Grado
Carga ventana_2.ui para configurar texto a decorar en el alfajor.
"""

import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class TextOptionsWindow(QMainWindow):
    """Ventana para configurar opciones de texto (ventana_2.ui)."""

    texto_configurado = pyqtSignal(str)  # Emite el texto ingresado
    ir_siguiente = pyqtSignal()          # Volver al panel principal
    ir_atras = pyqtSignal()              # Volver al menú principal
    actividad_detectada = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(BASE_DIR, "ventana_2.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Opciones de Texto")
        self._conectar_botones()

    def _conectar_botones(self):
        """Conecta botones de la UI."""
        # pushButton = "ATRAS"
        self.pushButton.clicked.connect(self._on_atras)
        # pushButton_2 = "SIGUIENTE"
        self.pushButton_2.clicked.connect(self._on_siguiente)

        # Limitar texto a 10 caracteres
        self.textEdit.textChanged.connect(self._limitar_texto)

    def _limitar_texto(self):
        """Limita el texto a 10 caracteres máximo."""
        texto = self.textEdit.toPlainText()
        if len(texto) > 10:
            self.textEdit.blockSignals(True)
            self.textEdit.setPlainText(texto[:10])
            # Mover cursor al final
            cursor = self.textEdit.textCursor()
            cursor.movePosition(cursor.End)
            self.textEdit.setTextCursor(cursor)
            self.textEdit.blockSignals(False)

        # Actualizar status bar
        restantes = 10 - len(self.textEdit.toPlainText())
        self.statusbar.showMessage(f"Caracteres restantes: {restantes}")

    def _on_atras(self):
        """Vuelve atrás."""
        self.actividad_detectada.emit()
        self.ir_atras.emit()
        self.hide()

    def _on_siguiente(self):
        """Valida texto y avanza."""
        self.actividad_detectada.emit()
        texto = self.textEdit.toPlainText().strip()

        if not texto:
            QMessageBox.warning(self, "Advertencia",
                                "Debe ingresar un texto antes de continuar.")
            return

        if len(texto) > 10:
            QMessageBox.warning(self, "Advertencia",
                                "El texto no puede ser mayor a 10 letras.")
            return

        self.texto_configurado.emit(texto)
        self.ir_siguiente.emit()
        self.hide()

    def reset(self):
        """Limpia el campo de texto."""
        self.textEdit.clear()

    def showEvent(self, event):
        self.actividad_detectada.emit()
        super().showEvent(event)

    def mousePressEvent(self, event):
        self.actividad_detectada.emit()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        self.actividad_detectada.emit()
        super().keyPressEvent(event)
