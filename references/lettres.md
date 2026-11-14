# Les lettres

> Valeurs par défaut : `regles.toml [lettre]` et `[formulaire]` l'emportent. Pars toujours de la lettre modèle validée dans `profil.md`.

Les premiers tris se font souvent sur le CV, parfois en quelques heures. La lettre ne sert pas à
raconter sa vie : elle doit montrer en dix secondes qu'on a lu la fiche et qu'on a une preuve
pour chaque attente.

## La méthode : partir de CE QU'ILS ATTENDENT
1. Extrais de `missions` et `profil` les 2 ou 3 attentes centrales, avec leurs mots à eux.
2. **Une preuve par attente**, tirée de `profil.md` : un fait et un chiffre vrai.
3. S'il y a un écart, une phrase honnête pour le dire, avec ce que tu viens apprendre. Pas de paragraphe d'excuses.
4. Termine sur l'envie, jamais sur une réserve.

## Format
- 3 à 5 paragraphes courts, dix à quinze lignes en tout. « Bonjour, » en ouverture, vouvoiement.
- Premier paragraphe : leur enjeu, celui de leurs clients ou de leur produit, pas « je ».
- Un seul lien (portfolio ou projet) par candidature, en clôture : « Mes projets sont visibles ici : … ».
  Si le formulaire a déjà un champ portfolio ou LinkedIn qui porte ce lien, retire-le de la lettre.
- Signature : prénom et nom.
- Texte brut, collé dans le champ du formulaire. Un PDF seulement si le formulaire l'exige.

## Interdits
- Inventer quoi que ce soit : un client, un chiffre, une date (« la semaine dernière »), un livrable.
  Ce qui n'est pas dans `profil.md` n'existe pas.
- Gonfler un projet perso (pas de « mes clients » s'il n'y en a pas).
- Les formules creuses : « passionné », « je coche toutes les cases », « c'est exactement votre fiche »,
  « n'hésitez pas à me contacter ».
- Copier-coller la même lettre : chaque premier paragraphe doit être impossible à envoyer ailleurs.

## Réponses aux questions du formulaire
- Réponds à TOUTES les questions, obligatoires ou non, de façon adaptée à l'entreprise.
- 2 à 4 phrases, à la première personne, avec un chiffre quand il est vrai.
- Prétentions : la fourchette du profil, ou à défaut celle de l'annonce.
- Question technique sur un outil jamais utilisé : dis-le honnêtement et cite l'équivalent réellement pratiqué.
- Questions sensibles (handicap, origine, situation familiale) : laisse vide ou « je préfère ne pas répondre », sauf consigne contraire.

## Stockage
Toutes les lettres d'un lot vont dans `candidatures/lot-AAAA-MM-JJ/lettres.json` (format dans
`templates/lettres.example.json`). Montre-les ensuite avec :

```bash
python ~/.claude/skills/wttj-job-hunter/scripts/lettres_view.py candidatures/lot-AAAA-MM-JJ/lettres.json
open candidatures/lot-AAAA-MM-JJ/lettres.html
```

Ne jamais ouvrir le .json brut pour la relecture.

## Corrections
Quand l'utilisateur corrige UNE règle (« applique juste la règle du lien »), corrige cette règle
et rien d'autre. Ne réécris pas tout le lot.
