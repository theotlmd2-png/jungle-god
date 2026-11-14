# WTTJ Job Hunter

**Un skill Claude Code qui transforme ta recherche d'emploi sur Welcome to the Jungle en pipeline.**
Il balaye des centaines d'offres par mots-clés, garde celles qui te correspondent vraiment, écrit une
lettre ciblée pour chacune à partir de TES faits, remplit les formulaires et n'oublie jamais où tu as déjà postulé.

> Construit et utilisé pendant deux mois de recherche réelle : **plus de 130 candidatures ciblées**,
> dont une bonne partie sur des offres que je n'aurais jamais trouvées en cherchant à la main.

---

## Pourquoi

Chercher un job à la main, c'est taper trois intitulés dans une barre de recherche, rater 80 % des
offres qui te correspondent (parce qu'elles s'appellent autrement) et réécrire la même lettre à 23 h.

Ce skill inverse la logique :

| À la main | Avec le skill |
|---|---|
| 3 intitulés cherchés | 15 à 60 mots-clés par métier (outils, jargon, FR et EN) |
| Tu lis le titre | Claude lit la fiche **en entier** et écarte celles qui demandent 5 ans ou un diplôme que tu n'as pas |
| Une lettre générique | Une lettre par offre : une preuve tirée de ton parcours pour chaque attente de la fiche |
| « J'ai déjà postulé là-bas ? » | Liste noire automatique, alimentée par ton suivi WTTJ |
| 20 minutes par formulaire | Claude remplit dans Chrome, tu valides |

## Comment ça marche

```
          ┌───────────── première fois seulement ─────────────┐
          │ 0. Onboarding : situation → CV → preuves → règles │
          │    → lettre modèle validée → critères             │
          └───────────────────────┬───────────────────────────┘
                                  ▼
 1. Balayage ──▶ 2. Tri ──▶ 3. Shortlist ──▶ GO ──▶ 4. Lettres ──▶ 5. Envoi ──▶ 6. Suivi
  mots-clés     fiche lue     tableau        toi     une par offre   Chrome      liste noire
      ▲                                                                              │
      └─────────────────── entreprises contactées exclues ◀──────────────────────────┘
```

**0. Onboarding.** Au premier lancement, Claude t'interviewe : métier visé, zone, expérience réelle,
preuves (ce que tu as construit et avec quel résultat), ce qu'il ne faut jamais écrire. Pas de CV ?
Il t'en construit un. Puis il écrit une **lettre modèle sur une vraie offre**, tu la corriges, et
toutes les suivantes partent de cette base.

**1. Balayage.** Interrogation de l'index de recherche de WTTJ avec tous tes mots-clés, filtrage par
date, ville, télétravail et titre, puis exclusion des entreprises déjà contactées.

**2. Tri.** Lecture complète des fiches retenues (missions, profil recherché, process, salaire,
formulaire, questions obligatoires). C'est ici que se fait la précision : mieux vaut 5 offres justes que 16 approximatives.

**3. Shortlist.** Un tableau : entreprise, poste, salaire, parcours de candidature, pourquoi ça colle,
quel est le risque. **Rien ne part sans ton GO.**

**4. Lettres.** Pour chaque offre, une preuve par attente de la fiche, l'écart assumé en une phrase,
les réponses à toutes les questions du formulaire. Relecture dans une page HTML avec bouton « Copier ».

**5. Envoi.** Claude remplit les formulaires un par un dans ton Chrome (WTTJ, Teamtailor, Greenhouse,
Lever, Ashby…), vérifie chaque champ et s'arrête dès qu'il faut créer un compte, passer un CAPTCHA ou trancher un doute.

**6. Suivi.** Statut de chaque candidature, liste noire mise à jour, et relevé des réponses dans Gmail si tu l'as branché.

## Il s'adapte à toi

Le pipeline est fixe, tes règles ne le sont pas. Pendant l'onboarding, Claude remplit `regles.toml` avec toi :

