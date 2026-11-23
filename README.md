# Le Repère — site de la collection

Site vitrine du manuel **Le Repère, Mathématiques Terminale S** (Bacc Série S, Madagascar),
par Mamiarilala Razafimahefa.

En ligne : https://lerepere-mada.com (l'ancienne adresse
https://amamiarilala-svg.github.io/le-repere/ y redirige automatiquement).

- `index.html` — la page (aucune dépendance à compiler). Son en-tête contient aussi les
  données structurées (bloc JSON-LD : livre, auteur, **prix**) : à mettre à jour avec le reste
  de la page si le prix ou le nombre de pages change.
- `assets/fonts/` — polices servies par le site (voir `assets/fonts/README.md`).
- **Charte graphique « Hautes Terres »** (depuis le 2026-11-23) : latérite `#a9432a`, vert rizière
  `#b7d36b`, brique `#6b2a1c`, blanc chaux `#f4f5ec`, vert forêt `#2f5a2e` ; titres en Zilla Slab,
  texte en Fira Sans, formules en STIX Two. Les couleurs sont des variables CSS en tête de
  `index.html`, `404.html` et `outils/modele_page_bac.html` : les changer aux trois endroits.
- `assets/couverture.jpg` + `assets/couverture.webp`, `assets/pages/` — couverture et pages
  d'aperçu. Changer les deux fichiers de couverture ensemble. La couverture est vectorielle,
  dessinée en TikZ dans le dépôt du livre (`couverture/`) : la rendre depuis
  `couverture/couverture-ecran.pdf` (pdftoppm -r 600, puis réduction LANCZOS en 700×994,
  JPEG qualité 84, WebP qualité 80).
- `assets/og.jpg` — image 1200×630 affichée quand le lien est partagé sur Facebook
  (source : `outils/og.tex`, voir `outils/README.md`).
- `favicon.svg`, `favicon.ico`, `icon-192.png`, `apple-touch-icon.png` — icônes du site : carré
  latérite, coin de repère blanc chaux, point vert rizière (dessin de `favicon.svg`, repère 30×30).
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
