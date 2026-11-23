// Rend une liste de formules LaTeX en HTML avec KaTeX (côté serveur, sans JavaScript dans la page).
// Entrée : fichier JSON { "macros": {...}, "formules": [ { "tex": "...", "display": true|false }, ... ] }
// Sortie (stdout) : tableau JSON des fragments HTML, dans le même ordre.
// Utilisé par page_bac.py ; KaTeX est installé par `npm install --ignore-scripts` dans outils/.
"use strict";
const fs = require("fs");
const katex = require("katex");

const entree = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const sortie = entree.formules.map(function (f, i) {
  try {
    return katex.renderToString(f.tex, {
      displayMode: f.display,
      macros: Object.assign({}, entree.macros),
      throwOnError: true,
      strict: "ignore",
      output: "htmlAndMathml",
    });
  } catch (e) {
    process.stderr.write("Formule " + i + " : " + e.message + "\n  " + f.tex + "\n");
    process.exitCode = 1;
    return "";
  }
});
process.stdout.write(JSON.stringify(sortie));
