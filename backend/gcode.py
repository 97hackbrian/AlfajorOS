#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador y Parser de G-Code - Proyecto de Grado
Genera G-Code para patrones de crema sobre alfajores.
"""

import math
from backend.config import SystemConfig


class GCodeGenerator:
    """Genera G-Code para patrones de extrusión de crema."""

    def __init__(self):
        self.velocidad = SystemConfig.VELOCIDAD_DEFAULT
        self.grosor = SystemConfig.GROSOR_LINEA_DEFAULT
        self.diametro = SystemConfig.ALFAJOR_DIAMETRO_CM * 10  # mm
        self.centro_x = self.diametro / 2
        self.centro_y = self.diametro / 2

    def generar_header(self):
        """Genera el header estándar del G-Code."""
        return (
            "; === G-Code Extrusora de Crema ===\n"
            "; Proyecto de Grado - Alfajores\n"
            ";\n"
            "G28          ; Home todos los ejes\n"
            "G1 Z10 F1000 ; Subir boquilla\n"
            f"M104 S{SystemConfig.TEMP_CREMA_DEFAULT}     ; Temp crema\n"
            f"M109 S{SystemConfig.TEMP_CREMA_DEFAULT}     ; Esperar temp crema\n"
            "G92 E0       ; Reset extrusor\n"
            ";\n"
            "; === Purga inicial ===\n"
            "G1 X5 Y5 F1500\n"
            "G1 E5 F300   ; Purgar crema\n"
            "G92 E0       ; Reset extrusor\n"
        )

    def generar_footer(self):
        """Genera el footer estándar del G-Code."""
        return (
            ";\n"
            "; === Fin ===\n"
            "G1 E-2 F500  ; Retracción crema\n"
            "G1 Z20 F1000 ; Subir boquilla\n"
            "G28 X Y      ; Home XY\n"
        )

    def generar_espiral(self, vueltas=4):
        """Genera G-Code para patrón espiral."""
        lines = ["; === Patrón espiral ===\n"]
        lines.append(f"G1 Z{SystemConfig.ALFAJOR_ALTURA_CREMA_MM} F500\n")
        lines.append(f"G1 X{self.centro_x} Y{self.centro_y} F1000\n")

        radio_max = (self.diametro / 2) - SystemConfig.ALFAJOR_MARGEN_MM
        pasos = vueltas * 36
        e_total = 0

        for i in range(pasos):
            angulo = math.radians(i * 10)
            radio = (i / pasos) * radio_max
            x = self.centro_x + radio * math.cos(angulo)
            y = self.centro_y + radio * math.sin(angulo)
            e_total += 0.3
            lines.append(f"G1 X{x:.1f} Y{y:.1f} E{e_total:.1f} F{self.velocidad * 60}\n")

        return "".join(lines)

    def generar_zigzag(self, lineas=8):
        """Genera G-Code para patrón zigzag."""
        lines = ["; === Patrón zigzag ===\n"]
        lines.append(f"G1 Z{SystemConfig.ALFAJOR_ALTURA_CREMA_MM} F500\n")

        margen = SystemConfig.ALFAJOR_MARGEN_MM
        paso = (self.diametro - 2 * margen) / lineas
        e_total = 0

        for i in range(lineas):
            y = margen + i * paso
            if i % 2 == 0:
                x_start, x_end = margen, self.diametro - margen
            else:
                x_start, x_end = self.diametro - margen, margen
            e_total += 2.0
            lines.append(f"G1 X{x_start:.1f} Y{y:.1f} F{self.velocidad * 60}\n")
            lines.append(f"G1 X{x_end:.1f} Y{y:.1f} E{e_total:.1f} F{self.velocidad * 60}\n")

        return "".join(lines)

    def generar_completo(self, patron="Espiral clasica"):
        """Genera G-Code completo para un patrón."""
        code = self.generar_header()

        if "espiral" in patron.lower():
            code += self.generar_espiral()
        elif "zigzag" in patron.lower():
            code += self.generar_zigzag()
        else:
            code += self.generar_espiral()

        code += self.generar_footer()
        return code


class GCodeParser:
    """Parser básico de G-Code."""

    @staticmethod
    def validar(gcode_text):
        """Valida que el G-Code sea sintácticamente correcto."""
        errores = []
        for i, linea in enumerate(gcode_text.split("\n"), 1):
            linea = linea.strip()
            if not linea or linea.startswith(";"):
                continue
            # Verificar que empiece con un comando válido
            cmd = linea.split()[0].upper()
            if not any(cmd.startswith(p) for p in ("G", "M", "T", ";")):
                errores.append(f"Línea {i}: comando no reconocido '{cmd}'")

        return len(errores) == 0, errores

    @staticmethod
    def contar_lineas(gcode_text):
        """Cuenta líneas de código (no comentarios ni vacías)."""
        count = 0
        for linea in gcode_text.split("\n"):
            linea = linea.strip()
            if linea and not linea.startswith(";"):
                count += 1
        return count
