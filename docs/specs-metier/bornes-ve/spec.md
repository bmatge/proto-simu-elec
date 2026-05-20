---
title: "Carte des bornes de recharge IRVE — Spécification métier"
simulateur: bornes-ve
version: 0.1
date: 2026-05-20
statut: brouillon — à valider
auteur: Bertrand Matge
destinataires: DGEC mobilité, Avere-France, collectivités
---

# 1. Objectif & public visé

**Question à laquelle l'outil répond :** « Où se trouvent les bornes de recharge publiques en France, et quelles sont leurs caractéristiques (puissance, type de prise, conditions d'accès, paiement) ? »

**Public cible :** grand public planifiant un trajet en VE, élus locaux et services techniques de collectivités suivant le maillage de leur territoire, agents DGEC / Avere-France produisant des indicateurs publics.

**Décision aidée :**

- côté usager : identifier la borne adaptée (vitesse, accessibilité, paiement) pour une zone donnée ;
- côté pilotage : comparer la densité de points de recharge entre régions / départements, repérer les zones sous-équipées.

**Hors périmètre :**

- Données temps réel d'occupation et de disponibilité (panne, en charge) — *non couvert*.
- Bornes privées (résidentielles, entreprises) non déclarées au fichier IRVE.
- Recharge poids-lourds (HPC > 350 kW) en tant que filtre dédié — *à instruire en v2*.
- Cible AFIR (recharge tous les 60 km sur le réseau RTE-T) en overlay — *à instruire*.

---

# 2. Scénario par défaut — fil rouge des exemples

Tous les exemples chiffrés de ce document utilisent les **paramètres affichés au chargement** de la carte.

| Catégorie | Valeurs par défaut |
|---|---|
| **Centre carte** | 46.6, 2.3 (France métropolitaine) |
| **Zoom initial** | 6 (vue France entière, choroplèthe régionale) |
| **Filtres** | Aucun filtre actif (toutes les bornes) |
| **KPI nationaux** | ~220 000 stations · ~3,3 M points de charge · ~50 kW de puissance moyenne |
| **Cible 2030 (rappel)** | 400 000 points de recharge publics (cf. dashboard `plan-electrification`) |

> Les volumes affichés dans les KPIs sont rafraîchis en temps réel depuis le miroir Opendatasoft `mobilityref-france-irve-220` (MAJ quotidienne).

---

# 3. Vue d'ensemble du parcours

L'outil est une **carte interactive plein écran** avec, du haut vers le bas :

1. Bandeau de 3 KPI nationaux (stations / points de charge / puissance moyenne)
2. Champ de recherche d'adresse (Base Adresse Nationale)
3. Bloc dépliable « Filtres » : 6 facettes multi-sélect DSFR + 6 filtres booléens custom
4. Carte interactive avec 3 calques pilotés par le niveau de zoom :
   - **Zoom 5-6** : choroplèthe régionale (13 régions, palette séquentielle ascendante)
   - **Zoom 7-9** : choroplèthe départementale (96 départements)
   - **Zoom 10+** : marqueurs individuels (stations IRVE, clusterisés au-delà de 60 pixels de rayon)
5. Panneau latéral droit (auto-ouvert au clic sur une station) avec le détail enrichi (chips, badges, sections)

## 3.1 Vue France entière (zoom 6, choroplèthe régionale)

![](<images/bornes-ve - carte.png>){width=14cm}

Au chargement, la carte affiche le territoire français avec le choroplèthe **régional** des points de charge IRVE (fond IGN Plan, palette bleu DSFR ascendante). Les KPI nationaux en haut donnent un cadrage immédiat. La légende en bas à droite explique la palette et précise la bascule POI au-delà du zoom 10.

### Points à valider sur cette vue

- ☐ Les 3 KPIs en bandeau (stations, points de charge, puissance moyenne) sont-ils les indicateurs cardinaux ? Faut-il en ajouter (densité bornes / 100 km routier, % AFIR atteint) ?
- ☐ Choix de la palette **séquentielle ascendante bleue** (faible → élevé) : permet-elle de bien repérer les zones sous-équipées, ou faut-il une palette divergente autour d'une médiane nationale ?
- ☐ Le **fond cartographique IGN Plan** est-il le bon choix, ou doit-on basculer sur un fond plus neutre (carto positron) pour donner plus de poids au choroplèthe ?
- ☐ La métropole et les DROM sont-ils traités de la même manière dans le fichier IRVE ? Faut-il les exposer dans la même choroplèthe ou séparer ?

---

# 4. Détail par zone fonctionnelle

## 4.1 Zone — Recherche d'adresse (Base Adresse Nationale)

![](<images/bornes-ve - recherche.png>){width=12cm}

