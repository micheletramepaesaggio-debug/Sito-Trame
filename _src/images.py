"""Converte le immagini originali di _materiali/ in versioni ottimizzate per il web.

Uso: python3 _src/images.py
Ogni immagine viene esportata in JPEG a più larghezze (srcset) in assets/img/<cartella>/.
"""
from pathlib import Path
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_materiali" / "04_immagini_casi_studio"
OUT = ROOT / "assets" / "img"
WIDTHS = (800, 1400, 2200)

# (file originale, cartella, nome di uscita, ritaglio opzionale come frazioni l,t,r,b)
IMAGES = [
    ("2. Ingresso 02.12.25 hortus.jpg", "hortus", "ingresso", None),
    ("1. Ingresso Parcheggio_30.11.25_hortus.jpg", "hortus", "ingresso-parcheggio", None),
    ("6_Assonometria concept_24.12.25hortus.jpg", "hortus", "concept-colore", (0.18, 0.12, 0.98, 0.88)),
    ("immagine paternostro_26.08.26_1.jpg", "paternostro", "padiglione-uliveto", None),
    ("paternostro.png", "paternostro", "padiglione-vista", None),
    ("schizzo padiglione paternostro.jpg", "paternostro", "schizzo-padiglione", None),
    ("WhatsApp Image 2026-04-14 at 15.41.12paternostro.jpg", "paternostro", "schizzo-studio", None),
    ("3_panorama poggetello_23.09.26.jpg", "poggetello", "terrazza-panorama", None),
    ("2_padiglione_22.09.26.jpg", "poggetello", "padiglione", None),
    ("1_fontana poggetello_22.09.26.jpg", "poggetello", "fontana", None),
    ("ChatGPT Image 23 set 2026, 10_12_19 borgo pogetello.png", "poggetello", "terrazza-tramonto", None),
    ("vista panorama__22.09.26borgo pogetello.jpg", "poggetello", "prato-pergolato", None),
    ("VILLA CLODIA_volo d uccello_17.09.26.jpg", "villa-clodia", "vista-alto", None),
    ("VILLA CLODIA_agrumeto_17.09.26.jpg", "villa-clodia", "agrumeto", None),
    ("VILLA CLODIA_forno2_17.09.26.jpg", "villa-clodia", "forno", None),
    ("VILLA CLODIA_strada terrastabilizzata forno_17.09.26.jpg", "villa-clodia", "percorso", None),
    ("schizzi villa c.jpg", "villa-clodia", "schizzi", None),
    ("VISTA3 park hotel.jpg", "park-hotel-sabina", "vista-alto", None),
    ("cartolina park hotel sabina 19.05.25.jpg", "park-hotel-sabina", "cartolina", None),
]


# Loghi delle strutture: (file originale, nome di uscita)
LOGOS_SRC = ROOT / "_materiali" / "06_loghi_strutture"
LOGOS = [
    ("logo hortus natural living.jpg", "hortus"),
    ("logo park hotel sabina.png", "park-hotel-sabina"),
    ("logo borgo pogetello.png", "borgo-poggetello"),
    ("logo tenuta paternostro.png", "tenuta-paternostro"),
]


def export_logo(src, name):
    """Ritaglia i margini vuoti e salva il logo in PNG a 480 px di larghezza massima."""
    im = Image.open(LOGOS_SRC / src).convert("RGBA")
    # bordo da ritagliare: pixel trasparenti oppure quasi bianchi
    px = im.load()
    w, h = im.size
    mask = Image.new("L", im.size, 0)
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 20 and not (r > 245 and g > 245 and b > 245):
                mp[x, y] = 255
    box = mask.getbbox()
    if box:
        pad = int(max(w, h) * 0.04)
        box = (max(0, box[0] - pad), max(0, box[1] - pad), min(w, box[2] + pad), min(h, box[3] + pad))
        im = im.crop(box)
    im.thumbnail((480, 480), Image.LANCZOS)
    dest = OUT / "loghi"
    dest.mkdir(parents=True, exist_ok=True)
    im.save(dest / f"{name}.png", optimize=True)
    print(f"loghi/{name}: {im.width}x{im.height}")


def export(src, folder, name, crop):
    im = Image.open(SRC / src)
    im = ImageOps.exif_transpose(im)
    if im.mode != "RGB":
        im = im.convert("RGB")
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    dest = OUT / folder
    dest.mkdir(parents=True, exist_ok=True)
    for width in WIDTHS:
        if width > im.width and width != WIDTHS[0]:
            continue
        copy = im.copy()
        if copy.width > width:
            copy = copy.resize((width, round(copy.height * width / copy.width)), Image.LANCZOS)
        copy.save(dest / f"{name}-{width}.jpg", "JPEG", quality=80, optimize=True, progressive=True)
    print(f"{folder}/{name}: {im.width}x{im.height}")


if __name__ == "__main__":
    for args in IMAGES:
        export(*args)
    for args in LOGOS:
        export_logo(*args)
