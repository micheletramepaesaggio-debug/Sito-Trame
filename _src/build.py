"""Genera le pagine HTML del sito a partire dai template in _src/.

Uso:  python3 _src/build.py
Richiede: Jinja2 e Pillow (pip install jinja2 pillow)

Le pagine generate (index.html, chi-siamo.html, casi-studio/*.html, ...) vanno
pubblicate così come sono, insieme alla cartella assets/. Per modificare un testo,
intervenire sui template in _src/pages/ o sui dati qui sotto, poi rilanciare lo script.
"""
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup, escape
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(__file__).resolve().parent
SITE_URL = "https://tramedipaesaggioatelier.it/"

TBC = "DA COMPLETARE"

COMPANY = {
    "legal_name": "Trame di Paesaggio Atelier",
    "address": "Strada della Contessa, 01019 Vetralla (VT)",
    "vat": "02424620561",
    "email": "tramedipaesaggioatelier@gmail.com",
    "phone": "334 8357657",
    "phone_href": "+393348357657",
    "instagram": "https://www.instagram.com/tramedipaesaggioatelier",
    "privacy": "https://www.iubenda.com/privacy-policy/85171804",
    "cookie": "https://www.iubenda.com/privacy-policy/85171804/cookie-policy",
}

# Servizi comuni ai casi studio, riscritti senza linguaggio da studio tecnico.
SERVICES = [
    "Valutazione paesaggistica online",
    "Visione d'insieme dello spazio esterno",
    "Disegno del paesaggio, dall'idea al dettaglio",
    "Immagini fotorealistiche",
    "Disegno della luce",
    "Regia della realizzazione",
]

