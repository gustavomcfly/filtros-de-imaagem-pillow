"""Versão 1 - Filtro da MEDIANA (ImageFilter.MedianFilter) com janelas 3, 5 e 7."""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import ImageFilter
from utils_filtros import executar

filtros = {
    f"Mediana {s}x{s}": (lambda img, s=s: img.filter(ImageFilter.MedianFilter(size=s)))
    for s in (3, 5, 7)           # tamanho da janela (precisa ser ímpar)
}
executar("v1", filtros, "versao1_mediana.png")