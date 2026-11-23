# Le Repère — site de la collection

Site vitrine du manuel **Le Repère, Mathématiques Terminale S** (Bacc Série S, Madagascar),
par Mamiarilala Razafimahefa.

En ligne : https://lerepere-mada.com (l'ancienne adresse
https://amamiarilala-svg.github.io/le-repere/ y redirige automatiquement).

- `index.html` — la page (aucune dépendance à compiler). Son en-tête contient aussi les
  données structurées (bloc JSON-LD : livre, auteur, **prix**) : à mettre à jour avec le reste
  de la page si le prix ou le nombre de pages change.
- `assets/fonts/` — polices servies par le site (voir `assets/fonts/README.md`).
- `assets/couverture.jpg` + `assets/couverture.webp`, `assets/pages/` — couverture et pages
  d'aperçu. Changer les deux fichiers de couverture ensemble.
- `assets/og.jpg` — image 1200×630 affichée quand le lien est partagé sur Facebook.
- `favicon.svg`, `favicon.ico`, `icon-192.png`, `apple-touch-icon.png` — icônes du site.
- `robots.txt`, `sitemap.xml` — pour les moteurs de recherche. Ajouter toute nouvelle page ou
  tout nouveau PDF au sitemap (avec sa date `lastmod`).
- `404.html` — page affichée pour une adresse inconnue (chemins absolus obligatoires).
- `sujets/` — sujets du Bac 2021–2026 et corrigé 2026 à télécharger (voir `outils/README.md`).
- `bac-s/2026/` — sujet et corrigé 2026 en ligne (page générée par `outils/page_bac.py`,
  ne pas la modifier à la main) ; `assets/katex/` — feuille de style et polices des formules.
- `CNAME` — nom de domaine du site pour GitHub Pages. Ne pas le supprimer : sans lui, le
  site repasse sur l'adresse github.io.

## Domaine `lerepere-mada.com`

Hébergement : GitHub Pages (branche `main`, racine). Domaine acheté chez GoDaddy le
2026-10-22 ; zone DNS à régler dans GoDaddy (Mes produits → DNS) :

| Type  | Nom   | Valeur                                                            |
|-------|-------|-------------------------------------------------------------------|
| A     | `@`   | `185.199.108.153`                                                 |
| A     | `@`   | `185.199.109.153`                                                 |
| A     | `@`   | `185.199.110.153`                                                 |
| A     | `@`   | `185.199.111.153`                                                 |
| CNAME | `www` | `amamiarilala-svg.github.io`                                      |
| TXT   | donné par GitHub (vérification du domaine, réglages du profil → Pages) | |

Pas d'enregistrement « joker » (`*`). Dans le dépôt : Settings → Pages → *Custom domain*
`lerepere-mada.com`, puis *Enforce HTTPS*.
