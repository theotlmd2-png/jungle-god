---
name: wttj-job-hunter
description: Pipeline de recherche d'emploi sur Welcome to the Jungle avec Claude Code. Au premier lancement, interviewe la personne (métier, zone, preuves, règles), construit son CV si besoin et valide avec elle une lettre modèle. Ensuite, à chaque lot, balaye des centaines d'offres par mots-clés, écarte celles qui ne collent pas après lecture complète de la fiche, rédige une lettre ciblée par offre à partir de faits vérifiés, remplit les formulaires dans Chrome et tient une liste noire pour ne jamais postuler deux fois. À utiliser quand l'utilisateur parle de chercher un job, un CDI, une alternance, de postuler, de candidatures, de CV, de lettres de motivation, de WTTJ ou de Welcome to the Jungle, ou demande « trouve-moi des offres », « un nouveau lot », « postule ».
---

# WTTJ Job Hunter

Le principe : **beaucoup de candidatures, mais chacune juste.** La machine fait le volume (balayage,
tri, rédaction, remplissage). L'humain garde les décisions qui comptent : la vérité de son profil,
ses règles, le GO sur la shortlist.

```
          ┌───────────── première fois seulement ─────────────┐
          │ 0. Onboarding : situation → CV → preuves → règles │
          │    → lettre modèle validée → critères             │
          └───────────────────────┬───────────────────────────┘
                                  ▼
 1. Balayage ──▶ 2. Tri ──▶ 3. Shortlist ──▶ GO ──▶ 4. Lettres ──▶ 5. Envoi ──▶ 6. Suivi
  search.py      details.py    tableau       humain   lettres.json    Chrome       blacklist.py
      ▲                                                                                │
      └──────────────────── entreprises contactées exclues ◀───────────────────────────┘
```

## Deux couches de règles
- **Le socle** (fin de ce fichier) : l'ordre du pipeline, les formats de fichiers, zéro invention,
  le GO humain, la liste noire. Il est identique pour tout le monde et ne se désactive pas.
- **Les règles réglables** : `regles.toml` dans le dossier de travail, créé à l'onboarding à partir
  de `templates/regles.example.toml`. Chaque personne garde, change ou désactive ce qu'elle veut
  (années d'expérience visées, lettre ou non, tutoiement, qui clique sur « Envoyer », taille des lots…).
  **Relis `regles.toml` au début de chaque lot** ; quand une référence donne une valeur par défaut,
  c'est `regles.toml` qui l'emporte.

Quand la personne énonce une nouvelle préférence durable (« plus jamais de sales », « max 4 bizdev »),
écris-la dans `regles.toml` ou `profil.md` et dis-le en une ligne.

## Repères
- `SK=~/.claude/skills/wttj-job-hunter` : scripts, références, templates
- dossier de travail, par défaut `~/recherche-emploi` : `.env`, `profil.md`, `regles.toml`,
  `criteres.toml`, `cv/`, `candidatures/`. Lance toujours les scripts **depuis ce dossier**.
- un lot = `candidatures/lot-AAAA-MM-JJ/`

## Étape 0 — Onboarding (si `profil.md` n'indique pas « Onboarding : terminé »)
1. Mise en place technique : `references/setup.md`. Fais toi-même tout ce que tu peux.
2. Interview et construction : `references/onboarding.md`, blocs A à F. Elle couvre la situation, le CV
   (lu, amélioré ou construit avec `templates/cv.html` et `scripts/cv_pdf.py`), les preuves, les règles,
   la **lettre modèle validée sur une vraie offre** et les critères de recherche.
3. Si la personne veut aller vite, fais les blocs A, B et E, mets les défauts ailleurs et dis-le.

## Étape 1 — Balayage
```bash
python $SK/scripts/blacklist.py --root candidatures
python $SK/scripts/search.py --days 14 --out candidatures/lot-AAAA-MM-JJ/hits.json
```
- Fenêtre : depuis le dernier lot s'il est récent, sinon `age_max_offre_jours`.
- Plus de 300 résultats : resserre les filtres de titre. Moins de 20 : élargis les mots-clés ou la fenêtre.
- Annonce le volume brut, les offres écartées par la liste noire et la répartition par famille.

## Étape 2 — Tri (le cœur)
`references/tri.md`, avec les seuils de `regles.toml [tri]`. Passe titre sur `hits.json` → `keys.txt`, puis :
```bash
python $SK/scripts/details.py --keys candidatures/lot-AAAA-MM-JJ/keys.txt --out candidatures/lot-AAAA-MM-JJ/details.json
```
Lis chaque fiche EN ENTIER. Une offre passe parce que ses missions correspondent aux preuves de
`profil.md`, pas parce qu'elle contient un mot-clé.

## Étape 3 — Shortlist et GO
Tableau de `references/tri.md`, offres écartées comprises, avec leur raison, puis attends le GO.
Respecte `taille_lot` et `dosage`. **Rien ne s'écrit ni ne s'envoie avant le GO.**

## Étape 4 — Lettres
`references/lettres.md` + `regles.toml [lettre]`, **en partant de la lettre modèle validée** (même ton,
même structure, contenu propre à l'offre). Réponses préparées pour toutes les questions du
formulaire. CV choisi par famille. Tout va dans `lettres.json`, puis `lettres_view.py`, puis tu ouvres le HTML.
Si `lettre.actif = false`, ne prépare que les réponses au formulaire.

## Étape 5 — Envoi
`references/envoi.md`, dans le mode choisi (`envoi.mode`) : Claude envoie après le GO, Claude remplit et
l'humain envoie, ou textes seulement. Mets à jour le `statut` après chaque offre.

## Étape 6 — Suivi
Relance `blacklist.py`, puis fais le bilan : envoyées, remplies mais non envoyées avec la raison, actions
laissées à l'humain (compte à créer, lien de vérification). Si `suivi.gmail = true`, relève les réponses.
Des refus en moins de 48 h veulent dire un tri sur le CV : propose de retravailler le CV, pas les lettres.

## Le socle (non négociable, quelles que soient les règles)
1. **Zéro invention.** Aucun fait, chiffre, client, date ou outil absent de `profil.md`. En cas de doute, demande.
2. **Pipeline dans l'ordre** : pas de lettre sans tri, pas d'envoi sans GO.
3. **Liste noire** tenue à jour : jamais deux candidatures identiques dans la même entreprise.
4. **Formats stables** : `hits.json`, `keys.txt`, `details.json`, `lettres.json` (voir `templates/`),
   pour que chaque lot puisse être repris par une autre session.
5. **Politesse réseau** : délais entre requêtes conservés, pas de balayage en boucle, un lot par jour au plus.
6. **Données personnelles en local** : `profil.md`, `regles.toml`, CV et `candidatures/` ne sont jamais commités ni publiés.
7. **Arrêt et main rendue** sur création de compte, CAPTCHA, paiement, pièce d'identité ou doute.
