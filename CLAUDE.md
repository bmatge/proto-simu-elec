# CLAUDE.md — simulateurs-portail-elec

> **Important** : ce fichier ne réécrit pas la doc du projet. Avant toute tâche, **lire d'abord** les docs listées ci-dessous.

## 📚 Documentation à lire en priorité

- `README.md` (architecture, ajout d'un simulateur, déploiement)
- Fiche vault : `~/Documents/Obsidian/10-Projects/simulateurs-portail-elec.md`

## 🧰 Stack

- HTML / CSS / JS statique, **pas de framework imposé** au niveau du portail.
- DSFR via CDN jsdelivr (`@gouvfr/dsfr@1.14.4`) — uniquement pour le portail d'accueil ; les simulateurs sont libres de leur stack.
- nginx (alpine) en runtime, Docker Compose au **contrat spawn** (réseau `proxy`, labels Traefik `${APP_NAME}`/`${DOMAIN}`, ACME `letsencrypt`). Déploiement : `ssh vps "spawn up proto-simu-elec git@github.com:bmatge/proto-simu-elec.git"`. Dev : `docker compose -f docker-compose.yml -f docker-compose.dev.yml up`.
- Domaine : `proto-simu-elec.lab.miweb.run` (ancien `simu-elec.bercy.matge.com` redirigé 301).

## 🗂️ Convention d'arborescence

- Chaque simulateur = un dossier à la racine (`voiture/`, …) avec un `index.html` → URL `/<slug>/`.
- Le manifeste `shared/simulators.json` est la source de vérité pour la home et la barre de portail.
- Ne pas créer de dossier `simulators/` parent — les simulateurs vivent à plat à la racine.

## ✅ Règles Claude-specific

1. **Toujours lire la doc** listée ci-dessus avant d'agir.
2. **Ajouter un simulateur** ⇒ créer le dossier, déposer un `index.html` minimal incluant `portal-bar.css/js`, puis mettre à jour `shared/simulators.json`. Voir README.
3. **Pas de framework au portail** sans en parler — `index.html` à la racine reste un HTML statique servi tel quel.
4. **Décision structurante** (choix de lib, refactor majeur, mutualisation cross-simulateurs, migration DSFR) → `/new-adr "<titre>"`.
5. **Fin de session significative** → `/session-end`.
6. **Pas de commit direct sur `main`**, pas de `git push --force`, pas de modification des `.env*`.
7. **Pas d'install de dépendance** au niveau du portail sans m'en parler. Pour un simulateur lourd, dépendances scopées à son sous-dossier.
8. Doc obsolète ou manquante → la signaler et proposer la MAJ.

## 📏 Règle d'or

Ce fichier doit rester **sous 80 lignes**. Son rôle : pointer vers la vraie doc et rappeler les règles Claude.
