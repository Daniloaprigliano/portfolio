#!/usr/bin/env python3
"""Compone la pagina dei link, /link/ e /en/link/, da link/pezzi.json.

Si lancia dalla radice del repository:  python3 link/componi.py
Riscrive per intero link/index.html e en/link/index.html: le correzioni
si fanno qui o in pezzi.json, mai sulle pagine composte.

Regole:
- «In evidenza»: i pezzi con "evidenza": true, dal più recente.
- «Gli ultimi pezzi»: i tre più recenti fra gli altri, dovunque siano usciti.
- «nuovo»: un pezzo uscito da meno di quattordici giorni al momento in cui si
  compone la pagina. La pagina è statica: l'etichetta sparisce alla prima
  composizione dopo i quattordici giorni.
"""
import datetime as dt
import html
import json
import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
GIORNI_NUOVO = 14
OGGI = dt.date.today()

MESI_IT = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
           "agosto", "settembre", "ottobre", "novembre", "dicembre"]
MESI_EN = ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"]
GENERI_EN = {"racconto": "short story", "intervista": "interview", "recensione": "review"}

PUNTINA = ('<svg width="14" height="18" viewBox="0 0 14 18" aria-hidden="true">'
           '<path d="M2 1h10M4 1v6L1.5 10h11L10 7V1M7 10v7" fill="none" stroke="currentColor" '
           'stroke-width="1.4" stroke-linejoin="round"/></svg>')

ICONE = [
    ("mailto:danilo@daniloaprigliano.it", "Mail", "Mail",
     '<rect x="3" y="5.5" width="18" height="13" rx="1"/><path d="M3.5 6.5 12 13l8.5-6.5"/>'),
    ("https://substack.com/@daniloaprigliano", "Substack", "Substack",
     '<path d="M5 4h14M5 8h14"/><path d="M5 12h14v9l-7-4-7 4z"/>'),
    ("https://www.linkedin.com/in/daniloaprigliano", "LinkedIn", "LinkedIn",
     '<rect x="3" y="3" width="18" height="18" rx="2.5"/>'
     '<path d="M8 10.5V17M8 7.4v.1M12 17v-6.5M12 13.5c0-2 1.2-3 2.6-3S17 11.4 17 13.3V17" stroke-linecap="round"/>'),
    ("https://www.instagram.com/daniloaprigliano/", "Instagram", "Instagram",
     '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/>'
     '<circle cx="17.3" cy="6.7" r=".6" fill="currentColor"/>'),
    ("https://x.com/DaniloApriglian", "X", "X",
     '<path d="M4.5 4h4.2l10.8 16h-4.2z"/><path d="M19.2 4l-6.1 7M10.9 13 4.8 20" stroke-linecap="round"/>'),
    ("https://unisi.academia.edu/DaniloAprigliano", "Academia.edu", "Academia.edu",
     '<path d="M2.5 9 12 4.5 21.5 9 12 13.5z"/><path d="M6.5 11v4.5c1.5 1.6 3.4 2.4 5.5 2.4s4-.8 5.5-2.4V11M21.5 9v5"/>'),
]