**Composant** : champ DSFR `fr-input--lg` avec autocomplétion BAN (`api-adresse.data.gouv.fr/search`), résultats en liste déroulante avec libellé + contexte + type (rue, code postal, commune, etc.).

**Fonctionnement :**

- Au-delà de 3 caractères saisis, requête BAN après 300 ms de debounce
- Liste jusqu'à 6 résultats, sélection via clic ou navigation clavier (↑ ↓ Enter, Esc pour fermer)
- À la sélection, la carte exécute un `flyTo([lat, lon], zoom)` avec un zoom adapté au type de résultat :

| Type BAN | Zoom appliqué |
|---|---|
| `housenumber` | 18 |
| `street` | 17 |
| `municipality` | 13 |
| `locality` | 14 |
| autre | 14 |

### Points à valider sur cette zone

- ☐ La granularité par défaut (zoom 18 sur un numéro de rue) est-elle pertinente, ou faut-il un zoom moins serré pour voir aussi les bornes du voisinage ?
- ☐ Faut-il ajouter une géolocalisation HTML5 (« autour de moi ») en complément de la recherche d'adresse ?
- ☐ La BAN ne couvre que la France — comportement attendu si l'utilisateur tape une adresse étrangère ?

---

## 4.2 Zone — Filtres (facettes DSFR + radios booléens)

![](<images/bornes-ve - filtres.png>){width=14cm}

Bloc dépliable « Filtres : type de prise, paiement, accès, opérateur… » contenant deux familles de filtres câblés sur l'attribut `where` de la source ODS.

### 4.2.1 Facettes multi-sélect (6 champs)

| Facette | Champ ODS | Affichage | Recherche |
|---|---|---|---|
| Région | `reg_name` | multiselect | ✓ |
| Type d'implantation | `implantation_station` | multiselect | — |
| Conditions d'accès | `condition_acces` | multiselect | — |
| Accessibilité PMR | `accessibilite_pmr` | multiselect | — |
| Raccordement | `raccordement` | multiselect | — |
| Opérateur | `nom_operateur` | multiselect | ✓ |

Chaque facette affiche jusqu'à 6 valeurs, persiste dans l'URL via `url-params url-sync` (deep-linkable).

### 4.2.2 Filtres booléens custom (6 champs)

Implémentation custom (DSFR `fr-radio-group--inline`) car `dsfr-data-facets@0.7.1` ne propose pas de mode « radio inline » — son mode `radio` est un dropdown.

| Filtre | Champ ODS | Valeurs |
|---|---|---|
| Prise Type 2 | `prise_type_2` | Tous / Oui / Non |
| Combo CCS | `prise_type_combo_ccs` | Tous / Oui / Non |
| CHAdeMO | `prise_type_chademo` | Tous / Oui / Non |
| Recharge gratuite | `gratuit` | Tous / Oui / Non |
| Paiement CB | `paiement_cb` | Tous / Oui / Non |
| Réservation possible | `reservation` | Tous / Oui / Non |

Le filtre booléen modifie dynamiquement l'attribut `where` de `<dsfr-data-source>` en composant un ODSQL du type `prise_type_2=1 AND paiement_cb=1`.

### Points à valider sur cette zone

- ☐ Le choix des **6 facettes multi-sélect** couvre-t-il les besoins métier ? Faut-il en ajouter (puissance par paliers, nombre de PDC par station) ?
- ☐ Les **6 booléens** sont les bons ? Manque-t-il `accessibilite_24_7`, `paiement_acte`, `paiement_application` ?
- ☐ Combinaison « ET » de toutes les facettes : faut-il offrir un mode « OU » sur certaines (ex. plusieurs types de prise) ?
- ☐ Les filtres booléens **ne sont pas persistés dans l'URL** (limite `dsfr-data-facets` 0.7.1 — crashe sur un URL param inconnu). Acceptable, ou à fixer en priorité ?
- ☐ Combien de bornes restent affichables avec les filtres les plus restrictifs ? Quel seuil minimal d'affichage ?

---

## 4.3 Zone — Carte interactive (3 calques pilotés par le zoom)

![](<images/bornes-ve - carte.png>){width=14cm}

Carte Leaflet avec fond IGN Plan, 3 calques superposés activés par paliers de zoom :

| Zoom | Calque actif | Source | Style |
|---|---|---|---|
| 5-6 | Choroplèthe régionale | `geo-reg` joint à `irve-by-reg` (agrégat `count(*)`, `sum(nbre_pdc)`) | Palette séquentielle ascendante, opacité 0,7 |
| 7-9 | Choroplèthe départementale | `geo-dep` joint à `irve-by-dep` | Idem |
| 10+ | Marqueurs stations | `irve-q` (server-side, bbox debounce 450 ms) | Cluster radius 60 px, max-items 3000 |

**Fond cartographique** : IGN Plan (Géoplateforme).

