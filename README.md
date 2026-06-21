# simulateurs-portail-elec

Portail regroupant plusieurs simulateurs autour de l'**énergie / électricité** (DGEC),
servi en statique par nginx, déployé sur `https://proto-simu-elec.lab.miweb.run`
(ancien domaine `simu-elec.bercy.matge.com` redirigé en 301).

## Architecture

Static multi-pages — chaque simulateur vit dans son propre dossier à la racine
et est servi tel quel à l'URL `/<slug>/`. Pas de framework imposé : un
simulateur peut être un simple `index.html` (CSS + JS inline) ou bien un projet
plus lourd avec son propre `package.json` et un `dist/` buildé en amont.

```
.
├── index.html               # portail d'accueil (DSFR, liste les simulateurs)
├── shared/
│   ├── simulators.json      # manifeste des simulateurs (slug, titre, statut…)
│   ├── portal-bar.css       # barre de portail injectée dans chaque simu
│   └── portal-bar.js
├── voiture/                 # ← un simulateur
│   └── index.html
├── nginx.conf
├── Dockerfile
├── docker-compose.yml            # contrat spawn (réseau proxy, labels Traefik ${APP_NAME}/${DOMAIN})
└── docker-compose.dev.yml        # dev (port 8080, hot-reload volumes) — à passer via -f
```

## Ajouter un simulateur

1. Créer un dossier `mon-simu/` à la racine du repo.
2. Y poser au minimum un `index.html` (et tous les assets qui vont avec).
3. Ajouter dans `<head>` ces deux lignes pour récupérer la barre de portail :
   ```html
   <link rel="stylesheet" href="/shared/portal-bar.css">
   <script src="/shared/portal-bar.js" defer></script>
   ```
4. Référencer le simulateur dans `shared/simulators.json` :
   ```json
   {
     "slug": "mon-simu",
     "title": "Titre affiché",
     "tagline": "Phrase d'accroche.",
     "status": "draft",
     "tags": ["catégorie"]
   }
   ```
   `status` ∈ `draft | beta | published | archived`.

Pas de build à lancer — le compose dev recharge tout au refresh navigateur
grâce aux volumes montés en read-only.

## Dev local

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up   # → http://localhost:8080
```

## Déploiement (lab VibeLab / spawn)

```bash
ssh vps "spawn up proto-simu-elec git@github.com:bmatge/proto-simu-elec.git"
```

`spawn` fait pull → build → up derrière Traefik (réseau `proxy`, ACME
`letsencrypt`) et expose `https://proto-simu-elec.lab.miweb.run`. L'ancien
domaine `simu-elec.bercy.matge.com` est redirigé 301 (cf. skill `vps-spawn`,
section « Migration oldvps → lab », et ADR-047).

## Doc projet

- Fiche vault : `~/Documents/Obsidian/10-Projects/simulateurs-portail-elec.md`
- ADR : `~/Documents/Obsidian/30-Knowledge/ADR/` (filtrer par projet)