TESTI = {
    "it": {
        "lang": "it", "pre": "../", "radice": "../",
        "title": "Link – Danilo Aprigliano",
        "description": "Tutti i link di Danilo Aprigliano: la newsletter «Il punto cieco», gli ultimi pezzi, le pagine del sito, i profili.",
        "testata": ("Milano", "Link", "daniloaprigliano.it"),
        "mestieri": "Docente · public historian · filologo · sviluppatore",
        "presenta": "Insegno lettere a Milano, studio la Resistenza e formo i docenti all’uso dell’intelligenza artificiale. Qui sotto, le strade per arrivare a quello che scrivo e faccio.",
        "icone": "Profili e contatti",
        "news_sotto": "La newsletter · iscriviti",
        "evidenza": ("In evidenza", "scelti da me"),
        "ultimi": ("Gli ultimi pezzi", "dovunque escano"),
        "tutti": "Tutti gli articoli, dal 2012 →",
        "tutti_url": "../articoli/",
        "sito": ("Il sito", "le pagine"),
        "nuovo": "nuovo",
        "pagine": [
            ("ia-a-scuola/", "IA a scuola", "Il percorso di formazione per i docenti, com’era fatto e con i numeri."),
            ("public-history/", "Public history", "I quindici martiri di Piazzale Loreto, le mostre della Fondazione Feltrinelli, le Fiamme Verdi."),
            ("scrittura/", "Scrittura", "Libri, saggi e ricerca; le puntate per Gli Ascoltabili; la newsletter."),
            ("web/", "Web", "Siti e applicazioni per archivi, associazioni e riviste."),
            ("impegno/", "Impegno civile", "Il Circolo e Centro studi «Emilio Caldara», la FIVL, «Hey Milano»."),
            ("lezioni/", "Lezioni private", "Latino, italiano, storia e metodo di studio."),
            ("materiali/", "Materiali didattici", "Schede, dispense e verifiche, libere da scaricare."),
            ("curriculum/", "Curriculum", "Per esteso, numerato e con le date, con il PDF."),
            ("tutto/", "Tutto", "Ogni cosa fatta, in un elenco solo, in ordine di data."),
        ],
        "piede": 'Una pagina di <a href="../">daniloaprigliano.it</a>, nello stesso foglio di stile. Nessuno script, nessun cookie, nessuna pubblicità. <a href="../en/link/">English</a>',
        "ritratto_alt": "Ritratto di Danilo Aprigliano",
    },
    "en": {
        "lang": "en", "pre": "../../", "radice": "../",
        "title": "Links – Danilo Aprigliano",
        "description": "All of Danilo Aprigliano’s links: the newsletter Il punto cieco, the latest pieces, the pages of the site, the profiles.",
        "testata": ("Milan", "Links", "daniloaprigliano.it"),
        "mestieri": "Teacher · public historian · philologist · developer",
        "presenta": "I teach Italian literature in Milan, research the Italian Resistance and train teachers to use artificial intelligence. Below, the ways into what I write and do. Most of the writing is in Italian.",
        "icone": "Profiles and contacts",
        "news_sotto": "The newsletter, in Italian · subscribe",
        "evidenza": ("Featured", "my choice"),
        "ultimi": ("Latest pieces", "wherever they appear"),
        "tutti": "All articles since 2012, in Italian →",
        "tutti_url": "../../articoli/",
        "sito": ("The site", "the pages"),
        "nuovo": "new",
        "pagine": [
            ("ia-a-scuola/", "AI at school", "The training course for teachers, how it was built, with the figures."),
            ("public-history/", "Public history", "The fifteen martyrs of Piazzale Loreto, the Feltrinelli Foundation exhibitions, the Fiamme Verdi."),
            ("scrittura/", "Writing", "Books, essays and research; episodes for Gli Ascoltabili; the newsletter."),
            ("web/", "Web", "Websites and applications for archives, associations and magazines."),
            ("impegno/", "Civic work", "The Emilio Caldara study centre, the FIVL, Hey Milano."),
            ("lessons/", "Private lessons", "Latin, Italian, history and study skills."),
            ("materials/", "Teaching materials", "Worksheets, handouts and tests, free to download."),
            ("../curriculum/", "Curriculum (IT)", "In full, numbered and dated, with the PDF."),
            ("tutto/", "Everything", "Everything I have done, in one list, by date."),
        ],
        "piede": 'A page of <a href="../">daniloaprigliano.it</a>, in the same stylesheet. No scripts, no cookies, no advertising. <a href="../../link/">Italiano</a>',
        "ritratto_alt": "Portrait of Danilo Aprigliano",
    },
}


def e(s):
    return html.escape(s, quote=False)


def data_umana(d, lingua):
    if lingua == "it":
        return f"{d.day} {MESI_IT[d.month - 1]} {d.year}"
    return f"{d.day} {MESI_EN[d.month - 1]} {d.year}"


def descrizione(p, lingua, t):
    d = dt.date.fromisoformat(p["data"])
    if lingua == "it":
        testata = f"«{e(p['testata'])}»"
        genere = p.get("genere")
    else:
        testata = f"<i>{e(p['testata'])}</i>"
        genere = GENERI_EN.get(p.get("genere", ""), p.get("genere"))
    pezzi = [testata, data_umana(d, lingua)]
    riga = ", ".join(pezzi) + "."
    if genere:
        riga = genere[0].upper() + genere[1:] + ", " + riga
    if (OGGI - d).days < GIORNI_NUOVO:
        riga = f'<span class="pl-nuovo">{t["nuovo"]}</span>' + riga
    return riga


def titolo(p):
    return f"“{e(p['titolo'])}”"


