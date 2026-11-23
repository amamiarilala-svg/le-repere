# Polices du site

Sous-ensembles WOFF2 téléchargés depuis Google Fonts (`fonts.gstatic.com`) le 2026-11-23, pour
servir les polices depuis le site lui-même (plus de feuille de style externe qui bloque
l'affichage). Les règles `@font-face` correspondantes sont écrites en tête de `index.html`
(et en chemins absolus dans `404.html`).

| Fichier | Police | Graisses | Sous-ensemble |
|---|---|---|---|
| `archivo-latin.woff2`, `archivo-latin-ext.woff2` | Archivo (texte) | 400 à 700, variable | latin, latin étendu |
| `young-serif-latin.woff2`, `young-serif-latin-ext.woff2` | Young Serif (titres) | 400 | latin, latin étendu |
| `stix-two-text-latin.woff2`, `stix-two-text-latin-ext.woff2`, `stix-two-text-greek.woff2` | STIX Two Text italique (formules) | 400 à 600, variable | latin, latin étendu, grec |

Les trois polices sont distribuées sous la licence SIL Open Font License 1.1
(https://openfontlicense.org), qui autorise leur redistribution avec un site web.
Le navigateur ne télécharge que les fichiers dont il a besoin (`unicode-range`).
