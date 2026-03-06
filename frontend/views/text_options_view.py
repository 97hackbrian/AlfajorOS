#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Options View - Proyecto de Grado
Ventana para configurar texto a decorar en el alfajor.
Incluye teclado virtual integrado.
"""

import os
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Signal

from frontend.resources.ui_loader import load_ui
from frontend.widgets.virtual_keyboard import VirtualKeyboard
from backend.config import SystemConfig


class TextOptionsView(QMainWindow):
    """Ventana para configurar opciones de texto."""

    texto_configurado = Signal(str)
    ir_siguiente = Signal()
    ir_atras = Signal()
    actividad_detectada = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        load_ui("ventana_2.ui", self)
        self.setWindowTitle("Opciones de Texto")
        self._setup_keyboard()
        self._conectar_botones()

    def _setup_keyboard(self):
        """Integra teclado virtual debajo del campo de texto."""
        self.keyboard = VirtualKeyboard()
        self.keyboard.set_target(self.textEdit)
        central = self.centralWidget()
        if central and central.layout():
            layout = central.layout()
            for i in range(layout.count() - 1, -1, -1):
                item = layout.itemAt(i)
                if item.spacerItem():
                    layout.removeItem(item)
                    break
            self.textEdit.setMinimumHeight(100)
            self.textEdit.setMaximumHeight(120)
            layout.addWidget(self.keyboard)

    def _conectar_botones(self):
        self.pushButton.clicked.connect(self._on_atras)
        self.pushButton_2.clicked.connect(self._on_siguiente)
        self.textEdit.textChanged.connect(self._limitar_texto)

    def _limitar_texto(self):
        texto = self.textEdit.toPlainText()
        if len(texto) > SystemConfig.MAX_TEXTO_CHARS:
            self.textEdit.blockSignals(True)
            self.textEdit.setPlainText(texto[:SystemConfig.MAX_TEXTO_CHARS])
            cursor = self.textEdit.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.textEdit.setTextCursor(cursor)
            self.textEdit.blockSignals(False)
        restantes = SystemConfig.MAX_TEXTO_CHARS - len(self.textEdit.toPlainText())
        self.statusbar.showMessage(f"Caracteres restantes: {restantes}")

    def _on_atras(self):
        self.actividad_detectada.emit()
        self.ir_atras.emit()
        self.hide()

    def _on_siguiente(self):
        self.actividad_detectada.emit()
        texto = self.textEdit.toPlainText().strip()
        if not texto:
            QMessageBox.warning(self, "Advertencia",
                                "Debe ingresar un texto antes de continuar.")
            return
        if len(texto) > SystemConfig.MAX_TEXTO_CHARS:
            QMessageBox.warning(self, "Advertencia",
                                f"El texto no puede ser mayor a {SystemConfig.MAX_TEXTO_CHARS} letras.")
            return
        self.texto_configurado.emit(texto)
        self.ir_siguiente.emit()
        self.hide()

    def reset(self):
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