# Ogni blocco narrativo: ("h", sottotitolo) oppure ("p", [righe]).
# Le righe di un paragrafo vanno a capo una per una, come nei copy originali.
CASES = [
    {
        "slug": "villa-clodia",
        "published": True,
        "website": "https://www.villaclodia.com/",
        "logo": "villa-clodia",
        "name": "Villa Clodia",
        "subtitle": "Quando il dislivello diventa il progetto",
        "claim": "Tre giardini su un unico pendio.",
        "place_short": "Manziana",
        "details": [
            ("Località", "Manziana"),
            ("Anno", "2026 — in corso"),
            ("Superficie", "1.800 mq"),
            ("Tipologia", "Villino privato / Struttura ricettiva"),
        ],
        "services": SERVICES,
        "hero": "villa-clodia/vista-alto",
        "hero_alt": "Vista dall'alto dei nuovi giardini a terrazze di Villa Clodia, tra la villa storica e il paesaggio di Manziana",
        "card": "villa-clodia/agrumeto",
        "situazione_title": "Un terreno in pendenza. Una preoccupazione reale.",
        "situazione": [
            ("p", ["Villa Clodia è un nome noto.", "Una struttura storica, rinomata, immersa nel paesaggio di Manziana."]),
            ("p", ["Il villino adiacente era tutta un'altra storia.", "Spazi da ripensare da zero.",
                   "E fuori, un terreno in forte pendenza che sembrava un problema senza soluzione."]),
            ("p", ["Il titolare era preoccupato.", "Come si valorizza un dislivello così importante?",
                   "Come si rende vivibile uno spazio che la pendenza sembrava rendere inutilizzabile?"]),
            ("p", ["La risposta non era combattere il terreno.", "Era ascoltarlo."]),
        ],
        "approccio_title": "Il dislivello come struttura del progetto",
        "approccio": [
            ("p", ["Anche in questo caso, il progetto è iniziato prima del sopralluogo.",
                   "Lettura da remoto dello spazio, del contesto, del territorio.", "Quando siamo arrivati, avevamo già una visione."]),
            ("p", ["Il dislivello non era un problema.", "Era la struttura del progetto."]),
            ("p", ["Abbiamo trasformato la pendenza in una sequenza di tre piani all'aperto, ognuno con una funzione precisa e un'identità distinta."]),
            ("h", "Piano superiore — Il Teatro del Convivio"),
            ("p", ["Un tavolo imperiale affacciato sul paesaggio di Manziana.",
                   "Lo spazio per gli eventi, i pranzi, i momenti da ricordare.",
                   "Qui la relazione visiva con il territorio è protagonista."]),
            ("h", "Piano intermedio — Il Giardino Segreto"),
            ("p", ["Il cuore verde del progetto.", "Essenze xerofite selezionate, uno spazio raccolto e sensoriale.",
                   "Un luogo che si scopre.", "Che non si vede dall'esterno.", "Che sorprende chi ci arriva."]),
            ("h", "Piano inferiore — Il Giardino delle Pietre"),
            ("p", ["L'inizio del percorso, dal parcheggio in basso.",
                   "Un paesaggio più naturale, più aperto, che introduce il visitatore al racconto."]),
            ("p", ["Due modi per muoversi.", "Chi vuole esplorare segue il percorso lento attraverso i giardini.",
                   "Chi ha fretta sale direttamente con le scale."]),
            ("p", ["Il risultato è uno spazio che funziona a più velocità.", "Che si adatta all'ospite.",
                   "Che valorizza ogni centimetro di dislivello invece di ignorarlo."]),
            ("p", ["Tutto costruito con materiali locali, essenze adatte al clima, nel rispetto del carattere del luogo.",
                   "E con una relazione visiva con il paesaggio di Manziana che il progetto amplifica invece di nascondere."]),
        ],
        "gallery": [
            ("villa-clodia/agrumeto", "L'agrumeto sotto il pergolato: un giardino raccolto, tra prato, pietra e fioriture.", "wide"),
            ("villa-clodia/forno", "Il forno all'aperto, tra cipressi, ulivi e lavanda.", ""),
            ("villa-clodia/percorso", "Il percorso lungo il muro in pietra, verso il forno.", ""),
            ("villa-clodia/vista-alto", "Vista dall'alto: i giardini a terrazze tra la villa e il paesaggio di Manziana.", "wide"),
            ("villa-clodia/schizzi", "I primi schizzi: il pendio letto come una sequenza di piani all'aperto.", "wide"),
        ],
        "quote": ("Quello che sembrava il limite principale del terreno è diventato l'elemento più caratteristico del progetto. "
                  "Non avrei immaginato che la pendenza potesse diventare un punto di forza.",
                  "Leonardo, Villa Clodia"),
        "cta_title": "Hai uno spazio con un vincolo che non sai come affrontare?",
        "cta_text": "Spesso è proprio lì che si nasconde il progetto più interessante. Inizia con una valutazione paesaggistica online, gratuita e senza impegno.",
    },
    {
        "slug": "hortus-natural-living",
        "published": True,
        "website": "https://www.hortustodi.it/",
        "logo": "hortus",
        "video": {
            "drive_id": "1_lz4-zj7lMV10SNzxT1aDJx9nrYblEGq",
            "poster": "hortus/ingresso",
            "title": "Il giardino in movimento",
            "text": "La visione del nuovo giardino, in un video 3D.",
        },
        "name": "Hortus Natural Living",
        "subtitle": "Il Giardino dei Frammenti e dei Profumi Perduti",
        "claim": "Una tenuta in Umbria che impara a raccontarsi.",
        "place_short": "Todi, Umbria",
        "details": [
            ("Località", "Todi, Umbria"),
            ("Anno", "2025 — 2026"),
            ("Superficie", "1.800 mq"),
            ("Tipologia", "Struttura ricettiva / Agriturismo"),
        ],
        "services": SERVICES,
        "hero": "hortus/ingresso",
        "hero_alt": "Disegno dell'ingresso di Hortus Natural Living: un sentiero in pietra tra cipressi e fioriture",
        "card": "hortus/ingresso",
        "situazione_title": "L'esterno che non raccontava nulla",
        "situazione": [
            ("p", ["Hortus Natural Living è una struttura di valore reale.",
                   "Interni curati, posizione straordinaria sulle colline di Todi, un'accoglienza genuina."]),
            ("p", ["Ma gli spazi esterni erano rimasti indietro.", "Disallineati rispetto al resto.",
                   "Un'area che non raccontava nulla.", "E che nelle foto, non aiutava."]),
            ("p", ["Il titolare lo sapeva.", "Voleva un salto di qualità vero.", "Non più verde.",
                   "Voleva che l'ospite fosse accompagnato.", "Quasi senza accorgersene.", "Da un percorso con una regia."]),
        ],
        "approccio_title": "Il giardino come sequenza di stanze all'aperto",
        "approccio": [
            ("p", ["Prima ancora di arrivare in loco, abbiamo analizzato lo spazio da remoto.",
                   "Immagini, contesto, territorio.", "Quando ci siamo incontrati, avevamo già una visione."]),
            ("p", ["Il progetto parte da un'idea semplice: il giardino come sequenza di stanze all'aperto.",
                   "Non uno spazio da attraversare.", "Uno spazio da vivere."]),
            ("p", ["Dal vialetto d'ingresso fino all'area del giardino, ogni elemento ha una funzione.",
                   "Ogni scelta racconta qualcosa."]),
            ("list", ["Essenze xerofite che guidano lo sguardo lungo il percorso.",
                      "Sentieri in scaglie di pietra umbra: materiale locale, sostenibile, narrativo.",
                      "Una seduta in pietra con specchio d'acqua integrato, punto di sosta e contemplazione.",
                      "Un albero di Giuda come elemento poetico e focale.",
                      "Aiuole con bordure in pietra locale.",
                      "Un'area con tavolo imperiale per eventi, aperitivi, esperienze all'aperto."]),
            ("p", ["Ogni cosa al suo posto.", "Con una regia precisa."]),
            ("h", "Una prateria mediterranea"),
            ("p", ["Per le piante abbiamo lasciato che le specie si mescolassero come in natura, compenetrandosi nello stesso spazio.",
                   "Il risultato non è un giardino botanico per macchie ordinate.",
                   "È una prateria mediterranea che cambia con le stagioni, con fioriture continue da gennaio a ottobre."]),
            ("h", "La luce della sera"),
            ("p", ["Per la luce abbiamo disegnato un sistema integrato, con tre famiglie di luci calde.",
                   "Valorizzano le masse vegetali, i cipressi, gli ulivi e creano atmosfera nelle ore serali.",
                   "Perché di notte lo spazio deve continuare a raccontare."]),
        ],
        "gallery": [
            ("hortus/concept-colore", "La visione d'insieme: il nuovo giardino tra la tenuta e le colline di Todi.", "wide"),
            ("hortus/ingresso-parcheggio", "L'arrivo: il percorso accoglie l'ospite fin dal parcheggio.", "wide"),
        ],
        "quote": ("Volevo che l'ospite fosse accompagnato nel giardino, quasi senza accorgersene. "
                  "Federico ha costruito esattamente questo: un percorso che ti prende per mano.",
                  "Pasquale, titolare Hortus Natural Living"),
        "cta_title": "Vuoi vedere cosa può diventare il tuo spazio?",
        "cta_text": "Inizia con una valutazione paesaggistica online. In 30 minuti capiamo insieme il potenziale della tua struttura.",
    },
    {
        "slug": "park-hotel-sabina",
        "published": True,
        "website": "https://www.parkhotelsabina.com/",
        "logo": "park-hotel-sabina",
        "name": "Park Hotel Sabina",
        "subtitle": "Un giardino che chiede poco e restituisce molto",
        "claim": "Fino all'80% di acqua e al 70% di risorse in meno.",
        "place_short": "Magliano Sabina, Rieti",
        "details": [
            ("Località", "Magliano Sabina, Rieti"),
            ("Anno", "2025"),
            ("Superficie", "300 mq"),
            ("Tipologia", "Hotel"),
        ],
        "services": None,
        "hero": "park-hotel-sabina/giardino",
        "hero_alt": "Il giardino di Park Hotel Sabina: un percorso in pietra tra fioriture mediterranee, ulivi e vele ombreggianti",
        "card": "park-hotel-sabina/giardino",
        "draft_note": "Testo scritto dall'atelier a partire dalle immagini: da verificare con la situazione reale della struttura.",
        "situazione_title": "Il verde che costa, e non racconta",
        "situazione": [
            ("p", ["Le aree verdi tradizionali chiedono molto.", "Acqua, cura continua, risorse.",
                   "E spesso restituiscono poco: un prato da mantenere, non uno spazio da vivere."]),
            ("p", ["Park Hotel Sabina voleva un esterno all'altezza dell'accoglienza.",
                   "Un luogo dove fermarsi, non solo da attraversare.",
                   "Senza moltiplicare i consumi."]),
            ("tbc", "Dettagli sulla situazione iniziale degli spazi esterni"),
        ],
        "approccio_title": "Il giardino secco, nella sua forma più completa",
        "approccio": [
            ("p", ["Abbiamo ripensato lo spazio come un paesaggio da abitare.",
                   "Percorsi in pietra che disegnano stanze all'aperto.",
                   "Ulivi e cipressi a dare struttura e ombra."]),
            ("p", ["Tra i percorsi, aiuole di piante xerofile che si mescolano come in natura.",
                   "Fioriture gialle, bianche, rosate.", "Graminacee che si muovono con il vento."]),
            ("p", ["Ogni area ha una funzione.",
                   "Le sedute sotto le vele ombreggianti, per una pausa all'ombra.",
                   "Lo specchio d'acqua, punto di quiete.",
                   "La terrazza dei lettini, affacciata sul verde.",
                   "La fila di ombrelloni, per pranzi e aperitivi all'aperto."]),
            ("h", "Il risultato"),
            ("p", ["Fino all'80% di acqua e al 70% di risorse in meno rispetto alle aree verdi tradizionali.",
                   "Una cura ridotta nel tempo.",
                   "E un giardino che, invece di consumarsi, matura con gli anni."]),
        ],
        "gallery": [
            ("park-hotel-sabina/vista-alto", "Il giardino visto dall'alto: percorsi, stanze all'aperto, terrazza dei lettini.", "wide"),
            ("park-hotel-sabina/percorso", "Il percorso centrale, tra aiuole di piante xerofile e graminacee.", ""),
            ("park-hotel-sabina/pianta", "Il disegno delle essenze, aiuola per aiuola.", ""),
            ("park-hotel-sabina/cartolina", "La visione dell'atelier: sedute all'ombra degli ulivi, tra fioriture xerofile.", "wide"),
        ],
        "quote": None,
        "cta_title": "Quanto ti costa, oggi, il tuo verde?",
        "cta_text": "Inizia con una valutazione paesaggistica online. In 30 minuti capiamo insieme come trasformarlo in un paesaggio che consuma meno e vale di più.",
    },
    {
        "slug": "borgo-poggetello",
        "published": True,
        "website": "https://www.borgopoggetello.com/",
        "logo": "borgo-poggetello",
        "logo_dark": True,
        "name": "Borgo Poggetello",
        "subtitle": "La soglia tra il paese e il bosco",
        "claim": "Un giardino che era già pieno di storie.",
        "place_short": "Poggetello, L'Aquila",
        "details": [
            ("Località", "Poggetello, L'Aquila"),
            ("Anno", "2026 — in corso"),
            ("Superficie", None),
            ("Tipologia", "Struttura ricettiva / Ristorazione"),
        ],
        "services": SERVICES,
        "hero": "poggetello/terrazza-panorama",
        "hero_alt": "La terrazza di Borgo Poggetello al tramonto, sotto la tenda leggera, con la vista sulla valle",
        "card": "poggetello/terrazza-panorama",
        "situazione_title": "Un giardino che era già pieno di storie",
        "situazione": [
            ("p", ["Borgo Poggetello non è uno spazio anonimo.", "È un luogo che vive.",
                   "Un ristorante attivo, un braciere che è già il punto di forza della serata, ospiti che si fermano più del previsto."]),
            ("p", ["Ma il giardino non rifletteva ancora tutto questo.", "Spazi poco leggibili.",
                   "Un angolo che gli ospiti evitavano, perché sembrava non essere per loro.",
                   "Un terrazzamento verso il bosco che restava inespresso."]),
            ("p", ["I proprietari avevano già capito una cosa fondamentale.",
                   "Il braciere funzionava perché creava un'esperienza.",
                   "Serviva applicare la stessa logica a tutto il resto."]),
        ],
        "approccio_title": "Il giardino come soglia",
        "approccio": [
            ("p", ["Il punto di partenza è stato il luogo stesso.", "Poggetello è storicamente la porta del paese.",
                   "Il confine tra l'abitato e il bosco."]),
            ("p", ["Il progetto ha preso questa identità e l'ha trasformata in idea: il giardino come soglia.",
                   "Uno spazio che accompagna l'ospite dal paese verso la natura, senza interruzioni nette."]),
            ("h", "L'ingresso"),
            ("p", ["Una pergola accoglie chi arriva.",
                   "Crea gerarchia, ombra, una prima relazione visiva con il bosco e con il braciere."]),
            ("h", "Il padiglione del tè"),
            ("p", ["Un rifugio materico in legno, che richiama la capanna primigenia.",
                   "Una cornice verso il bosco, una soglia tra dentro e fuori.",
                   "Su richiesta della proprietà, lo abbiamo reso più aperto e permeabile.",
                   "Lo spazio deve essere percepito come accessibile, non come un angolo riservato."]),
            ("h", "Il braciere"),
            ("p", ["Confermato come elemento centrale.",
                   "È l'attrattore serale, l'effetto falò, la ragione per cui gli ospiti restano.",
                   "Il progetto lo valorizza con una seduta pensata apposta."]),
            ("h", "I terrazzamenti verso il bosco"),
            ("p", ["Il sistema più ambizioso del progetto.",
                   "Camminamenti ridisegnati con pietra calcarea locale, legno e ferro.",
                   "La storica vasca in marmo per gli animali, mantenuta e integrata nel nuovo disegno.",
                   "Una fontana sul livello superiore, un'area benessere su quello inferiore."]),
            ("p", ["L'intero sistema è pensato come un museo all'aperto.",
                   "Un aratro storico trova posto come elemento espositivo.",
                   "Ogni oggetto del passato del Borgo torna a raccontare qualcosa."]),
            ("h", "Il prato e il pergolato"),
            ("p", ["Per l'area eventi, la scelta è andata verso un sistema leggero: ferro, cavi, tende retrattili.",
                   "Più tenda che pergola.", "Più reversibile, più flessibile, meno impattante."]),
            ("p", ["Il prato centrale, pensato per resistere al passaggio degli eventi, utilizza specie xerofile scelte per densità e resistenza."]),
            ("p", ["Tutto il progetto utilizza materiali già presenti nel luogo: pietra calcarea, legno lavorato localmente, ferro.",
                   "Non per risparmiare.", "Per restare fedeli a un'identità rurale che non va inventata.", "Va solo fatta emergere."]),
        ],
        "gallery": [
            ("poggetello/padiglione", "Dalla pergola d'ingresso, lo sguardo attraversa il giardino fino al padiglione del tè.", "wide"),
            ("poggetello/terrazza-panorama", "La terrazza verso la valle, sotto la tenda leggera, con il muro di foglie.", ""),
            ("poggetello/fontana", "La fontana sui terrazzamenti: pietra calcarea locale, acqua, essenze.", ""),
        ],
        "quote": ("Il braciere funzionava perché creava un'esperienza. Il team di Trame di Paesaggio ha preso "
                  "quella stessa logica e l'ha applicata a tutto il giardino. Ora ogni angolo ha una ragione per essere vissuto.",
                  "Mario, Borgo Poggetello"),
        "cta_title": "La tua struttura ha già un punto di forza. Il resto dello spazio lo riflette?",
        "cta_text": "A volte basta prendere quello che già funziona e applicarlo a tutto il resto. Inizia con una valutazione paesaggistica online, gratuita e senza impegno.",
    },
    {
        "slug": "tenuta-paternostro",
        "published": True,
        "website": "https://tenutadipaternostro.it/",
        "logo": "tenuta-paternostro",
        "name": "Tenuta Paternostro",
        "subtitle": "Un uliveto che torna a vivere",
        "claim": "Un padiglione che non si impone. Si appoggia.",
        "place_short": "Vetralla, Viterbo",
        "details": [
            ("Località", "Vetralla, Viterbo"),
            ("Anno", "2026"),
            ("Superficie coperta", "340 mq di padiglione"),
            ("Tipologia", "Tenuta agricola / Spazio eventi"),
        ],
        "services": SERVICES,
        "hero": "paternostro/padiglione-uliveto",
        "hero_alt": "Il padiglione in legno di Tenuta Paternostro tra gli ulivi, nella luce del pomeriggio",
        "card": "paternostro/padiglione-uliveto",
        "situazione_title": "Un uliveto bellissimo. Inutilizzato.",
        "situazione": [
            ("p", ["Tenuta Paternostro è immersa nel paesaggio della Tuscia.",
                   "Un fondo agricolo di quasi 2,5 ettari, coltivato a ulivo.",
                   "Ulivi vetrallesi, paesaggio autentico, aria che sa di campagna vera."]),
            ("p", ["Ma tutto quello spazio non lavorava.", "Era lì.", "Bello da vedere.", "Impossibile da vivere."]),
            ("p", ["La proprietaria aveva una visione chiara.",
                   "Voleva trasformare quell'uliveto in un luogo dove le persone potessero fermarsi davvero.",
                   "Yoga, meditazione, ritiri aziendali, eventi privati.",
                   "Uno spazio per ritrovare il respiro.", "A contatto diretto con il paesaggio."]),
            ("p", ["Mancava solo la struttura giusta per farlo."]),
        ],
        "approccio_title": "La risposta era già nel terreno",
        "approccio": [
            ("p", ["Un padiglione in legno lamellare certificato PEFC/FSC, inserito nell'uliveto senza forzarlo.",
                   "Rivestito in doghe di legno naturale, con una copertura che segue il profilo del paesaggio.",
                   "Un edificio che non si impone.", "Si appoggia."]),
            ("p", ["Il progetto ha lavorato sulla relazione tra dentro e fuori.",
                   "Il padiglione non è un contenitore chiuso.", "È un filtro tra l'ospite e il paesaggio."]),
            ("p", ["Grandi aperture sui fronti.", "Un portico di 98 mq aperto sul verde.",
                   "La vista sugli ulivi sempre presente, da ogni angolo dello spazio interno."]),
            ("p", ["Chi viene per un ritiro di yoga non vede quattro mura.",
                   "Vede il cielo, gli ulivi, la luce che cambia nel corso della giornata."]),
            ("p", ["Chi organizza un evento aziendale trova uno spazio che decomprime.",
                   "Che abbassa la guardia.", "Che mette le persone in uno stato diverso."]),
            ("p", ["Materiali locali, costruzione a basso impatto, piena armonia con il Paesaggio Agrario di Valore della Tuscia.",
                   "Non per obbligo.", "Per scelta.",
                   "Perché il paesaggio di Vetralla merita di essere rispettato.", "E amplificato."]),
        ],
        "gallery": [
            ("paternostro/padiglione-tramonto", "Il padiglione al tramonto: il portico aperto sull'uliveto.", "wide"),
            ("paternostro/schizzo-padiglione", "Il primo schizzo del padiglione tra gli ulivi.", ""),
            ("paternostro/pianta-padiglione", "La pianta del padiglione, tra le chiome degli ulivi.", ""),
            ("paternostro/padiglione-vista", "Il padiglione nel paesaggio della Tuscia.", "wide"),
            ("paternostro/schizzo-studio", "Dallo schizzo alla forma: la copertura che segue il paesaggio.", "wide"),
        ],
        "quote": ("Volevo che chi veniva qui si sentisse dentro il paesaggio, non di fronte ad esso. "
                  "Il progetto ha fatto esattamente questo.",
                  "Olivia, proprietaria Tenuta Paternostro"),
        "cta_title": "Hai uno spazio agricolo o naturale con potenziale inespresso?",
        "cta_text": "Possiamo aiutarti a capire cosa può diventare. Inizia con una valutazione paesaggistica online, gratuita e senza impegno.",
    },

]

