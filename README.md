# Trame di Paesaggio Atelier — sito web

Sito statico (HTML, CSS, JavaScript), senza database e senza dipendenze esterne:
font e immagini sono ospitati nel sito stesso.

## Struttura

| Percorso | Contenuto |
|---|---|
| `index.html`, `chi-siamo.html`, `regia-del-paesaggio.html`, `contatti.html`, `casi-studio/` | Pagine pubblicate (generate, non modificarle a mano) |
| `assets/` | Fogli di stile, script, font, immagini ottimizzate, logo |
| `_src/pages/` | Testi e struttura delle pagine |
| `_src/build.py` | Dati aziendali e contenuti dei casi studio, generazione delle pagine |
| `_src/images.py` | Elenco delle immagini e loro ottimizzazione per il web |
| `_materiali/` | Materiali originali forniti dal cliente (da non pubblicare) |

## Modificare testi e immagini

```bash
pip install jinja2 pillow
python3 _src/images.py   # solo se sono cambiate le immagini
python3 _src/build.py    # rigenera tutte le pagine
```

- Testi di Home, Chi siamo, Regia, Contatti: `_src/pages/*.html`.
- Casi studio (dettagli, servizi, testi, galleria, testimonianza): elenco `CASES` in `_src/build.py`.
- Nuova immagine: aggiungere l'originale in `_materiali/04_immagini_casi_studio/`, registrarla in
  `IMAGES` dentro `_src/images.py`, quindi lanciare i due comandi sopra.
- Loghi delle strutture: originali in `_materiali/06_loghi_strutture/`, elenco `LOGOS` in
  `_src/images.py`; il collegamento al sito della struttura è il campo `website` del caso studio.
- Video 3D: campo `video` del caso studio (identificativo del file Google Drive). Il file su Drive
  deve essere condiviso come "Chiunque abbia il link". Il video si carica solo al clic.

I segnaposto `[DA COMPLETARE: …]` sono evidenziati in giallo nel sito: vanno sostituiti prima della
messa online.

## Modulo di contatto

In `assets/js/main.js`, la variabile `FORM_ENDPOINT` è vuota: finché non viene configurata, l'invio
apre il programma di posta del visitatore con la richiesta già compilata.

Per ricevere le richieste direttamente all'indirizzo riservato:
1. creare un modulo gratuito su un servizio come Formspree, collegato all'indirizzo email riservato
   per le richieste;
2. incollare l'indirizzo del modulo (es. `https://formspree.io/f/xxxxxxx`) in `FORM_ENDPOINT`.

In questo modo l'indirizzo riservato non compare mai nel codice del sito.

## Pubblicazione

Caricare sul server (ad esempio l'hosting di Register.it, via FTP) tutti i file **tranne** `_src/`,
`_materiali/` e `README.md`. La pagina `404.html` va indicata come pagina di errore nel pannello
dell'hosting. Il dominio previsto è `https://tramedipaesaggioatelier.it/` (usato in `sitemap.xml`,
`robots.txt` e nei metadati).

Il sito non usa cookie né servizi di terze parti; privacy e cookie policy rimandano a iubenda.