- années d'expérience que tu acceptes de viser, part d'offres « stretch » ;
- lettre pour chaque offre, ou CV seul ;
- tutoiement ou vouvoiement, longueur, formules interdites, projets à ne jamais citer ;
- un CV par métier, ou retouches légères par offre ;
- qui clique sur « Envoyer » : Claude après ton GO, toi après son remplissage, ou textes seulement ;
- taille des lots, dosage par métier (« max 4 offres sales par lot »).

Ce qui ne bouge jamais, c'est le socle : **zéro invention** (rien n'est écrit qui ne soit dans ton
profil), pas d'envoi sans GO, jamais deux candidatures identiques dans la même boîte, tes données restent chez toi.

## Installation

Prérequis : [Claude Code](https://claude.com/claude-code), Python 3.11+ (aucune dépendance), Google Chrome.
L'extension [Claude in Chrome](https://claude.com/chrome) est recommandée pour l'envoi automatique ;
sans elle, Claude te prépare les textes à coller.

```bash
git clone https://github.com/theotlmd2-png/wttj-job-hunter ~/.claude/skills/wttj-job-hunter
```

Puis, dans Claude Code :

```
Je cherche un CDI, aide-moi à postuler sur Welcome to the Jungle.
```

Le skill se déclenche tout seul et lance l'onboarding. Le détail technique (identifiants de
recherche, liste noire de départ) est dans [`references/setup.md`](references/setup.md), et Claude le fait avec toi.

## Au quotidien

```
Nouveau lot : les offres des 7 derniers jours, max 10.
GO pour 1, 3, 4, 7 et 9.
Envoie.
Change mes règles : je veux bien viser 3 ans d'expérience maintenant.
```

## Contenu du repo

```
SKILL.md                     le cerveau : le pipeline que Claude suit
references/
  onboarding.md              l'interview du premier lancement, construction du CV
  setup.md                   mise en place technique
  tri.md                     critères durs, format de la shortlist
  lettres.md                 méthode de rédaction, réponses aux formulaires
  envoi.md                   remplissage dans Chrome, arrêts obligatoires, pièges connus
scripts/
  search.py                  balayage par mots-clés
  details.py                 fiches complètes et questions des formulaires
  blacklist.py               entreprises déjà contactées
  lettres_view.py            relecture des lettres en HTML
  cv_pdf.py                  CV ou lettre HTML → PDF A4
templates/                   profil, règles, critères, CV, format des lettres
tests/                       tests unitaires (pytest)
```

Tes fichiers (`profil.md`, `regles.toml`, `criteres.toml`, `cv/`, `candidatures/`) vivent dans ton
dossier de travail, en dehors du skill, et sont exclus de git.

## Leçons apprises en route

- **Les refus en moins de 48 h sont des tris sur CV.** Si tu en enchaînes, c'est le CV qu'il faut revoir, pas les lettres.
- **Les mots-clés larges battent les intitulés.** « n8n », « agents IA » ou « adoption IA » font remonter des postes qui ne s'appellent jamais comme tu le penses.
- **Le tri sur le titre ne suffit pas.** Un tiers des offres « junior » demandent 3 à 5 ans dans le texte.
- **Un remplissage à la fois.** Plusieurs agents qui remplissent des formulaires en parallèle, c'est des onglets mélangés et des envois en double.
- **Deux champs fichier sur WTTJ** : la photo d'abord, le CV ensuite. Vise le bon.

## Avertissements

- Projet indépendant, **sans lien avec Welcome to the Jungle**. Il utilise les mêmes requêtes de
  recherche publiques que le site, à faible cadence, pour un usage personnel. Respecte les conditions
  d'utilisation des sites que tu utilises ; n'en fais pas un scraper de masse.
- Tu restes responsable de ce qui est envoyé en ton nom. Relis la shortlist et les lettres.
- Les sites changent : si une recherche ou un formulaire casse, ouvre une issue.

## Licence

MIT
