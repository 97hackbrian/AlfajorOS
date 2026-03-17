#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración del sistema - Proyecto de Grado
Constantes y parámetros del sistema de extrusión.
"""


class SystemConfig:
    """Configuración centralizada del sistema."""

    # === Dimensiones de pantalla ===
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 600

    # === Alfajor ===
    ALFAJOR_DIAMETRO_CM = 7.0
    ALFAJOR_MARGEN_MM = 3.0
    ALFAJOR_ALTURA_CREMA_MM = 5.0

    # === Temperaturas (°C) ===
    TEMP_CREMA_DEFAULT = 18
    TEMP_CREMA_MIN = 5
    TEMP_CREMA_MAX = 45
    TEMP_BASE_DEFAULT = 15
    TEMP_BASE_MIN = 5
    TEMP_BASE_MAX = 30

    # === Extrusión ===
    VELOCIDAD_DEFAULT = 25      # mm/s
    VELOCIDAD_MIN = 5
    VELOCIDAD_MAX = 80
    GROSOR_LINEA_DEFAULT = 2.0  # mm
    GROSOR_LINEA_MIN = 0.5
    GROSOR_LINEA_MAX = 5.0
    PRESION_DEFAULT = 60        # %
    PRESION_MIN = 10
    PRESION_MAX = 100
    BOQUILLA_DEFAULT = 3.0      # mm

    # === Tipos de crema ===
    TIPOS_CREMA = [
        "Dulce de Leche",
        "Chocolate",
        "Vainilla",
        "Crema Chantilly",
        "Merengue",
        "Ganache",
    ]

    # === Consistencias ===
    CONSISTENCIAS = ["Firme", "Media", "Suave", "Muy suave"]

    # === Patrones decorativos ===
    PATRONES = [
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

    PATRONES_PRO = [
        "Espiral", "Zigzag", "Circulos", "Lineas",
        "Rejilla", "Libre",
    ]

    # === Tiempos ===
    SCREENSAVER_TIMEOUT_S = 60
    EXTRUSION_TICK_MS = 100     # Intervalo de actualización de progreso
    ANIMACION_FPS = 30

    # === Seguridad ===
    PRO_PASSWORD = "pro2026"
    MAX_TEXTO_CHARS = 10

    # === Colores del tema ===
    COLOR_PRIMARIO = "#4DB6AC"
    COLOR_FONDO = "#2b2b2b"
    COLOR_FONDO_OSCURO = "#1e1e1e"
    COLOR_SUPERFICIE = "#3c3c3c"
    COLOR_TEXTO = "#e0e0e0"
    COLOR_ACENTO = "#FFAB40"
    COLOR_ERROR = "#F66151"
    COLOR_BORDE = "#555"

    # === Impresora Serial ===
    PRINTER_BAUDRATE = 115200
    PRINTER_SCAN_PATTERNS = ["/dev/ttyUSB*", "/dev/ttyACM*"]
    PRINTER_RECONNECT_MS = 5000    # Intervalo de reconexión (5s)
    PRINTER_SERIAL_TIMEOUT = 2.0
