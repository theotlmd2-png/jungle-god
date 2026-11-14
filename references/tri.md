# Le tri : critères durs

> Les seuils ci-dessous sont des valeurs par défaut : `regles.toml [tri]` l'emporte toujours.

C'est l'étape qui fait la différence. Un balayage remonte des centaines d'offres, et la plupart
sont des faux positifs : le titre colle, mais la fiche demande autre chose. **Mieux vaut 5 offres
justes que 16 approximatives.**

## Deux passes
1. **Passe titre**, sur `hits.json` : écarte ce que le titre trahit déjà (séniorité, métier voisin,
   pays étranger, stage). Garde 20 à 40 candidates et écris leurs clés dans `keys.txt`.
2. **Passe fiche**, sur `details.json` : lis EN ENTIER `missions` + `profil` + `process`. C'est là
   que se cachent les vrais critères (« 5 ans minimum », « école d'ingénieur », « anglais C2 »).

## Écarter si (à adapter au profil, à valider à l'étape 0)
- Années d'expérience demandées au-delà de ce que le profil peut défendre (souvent > 2 à 3 ans pour un junior).
- Diplôme exigé que le profil n'a pas (grande école, ingénieur, Bac+5 spécifique) et écrit comme obligatoire.
- Compétence cœur que le profil n'a pas (ex. coder à la main en Python, SQL avancé, Figma, media buying).
- Langue exigée au-dessus du niveau réel.
- Le titre ment : un « Product Builder » qui est en fait PM, designer et dev à la fois ; un « Growth »
  qui est en fait 100 % ads payantes.
- Le poste est ailleurs que ce qu'affiche la carte (ex. « Paris » sur WTTJ, Francfort dans la fiche).
- Entreprise déjà contactée (le script l'écarte déjà, mais vérifie les filiales et les noms de marque).
- Doublon : deux postes dans la même boîte → n'en garder qu'un, le plus proche du profil.

## Garder en priorité
- Signaux d'ouverture : « profil atypique », « autodidacte », « junior bienvenu », « première expérience »,
  « montrez-nous vos projets », « pas besoin d'être développeur ».
- Le cœur du poste correspond aux preuves du profil, pas seulement les mots-clés.
- Offre de moins de 14 jours (au-delà, les chances chutent).

## Écart assumé (stretch)
Une offre qui demande un peu plus que le profil peut rester, à condition que l'écart soit d'UN seul
critère, et que ce soit marqué « stretch » dans la shortlist. Jamais plus de 20 % du lot.

## Présenter la shortlist
Un tableau, une ligne par offre, triée par adéquation :

| # | Entreprise | Poste | Publiée | Exp. | Salaire | Parcours | Pourquoi | Risque |
|---|---|---|---|---|---|---|---|---|

- « Pourquoi » : le signal décisif de la fiche, en 15 mots maximum.
- « Risque » : l'exigence manquante, sans l'enjoliver.
- « Parcours » : formulaire WTTJ, ou ATS externe (Teamtailor, Greenhouse, Lever, Workday…).
- Signale aussi les offres écartées en une ligne chacune avec la raison, pour que l'utilisateur puisse en repêcher une.

Puis demande le GO, offre par offre ou pour le lot entier.
