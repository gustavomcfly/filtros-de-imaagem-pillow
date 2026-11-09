"""
Funções auxiliares usadas pelas três versões (mediana, média e gaussiano).
Os FILTROS vêm do módulo ImageFilter do Pillow; o Numpy é usado só para
calcular as métricas e a Pillow para montar os painéis de comparação.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ARQUIVO = "salt_peper_1.png"


def carregar():
    """Abre a imagem ruidosa e converte para tons de cinza (modo 'L')."""
    return Image.open(ARQUIVO).convert("L")


def _gradiente(img):
    """Magnitude do gradiente (diferenças entre pixels vizinhos)."""
    a = np.asarray(img, dtype=float)
    gx = np.abs(np.diff(a, axis=1))[:-1, :]
    gy = np.abs(np.diff(a, axis=0))[:, :-1]
    return np.hypot(gx, gy)


def metricas(img):
    """
    Métricas sem imagem de referência (não existe versão limpa da foto):
      ruido    - desvio padrão numa região de céu (quase uniforme).
                 Quanto MENOR, mais ruído foi removido.
      nitidez  - percentil 99 do gradiente: força das bordas mais fortes.
                 Quanto MAIOR, mais detalhe foi preservado
                 (mas no original/filtros fracos o ruído também a eleva).
      extremos - % de pixels exatamente pretos (0) ou brancos (255).
    """
    a = np.asarray(img, dtype=float)
    ruido = a[5:65, 5:200].std()
    nitidez = np.percentile(_gradiente(img), 99)
    extremos = 100 * np.mean((a == 0) | (a == 255))
    return {"ruido": ruido, "nitidez": nitidez, "extremos": extremos}


def _fonte(tam):
    for nome in ("DejaVuSans-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf"):
        try:
            return ImageFont.truetype(nome, tam)
        except OSError:
            pass
    try:
        return ImageFont.load_default(size=tam)
    except TypeError:
        return ImageFont.load_default()


def montar_painel(imagens, titulos, colunas=2, arquivo="painel.png"):
    """Cola as imagens em grade, cada uma com um título acima."""
    w, h = imagens[0].size
    barra = 34
    linhas = (len(imagens) + colunas - 1) // colunas
    painel = Image.new("L", (colunas * w, linhas * (h + barra)), 255)
    d = ImageDraw.Draw(painel)
    fonte = _fonte(16)
    for k, (im, t) in enumerate(zip(imagens, titulos)):
        x, y = (k % colunas) * w, (k // colunas) * (h + barra)
        painel.paste(im, (x, y + barra))
        d.text((x + 8, y + 8), t, fill=0, font=fonte)
    painel.save(arquivo)
    return painel


def executar(nome, filtros, arquivo_painel):
    """
    Aplica cada filtro do dicionário {rótulo: função(img)->img}, imprime as
    métricas e salva o painel (original + resultados).
    """
    original = carregar()
    imagens, titulos = [original], []
    m0 = metricas(original)
    titulos.append(f"Original  ruido={m0['ruido']:.1f}  nitidez={m0['nitidez']:.0f}")
    print(f"{'Original':<22} ruido={m0['ruido']:6.2f} nitidez={m0['nitidez']:6.1f} "
          f"extremos={m0['extremos']:5.2f}%")
    for rotulo, f in filtros.items():
        res = f(original)
        m = metricas(res)
        imagens.append(res)
        titulos.append(f"{rotulo}  ruido={m['ruido']:.1f}  nitidez={m['nitidez']:.0f}")
        print(f"{rotulo:<22} ruido={m['ruido']:6.2f} nitidez={m['nitidez']:6.1f} "
              f"extremos={m['extremos']:5.2f}%")
        res.save(f"{nome}_{rotulo.replace(' ', '_').replace('=', '')}.png")
    montar_painel(imagens, titulos, colunas=2, arquivo=arquivo_painel)
    print("Painel salvo em", arquivo_painel)