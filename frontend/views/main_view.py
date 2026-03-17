#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main View - Proyecto de Grado
Ventana principal con visualización del alfajor y controles de extrusión.
Layout: barra superior (.ui) con Extruir/STOP/PRO +
        columna izquierda (Texto/Patrón/Limpiar) + canvas derecho.
"""

import os
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont

from frontend.resources.ui_loader import load_ui
from frontend.widgets.animated_button import aplicar_animacion_pulso
from frontend.widgets.alfajor_canvas import AlfajorCanvas
from frontend.widgets.printer_indicator import PrinterIndicator
from backend.config import SystemConfig
from backend.extruder import ExtruderEngine
from backend.printer import PrinterConnection


# Estilo celeste para botones laterales
BTN_LATERAL_STYLE = """
    QPushButton {
        background-color: #4DB6AC;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        font-family: Purisa;
    }
    QPushButton:pressed {
        background-color: #3d9e95;
    }
"""


class MainView(QMainWindow):
    """Ventana principal con visualización del alfajor."""

    abrir_texto = Signal()
    abrir_figura = Signal()
    abrir_pro = Signal()
    actividad_detectada = Signal()
    impresion_iniciada = Signal()
    impresion_terminada = Signal()

    def __init__(self, usuario="usuario", parent=None):
        super().__init__(parent)
        self.usuario = usuario

        # Motor de extrusión (backend)
        self.engine = ExtruderEngine(self)

        # Conexión serial con impresora
        self.printer = PrinterConnection(self)

        # Cargar UI
        load_ui("ventana_1_v2.ui", self)
        self.setWindowTitle(f"Extrusora de Crema — {self.usuario}")

        # Reemplazar el widget placeholder con AlfajorCanvas
        self._setup_alfajor_canvas()

        # Añadir columna izquierda con Texto/Patrón/Limpiar
        self._setup_columna_izquierda()

        # Ocultar botones de Texto y Figura del .ui (se reemplazan por la columna)
        self._ocultar_botones_ui()

        # Conectar
        self._conectar_botones()
        self._conectar_engine()
        self._conectar_printer()
        self._aplicar_animaciones()
        self._configurar_estado_inicial()

    def _setup_alfajor_canvas(self):
        """Reemplaza el openGLWidget placeholder con AlfajorCanvas."""
        self.canvas = AlfajorCanvas(self)

        if hasattr(self, 'openGLWidget'):
            old_widget = self.openGLWidget
            parent_layout = old_widget.parentWidget()

            if parent_layout and parent_layout.layout():
                layout = parent_layout.layout()
                self._replace_in_layout(layout, old_widget, self.canvas)
            else:
                self.canvas.setParent(old_widget.parentWidget())
                self.canvas.setGeometry(old_widget.geometry())
                self.canvas.setMinimumSize(old_widget.minimumSize())
                old_widget.hide()

            self.canvas.setMinimumSize(old_widget.minimumSize())
            self.canvas.setSizePolicy(old_widget.sizePolicy())

    def _replace_in_layout(self, layout, old_widget, new_widget):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() == old_widget:
                layout.removeWidget(old_widget)
                old_widget.hide()
                old_widget.deleteLater()
                layout.insertWidget(i, new_widget)
                return True
            elif item.layout():
                if self._replace_in_layout(item.layout(), old_widget, new_widget):
                    return True
        return False

    def _setup_columna_izquierda(self):
        """Añade columna izquierda con Texto/Patrón/Limpiar al lado del canvas."""
        # Crear la columna
        self._left_col = QWidget()
        left_layout = QVBoxLayout(self._left_col)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        # Indicador de impresora (LED + texto)
        self.printer_indicator = PrinterIndicator()
        left_layout.addWidget(self.printer_indicator)

        btn_font = QFont("Purisa", 11, QFont.Bold)

        # Botón TEXTO
        self.btn_texto = QPushButton("📝\nTEXTO")
        self.btn_texto.setMinimumSize(90, 65)
        self.btn_texto.setFont(btn_font)
        self.btn_texto.setStyleSheet(BTN_LATERAL_STYLE)
        self.btn_texto.clicked.connect(self._on_anadir_texto)
        left_layout.addWidget(self.btn_texto)

        # Botón PATRÓN
        self.btn_patron = QPushButton("🎨\nPATRÓN")
        self.btn_patron.setMinimumSize(90, 65)
        self.btn_patron.setFont(btn_font)
        self.btn_patron.setStyleSheet(BTN_LATERAL_STYLE)
        self.btn_patron.clicked.connect(self._on_anadir_figura)
        left_layout.addWidget(self.btn_patron)

        # Botón LIMPIAR
        self.btn_limpiar = QPushButton("🗑\nLIMPIAR")
        self.btn_limpiar.setMinimumSize(90, 65)
        self.btn_limpiar.setFont(btn_font)
        self.btn_limpiar.setStyleSheet(BTN_LATERAL_STYLE)
        self.btn_limpiar.clicked.connect(self._on_limpiar)
        left_layout.addWidget(self.btn_limpiar)

        left_layout.addStretch(1)

        # Botón PRO (al final de la columna)
        self.btn_pro = QPushButton("⚙\nPRO")
        self.btn_pro.setMinimumSize(90, 65)
        self.btn_pro.setFont(btn_font)
        self.btn_pro.setStyleSheet("""
            QPushButton {
                background-color: #FFAB40;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-family: Purisa;
            }
            QPushButton:pressed {
                background-color: #e09530;
            }
        """)
        self.btn_pro.clicked.connect(self._on_modo_pro)
        left_layout.addWidget(self.btn_pro)

        self._left_col.setFixedWidth(100)

        # Insertar la columna a la izquierda del canvas en su layout padre
        canvas_parent = self.canvas.parentWidget()
        if canvas_parent and canvas_parent.layout():
            layout = canvas_parent.layout()
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget() == self.canvas:
                    layout.insertWidget(i, self._left_col)
                    break
            else:
                self._insert_before_recursive(layout, self.canvas, self._left_col)

    def _insert_before_recursive(self, layout, target, new_widget):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() == target:
                layout.insertWidget(i, new_widget)
                return True
            elif item.layout():
                if self._insert_before_recursive(item.layout(), target, new_widget):
                    return True
        return False

    def _ocultar_botones_ui(self):
        """Elimina botones de Texto, Figura y PRO del .ui (reemplazados por columna)."""
        for attr in ['pushButton_3', 'pushButton_2', 'pushButton']:
            if hasattr(self, attr):
                btn = getattr(self, attr)
                parent = btn.parentWidget()
                if parent and parent.layout():
                    parent.layout().removeWidget(btn)
                btn.hide()
                btn.deleteLater()

    def _conectar_botones(self):
        """Conecta los botones de la UI (.ui)."""
        # Botones del .ui (barra superior)
        self.pushButton_4.clicked.connect(self._on_stop)      # STOP
        self.pushButton_5.clicked.connect(self._on_print)     # Extruir/Print
        # Agrandar botón Extruir
        self.pushButton_5.setMinimumHeight(75)
        self.pushButton_5.setFont(QFont("Purisa", 14, QFont.Bold))

    def _conectar_engine(self):
        self.engine.progress_updated.connect(self._on_progress)
        self.engine.extrusion_finished.connect(self._on_finished)
        self.engine.extrusion_stopped.connect(self._on_stopped)
        self.engine.status_message.connect(self._on_status)

    def _conectar_printer(self):
        """Conecta señales de la impresora al indicador visual."""
        self.printer.state_changed.connect(self.printer_indicator.set_state)
        self.printer.connection_info.connect(self.printer_indicator.set_port_info)
        self.printer.connection_info.connect(
            lambda info: self.statusbar.showMessage(f"Impresora: {info}")
        )
        self.printer.error_occurred.connect(
            lambda err: self.statusbar.showMessage(f"Error: {err}")
        )

    def _aplicar_animaciones(self):
        # Botones columna izquierda
        aplicar_animacion_pulso(self.btn_texto)
        aplicar_animacion_pulso(self.btn_patron)
        aplicar_animacion_pulso(self.btn_limpiar)
        aplicar_animacion_pulso(self.btn_pro)
        # Botones del .ui
        aplicar_animacion_pulso(self.pushButton_4)
        aplicar_animacion_pulso(self.pushButton_5)

    def _configurar_estado_inicial(self):
        self.progressBar.setValue(0)
        self.pushButton_4.setEnabled(False)
        self.statusbar.showMessage(f"Bienvenido, {self.usuario}. Listo para decorar.")

    # === Handlers ===

    def _on_anadir_texto(self):
        self.actividad_detectada.emit()
        self.abrir_texto.emit()
        self.statusbar.showMessage("Configurando texto para decorar...")

    def _on_anadir_figura(self):
        self.actividad_detectada.emit()
        self.abrir_figura.emit()
        self.statusbar.showMessage("Seleccionando patrón decorativo...")

    def _on_modo_pro(self):
        self.actividad_detectada.emit()
        self.abrir_pro.emit()
        self.statusbar.showMessage("Abriendo Modo PRO...")

    def _on_stop(self):
        self.actividad_detectada.emit()
        if self.engine.is_extruding:
            self.engine.stop()
            self.impresion_terminada.emit()

    def _on_limpiar(self):
        self.actividad_detectada.emit()
        if self.engine.is_extruding:
            self.engine.stop()
            self.impresion_terminada.emit()
        self.engine.reset()
        self.canvas.reset()
        self.progressBar.setValue(0)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(True)
        self.statusbar.showMessage("Todo reiniciado. Listo para decorar.")

    def _on_print(self):
        self.actividad_detectada.emit()
        if self.engine.is_extruding:
            return

        # Validar que haya algo configurado
        if not self.canvas._patron and not self.canvas._texto:
            QMessageBox.warning(
                self, "Sin configuración",
                "Debe seleccionar un patrón decorativo o\ningresar un texto antes de extruir."
            )
            return

        # Confirmar extrusión
        respuesta = QMessageBox.question(
            self, "Confirmar Extrusión",
            "¿Desea iniciar la extrusión de crema?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.canvas.start_animacion()
            self.engine.start()
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(False)
            self.impresion_iniciada.emit()

    def _on_progress(self, value):
        self.progressBar.setValue(value)
        self.canvas.set_progreso(value)

    def _on_finished(self):
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(True)
        self.canvas.stop_animacion()
        self.impresion_terminada.emit()
        QMessageBox.information(self, "Completado",
                                "¡La extrusión de crema ha finalizado!")

    def _on_stopped(self):
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(True)
        self.progressBar.setValue(0)
        self.canvas.stop_animacion()
        self.canvas.set_progreso(0)
        QMessageBox.warning(self, "Detenido",
                            "La extrusión fue detenida.\nProgreso reiniciado.")

    def _on_status(self, msg):
        self.statusbar.showMessage(msg)

    # === API ===

    def set_texto(self, texto):
        self.engine.set_texto(texto)
        self.canvas.set_texto(texto)
        self.statusbar.showMessage(f"Texto configurado: '{texto}'")

    def set_figura(self, figura, tamano):
        self.engine.set_patron(figura)
        self.canvas.set_patron(figura)
        self.canvas.set_grosor(tamano)
        self.statusbar.showMessage(f"Patrón: {figura} (grosor: {tamano}%)")

    def mousePressEvent(self, event):
        self.actividad_detectada.emit()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        self.actividad_detectada.emit()
        super().keyPressEvent(event)
