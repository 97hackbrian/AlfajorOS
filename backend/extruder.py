#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Extrusión - Proyecto de Grado
Máquina de estados para controlar el proceso de extrusión de crema.
"""

from enum import Enum
from PySide6.QtCore import QObject, Signal, QTimer
from backend.config import SystemConfig


class ExtruderState(Enum):
    """Estados posibles del extrusor."""
    IDLE = "idle"
    EXTRUDING = "extruding"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"


class ExtruderEngine(QObject):
    """
    Motor de extrusión con máquina de estados.
    Controla el ciclo de vida de una extrusión de crema.
    """

    # Señales
    progress_updated = Signal(int)          # 0-100
    state_changed = Signal(str)             # nuevo estado
    extrusion_finished = Signal()           # extrusión completada
    extrusion_stopped = Signal()            # extrusión detenida
    status_message = Signal(str)            # mensajes de estado

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = ExtruderState.IDLE
        self._progress = 0
        self._patron = ""
        self._texto = ""
        self._velocidad = SystemConfig.VELOCIDAD_DEFAULT
        self._presion = SystemConfig.PRESION_DEFAULT

        # Timer de simulación
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)

    # === Propiedades ===

    @property
    def state(self):
        return self._state

    @property
    def progress(self):
        return self._progress

    @property
    def is_extruding(self):
        return self._state == ExtruderState.EXTRUDING

    @property
    def is_idle(self):
        return self._state in (ExtruderState.IDLE, ExtruderState.STOPPED)

    # === Configuración ===

    def set_texto(self, texto):
        """Configura el texto a extruir."""
        self._texto = texto
        self.status_message.emit(f"Texto configurado: '{texto}'")

    def set_patron(self, patron):
        """Configura el patrón decorativo."""
        self._patron = patron
        self.status_message.emit(f"Patrón configurado: {patron}")

    def set_velocidad(self, vel):
        self._velocidad = vel

    def set_presion(self, presion):
        self._presion = presion

    # === Control ===

    def start(self):
        """Inicia la extrusión."""
        if self._state == ExtruderState.EXTRUDING:
            return False

        self._state = ExtruderState.EXTRUDING
        self._progress = 0
        self.progress_updated.emit(0)
        self.state_changed.emit(self._state.value)
        self.status_message.emit("Extruyendo crema...")
        self._timer.start(SystemConfig.EXTRUSION_TICK_MS)
        return True

    def stop(self):
        """Detiene la extrusión y reinicia progreso."""
        if self._state != ExtruderState.EXTRUDING:
            return

        self._timer.stop()
        self._state = ExtruderState.STOPPED
        self._progress = 0
        self.progress_updated.emit(0)
        self.state_changed.emit(self._state.value)
        self.extrusion_stopped.emit()
        self.status_message.emit("Extrusión detenida. Progreso reiniciado.")

    def pause(self):
        """Pausa la extrusión."""
        if self._state != ExtruderState.EXTRUDING:
            return

        self._timer.stop()
        self._state = ExtruderState.PAUSED
        self.state_changed.emit(self._state.value)
        self.status_message.emit("Extrusión en pausa.")

    def resume(self):
        """Reanuda la extrusión pausada."""
        if self._state != ExtruderState.PAUSED:
            return

        self._state = ExtruderState.EXTRUDING
        self.state_changed.emit(self._state.value)
        self.status_message.emit("Extrusión reanudada...")
        self._timer.start(SystemConfig.EXTRUSION_TICK_MS)

    def reset(self):
        """Resetea el motor al estado inicial."""
        self._timer.stop()
        self._state = ExtruderState.IDLE
        self._progress = 0
        self.progress_updated.emit(0)
        self.state_changed.emit(self._state.value)

    # === Interno ===

    def _tick(self):
        """Avanza un tick de simulación."""
        if self._state != ExtruderState.EXTRUDING:
            return

        self._progress += 1
        self.progress_updated.emit(self._progress)

        if self._progress >= 100:
            self._timer.stop()
            self._state = ExtruderState.IDLE
            self.state_changed.emit(self._state.value)
            self.extrusion_finished.emit()
            self.status_message.emit("Extrusión completada.")
