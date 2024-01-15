# color_schemes.py
from enum import Enum, auto
# no ELEGANT 	
# Vbrant red
# TECH tecnology
# Natural green
class ColorScheme(Enum):
    MODERN = {"main": "#EAEAEA", "secondary": "#003366", "accent": "#00BFFF","display":"#F0F0F0","pillar":"#002244"}
    VIBRANT = {"main": "#FFDAB9", "secondary": "#8B0000", "accent": "#FFD700","display":"#F0F0F0"}
    NATURAL = {"main": "#FFF8DC", "secondary": "#228B22", "accent": "#98FB98","display":"#F0F0F0"}
    ELEGANT = {"main": "#E6E6FA", "secondary": "#4169E1", "accent": "#EEDC82","display":"#F0F0F0"}
    TECH = {"main": "#2F4F4F", "secondary": "#7DF9FF", "accent": "#C0C0C0","display":"#F0F0F0"}

    def __str__(self):
        return f"Main: {self.value['main']}, Secondary: {self.value['secondary']}, Accent: {self.value['accent']}"