PAGES = [
    # (template, file di uscita, titolo, descrizione, voce di menu attiva)
    ("index.html", "index.html",
     "Trame di Paesaggio Atelier — Paesaggi su misura per l'ospitalità",
     "Atelier di progettazione e realizzazione del paesaggio per hotel, resort, relais, agriresort e dimore storiche. "
     "Inizia con la valutazione paesaggistica online gratuita.", "home"),
    ("chi-siamo.html", "chi-siamo.html",
     "Chi siamo — Trame di Paesaggio Atelier",
     "Un atelier del paesaggio per l'ospitalità di alta gamma, co-fondato dall'Arch. Federico Cuzzolini. "
     "Pochi progetti alla volta, un unico interlocutore dalla visione alla realizzazione.", "chi-siamo"),
    ("regia.html", "regia-del-paesaggio.html",
     "La Regia del Paesaggio — Trame di Paesaggio Atelier",
     "Il metodo dell'atelier: il progetto inizia prima del sopralluogo, con una valutazione paesaggistica online gratuita. "
     "Ascolto, visione, disegno, regia.", "regia"),
    ("casi-studio.html", "casi-studio/index.html",
     "Casi studio — Trame di Paesaggio Atelier",
     "Agriturismi, hotel, tenute e borghi: spazi esterni trasformati da problema irrisolto a vantaggio competitivo.", "casi"),
    ("contatti.html", "contatti.html",
     "Richiedi la valutazione paesaggistica online — Trame di Paesaggio Atelier",
     "Una videochiamata di 30 minuti, gratuita, senza impegno e senza sopralluogo. Scopri cosa può diventare lo spazio esterno della tua struttura.",
     "contatti"),
    ("404.html", "404.html", "Pagina non trovata — Trame di Paesaggio Atelier",
     "La pagina che cerchi non esiste più o è stata spostata.", ""),
]


