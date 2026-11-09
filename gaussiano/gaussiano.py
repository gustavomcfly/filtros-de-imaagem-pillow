"""Versão 3 - Filtro GAUSSIANO (ImageFilter.GaussianBlur) com raios 1, 2 e 3."""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import ImageFilter
from utils_filtros import executar

filtros = {
    f"Gaussiano raio={r}": (lambda img, r=r: img.filter(ImageFilter.GaussianBlur(radius=r)))
    for r in (1, 2, 3)           # radius = desvio padrão (sigma) da gaussiana
}
executar("v3", filtros, "versao3_gaussiano.png")