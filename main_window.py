#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ventana Principal - Proyecto de Grado
Carga ventana_1_v2.ui como pantalla principal de la extrusora de crema.
Conecta botones a las demas ventanas del sistema.
"""

import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5 import uic


# Directorio base donde están los .ui
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QMainWindow):
    """Ventana principal que carga ventana_1_v2.ui."""

    abrir_texto = pyqtSignal()          # Señal para abrir opciones de texto
    abrir_figura = pyqtSignal()         # Señal para abrir opciones de figura
    abrir_pro = pyqtSignal()            # Señal para abrir modo PRO
    actividad_detectada = pyqtSignal()  # Señal de actividad del usuario

    def __init__(self, usuario="usuario", parent=None):
        super().__init__(parent)
        self.usuario = usuario
        self.imprimiendo = False
        self.progreso = 0

        # Cargar UI
        ui_path = os.path.join(BASE_DIR, "ventana_1_v2.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle(f"Extrusora de Crema - {self.usuario}")

        # Timer de progreso para simulación
        self.timer_progreso = QTimer(self)
        self.timer_progreso.timeout.connect(self._avanzar_progreso)

        self._conectar_botones()
        self._configurar_estado_inicial()

    def _conectar_botones(self):
        """Conecta los botones de la UI a sus funciones."""
        # pushButton_3 = "Añadir Texto"
        self.pushButton_3.clicked.connect(self._on_anadir_texto)

        # pushButton_2 = "Añadir Figura"
        self.pushButton_2.clicked.connect(self._on_anadir_figura)

        # pushButton = "Modo PRO"
        self.pushButton.clicked.connect(self._on_modo_pro)

        # pushButton_4 = "STOP"
        self.pushButton_4.clicked.connect(self._on_stop)

        # pushButton_5 = "Print"
        self.pushButton_5.clicked.connect(self._on_print)

    def _configurar_estado_inicial(self):
        """Estado inicial de la ventana."""
        self.progressBar.setValue(0)
        self.pushButton_4.setEnabled(False)
        self.statusbar.showMessage(f"Bienvenido, {self.usuario}. Listo para decorar.")

    def _on_anadir_texto(self):
        """Abre la ventana de opciones de texto."""
        self.actividad_detectada.emit()
        self.abrir_texto.emit()
        self.statusbar.showMessage("Configurando texto para decorar...")

    def _on_anadir_figura(self):
        """Abre la ventana de opciones de patron decorativo."""
        self.actividad_detectada.emit()
        self.abrir_figura.emit()
        self.statusbar.showMessage("Seleccionando patron decorativo...")

    def _on_modo_pro(self):
        """Abre el modo PRO."""
        self.actividad_detectada.emit()
        self.abrir_pro.emit()
        self.statusbar.showMessage("Abriendo Modo PRO...")

    def _on_stop(self):
        """Detiene la extrusion actual."""
        self.actividad_detectada.emit()
        if self.imprimiendo:
            self.imprimiendo = False
            self.timer_progreso.stop()
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(True)
            self.statusbar.showMessage("Extrusion detenida.")
            QMessageBox.warning(self, "Detenido",
                                "La extrusion fue detenida por el usuario.")

    def _on_print(self):
        """Inicia la extrusion de crema."""
        self.actividad_detectada.emit()
        if self.imprimiendo:
            return

        respuesta = QMessageBox.question(
            self, "Confirmar Extrusion",
            "Desea iniciar la extrusion de crema?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.imprimiendo = True
            self.progreso = 0
            self.progressBar.setValue(0)
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(False)
            self.timer_progreso.start(100)
            self.statusbar.showMessage("Extruyendo crema...")

    def _avanzar_progreso(self):
        """Avanza la barra de progreso durante la extrusion."""
        if not self.imprimiendo:
            return

        self.progreso += 1
        self.progressBar.setValue(self.progreso)

        if self.progreso >= 100:
            self.imprimiendo = False
            self.timer_progreso.stop()
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(True)
            self.statusbar.showMessage("Extrusion completada.")
            QMessageBox.information(self, "Completado",
                                    "La extrusion de crema ha finalizado!")

    def set_texto(self, texto):
        """Configura el texto a extruir."""
        self.statusbar.showMessage(f"Texto configurado: '{texto}'")

    def set_figura(self, figura, tamano):
        """Configura el patron decorativo."""
        self.statusbar.showMessage(f"Patron: {figura} (grosor: {tamano}%)")

    def mousePressEvent(self, event):
        self.actividad_detectada.emit()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        self.actividad_detectada.emit()
        super().keyPressEvent(event)
