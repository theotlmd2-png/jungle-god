# L'envoi via Claude in Chrome

> Le mode d'envoi et la gestion des consentements viennent de `regles.toml [envoi]`.

Charge d'abord le skill ou les outils `mcp__claude-in-chrome__*`. Si l'extension n'est pas connectée,
ouvre les offres avec `open -a "Google Chrome" <url>` et donne à l'utilisateur les textes à coller.

## Règles
- **Séquentiel, une seule fenêtre, au premier plan.** Un onglet par offre, l'un après l'autre.
  Le remplissage en parallèle par plusieurs agents finit en chaos (onglets mélangés, envois en double).
- Avant de cliquer sur « Envoyer », relis tous les champs par JavaScript : nom, email, téléphone,
  fichier CV, lettre, réponses.
- **Le bon fichier dans le bon champ.** Sur WTTJ, il y a deux `input[type=file]` : la photo de profil
  d'abord, puis le CV. Vise `input[name="resume"]`, jamais le premier venu.
- CV : le PDF de la famille indiquée dans `lettres.json`, jamais un autre.
- Consentements, CGU, newsletters : coche ce qui est obligatoire pour postuler, seulement après
  l'accord explicite de l'utilisateur. Ne coche jamais l'optionnel.
- LinkedIn obligatoire et absent du profil : mets le lien portfolio si le champ l'accepte, sinon demande.
- Envoi : seulement après le GO de l'utilisateur sur le lot. Si un doute apparaît pendant le
  remplissage (question imprévue, prétention à fixer, info manquante), arrête-toi et demande.

## Arrêts obligatoires (on rend la main)
- Création de compte (Workday, Taleo, Yello, SuccessFactors…) : l'utilisateur la fait lui-même.
- CAPTCHA, vérification par email ou SMS.
- Paiement, ou demande de pièce d'identité.
- Formulaire qui ne trouve pas son bouton d'envoi : ne pas cliquer au hasard, signaler.

## Après chaque envoi
1. Vérifie la page de confirmation (ou le bandeau « Candidature envoyée »).
2. Mets à jour le `statut` dans `lettres.json` : `envoyée AAAA-MM-JJ`, `remplie non envoyée`,
   `bloquée : <raison>`, `écartée : <raison>`.
3. En fin de lot, relance `blacklist.py` pour que ces entreprises disparaissent des prochains balayages.

## Pièges connus
- Fenêtre Chrome minuscule (Stage Manager) : ramène-la au premier plan et agrandis-la avant d'agir.
- Formulaires Teamtailor, Ashby, Greenhouse : questions en anglais, alors réponds en anglais.
- Annonce en anglais : lettre en anglais, sauf si la fiche dit le contraire.
- WTTJ peut afficher la ville du siège et non celle du poste : la fiche fait foi.
