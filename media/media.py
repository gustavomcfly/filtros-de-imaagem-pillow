"""Versão 2 - Filtro da MÉDIA (ImageFilter.BoxBlur) com raios 1, 2 e 3."""
from PIL import ImageFilter
from utils_filtros import executar

filtros = {
    f"Media raio={r}": (lambda img, r=r: img.filter(ImageFilter.BoxBlur(radius=r)))
    for r in (1, 2, 3)           # janela de (2r+1) x (2r+1) pixels
}
executar("v2", filtros, "versao2_media.png")