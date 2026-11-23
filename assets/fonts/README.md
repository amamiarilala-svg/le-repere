# Polices du site

Sous-ensembles WOFF2 téléchargés depuis Google Fonts (`fonts.gstatic.com`) le 2026-11-23, pour
servir les polices depuis le site lui-même (plus de feuille de style externe qui bloque
l'affichage). Les règles `@font-face` correspondantes sont écrites en tête de `index.html`
(et en chemins absolus dans `404.html`).

| Fichier | Police | Graisses | Sous-ensemble |
|---|---|---|---|
| `fira-sans-400-*.woff2`, `fira-sans-400i-*.woff2`, `fira-sans-600-*.woff2`, `fira-sans-700-*.woff2` | Fira Sans (texte) | 400, 400 italique, 600, 700 | latin, latin étendu |
| `zilla-slab-500-*.woff2`, `zilla-slab-700-*.woff2` | Zilla Slab (titres, grands chiffres) | 500, 700 | latin, latin étendu |
| `stix-two-text-latin.woff2`, `stix-two-text-latin-ext.woff2`, `stix-two-text-greek.woff2` | STIX Two Text italique (formules) | 400 à 600, variable | latin, latin étendu, grec |

Charte « Hautes Terres » du 2026-11-23 : Zilla Slab et Fira Sans remplacent Young Serif et
Archivo. Zilla Slab dessine des chiffres elzéviriens par défaut ; le site force les chiffres
alignés (`font-variant-numeric: lining-nums`).

Les trois polices sont distribuées sous la licence SIL Open Font License 1.1
(https://openfontlicense.org), qui autorise leur redistribution avec un site web.
Le navigateur ne télécharge que les fichiers dont il a besoin (`unicode-range`).
