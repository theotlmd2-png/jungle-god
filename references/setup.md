# Mise en place (10 minutes, une seule fois)

## 1. Dossier de travail
Tes données restent hors du skill, dans un dossier à toi :

```bash
mkdir -p ~/recherche-emploi/cv && cd ~/recherche-emploi
SK=~/.claude/skills/wttj-job-hunter
cp $SK/.env.example .env
cp $SK/templates/criteres.example.toml criteres.toml
cp $SK/templates/profil.example.md profil.md
cp $SK/templates/regles.example.toml regles.toml
```

Dépose tes CV en PDF dans `cv/`. Python 3.11 ou plus suffit, sans aucune dépendance.

## 2. Identifiants de recherche WTTJ
La page de recherche de welcometothejungle.com interroge un index Algolia avec un identifiant
d'application et une clé de **recherche publique** (lecture seule), visibles par n'importe quel navigateur.
Pour les retrouver :

1. Ouvre https://www.welcometothejungle.com/fr/jobs dans Chrome, puis les DevTools (`Cmd+Option+I`), onglet **Network**.
2. Tape un mot-clé dans la barre de recherche du site.
3. Filtre les requêtes sur `algolia`. Ouvre l'une d'elles :
   - `x-algolia-application-id` → `WTTJ_ALGOLIA_APP`
   - `x-algolia-api-key` → `WTTJ_ALGOLIA_KEY`
   - le nom d'index dans l'URL (`/indexes/<nom>/`) doit se terminer par `published_at_desc`
4. Colle les valeurs dans `.env`.

Avec l'extension Claude in Chrome, Claude peut faire cette lecture à ta place (`read_network_requests`).
Si la recherche renvoie un jour 403, c'est que la clé a changé : refais la manip.

## 3. Test
```bash
python $SK/scripts/search.py --days 3 --out candidatures/test/hits.json
```
Tu dois voir `[OK] N offres depuis le ...`.

## 4. Liste noire de départ
Si tu as déjà postulé via WTTJ, récupère tes candidatures pour ne jamais repostuler au même endroit :
ouvre https://www.welcometothejungle.com/fr/me/application-tracker, fais défiler jusqu'en bas,
puis colle ce snippet dans la console. Il copie un nom d'entreprise par ligne :

```js
copy([...new Set([...document.querySelectorAll('a[href*="/companies/"]')]
  .map(a => a.href.split('/companies/')[1]?.split('/')[0]).filter(Boolean))].join('\n'))
```

Colle le résultat dans `candidatures/tracker.txt`, ajoute les candidatures hors WTTJ dans
`candidatures/extra.txt`, puis lance :

```bash
python $SK/scripts/blacklist.py --root candidatures
```

Le sélecteur dépend du HTML de WTTJ. S'il ne renvoie rien, demande à Claude de lire la page et
d'extraire les noms.