def image_info(key):
    """Restituisce src, srcset e dimensioni di un'immagine elaborata da images.py."""
    folder, name = key.split("/")
    files = sorted((p for p in (ROOT / "assets/img" / folder).glob(f"{name}-*.jpg")
                    if re.fullmatch(rf"{re.escape(name)}-\d+", p.stem)),
                   key=lambda p: int(p.stem.rsplit("-", 1)[1]))
    if not files:
        raise FileNotFoundError(f"Immagine non trovata: {key} (eseguire _src/images.py)")
    widths = [int(p.stem.rsplit("-", 1)[1]) for p in files]
    w, h = Image.open(files[-1]).size
    return {
        "src": f"assets/img/{folder}/{files[min(1, len(files) - 1)].name}",
        "srcset": ", ".join(f"assets/img/{folder}/{p.name} {Image.open(p).width}w" for p, _ in zip(files, widths)),
        "width": w, "height": h,
    }


def make_env(root):
    env = Environment(loader=FileSystemLoader([SRC / "pages", SRC / "templates"]),
                      undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True, autoescape=True)

    def img(key, alt, sizes="100vw", cls="", eager=False):
        info = image_info(key)
        srcset = ", ".join(root + part for part in info["srcset"].split(", "))
        loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
        return Markup(
            f'<img class="{escape(cls)}" src="{root}{info["src"]}" srcset="{srcset}" sizes="{escape(sizes)}" '
            f'width="{info["width"]}" height="{info["height"]}" alt="{escape(alt)}" {loading} decoding="async">')

    def img_src_full(key):
        return image_info(key)["srcset"].split(", ")[-1].split(" ")[0]

    env.globals.update(img=img, img_src_full=img_src_full, TBC=TBC)
    return env


