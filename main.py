#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================
  PROYECTO DE GRADO - Extrusora de Crema para Alfajores
  Punto de entrada principal (main.py)
=============================================================

  Flujo de la aplicación:
  ┌─────────┐     ┌─────────────┐     ┌──────────────────┐
  │  Login  │ ──► │  Main Panel │ ──► │  Añadir Texto    │
  └─────────┘     │ (ventana_1  │     │  (ventana_2.ui)  │
                  │   _v2.ui)   │     └──────────────────┘
                  │             │──► │  Añadir Figura    │
                  │             │     │  (ventana_4.ui)  │
                  │             │     └──────────────────┘
                  │             │──► │  Modo PRO         │
                  │             │     │  (pro_mode.py)   │
                  └─────────────┘     └──────────────────┘
                        │
                  Protector de Pantalla (tras inactividad)

  Archivos .ui utilizados:
  - ventana_1_v2.ui  → Panel principal (estilizado)
  - ventana_1.ui     → Panel principal (básico, referencia)
  - ventana_2.ui     → Opciones de texto
  - ventana_4.ui     → Opciones de patron decorativo
  - EJEMPLO_1.ui     → Ventana de confirmación
  - experimento.ui   → Opciones de texto (versión experimental)

  Ejecutar:
    python3 main.py

  Requisitos:
    pip install PyQt5
