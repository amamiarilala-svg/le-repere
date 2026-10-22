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
