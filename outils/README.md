# Outils

## Régénérer les sujets du Bac (`sujets/`)

Les PDF de `sujets/` sont compilés à partir des sujets transcrits dans le livre
(`Livre_bac_S/parties/annales/bac_AAAA.tex`), avec la mise en page du livre (A5).

Depuis le dossier du livre, dans Git Bash :

```bash
export MSYS_NO_PATHCONV=1
for y in 2021 2022 2023 2024 2025 2026; do
  pdflatex -interaction=nonstopmode -output-directory="C:/Users/MAMIARILALA/Desktop/le-repere/build-sujets" \
    -jobname=bac-$y "\def\annee{$y}\input{C:/Users/MAMIARILALA/Desktop/le-repere/outils/sujet_bac.tex}"
done
```

Puis copier chaque `build-sujets/bac-AAAA.pdf` en `sujets/bac-s-AAAA-mathematiques.pdf`,
refaire le ZIP `sujets/bac-s-2021-2026-mathematiques.zip`, et supprimer `build-sujets/`.

`MSYS_NO_PATHCONV=1` évite que Git Bash transforme `\def\annee{…}` et les chemins
`C:/…` passés à `pdflatex`.

## Régénérer le corrigé offert (`sujets/bac-s-2026-mathematiques-corrige.pdf`)

Seul le corrigé de la session 2026 est en téléchargement ; les autres restent dans
le livre. Il est compilé à partir de `Livre_bac_S/parties/annales/corrige_2026.tex`
avec `outils/corrige_bac.tex` (deux passes, pour les références internes) :

```bash
export MSYS_NO_PATHCONV=1
mkdir -p "C:/Users/MAMIARILALA/Desktop/le-repere/build-sujets"
for i in 1 2; do
  pdflatex -interaction=nonstopmode -output-directory="C:/Users/MAMIARILALA/Desktop/le-repere/build-sujets" \
    -jobname=corrige-2026 "\def\annee{2026}\input{C:/Users/MAMIARILALA/Desktop/le-repere/outils/corrige_bac.tex}"
done
```

Puis copier `build-sujets/corrige-2026.pdf` en `sujets/bac-s-2026-mathematiques-corrige.pdf`,
mettre à jour le nombre de pages et la taille (en Ko) dans `index.html`, et
supprimer `build-sujets/`. `corrige_bac.tex` protège les titres d'exercice et de
problème d'un saut de page juste après eux ; vérifier quand même le rendu, car la
pagination diffère de celle du livre.

## Générer une page « sujet et corrigé » en ligne (`bac-s/AAAA/`)

`outils/page_bac.py` convertit le sujet (`bac_AAAA.tex`) et, s'il est publié, le
corrigé (`corrige_AAAA.tex`) du livre en une page web : texte en HTML, formules
dessinées à l'avance par KaTeX (aucun JavaScript dans la page), figures TikZ en SVG.

Une seule fois, installer KaTeX (version figée dans `outils/package.json`) :

```bash
cd outils && npm install --ignore-scripts
```

Puis, depuis le dossier du site :

```bash
python -I outils/page_bac.py 2026
```

Le script écrit `bac-s/AAAA/index.html` et `bac-s/AAAA/figure-N.svg`, et met à
jour `assets/katex/` (feuille de style et polices WOFF2 de KaTeX). Il s'arrête
sur toute commande LaTeX qu'il ne sait pas convertir plutôt que de la laisser
passer : compléter alors `page_bac.py`. Le modèle de page est
`outils/modele_page_bac.html`.

- **À relancer** si le sujet ou le corrigé change dans le livre, ou si le prix
  ou le numéro de commande change (constantes `PRIX` et `WHATSAPP` en tête de
  `page_bac.py`, à garder identiques à `index.html`).
- **Commande** : trois boutons WhatsApp par page (encart entre sujet et
  corrigé, bouton vert flottant sur téléphone, encart du livre en bas). Le
  message pré-rempli finit par « (page Bac S AAAA) ». Le bouton flottant est
  en `position: sticky` dans `.lecture`, sans JavaScript : il disparaît avant
  l'encart du livre.
- **Nouvelle page** : ajouter son adresse à `sitemap.xml`, un lien depuis la
  section « Sujets du Bac » de `index.html`, et un texte alternatif pour chaque
  figure dans `FIG_ALT` (`page_bac.py`). Seul le corrigé 2026 est publié
  (`CORRIGES_PUBLIES`) ; une page sans corrigé demandera d'adapter le modèle.
- Les fichiers de travail vont dans `build-pages/` (ignoré par git).

## Refaire l'image de partage (`assets/og.jpg`)

`outils/og.tex` dessine l'image 1200×630 (fond brique, titre, prix, couverture du
livre). Elle reprend `couverture/couverture-ecran.pdf` du dépôt du livre : à refaire
si la couverture, le prix ou le numéro change. LuaLaTeX ne retrouve la police Zilla
Slab que si elle est dans le dossier de compilation :

```bash
mkdir -p build-og
cp outils/og.tex ../Livre_bac_S/couverture/polices/ZillaSlab-Bold.ttf build-og/
cd build-og && lualatex og.tex && lualatex og.tex && pdftoppm -r 72 -png -singlefile og.pdf og && cd ..
python -I -c "from PIL import Image; Image.open('build-og/og.png').convert('RGB').save('assets/og.jpg', quality=86, optimize=True)"
rm -rf build-og
```

Deux passes sont nécessaires (dessin en surimpression). Après publication, repasser
l'adresse dans le débogueur de partage de Facebook pour rafraîchir l'aperçu.