"""

import sys
import os

from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

# Importar módulos del proyecto
from login_window import LoginWindow
from screensaver import ScreensaverWindow
from main_window import MainWindow
from text_options import TextOptionsWindow
from figure_options import FigureOptionsWindow
from pro_mode import ProModeWindow
from example_window import ExampleWindow


class AppController:
    """
    Controlador principal de la aplicación.
    Gestiona la navegación entre ventanas y el ciclo de vida.
    """

    SCREENSAVER_TIMEOUT = 60  # Segundos de inactividad para activar screensaver

    def __init__(self):
        self.usuario_actual = ""

        # === Crear todas las ventanas ===
        self.login = LoginWindow()
        self.screensaver = ScreensaverWindow(timeout_seconds=self.SCREENSAVER_TIMEOUT)
        self.main_win = None  # Se crea después del login
        self.text_opts = TextOptionsWindow()
        self.figure_opts = FigureOptionsWindow()
        self.pro_mode = ProModeWindow()
        self.example_win = ExampleWindow()

        # === Conectar señales ===
        self._conectar_login()
        self._conectar_text_opts()
        self._conectar_figure_opts()
        self._conectar_pro_mode()
        self._conectar_example()
        self._conectar_actividad([
            self.text_opts,
            self.figure_opts, self.pro_mode, self.example_win
        ])

    def _conectar_login(self):
        """Conecta señales del login."""
        self.login.login_exitoso.connect(self._on_login_exitoso)

    def _conectar_main(self):
        """Conecta señales de la ventana principal."""
        self.main_win.abrir_texto.connect(self._on_abrir_texto)
        self.main_win.abrir_figura.connect(self._on_abrir_figura)
        self.main_win.abrir_pro.connect(self._on_abrir_pro)
        self.main_win.actividad_detectada.connect(self._on_actividad)

    def _conectar_text_opts(self):
        """Conecta señales de opciones de texto."""
        self.text_opts.texto_configurado.connect(self._on_texto_configurado)
        self.text_opts.ir_siguiente.connect(self._on_texto_siguiente)
        self.text_opts.ir_atras.connect(self._on_texto_atras)

    def _conectar_figure_opts(self):
        """Conecta señales de opciones de figura."""
        self.figure_opts.figura_configurada.connect(self._on_figura_configurada)
        self.figure_opts.ir_atras.connect(self._on_figura_atras)

    def _conectar_pro_mode(self):
        """Conecta señales del modo PRO."""
        self.pro_mode.volver_basico.connect(self._on_volver_basico)

    def _conectar_example(self):
        """Conecta señales de la ventana de ejemplo."""
        self.example_win.confirmado.connect(self._on_confirmado)

    def _conectar_actividad(self, ventanas):
        """Conecta señales de actividad de múltiples ventanas."""
        for ventana in ventanas:
            ventana.actividad_detectada.connect(self._on_actividad)

    # ===================== HANDLERS =====================

    def _posicionar_ventana(self, ventana):
        """Posiciona una ventana en (0,0) para pantalla tactil."""
        ventana.move(0, 0)

    def _on_login_exitoso(self, usuario):
        """Login exitoso -> mostrar ventana principal."""
        self.usuario_actual = usuario
        self.login.hide()

        # Crear ventana principal con el usuario
        self.main_win = MainWindow(usuario=usuario)
        self._conectar_main()
        self._posicionar_ventana(self.main_win)
        self.main_win.show()

        # Iniciar timer del screensaver
        self.screensaver.reiniciar_timer_inactividad()

    def _on_abrir_texto(self):
        """Abrir opciones de texto."""
        self.text_opts.reset()
        self._posicionar_ventana(self.text_opts)
        self.text_opts.show()
        self.text_opts.raise_()

    def _on_abrir_figura(self):
        """Abrir opciones de figura."""
        self.figure_opts.reset()
        self._posicionar_ventana(self.figure_opts)
        self.figure_opts.show()
        self.figure_opts.raise_()

    def _on_abrir_pro(self):
        """Abrir modo PRO - requiere contrasena."""
        password, ok = QInputDialog.getText(
            self.main_win, "Modo PRO",
            "Ingrese la contrasena para Modo PRO:",
            QLineEdit.Password
        )
        if ok and password == "pro2026":
            self._posicionar_ventana(self.pro_mode)
            self.pro_mode.show()
            self.pro_mode.raise_()
        elif ok:
            QMessageBox.warning(
                self.main_win, "Acceso Denegado",
                "Contrasena incorrecta.\nNo se puede acceder al Modo PRO."
            )

    def _on_texto_configurado(self, texto):
        """Se configuró un texto."""
        if self.main_win:
            self.main_win.set_texto(texto)

    def _on_texto_siguiente(self):
        """Desde texto → volver al panel principal."""
        if self.main_win:
            self.main_win.show()
            self.main_win.raise_()

    def _on_texto_atras(self):
        """Desde texto → volver al menu principal."""
        if self.main_win:
            self.main_win.show()
            self.main_win.raise_()

    def _on_figura_configurada(self, figura, tamano):
        """Se configuro una figura."""
        if self.main_win:
            self.main_win.set_figura(figura, tamano)
            self.main_win.show()
            self.main_win.raise_()

    def _on_figura_atras(self):
        """Desde figuras → volver al menu principal."""
        if self.main_win:
            self.main_win.show()
            self.main_win.raise_()

    def _on_volver_basico(self):
        """Desde modo PRO → volver al modo básico."""
        if self.main_win:
            self.main_win.show()
            self.main_win.raise_()

    def _on_confirmado(self, resultado):
        """Respuesta de ventana de confirmación."""
        if resultado:
            print("[INFO] Usuario confirmó: SÍ")
        else:
            print("[INFO] Usuario confirmó: NO")

    def _on_actividad(self):
        """Actividad detectada → reiniciar timer de screensaver."""
        self.screensaver.reiniciar_timer_inactividad()

    # ===================== INICIO =====================

    def iniciar(self):
        """Inicia la aplicacion mostrando la pantalla de inicio."""
        self.login.move(0, 0)
        self.login.show()


def main():
    """Función principal."""
    # Habilitar High DPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Proyecto de Grado - Extrusora de Crema")
    app.setOrganizationName("Universidad")

    # Estilo global oscuro
    app.setStyleSheet("""
        QMainWindow {
            background-color: #2b2b2b;
        }
        QWidget {
            background-color: #2b2b2b;
        }
        QStatusBar {
            background-color: #1e1e1e;
            color: #4DB6AC;
            font-family: Purisa;
            font-size: 12px;
            padding: 4px;
        }
        QMenuBar {
            background-color: #1e1e1e;
            color: #e0e0e0;
            max-height: 0px;
        }
        QMessageBox {
            background-color: #2b2b2b;
        }
        QMessageBox QLabel {
            color: #e0e0e0;
            font-family: Purisa;
            font-size: 14px;
        }
        QMessageBox QPushButton {
            min-width: 120px;
            min-height: 45px;
            font-family: Purisa;
            font-size: 13px;
            font-weight: bold;
            background-color: #4DB6AC;
            color: white;
            border: none;
            border-radius: 8px;
        }
        QMessageBox QPushButton:pressed {
            background-color: #3d9e95;
        }
        QInputDialog {
            background-color: #2b2b2b;
        }
        QInputDialog QLabel {
            color: #e0e0e0;
            font-family: Purisa;
            font-size: 14px;
        }
        QInputDialog QLineEdit {
            background-color: #3c3c3c;
            color: #e0e0e0;
            border: 2px solid #4DB6AC;
            border-radius: 8px;
            padding: 10px;
            font-size: 16px;
            min-height: 35px;
        }
        QInputDialog QPushButton {
            min-width: 100px;
            min-height: 40px;
            font-family: Purisa;
            font-size: 13px;
            font-weight: bold;
            background-color: #4DB6AC;
            color: white;
            border: none;
            border-radius: 8px;
        }
        QInputDialog QPushButton:pressed {
            background-color: #3d9e95;
        }
        QScrollBar:vertical {
            background: #2b2b2b;
            width: 14px;
            border-radius: 7px;
        }
        QScrollBar::handle:vertical {
            background: #4DB6AC;
            border-radius: 7px;
            min-height: 30px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """)

    # Instalar filtro de eventos global para detectar actividad
    controller = AppController()
    controller.iniciar()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