**Contours géo** : `bornes-ve/data/{regions,departements}.geojson` (servis localement — gregoiredavid/france-geojson @ IGN/INSEE 2018, ~4,8 MB).

**Popup au survol** (`tooltip-field="nom"` pour les choroplèthes, `nom_station` pour les marqueurs).

**Au clic** sur un marqueur, ouverture du panneau latéral droit (cf. 4.4).

### Points à valider sur cette zone

- ☐ Les **paliers de bascule de zoom** (5-6 / 7-9 / 10+) sont-ils les bons ? À zoom 9 on n'a plus que le département mais déjà besoin de voir des stations dans certaines zones denses (Paris intra-muros).
- ☐ Le **clustering au zoom POI** (cluster-radius 60 px) limite l'affichage à 3 000 marqueurs visibles à la fois — pertinent ?
- ☐ Les agrégats `count(*) as stations` et `sum(nbre_pdc) as pdc` portés au popup : **station vs point de charge** — laquelle est l'unité de référence pour le pilotage ?
- ☐ Les contours **INSEE 2018** sont-ils suffisamment à jour ? Mises à jour annuelles via IGN AdminExpress à industrialiser ?

---

## 4.4 Zone — Panneau latéral détail station

![](<images/bornes-ve - detail1.png>){width=12cm}

Panneau ouvert au clic sur une station. Rendu **enrichi** (override de `_renderTemplate` de `dsfr-data-map-popup` après `DOMContentLoaded`), car le rendu natif `{{champ}}` ne supporte pas le mapping `0/1 → Non/Oui`, les badges, ni les sections.

**Structure** (séquentielle, du haut vers le bas) :

1. **Badge type d'implantation** (en haut) — `implantation_station` (ex. « Parking privé à usage public »)
2. **Adresse complète** — `adresse_station` + `consolidated_code_postal` + `consolidated_commune`
3. **Bloc « héros »** centré (gradient bleu pâle) : 2 KPI (nombre de bornes, puissance en kW) + 1 KPI « Gratuit » conditionnel
4. **Section « Connectique »** — chips colorées par type de prise (Type 2, Combo CCS, CHAdeMO), pictogramme `fr-icon-flashlight-fill`
5. **Section « Accès »** — type d'accès, horaires (avec mise en valeur « 24h/24 et 7j/7 »), réservation, accessibilité PMR
6. **Section « Paiement »** — gratuité, carte bancaire
7. **Section « Exploitation »** — puissance avec badge qualitatif (Ultra-rapide ≥ 150 kW, Rapide ≥ 50, Accélérée ≥ 22, normale < 22), exploitant·e·s, raccordement
8. **Méta** en bas : département + région

![](<images/bornes-ve - detail2.png>){width=12cm}

Variante d'affichage (autre station) — démontre la robustesse du rendu face aux valeurs manquantes (« Non renseigné » en italique gris) et aux variantes de typage des booléens (`0/1`, `"True"/"False"`, `OUI/NON`).

### Points à valider sur cette zone

- ☐ La **hiérarchie d'information** (badge type → adresse → KPI héros → connectique → accès → paiement → exploitation) est-elle la bonne pour un usager qui découvre une station ?
- ☐ La **mention « Gratuit » conditionnelle** (3e KPI héros) n'apparaît que si `gratuit=1`. Faut-il aussi mettre en avant `paiement_cb` au même niveau ?
- ☐ Les **badges qualitatifs de puissance** (Ultra-rapide / Rapide / Accélérée) : seuils à confirmer (norme AFIR ? convention Avere ?).
- ☐ Cas des **données manquantes** : on affiche « Non renseigné » en italique gris. Faut-il signaler à l'utilisateur qu'il peut **contribuer à compléter** ou contacter l'opérateur ?
- ☐ Le **lien direct vers data.gouv.fr** pour signaler une erreur sur une station : à ajouter en bas de panneau ?

---

# 5. Récapitulatif des hypothèses & constantes

## 5.1 Sources de données

| Source | Endpoint | Volume |
|---|---|---|
| Base IRVE Etalab (miroir Opendatasoft) | `https://public.opendatasoft.com/.../mobilityref-france-irve-220` | ~220 000 stations |
| Contours régions | `bornes-ve/data/regions.geojson` (gregoiredavid/france-geojson @ IGN/INSEE 2018) | 1,4 MB / 13 régions |
| Contours départements | `bornes-ve/data/departements.geojson` (idem) | 3,4 MB / 96 départements |
| Géocodage adresses | `api-adresse.data.gouv.fr/search` (Etalab) | — |
| Fond cartographique | IGN Plan via Géoplateforme | — |

## 5.2 Champs IRVE exploités (source : schéma IRVE v2.3.1, Etalab)