def voce_fissata(p, lingua, t):
    return (f'<a class="pl-voce fissato" href="{e(p["url"])}">{PUNTINA}'
            f'<span><span class="pl-tit">{titolo(p)}</span>'
            f'<span class="pl-des">{descrizione(p, lingua, t)}</span></span>'
            f'<span class="pl-fr">→</span></a>')


def voce(n, tit, des, url):
    return (f'<a class="pl-voce" href="{url}"><span class="pl-num">{n}</span>'
            f'<span class="pl-tit">{tit}<span class="pl-des">{des}</span></span>'
            f'<span class="pl-fr">→</span></a>')


def rubrica(coppia):
    return (f'<div class="pl-rubrica"><span class="rub">{coppia[0]}</span>'
            f'<span>{coppia[1]}</span></div>')


def componi(lingua, pezzi):
    t = TESTI[lingua]
    pre = t["pre"]
    ordinati = sorted(pezzi, key=lambda p: p["data"], reverse=True)
    fissati = [p for p in ordinati if p.get("evidenza")]
    ultimi = [p for p in ordinati if not p.get("evidenza")][:3]

    icone = "\n    ".join(
        f'<a href="{url}" aria-label="{etichetta}" title="{titolo_}"><svg viewBox="0 0 24 24" aria-hidden="true" '
        f'fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round">{disegno}</svg></a>'
        for url, etichetta, titolo_, disegno in ICONE)

    righe = []
    righe.append(rubrica(t["evidenza"]))
    righe += [voce_fissata(p, lingua, t) for p in fissati]
    righe.append(rubrica(t["ultimi"]))
    righe += [voce(i, titolo(p), descrizione(p, lingua, t), e(p["url"])) for i, p in enumerate(ultimi, 1)]
    righe.append(f'<a class="pl-tutti" href="{t["tutti_url"]}">{t["tutti"]}</a>')
    righe.append(rubrica(t["sito"]))
    righe += [voce(i, e(nome), e(des), t["radice"] + url)
              for i, (url, nome, des) in enumerate(t["pagine"], len(ultimi) + 1)]
    corpo = "\n  ".join(righe)

    alt_it = "https://daniloaprigliano.it/link/"
    alt_en = "https://daniloaprigliano.it/en/link/"
    qui = alt_it if lingua == "it" else alt_en

    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{e(t['description'])}">
<link rel="canonical" href="{qui}">
<link rel="alternate" hreflang="it" href="{alt_it}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{e(t['description'])}">
<meta property="og:url" content="{qui}">
<meta property="og:image" content="https://daniloaprigliano.it/og.png">
<link rel="icon" href="{pre}favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Vollkorn:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Space+Mono:wght@400;700&display=swap">
<link rel="stylesheet" href="{pre}stile.css">
</head>
<!-- Pagina composta da link/componi.py: non si corregge a mano. -->
<body>
<main class="pl">
  <div class="pl-testata"><span>{t['testata'][0]}</span><span>{t['testata'][1]}</span><a href="{t['radice']}">{t['testata'][2]}</a></div>

  <div class="pl-chi">
    <img src="{pre}media/ritratto.webp" alt="{t['ritratto_alt']}" width="76" height="76">
    <div>
      <h1>Danilo Aprigliano</h1>
      <div class="pl-mestieri">{t['mestieri']}</div>
    </div>
  </div>

  <p class="pl-presenta">{t['presenta']}</p>

  <nav class="pl-icone" aria-label="{t['icone']}">
    {icone}
  </nav>

  <a class="pl-newsletter" href="https://www.ilpuntocieco.it/">
    <span><b>«Il punto cieco»</b><small>{t['news_sotto']}</small></span><span class="fr">→</span>
  </a>

  {corpo}

  <div class="pl-piede" role="contentinfo"><span class="pl-marchio" aria-hidden="true">A</span><span>{t['piede']}</span></div>
</main>
</body>
</html>
"""


def main():
    dati = json.loads((RADICE / "link" / "pezzi.json").read_text(encoding="utf-8"))
    pezzi = dati["pezzi"]
    for lingua, dove in (("it", RADICE / "link" / "index.html"),
                         ("en", RADICE / "en" / "link" / "index.html")):
        dove.parent.mkdir(parents=True, exist_ok=True)
        dove.write_text(componi(lingua, pezzi), encoding="utf-8")
        print("scritta", dove.relative_to(RADICE))


if __name__ == "__main__":
    main()