def render(template, out, title, description, nav, extra=None):
    depth = out.count("/")
    root = "/" if out == "404.html" else "../" * depth
    env = make_env(root)
    published = [c for c in CASES if c["published"]]
    ctx = {
        "root": root, "cases": published, "company": COMPANY, "site_url": SITE_URL, "out": out,
        "page": {"title": title, "description": description, "nav": nav,
                 "canonical": SITE_URL + ("" if out == "index.html" else out.replace("index.html", ""))},
    }
    ctx.update(extra or {})
    html = env.get_template(template).render(**ctx)
    dest = ROOT / out
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    print("  ", out)


def main():
    print("Generazione pagine:")
    for args in PAGES:
        render(*args)
    published = [c for c in CASES if c["published"]]
    for i, case in enumerate(published):
        nxt = published[(i + 1) % len(published)]
        render("caso.html", f"casi-studio/{case['slug']}.html",
               f"{case['name']} — Casi studio — Trame di Paesaggio Atelier",
               f"{case['name']}, {case['place_short']}. {case['subtitle']}. {case['claim']}",
               "casi", {"case": case, "next_case": nxt})
    # Rimuove pagine di casi studio non più pubblicati
    for c in CASES:
        if not c["published"]:
            (ROOT / f"casi-studio/{c['slug']}.html").unlink(missing_ok=True)

    urls = ["", "chi-siamo.html", "regia-del-paesaggio.html", "casi-studio/", "contatti.html"]
    urls += [f"casi-studio/{c['slug']}.html" for c in published]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{SITE_URL}{u}</loc></url>" for u in urls]
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    print("Fatto.")


if __name__ == "__main__":
    main()
