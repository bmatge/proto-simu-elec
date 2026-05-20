# Spécifications métier des simulateurs

Chaque sous-dossier `<simulateur>/` contient :

- `spec.md` — la **méthode et les données** du simulateur, structurée **étape par étape**.
- `images/` — captures d'écran référencées par le `spec.md` (une capture par étape ou zone fonctionnelle).

Le format est conçu pour être **validé par des experts métier** (Anah, DGEC, ADEME, etc.) qui voient à la fois l'interface réelle (capture) et la méthode (texte, formules, tableaux d'hypothèses).

## Pour qui ?

- **Auteurs** : développeurs du portail (Bertrand). La source de vérité textuelle vit ici, à côté du code.
- **Diffusion métier** : chef de projet. Reçoit les `.docx` générés et les redistribue par les canaux de l'administration (Resana, Tchap, mail, SharePoint).

## Structure d'une spec

Chaque `spec.md` suit ce plan (voir `template.md`) :

1. Objectif & public visé
2. Vue d'ensemble du parcours
3. **Détail étape par étape** — chaque étape contient sa capture, ses champs, ses constantes, sa formule, sa sortie, ses points à valider
4. Récapitulatif consolidé des hypothèses & constantes
5. Sources des données
6. Limites connues

## Arborescence

```
docs/specs-metier/
├── README.md
├── template.md                       ← squelette à recopier
├── build.sh                          ← génère les .docx
├── reference.docx                    ← (optionnel) style Word de référence
├── <simulateur>/
│   ├── spec.md
│   └── images/
│       ├── 00-parcours-vue-ensemble.png
│       ├── 01-etape-...png
│       └── ...
└── dist/                             ← .docx générés (ignoré par Git)
```

## Workflow

### Côté développeur (Bertrand)

1. Créer le sous-dossier `<simulateur>/` et recopier `template.md` en `<simulateur>/spec.md`.
2. Le remplir en lisant le code du simulateur correspondant — laisser les balises image vides au début.
3. Prendre les captures d'écran et les déposer dans `<simulateur>/images/`.
4. Régénérer le `.docx` : `./build.sh`.
5. Commit du `.md` et des images dans le repo (le `.docx` est ignoré).

### Côté chef de projet

1. Reçoit les `.docx` depuis `dist/` (ou via lien partagé).
2. Choisit le canal de diffusion adapté à chaque expert (mail avec mode Révision Word, réunion, etc.).
3. Centralise les retours dans le Word ou dans un compte-rendu séparé.
4. Remonte les arbitrages au développeur sous forme de modifications à apporter au `.md` source.

## Génération des `.docx`

Prérequis : pandoc installé (`brew install pandoc`, une seule fois).

```bash
cd docs/specs-metier
./build.sh                 # itère sur tous les <simulateur>/spec.md
```

**Style Word homogène** : un `reference.docx` est présent à la racine de `specs-metier/`. C'est un .docx remis en forme à la main (polices, couleurs, espacements, bordures de tableaux) ; pandoc applique automatiquement ses styles à toutes les générations. Pour le faire évoluer : ouvrir, modifier la mise en forme, sauvegarder par-dessus.

## Versioning

Le `spec.md` et les images sont versionnés dans Git ; les `.docx` générés (`dist/`) sont ignorés. Le numéro de version de chaque spec est porté dans son frontmatter (`version:`), à incrémenter à chaque changement substantiel transmis pour validation.
