#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper para cargar archivos .ui con PySide6.
Reemplaza la funcionalidad de PyQt5.uic.loadUi().
"""

from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice


class UiLoader(QUiLoader):
    """
    Loader personalizado que permite cargar .ui directamente
    sobre un widget existente (similar a PyQt5 uic.loadUi).
    """

    def __init__(self, base_instance):
        super().__init__(base_instance)
        self.base_instance = base_instance

    def createWidget(self, class_name, parent=None, name=""):
        # Si es el widget raíz, devolver la instancia base
        if parent is None and self.base_instance is not None:
            return self.base_instance
        else:
            widget = super().createWidget(class_name, parent, name)
            if self.base_instance is not None and name:
                setattr(self.base_instance, name, widget)
            return widget


def load_ui(ui_file, base_instance=None):
    """
    Carga un archivo .ui y sus widgets sobre base_instance.

    Args:
        ui_file: Ruta al archivo .ui
        base_instance: Instancia del widget donde cargar la UI.
                       Si es None, crea un nuevo widget.

    Returns:
        El widget cargado.
    """
    loader = UiLoader(base_instance)
    f = QFile(ui_file)
    if not f.open(QIODevice.ReadOnly):
        raise IOError(f"No se pudo abrir el archivo: {ui_file}")
    ui = loader.load(f, base_instance.parent() if base_instance else None)
    f.close()
    return ui
