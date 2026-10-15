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
