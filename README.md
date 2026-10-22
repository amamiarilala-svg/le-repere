# Le Repère — site de la collection

Site vitrine du manuel **Le Repère, Mathématiques Terminale S** (Bacc Série S, Madagascar),
par Mamiarilala Razafimahefa.

En ligne : https://lerepere.mg (l'ancienne adresse
https://amamiarilala-svg.github.io/le-repere/ y redirige automatiquement).

- `index.html` — la page (aucune dépendance à compiler ; polices Google Fonts).
- `assets/couverture.jpg`, `assets/pages/` — couverture et pages d'aperçu.
- `assets/og.jpg` — image 1200×630 affichée quand le lien est partagé sur Facebook.
- `sujets/` — sujets du Bac 2021–2026 et corrigé 2026 à télécharger (voir `outils/README.md`).
- `CNAME` — nom de domaine du site pour GitHub Pages. Ne pas le supprimer : sans lui, le
  site repasse sur l'adresse github.io.

## Domaine `lerepere.mg`

Hébergement : GitHub Pages (branche `main`, racine). Zone DNS chez le bureau
d'enregistrement du domaine :

| Type  | Nom   | Valeur                                                            |
|-------|-------|-------------------------------------------------------------------|
| A     | `@`   | `185.199.108.153`                                                 |
| A     | `@`   | `185.199.109.153`                                                 |
| A     | `@`   | `185.199.110.153`                                                 |
| A     | `@`   | `185.199.111.153`                                                 |
| CNAME | `www` | `amamiarilala-svg.github.io`                                      |
| TXT   | donné par GitHub (vérification du domaine, réglages du profil → Pages) | |

Pas d'enregistrement « joker » (`*`). Dans le dépôt : Settings → Pages → *Custom domain*
`lerepere.mg`, puis *Enforce HTTPS*.
