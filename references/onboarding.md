# Onboarding : le premier lancement

Objectif : adapter le skill à LA personne sans casser le pipeline. À la fin, son dossier de travail
contient `profil.md`, `regles.toml`, `criteres.toml`, au moins un CV en PDF et une **lettre modèle validée**.
Durée visée : 15 à 25 minutes.

## Comment poser les questions
- Par blocs de 2 à 4 questions avec l'outil AskUserQuestion quand il est disponible, avec des choix
  proposés et l'option recommandée en premier. Sinon, en texte, un bloc à la fois.
- Ne demande jamais ce que tu peux lire toi-même (CV, LinkedIn, portfolio, GitHub, offres).
- Reformule ce que tu as compris à la fin de chaque bloc, en une ligne.
- La personne peut sauter une question : la valeur par défaut de `regles.example.toml` s'applique.

## Bloc A — Situation
1. Quel(s) poste(s) vises-tu ? Propose 3 à 5 intitulés proches, déduits de ce qu'elle dit.
2. Où ? Ville, rayon, télétravail accepté ou exigé.
3. Contrat : CDI, CDD, freelance, alternance ? (pour l'alternance et le stage, adapte `filtre_algolia`)
4. Expérience réelle dans ce métier, en années, et niveau d'anglais honnête.

Ensuite, demande l'urgence et le volume : combien de candidatures par semaine ? (→ `taille_lot`)

## Bloc B — Matériel
- **CV existant** : demande le chemin du fichier, lis-le et extrais les faits dans `profil.md`. Signale
  en trois points ce qui le dessert (pas de chiffres, pas de liens, titre flou, trous non expliqués) et
  propose de le refaire. Ne le refais qu'avec son accord.
- **Pas de CV** : propose d'en construire un (section « Construire le CV » ci-dessous).
- Liens : LinkedIn, portfolio, GitHub, App Store, site. Lis-les si tu y as accès.
- Plusieurs métiers visés : propose un CV par famille (ex. « IA » et « growth »), même base, titre et
  ordre des preuves différents.

## Bloc C — Les preuves
Pour chaque expérience ou projet, obtiens au moins UNE preuve : un fait et un résultat. Questions utiles :
- « Qu'est-ce que tu as construit, lancé ou amélioré là-bas ? Avec quel résultat ? »
- « Un chiffre, même petit, qui le montre ? » (s'il n'y en a pas, on n'en invente pas)
- « Qu'est-ce qu'il ne faut surtout pas que j'écrive ou que j'exagère ? » → `Vérités à ne jamais tordre`
- « Y a-t-il un projet que tu ne veux jamais voir cité ? » → `mentions_interdites`

## Bloc D — Les règles
Montre les règles par défaut de `regles.example.toml` sous forme de tableau court (règle, défaut, ce que
ça change), puis demande ce qu'elle veut changer. Questions qui font vraiment varier les gens :
- Combien d'années d'expérience demandées tu acceptes de viser ? (`experience_max_ans`)
- Une lettre pour chaque offre, ou CV seul ? (`lettre.actif`)
- Tutoiement ou vouvoiement ? (`tutoiement`)
- Qui clique sur « Envoyer » : moi après ton GO, toi après mon remplissage, ou tu préfères juste les textes ? (`envoi.mode`)
- Prétentions salariales à donner ? (`formulaire.pretentions`)

Écris `regles.toml` à partir du template, avec ses choix.

## Bloc E — La lettre modèle (le moment clé)
1. Lance un premier petit balayage (`search.py --days 7`) et choisis UNE offre très adaptée au profil.
2. Rédige la lettre selon `references/lettres.md` et `regles.toml`, ouvre-la en HTML.
3. Demande un retour précis : ton, longueur, ce qui sonne faux, ce qui manque.
4. Corrige jusqu'à validation, puis enregistre-la dans `profil.md`, section `## Lettre modèle validée`,
   avec la liste des retours transformés en règles (`formules_interdites`, `paragraphe_ecart`…).
5. Toutes les lettres suivantes partent de cette base : même ton, même structure, contenu propre à chaque offre.

## Bloc F — Les critères de recherche
Génère `criteres.toml` : une famille par métier, 15 à 60 mots-clés (intitulés FR et EN, outils, jargon,
synonymes), filtres de titre inclure / exclure tirés du bloc A. Fais un balayage de contrôle et montre
le volume par famille ; ajuste si une famille est vide ou noyée.

## Fin d'onboarding
- Ajoute en tête de `profil.md` : `Onboarding : terminé le AAAA-MM-JJ`. Au prochain lancement, le skill
  saute directement à l'étape 1.
- Résume en 5 lignes : métiers, zone, règles changées par rapport au défaut, CV disponibles, prochaine action.
- À tout moment, « change mes règles » ou « refais mon onboarding » relance le bloc concerné.

## Construire le CV
Pars de `templates/cv.html` (une page A4, sobre, lisible par les ATS) :
1. Collecte : titre visé, 3 à 5 expériences ou projets avec une preuve chacun, compétences et outils réels,
   formation, langues, liens. Photo seulement si la personne en veut une.
2. Écris `cv/cv-<famille>.html` en remplaçant les blocs du template. Titre = le métier visé, pas « en recherche d'emploi ».
3. Génère le PDF : `python $SK/scripts/cv_pdf.py cv/cv-<famille>.html`. Vérifie qu'il tient sur une page.
4. Montre le PDF (`open`), corrige selon les retours, puis reporte les faits dans `profil.md`.
Règles : zéro invention, des verbes d'action, un chiffre par ligne quand il existe, pas de jauges de compétences.