| Champ | Usage |
|---|---|
| `nom_station`, `nom_operateur`, `nom_amenageur`, `nom_enseigne` | identifications et popup |
| `implantation_station` | badge type, facette |
| `adresse_station`, `consolidated_code_postal`, `consolidated_commune` | adresse panneau |
| `nbre_pdc`, `puissance_nominale` | KPI héros, popup, agrégats |
| `prise_type_2`, `prise_type_combo_ccs`, `prise_type_chademo` | chips connectique, filtres booléens |
| `gratuit`, `paiement_cb`, `condition_acces`, `reservation`, `horaires`, `accessibilite_pmr` | section accès/paiement, facettes, filtres |
| `raccordement` | section exploitation, facette |
| `point_geo` | géoréférencement |
| `dep_code`, `dep_name`, `reg_code`, `reg_name` | choroplèthes, facette région |

## 5.3 Seuils & paramètres techniques

| Paramètre | Valeur |
|---|---|
| Zoom initial | 6 |
| Zoom min / max | 5 / 18 |
| Bascule choroplèthe régionale | zoom 5-6 |
| Bascule choroplèthe départementale | zoom 7-9 |
| Bascule POI individuels | zoom ≥ 10 |
| Cluster radius (POI) | 60 px |
| Max items POI affichés | 3 000 |
| Bbox debounce (POI) | 450 ms |
| Page size facettes | 50 |
| Max values par facette | 6 |

---

# 6. Sources des données

| Donnée | Source officielle | Année / version | Référence |
|---|---|---|---|
| Base nationale IRVE | Etalab (consolidée) | schéma 2.3.1, MAJ quotidienne | `data.gouv.fr/datasets/base-nationale-des-irve` |
| Miroir Opendatasoft | mobilityref-france-irve-220 | MAJ quotidienne | `public.opendatasoft.com` |
| Contours régions/départements | gregoiredavid/france-geojson | INSEE/IGN 2018 | github.com/gregoiredavid/france-geojson |
| Géocodage adresses | API Base Adresse Nationale (Etalab) | continu | `adresse.data.gouv.fr` |
| Fond IGN Plan | Géoplateforme IGN | continu | `geoservices.ign.fr` |

---

# 7. Limites connues

## 7.1 Hypothèses simplificatrices assumées

- Le simulateur compte **un point de recharge = une prise (PDC)**, conformément au schéma IRVE. Ce choix peut diverger du décompte « station » utilisé par certains tableaux de bord publics.
- Les **données IRVE sont déclaratives** : champs facultatifs (puissance, horaires, paiement) peuvent être absents — affichés « Non renseigné ».
- Les **bornes domestiques** (privées, entreprises) **ne figurent pas** dans le fichier IRVE — volontairement exclues du périmètre.
- Le **fond cartographique IGN** est en métropole/DROM uniquement.

## 7.2 Cas non traités (v1)

- **Disponibilité temps réel** (occupation, panne) : nécessiterait un branchement aux opérateurs (Gireve, Hubject, SDMX / FlexiCharge) — *hors scope v1*.
- **Filtre dédié HPC poids lourds** (≥ 350 kW) : à ajouter quand un consensus métier sera établi.
- **Overlay cible AFIR** (recharge tous les 60 km sur RTE-T) : à instruire.
- **Densité bornes par 100 km de route** (vs bornes / habitant ou bornes / km²) : indicateur à arbitrer.

## 7.3 Points ouverts à arbitrer avec les experts

1. **Mise en avant éditoriale des zones sous-équipées** (zones blanches) : politiquement sensible — qui arbitre l'éditorial ? *(open dans la modale business)*
2. **Distinction VL vs PL** comme filtre dédié de premier niveau ?
3. **Pilotage de référence** : région ou département pour les indicateurs de densité ?
4. **Comparaison cible AFIR vs déploiement réel** : qui valide les jalons et leur affichage public ?

## 7.4 Limites techniques `dsfr-data` connues (à reporter au mainteneur)

- `dsfr-data-facets` exige l'attribut `id` (warn silencieux, non documenté).
- Mode `radio` de `dsfr-data-facets` est un dropdown, pas un radio inline.
- `dsfr-data-facets url-params` crashe avec n'importe quel URL param inconnu.
- `dsfr-data-facets` ne supporte pas le remapping des valeurs (`0/1` → `Non/Oui`).
- `dsfr-data-map-popup` capte son `<template>` enfant dans `connectedCallback` avant que le parser HTML insère l'enfant — workaround : override `_renderTemplate` après `DOMContentLoaded`.

---

# Annexe — Historique des versions

| Version | Date | Auteur | Modifications |
|---|---|---|---|
| 0.1 | 2026-05-20 | Bertrand Matge | Création initiale (zones fonctionnelles : carte, recherche BAN, filtres, panneau station) |
