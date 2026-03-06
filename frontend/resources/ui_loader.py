#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI Loader para PySide6 - Proyecto de Grado
Carga archivos .ui de manera compatible con QMainWindow.
"""

import os
from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

# Directorio de recursos donde están los .ui
RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))


def load_ui(ui_filename, base_instance):
    """
    Carga un archivo .ui y aplica sus widgets sobre base_instance.

    Para QMainWindow: carga el .ui como widget separado, copia sus
    propiedades y lo establece como centralWidget.

    Args:
        ui_filename: Nombre del .ui o ruta completa
        base_instance: Widget destino
    """
    # Resolver ruta del archivo .ui
    if os.path.isabs(ui_filename) and os.path.exists(ui_filename):
        ui_path = ui_filename
    else:
        basename = os.path.basename(ui_filename)
        ui_path = os.path.join(RESOURCES_DIR, basename)

    if not os.path.exists(ui_path):
        raise FileNotFoundError(f"Archivo UI no encontrado: {ui_path}")

    loader = QUiLoader()
    ui_file = QFile(ui_path)
    ui_file.open(QFile.ReadOnly)
    loaded_widget = loader.load(ui_file)
    ui_file.close()

    if loaded_widget is None:
        raise RuntimeError(f"No se pudo cargar: {ui_path}")

    # Copiar propiedades de la ventana cargada
    base_instance.setWindowTitle(loaded_widget.windowTitle())
    base_instance.resize(loaded_widget.size())
    base_instance.setMinimumSize(loaded_widget.minimumSize())
    base_instance.setMaximumSize(loaded_widget.maximumSize())

    # Si es QMainWindow, transferir el central widget y barras
    if isinstance(base_instance, QMainWindow) and isinstance(loaded_widget, QMainWindow):
        # Transferir central widget
        central = loaded_widget.centralWidget()
        if central:
            central.setParent(None)  # Desconectar del widget cargado
            base_instance.setCentralWidget(central)

        # Transferir menubar
        menubar = loaded_widget.menuBar()
        if menubar:
            base_instance.setMenuBar(menubar)

        # Transferir statusbar
        statusbar = loaded_widget.statusBar()
        if statusbar:
            base_instance.setStatusBar(statusbar)
    else:
        # Para QWidget normal, copiar el layout
        if loaded_widget.layout():
            if base_instance.layout():
                # Limpiar layout existente
                old_layout = base_instance.layout()
                while old_layout.count():
                    old_layout.takeAt(0)
            base_instance.setLayout(loaded_widget.layout())

    # Copiar stylesheet
    style = loaded_widget.styleSheet()
    if style:
        base_instance.setStyleSheet(style)

    # Hacer accesibles todos los widgets hijos como atributos
    _copiar_widgets_hijos(loaded_widget, base_instance)
    _copiar_widgets_hijos(base_instance.centralWidget(), base_instance)
    # También escanear base_instance (statusbar/menubar ya transferidos)
    _copiar_widgets_hijos(base_instance, base_instance)

    # Limpiar widget temporal
    loaded_widget.deleteLater()


def _copiar_widgets_hijos(source, target):
    """Copia referencias a widgets hijos como atributos del target."""
    if source is None:
        return
    from PySide6.QtCore import QObject
    for child in source.findChildren(QObject):
        name = child.objectName()
        if name and not name.startswith("_") and not name.startswith("qt_"):
            setattr(target, name, child)
