# daniloaprigliano.it — pagina di presentazione

Pagina personale di Danilo Aprigliano: docente di italiano e storia, sviluppatore web,
formatore sull'intelligenza artificiale per la scuola.

Un solo file, `index.html`, senza dipendenze da costruire: HTML e CSS scritti a mano,
ritratto incorporato nel documento, unico caricamento esterno il carattere
[Source Serif 4](https://fonts.google.com/specimen/Source+Serif+4) da Google Fonts.

- Tema chiaro e scuro, agganciati alle impostazioni di sistema di chi legge.
- Adattiva: tre punti di rottura (1080, 820, 660 px); il testo passa da tre colonne a una.
- Il contenuto sta nel documento, non è costruito da JavaScript: leggibile dai motori
  di ricerca e da chi naviga senza script.

## Modificare

Si apre con un editor di testo. La tavolozza sta nelle variabili in cima al foglio di
stile, ripetute in tre blocchi: `:root` per il tema chiaro, il blocco
`prefers-color-scheme: dark` per chi ha il sistema in tema scuro, e `[data-theme="dark"]`
per una scelta esplicita. Se si cambia un colore vanno aggiornati tutti e tre.

## Pubblicazione

GitHub Pages serve la pagina dalla radice del ramo principale. Il file `.nojekyll`
disattiva l'elaborazione Jekyll, che qui non serve.
