#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main View - Proyecto de Grado
Ventana principal con visualización del alfajor y controles de extrusión.
Integra AlfajorCanvas para visualizar la crema en tiempo real.
"""

import os
from PySide6.QtWidgets import QMainWindow, QMessageBox, QPushButton
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont

from frontend.resources.ui_loader import load_ui
from frontend.widgets.animated_button import aplicar_animacion_pulso
from frontend.widgets.alfajor_canvas import AlfajorCanvas
from backend.config import SystemConfig
from backend.extruder import ExtruderEngine


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

        # Cargar UI
        load_ui("ventana_1_v2.ui", self)
        self.setWindowTitle(f"Extrusora de Crema — {self.usuario}")

        # Reemplazar el widget placeholder con AlfajorCanvas
        self._setup_alfajor_canvas()

        # Añadir botón LIMPIAR
        self._setup_boton_limpiar()

        # Conectar
        self._conectar_botones()
        self._conectar_engine()
        self._aplicar_animaciones()
        self._configurar_estado_inicial()

    def _setup_alfajor_canvas(self):
        """Reemplaza el openGLWidget placeholder con AlfajorCanvas."""
        self.canvas = AlfajorCanvas(self)

        # Buscar el openGLWidget cargado del .ui y reemplazarlo
        if hasattr(self, 'openGLWidget'):
            old_widget = self.openGLWidget
            parent_layout = old_widget.parentWidget()

            # Buscar el layout que contiene al widget
            if parent_layout and parent_layout.layout():
                layout = parent_layout.layout()
                # Buscar en todos los items del layout
                self._replace_in_layout(layout, old_widget, self.canvas)
            else:
                # Fallback: reemplazar propiedades y posición
                self.canvas.setParent(old_widget.parentWidget())
                self.canvas.setGeometry(old_widget.geometry())
                self.canvas.setMinimumSize(old_widget.minimumSize())
                old_widget.hide()

            # Copiar propiedades de tamaño
            self.canvas.setMinimumSize(old_widget.minimumSize())
            self.canvas.setSizePolicy(old_widget.sizePolicy())

    def _replace_in_layout(self, layout, old_widget, new_widget):
        """Reemplaza un widget dentro de un layout."""
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

    def _setup_boton_limpiar(self):
        """Añade botón LIMPIAR entre Figura y PRO."""
        self.btn_limpiar = QPushButton("LIMPIAR")
        self.btn_limpiar.setMinimumSize(120, 65)
        self.btn_limpiar.setMaximumSize(120, 65)
        self.btn_limpiar.setFont(QFont("Purisa", 12, QFont.Bold))
        self.btn_limpiar.setStyleSheet("""
            QPushButton {
                background-color: #FFAB40;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:pressed {
                background-color: #e09530;
            }
        """)

        # Insertar en el layout horizontal de la barra superior
        # pushButton_2 = Figura, pushButton = PRO
        # Buscar el layout que contiene pushButton (PRO)
        pro_btn = self.pushButton
        parent_widget = pro_btn.parentWidget()
        if parent_widget and parent_widget.layout():
            layout = parent_widget.layout()
            # Buscar el índice del botón PRO
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget() == pro_btn:
                    layout.insertWidget(i, self.btn_limpiar)
                    break
            else:
                # Buscar en sublayouts
                self._insert_before_in_layout(layout, pro_btn, self.btn_limpiar)

    def _insert_before_in_layout(self, layout, target_widget, new_widget):
        """Inserta new_widget antes de target_widget en cualquier sublayout."""
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() == target_widget:
                layout.insertWidget(i, new_widget)
                return True
            elif item.layout():
                if self._insert_before_in_layout(item.layout(), target_widget, new_widget):
                    return True
        return False

    def _conectar_botones(self):
        """Conecta los botones de la UI."""
        self.pushButton_3.clicked.connect(self._on_anadir_texto)   # Texto
        self.pushButton_2.clicked.connect(self._on_anadir_figura)  # Figura
        self.btn_limpiar.clicked.connect(self._on_limpiar)         # Limpiar
        self.pushButton.clicked.connect(self._on_modo_pro)         # PRO
        self.pushButton_4.clicked.connect(self._on_stop)           # STOP
        self.pushButton_5.clicked.connect(self._on_print)          # Print

    def _conectar_engine(self):
        """Conecta señales del motor de extrusión."""
        self.engine.progress_updated.connect(self._on_progress)
        self.engine.extrusion_finished.connect(self._on_finished)
        self.engine.extrusion_stopped.connect(self._on_stopped)
        self.engine.status_message.connect(self._on_status)

    def _aplicar_animaciones(self):
        """Aplica animaciones de pulso a los botones."""
        aplicar_animacion_pulso(self.pushButton_3)
        aplicar_animacion_pulso(self.pushButton_2)
        aplicar_animacion_pulso(self.btn_limpiar)
        aplicar_animacion_pulso(self.pushButton)
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
        """Reinicia todo: progreso, canvas, y motor."""
        self.actividad_detectada.emit()
        if self.engine.is_extruding:
            self.engine.stop()
            self.impresion_terminada.emit()
        self.engine.reset()
        self.canvas.reset()
        self.progressBar.setValue(0)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(True)
        self.statusbar.showMessage(f"Todo reiniciado. Listo para decorar.")

    def _on_print(self):
        self.actividad_detectada.emit()
        if self.engine.is_extruding:
            return

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
