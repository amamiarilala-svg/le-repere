"""Génère la page web « sujet + corrigé » d'une session du Bac S à partir des sources LaTeX du livre.

    python -I outils/page_bac.py 2026

Lit `Livre_bac_S/parties/annales/bac_AAAA.tex` (et `corrige_AAAA.tex` si le corrigé est publié),
écrit `bac-s/AAAA/index.html` et les figures `bac-s/AAAA/figure-N.svg`, et copie la feuille de
style et les polices de KaTeX dans `assets/katex/`. Prérequis : TeX Live (pdflatex, pdftocairo),
Node.js et KaTeX (`npm install --ignore-scripts` dans `outils/`). Voir `outils/README.md`.

Le convertisseur ne couvre que le LaTeX employé dans les annales du livre (enumerate, itemize,
center, remarque, tabular, tikzpicture, \\textbf, \\emph, \\fbox, \\bareme, \\hfill (x pt)…) :
toute commande inconnue fait échouer la génération plutôt que de passer en silence.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
OUTILS = SITE / "outils"
LIVRE = Path(os.environ.get("LIVRE_BAC_S", "C:/Users/MAMIARILALA/Desktop/Livre_bac_S"))
ANNEES = range(2021, 2027)
CORRIGES_PUBLIES = {2026}  # les autres corrigés restent réservés au livre
PRIX = "55&#8239;000&nbsp;Ar"  # à garder identique à index.html
# Lien de commande (3 boutons par page). Le message pré-rempli cite la page, pour savoir d'où vient
# chaque commande reçue sur WhatsApp.
WHATSAPP = ("https://wa.me/261348606886?text=Bonjour%2C%20je%20souhaite%20commander%20le%20livre%20"
            "Le%20Rep%C3%A8re%2C%20Math%C3%A9matiques%20Terminale%20S%20(page%20Bac%20S%20{annee}).")

MACROS = {
    "\\N": "\\mathbb{N}", "\\Z": "\\mathbb{Z}", "\\Q": "\\mathbb{Q}", "\\R": "\\mathbb{R}",
    "\\C": "\\mathbb{C}", "\\e": "\\mathrm{e}", "\\ii": "\\mathrm{i}", "\\dd": "\\,\\mathrm{d}",
    "\\vect": "\\overrightarrow{#1}", "\\abs": "\\left|#1\\right|", "\\p": "\\left(#1\\right)",
}

# Textes de remplacement des figures (alt), par année puis par ordre d'apparition.
FIG_ALT = {
    2026: [
        "Figure du problème 1 : triangle ABC rectangle en A, points O, D et G, rectangle ABGC, "
        "droite (L) et cercle (C) de centre G et de rayon 4",
        "Courbes (C1) et (C2) des fonctions f1 et f2 dans un repère orthonormé, "
        "sécantes aux points (-1 ; 0) et (0 ; 1)",
    ],
}

PREAMBULE_FIGURE = r"""\documentclass[tikz,border=4pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,mathrsfs}
\usepackage{newtxtext,newtxmath}
\usetikzlibrary{arrows.meta,calc}
\newcommand{\e}{\mathrm{e}}
\newcommand{\ii}{\mathrm{i}}
\begin{document}
"""


def entre_accolades(s, i):
    """s[i] == '{' : renvoie (contenu, indice après l'accolade fermante)."""
    assert s[i] == "{", s[i:i + 30]
    prof = 0
    for j in range(i, len(s)):
        if s[j] == "{" and s[j - 1] != "\\":
            prof += 1
        elif s[j] == "}" and s[j - 1] != "\\":
            prof -= 1
            if prof == 0:
                return s[i + 1:j], j + 1
    raise ValueError("accolade non fermée : " + s[i:i + 60])


def remplacer_commande(s, nom, fabrique):
    r"""Remplace chaque \nom{…} (accolades imbriquées gérées) par fabrique(contenu converti)."""
    motif = "\\" + nom + "{"
    while True:
        i = s.find(motif)
        if i < 0:
            return s
        contenu, fin = entre_accolades(s, i + len(motif) - 1)
        s = s[:i] + fabrique(texte_en_ligne(contenu)) + s[fin:]


def texte_en_ligne(s):
    s = remplacer_commande(s, "textbf", lambda c: f"<strong>{c}</strong>")
    s = remplacer_commande(s, "emph", lambda c: f"<em>{c}</em>")
    s = remplacer_commande(s, "fbox", lambda c: f'<span class="encadre">{c}</span>')
    s = remplacer_commande(s, "bareme", lambda c: f'<span class="bareme">{c}</span>')
    return s


class Document:
    """Conversion d'un fichier d'annale en fragment HTML (formules en attente de rendu)."""

    def __init__(self, source, prefixe, annee, formules, figures):
        self.prefixe, self.annee = prefixe, annee
        self.formules, self.figures = formules, figures
        self.points = []  # barème de chaque exercice / problème, dans l'ordre
        self.titres = []  # (id, libellé) pour le sommaire de la page
        self.html = self.convertir(source)

    # -- étapes ----------------------------------------------------------------------------
    def convertir(self, s):
        s = re.sub(r"(?<!\\)%.*", "", s)
        s = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", self._figure, s, flags=re.S)
        s = re.sub(r"\$\$(.+?)\$\$", lambda m: self._formule(m.group(1), True), s, flags=re.S)
        s = re.sub(r"\$(.+?)\$", lambda m: self._formule(m.group(1), False), s, flags=re.S)
        s = html.escape(s, quote=False)
        # Typographie française : espace insécable avant : ; ? ! » et après «.
        s = re.sub(r"[ \t\n]+([:;?!»])", r"&nbsp;\1", s)
        s = re.sub(r"«[ \t\n]+", "«&nbsp;", s)
        s = re.sub(r"\\begin\{tabular\}\{[^}]*\}(.*?)\\end\{tabular\}", self._tableau, s, flags=re.S)
        for bruit in (r"\\Needspace\{[^}]*\}", r"\\(big|med|small)skip\b", r"\\noindent\b",
                      r"\\renewcommand\{\\arraystretch\}\{[^}]*\}",
                      r"\\(sujetbac|corrige)header\{[^}]*\}"):
            s = re.sub(bruit, "", s)
        s = re.sub(r"\\hfill\s*\(([^()]*pts?)\)", r'<span class="pts">\1</span>', s)
        s = texte_en_ligne(s)
        s = s.replace("~", "&nbsp;")
        return self.structurer(s)

    def _formule(self, tex, display):
        self.formules.append({"tex": tex.strip(), "display": display})
        return f"\x00F{len(self.formules) - 1}\x00"

    def _figure(self, m):
        self.figures.append(m.group(0))
        return f"\x00G{len(self.figures) - 1}\x00"

    def _tableau(self, m):
        lignes = [l for l in re.split(r"\\\\", m.group(1)) if l.strip()]
        corps = []
        for l in lignes:
            l = l.replace("\\hline", "").strip()
            if not l:
                continue
            cases = [c.strip() for c in l.split("&amp;")]
            tete = f"<th scope=\"row\">{cases[0]}</th>"
            corps.append("<tr>" + tete + "".join(f"<td>{c}</td>" for c in cases[1:]) + "</tr>")
        return '\x00T<div class="tab"><table class="variations">' + "".join(corps) + "</table></div>\x00"

    def structurer(self, s):
        jeton = re.compile(
            r"\\begin\{(enumerate|itemize|center|remarque)\}(\[[^\]]*\])?"
            r"|\\end\{(enumerate|itemize|center|remarque)\}"
            r"|\\item\b|\\(exercice|probleme)\{([^}]*)\}|\n[ \t]*\n"
        )
        sortie, pile, tampon = [], [], []
        compte = {"exercice": 0, "probleme": 0}

        def vider():
            texte = re.sub(r"\s+", " ", " ".join(tampon)).strip()
            tampon.clear()
            if not texte:
                return
            if re.fullmatch(r"\x00(G\d+|T.*)\x00", texte, flags=re.S):
                sortie.append(texte)  # figure ou tableau : bloc, pas de paragraphe autour
            elif re.fullmatch(r"<strong>[^<]{1,40}</strong>", texte):
                sortie.append(f"<h4>{texte[8:-9]}</h4>")
            else:
                sortie.append(f"<p>{texte}</p>")

        pos = 0
        for m in jeton.finditer(s):
            tampon.append(s[pos:m.start()])
            pos = m.end()
            t = m.group(0)
            vider()
            if t.startswith("\\begin"):
                env, opt = m.group(1), m.group(2) or ""
                if env == "enumerate":
                    niveau = sum(1 for e in pile if e[0] == "ol") + 1
                    sortie.append(f'<ol class="n{niveau}">')
                    pile.append(["ol", False])
                elif env == "itemize":
                    classe = "tirets" if "--" in opt else "puces"
                    sortie.append(f'<ul class="{classe}">')
                    pile.append(["ul", False])
                elif env == "center":
                    sortie.append('<div class="centre">')
                    pile.append(["div", False])
                else:
                    sortie.append('<aside class="remarque"><p class="remarque-h">Remarque</p>')
                    pile.append(["aside", False])
            elif t.startswith("\\end"):
                balise, li = pile.pop()
                if li:
                    sortie.append("</li>")
                sortie.append(f"</{balise}>")
            elif t == "\\item":
                if pile[-1][1]:
                    sortie.append("</li>")
                sortie.append("<li>")
                pile[-1][1] = True
            elif m.group(4):
                genre, pts = m.group(4), m.group(5)
                compte[genre] += 1
                n = compte[genre]
                nom = ("Exercice" if genre == "exercice" else "Problème") + f" {n}"
                ident = f"{self.prefixe}-{'ex' if genre == 'exercice' else 'pb'}{n}"
                self.points.append(int(pts.split()[0]))
                self.titres.append((ident, nom))
                sortie.append(f'<h3 id="{ident}">{nom} <span class="pts-titre">{pts}</span></h3>')
        tampon.append(s[pos:])
        vider()
        assert not pile, pile
        texte = "\n".join(sortie)
        reste = re.findall(r"\\[A-Za-z]+", re.sub(r"\x00F\d+\x00|\x00T.*?\x00", "", texte, flags=re.S))
        if reste:
            raise ValueError(f"commandes LaTeX non converties : {sorted(set(reste))}")
        return texte


def rendre_formules(formules):
    travail = SITE / "build-pages"
    travail.mkdir(exist_ok=True)
    entree = travail / "formules.json"
    entree.write_text(json.dumps({"macros": MACROS, "formules": formules}), encoding="utf-8")
    r = subprocess.run(["node", str(OUTILS / "katex_rendu.js"), str(entree)],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        sys.exit("KaTeX a refusé des formules :\n" + r.stderr)
    return json.loads(r.stdout)


def rendre_figures(figures, annee, dossier):
    travail = SITE / "build-pages"
    sorties = []
    for i, code in enumerate(figures, 1):
        nom = f"figure-{i}"
        (travail / f"{nom}.tex").write_text(PREAMBULE_FIGURE + code + "\n\\end{document}\n", encoding="utf-8")
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{nom}.tex"],
                           cwd=travail, capture_output=True, text=True, encoding="latin-1")
        if r.returncode:
            sys.exit(f"Figure {i} : échec de pdflatex\n" + r.stdout[-1500:])
        subprocess.run(["pdftocairo", "-svg", f"{nom}.pdf", f"{nom}.svg"], cwd=travail, check=True)
        svg = (travail / f"{nom}.svg").read_text(encoding="utf-8")
        l, h = (float(re.search(fr'{a}="([\d.]+)pt"', svg).group(1)) for a in ("width", "height"))
        shutil.copy(travail / f"{nom}.svg", dossier / f"{nom}.svg")
        alt = FIG_ALT.get(annee, [])
        alt = alt[i - 1] if i <= len(alt) else f"Figure {i} du corrigé"
        # 1 pt TeX ≈ 1,33 px ; agrandi de 15 % pour la lecture à l'écran.
        lpx, hpx = round(l * 1.333 * 1.15), round(h * 1.333 * 1.15)
        sorties.append(f'<figure class="fig"><img src="{nom}.svg" alt="{html.escape(alt)}" '
                       f'width="{lpx}" height="{hpx}" loading="lazy" decoding="async"></figure>')
    return sorties


def copier_katex():
    src = OUTILS / "node_modules" / "katex" / "dist"
    dest = SITE / "assets" / "katex"
    (dest / "fonts").mkdir(parents=True, exist_ok=True)
    css = (src / "katex.min.css").read_text(encoding="utf-8")
    # On ne sert que le WOFF2 (tous les navigateurs actuels) : on retire WOFF et TTF de la feuille.
    css = re.sub(r',url\(fonts/[^)]+\.(woff|ttf)\) format\("(woff|truetype)"\)', "", css)
    (dest / "katex.min.css").write_text(css, encoding="utf-8")
    for f in (src / "fonts").glob("*.woff2"):
        shutil.copy(f, dest / "fonts" / f.name)
    shutil.copy(src.parent / "LICENSE", dest / "LICENSE")


def taille_ko(chemin):
    return f"{round(chemin.stat().st_size / 1024)}&nbsp;Ko"


def main():
    annee = int(sys.argv[1])
    dossier = SITE / "bac-s" / str(annee)
    dossier.mkdir(parents=True, exist_ok=True)
    formules, figures = [], []
    annales = LIVRE / "parties" / "annales"
    sujet = Document((annales / f"bac_{annee}.tex").read_text(encoding="utf-8"), "sujet", annee,
                     formules, figures)
    corrige = None
    if annee in CORRIGES_PUBLIES:
        corrige = Document((annales / f"corrige_{annee}.tex").read_text(encoding="utf-8"), "corrige",
                           annee, formules, figures)

    rendus = rendre_formules(formules)
    images = rendre_figures(figures, annee, dossier)

    def coller(m):
        """Formule en ligne courte + ponctuation voisine : pas de retour à la ligne entre elles."""
        i = int(m.group(2))
        avant, apres = m.group(1), m.group(3)
        if (avant or apres) and not formules[i]["display"] and len(formules[i]["tex"]) <= 40:
            return f'<span class="insec">{avant}{rendus[i]}{apres}</span>'
        return avant + rendus[i] + apres

    def injecter(fragment):
        fragment = re.sub(r"(\(?)\x00F(\d+)\x00((?:&nbsp;)?[,.;:!?)»]*)", coller, fragment)
        fragment = re.sub(r"\x00G(\d+)\x00", lambda m: images[int(m.group(1))], fragment)
        return re.sub(r"\x00T(.*?)\x00", lambda m: m.group(1), fragment, flags=re.S)

    copier_katex()

    pdf_sujet = SITE / "sujets" / f"bac-s-{annee}-mathematiques.pdf"
    pdf_corrige = SITE / "sujets" / f"bac-s-{annee}-mathematiques-corrige.pdf"
    autres = []
    for a in ANNEES:
        if a == annee:
            continue
        if (SITE / "bac-s" / str(a) / "index.html").exists():
            autres.append(f'<a class="annee" href="/bac-s/{a}/"><b>{a}</b><span>Sujet en ligne</span></a>')
        else:
            pdf = SITE / "sujets" / f"bac-s-{a}-mathematiques.pdf"
            autres.append(f'<a class="annee" href="/sujets/{pdf.name}" download><b>{a}</b>'
                          f'<span>PDF · {taille_ko(pdf)}</span></a>')

    sommaire = " · ".join(f'<a href="#{i}">{n}</a>' for i, n in sujet.titres)
    bareme = " + ".join(str(p) for p in sujet.points)
    v = {
        "ANNEE": str(annee),
        "SUJET": injecter(sujet.html),
        "CORRIGE": injecter(corrige.html) if corrige else "",
        "SOMMAIRE_SUJET": sommaire,
        "SOMMAIRE_CORRIGE": " · ".join(f'<a href="#{i}">{n}</a>' for i, n in corrige.titres) if corrige else "",
        "BAREME": bareme,
        "PRIX": PRIX,
        "WHATSAPP": WHATSAPP.format(annee=annee),
        "PDF_SUJET": pdf_sujet.name,
        "PDF_SUJET_KO": taille_ko(pdf_sujet),
        "PDF_CORRIGE": pdf_corrige.name if corrige else "",
        "PDF_CORRIGE_KO": taille_ko(pdf_corrige) if corrige else "",
        "AUTRES_ANNEES": "\n        ".join(autres),
    }
    modele = (OUTILS / "modele_page_bac.html").read_text(encoding="utf-8")
    if not corrige:
        sys.exit("Page sans corrigé : modèle à prévoir (seul le corrigé 2026 est publié).")
    page = re.sub(r"\{\{(\w+)\}\}", lambda m: v[m.group(1)], modele)
    (dossier / "index.html").write_text(page, encoding="utf-8", newline="\n")
    print(f"bac-s/{annee}/index.html : {len(page) // 1024} Ko, {len(formules)} formules, "
          f"{len(figures)} figures, barème {bareme}")


if __name__ == "__main__":
    main()
