---
title: "Tableau de bord Électrification de la France — Spécification métier"
simulateur: dashboard
version: 0.1
date: 2026-05-20
statut: brouillon — à valider
auteur: Bertrand Matge
destinataires: DGEC, cabinet MTE, direction de la communication, Pôle Vauban / MIWEB
---

# 1. Objectif & public visé

**Question à laquelle le tableau de bord répond :** « Où en est la France dans sa trajectoire d'électrification, vue par 4 angles (mix électrique, mobilité, bâtiment, cap 2050) ? Quelles sources opendata officielles le démontrent ? »

**Public cible :** journalistes spécialisés, parlementaires, ONG, grand public averti. Format **dashboard public** mobilisant des **données opendata officielles** uniquement.

**Décision aidée :**

- argumenter la trajectoire française face à un interlocuteur : « la production se décarbone, l'électrification des usages reste à accélérer » ;
- comparer les valeurs actuelles aux cibles 2030 (PPE 2) et 2050 (SNBC, scénarios ADEME Transition(s) 2050) ;
- mettre à disposition des **sources sourcées** (citation immédiate) pour journalistes et chercheurs.

**Hors périmètre (v0.2 démonstrateur) :**

- Pilotage opérationnel des 22 mesures → cf. `/plan-electrification/`.
- Comparaisons UE détaillées (Allemagne, Espagne) — *à instruire phase 2*.
- Données par région / commune / IRIS — *uniquement France entière en v0.2*.
- Couches scénarios prospectifs ADEME Transition(s) 2050 — *callout phase 2*.
- Carte choroplèthe départementale (Ecolab) — *callout phase 2*.

---

# 2. Scénario par défaut — fil rouge des exemples

Tous les exemples chiffrés de ce document utilisent les **données live** au chargement du tableau de bord (mai 2026).

| Onglet | Valeurs actuelles approximatives |
|---|---|
| **Mix électrique** | Intensité CO₂ ≈ 40 gCO₂/kWh · Production nucléaire ≈ 35 000 MW · Consommation ≈ 55 000 MW |
| **Mobilité** | ~220 000 points IRVE (référentiel consolidé) |
| **Bâtiment** | Répartition chauffage DPE et distribution classes A→G |
| **Cap 2050** | Mix bas-carbone ~92 %, solaire ~25 GW (cible 54-60), éolien ~24 GW (cible 33-35), VE ~3 % du parc VP (cible 15 % en 2030) |

> Les chiffres exacts du « scénario » varient à chaque ouverture (données temps réel ou consolidées récentes). Les **cibles**, en revanche, sont stables (sources PPE 2, SNBC, ADEME, Règlement UE).

---

# 3. Vue d'ensemble du parcours

Page unique avec un composant DSFR `fr-tabs` à **5 onglets** :

| Onglet | Angle éditorial | Captures |
|---|---|---|
| 1. Mix électrique | « Le mix se décarbone-t-il ? » | `dashboard - onglet 1 - mix.png` |
| 2. Mobilité | « La mobilité bascule-t-elle vers l'électrique ? » | `dashboard - onglet 2 - mobilite.png` |
| 3. Bâtiment | « Le bâtiment s'électrifie-t-il ? » | `dashboard - onglet 3 - batiment.png` |
| 4. Cap 2050 | « Où en est-on par rapport aux objectifs ? » | `dashboard - onglet 4 - objectifs.png` |
| 5. Brief & sources | Métadonnées techniques (sources câblées, endpoints, trous identifiés, composants ChartsBuilder) | — *(pas de capture, contenu technique)* |

Tous les visuels utilisent `<dsfr-data-source>` (ODRÉ Opendatasoft ou ADEME data-fair) et `<dsfr-data-chart>` / `<dsfr-data-kpi>` / `<dsfr-data-a11y>` de `dsfr-data@0.7.1`.

---

# 4. Détail par onglet

## 4.1 Onglet 1 — Mix électrique

![](<images/dashboard - onglet 1 - mix.png>){width=14cm}

**Question éditoriale :** « Le mix électrique se décarbone-t-il ? »

### 4.1.1 KPIs temps réel (3 indicateurs)

Source : `eco2mix-national-tr` (ODRÉ, RTE), filtrée sur `taux_co2 is not null` pour exclure les enregistrements de prévisions où seules les prévisions sont renseignées.

| KPI | Champ | Couleur DSFR | Icône |
|---|---|---|---|
| Intensité CO₂ (gCO₂/kWh) | `taux_co2` | vert | `ri-leaf-line` |
| Production nucléaire (MW) | `nucleaire` | bleu | `ri-flashlight-line` |
| Consommation France (MW) | `consommation` | bleu | `ri-plug-line` |

### 4.1.2 Visualisation 24h glissantes (line chart)

5 séries empilées : Nucléaire, Éolien, Solaire, Hydraulique, Gaz. Pas de 15 minutes. Palette catégorielle DSFR. Databox activée (titre, source, date, download).

### 4.1.3 Parc ENR installé (bar chart 2000-2024)

Source `parc-national-annuel-prod-eolien-solaire`. 2 séries empilées : éolien terrestre (MW) + solaire photovoltaïque (MW). Mode `stacked`.

### Points à valider sur cet onglet

- ☐ **3 KPIs temps réel** (CO₂ + nucléaire + consommation) : sont-ils les bons indicateurs cardinaux pour un grand public ? Manque la **part bas-carbone** ou la **part ENR** instantanée ?
- ☐ Affichage 24h glissantes avec **filtre `taux_co2 is not null`** : la convention masque les heures futures sans mesure réelle — bien expliqué au lecteur ?
- ☐ Le bar chart ENR couvre **2000-2024** (parc installé en MW). Faut-il prolonger à 2025-2026 si la donnée est dispo ?
- ☐ Source **eCO2mix temps réel** : licence Etalab 2.0 confirmée pour la rediffusion ?

---

## 4.2 Onglet 2 — Mobilité

![](<images/dashboard - onglet 2 - mobilite.png>){width=14cm}

**Question éditoriale :** « La mobilité bascule-t-elle vers l'électrique ? »

### 4.2.1 KPI principal

Source `bornes-irve` (ODRÉ) : `select count(*) as total`.

- **Points de recharge IRVE (référentiel consolidé)** — icône `ri-charging-pile-2-line`

### 4.2.2 Bornes par opérateur (bar chart horizontal, top 10)

Source `bornes-irve` avec `group-by="nom_operateur"`, `order-by="nb desc"`, `limit="10"`. Palette séquentielle descendante.

### 4.2.3 Bornes par puissance (bar chart vertical, top 10)

Source `bornes-irve` avec `group-by="puissance_nominale"`. Palette séquentielle ascendante.

### 4.2.4 Callout « À ajouter en phase 2 »

Indique les visualisations prévues mais non câblées : carte choroplèthe départementale (Ecolab : part de VP Crit'Air E), ratio bornes/VE, podium régional. Datasets en CSV statique sur `static.data.gouv.fr`.

### Points à valider sur cet onglet

- ☐ Le **KPI unique** (points IRVE) est-il suffisant comme entrée mobilité ? Manque le nombre de VE immatriculés.
- ☐ Le **top 10 opérateurs** sans seuil de qualité (déclarations parfois fautives, ex. opérateur « 0 ») — faut-il filtrer ?
- ☐ La **distribution par puissance** est très polluée par des valeurs aberrantes (3,7 / 7,2 / 11 / 22 / 50 / 150 / 350 kW). Faut-il **bucketiser** par paliers AFIR (Lent / Accéléré / Rapide / HPC) ?
- ☐ La carte choroplèthe départementale (en callout phase 2) : à prioriser ?

---

## 4.3 Onglet 3 — Bâtiment

![](<images/dashboard - onglet 3 - batiment.png>){width=14cm}

**Question éditoriale :** « Le bâtiment s'électrifie-t-il ? »

### 4.3.1 Répartition du chauffage dans le parc DPE (pie chart)

Source : ADEME data-fair sur le dataset `meg-83tjwtg8dyz4vv7h1dqe` (DPE logements existants).

```
url="https://data.ademe.fr/data-fair/api/v1/datasets/meg-83tjwtg8dyz4vv7h1dqe/values_agg
     ?field=type_energie_principale_chauffage&agg_size=10&size=0&sort=-count"
use-proxy
transform="aggs"
```

> Le `use-proxy` est obligatoire en prod : `data.ademe.fr` n'est pas dans `connect-src` du CSP, et `dsfr-data` tunnelise via `https://chartsbuilder.matge.com/cors-proxy` (domaine autorisé).

**Note de lecture** affichée sous le chart : le DPE n'est pas représentatif du parc total (surreprésentation des mutations et rénovations). À coupler avec le recensement INSEE pour une photo nationale.

### 4.3.2 Distribution des classes énergétiques (bar chart A→G)

Idem `meg-83tjwtg8dyz4vv7h1dqe` avec `field=etiquette_dpe&agg_size=7&size=0&sort=key`. Tri alphabétique pour conserver l'ordre A→G. Palette divergente descendante.

### Points à valider sur cet onglet

- ☐ La **note de lecture sur la non-représentativité du DPE** : suffisamment visible ? Faut-il un avertissement plus marqué (le DPE surreprésente les passoires en mutation) ?
- ☐ Le **passage par `use-proxy`** (chartsbuilder.matge.com) est-il accepté du côté DGEC pour la production ? Sinon, internaliser le snapshot ADEME.
- ☐ Manque-t-il un visuel sur les **PAC installées** (Mesure 4 du Plan : cible 1 M en 2030) ?
- ☐ Le **dataset ADEME** est-il le bon ? Le dataset « dpe-v2-logements-existants » n'existe pas ; on utilise `meg-83tjwtg8dyz4vv7h1dqe` — alias officiel ou identifiant volatil ?

---

## 4.4 Onglet 4 — Cap 2050

![](<images/dashboard - onglet 4 - objectifs.png>){width=14cm}

**Question éditoriale :** « Où en est-on par rapport aux objectifs 2050 ? »

### 4.4.1 Tableau de suivi des écarts

Table DSFR `fr-table fr-table--bordered` avec 7 lignes :

| Indicateur | Valeur actuelle | Cible 2030 | Cible 2050 | Statut |
|---|---|---|---|---|
| Part bas-carbone du mix | ~92 % | 95 % | 100 % | `fr-badge--success` « en route » |
| Capacité solaire installée | ~25 GW | 54-60 GW (PPE 2) | 100-200 GW (ADEME) | `fr-badge--warning` « à accélérer » |
| Capacité éolienne terrestre | ~24 GW | 33-35 GW | ~50 GW | `fr-badge--warning` |
| Part VE dans le parc VP | ~3 % | 15 % | ~100 % (UE 2035) | `fr-badge--warning` |
| Bornes IRVE installées | ~220 000 | 400 000 | — | `fr-badge--warning` |
| Pompes à chaleur installées/an | ~600 000 | 1 M/an | — | `fr-badge--info` « à confirmer » |
| Intensité carbone kWh | ~40 gCO₂/kWh | ~30 | ~10 | `fr-badge--success` |

### 4.4.2 Callout de lecture

Encadré bleu DSFR : « La France est sur la trajectoire de décarbonation côté production… mais le rythme de déploiement des ENR, des VE et des PAC reste en retard sur les cibles intermédiaires. La **production** est gagnée, l'**électrification des usages** reste à accélérer. »

### 4.4.3 Callout « À ajouter en phase 2 »

Visualisations confrontant les séries observées aux 4 scénarios ADEME Transition(s) 2050 (S1 → S4). CSV sur data.gouv.fr (id `61f3ba1456816c41f28c43ac`).

### Points à valider sur cet onglet

- ☐ Les **valeurs actuelles** dans la table sont saisies en dur dans le HTML. Faut-il les brancher dynamiquement à partir des sources des onglets 1-3 quand c'est possible (cohérence garantie) ?
- ☐ Le **statut** est un **jugement éditorial** (`en route` / `à accélérer` / `à confirmer`). Faut-il fixer une règle automatique (par ex. statut = `success` si valeur actuelle ≥ X% de la cible 2030, etc.) ?
- ☐ Les **cibles** sont issues de la **PPE 2 (avril 2020)**. Faut-il attendre la **PPE 3** (à venir) pour les mettre à jour ?
- ☐ Le **message éditorial** dans le callout (« production gagnée / usages à accélérer ») est-il un message politique consensuel ?

---

## 4.5 Onglet 5 — Brief & sources (métadonnées techniques)

Onglet **documentaire** non destiné au grand public, mais aux journalistes / développeurs / chercheurs qui veulent reproduire ou auditer le tableau de bord.

Sections :

1. **Objectif éditorial** : rappel des 4 angles + lecture indépendante de chaque onglet.
2. **Stack technique** : DSFR 1.14, dsfr-data web components, dsfr-chart 2.0, ODS v2.1, data-fair API (ADEME), Etalab 2.0.
3. **Sources de données effectivement câblées (v0.2)** :

| Source | Dataset ID | Endpoint | Champs utilisés |
|---|---|---|---|
| eCO2mix temps réel (RTE) | `eco2mix-national-tr` | ODRÉ ODS v2.1 | `date_heure, taux_co2, nucleaire, consommation, eolien, solaire, hydraulique, gaz` |
| Parc ENR annuel | `parc-national-annuel-prod-eolien-solaire` | ODRÉ ODS v2.1 | `annee, parc_installe_eolien, parc_installe_solaire` |
| Bornes IRVE | `bornes-irve` | ODRÉ ODS v2.1 | `nom_operateur, puissance_nominale, count(*)` |
| DPE logements existants | `meg-83tjwtg8dyz4vv7h1dqe` | ADEME data-fair (`values_agg`) | `type_energie_principale_chauffage, etiquette_dpe` |

4. **Sources à intégrer en phase 2+** : Ecolab (Crit'Air, immat. VUL/PL VE-H2), RTE eCO2mix régional, EDF (historique, indisponibilités), ADEME (RGE, audits énergétiques), Enedis (conso régionale), MTE (conso locale), ADEME Transition(s) 2050 (CSV).
5. **Endpoints clés** :
   - **ODRÉ** : `https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/{slug}/records`
   - **ADEME DPE** : `https://data.ademe.fr/data-fair/api/v1/datasets/meg-83tjwtg8dyz4vv7h1dqe/values_agg?field={champ}&agg_size={N}&size=0`
   - Convention `data-fair` : `agg_size` pour le nombre de valeurs distinctes, `size=0` pour ne pas embarquer les sous-résultats, `sort=-count` pour tri par fréquence, `sort=key` pour ordre alphabétique (utile sur DPE A→G).
6. **Trous identifiés** :
   - Prix électricité ménages / industrie : Eurostat `nrg_pc_204` ou CRE.
   - Stock annuel PAC installées : pas de série dédiée — reconstruction DPE post-réno ou AFPAC.
   - Bonus écologique / leasing social : pas d'opendata — demander à l'ASP.
   - Projets hydrogène : quasi inexistant — repli sur scénarios ADEME 2050.
7. **Composants ChartsBuilder utilisés** : 7 sources, 6 charts, 4 KPIs, 1 kpi-group, 6 a11y, 4 databox.

### Points à valider sur cet onglet

- ☐ Cet onglet est-il **trop technique** pour figurer dans le tableau de bord public ? Faut-il le déplacer dans une page séparée ou en footer ?
- ☐ La liste des **trous identifiés** doit-elle être complétée par une liste prioritaire pour la phase 2 ?
- ☐ Le **rappel CSP / use-proxy** doit-il figurer ici en plus du commentaire dans le code ?

---

# 5. Récapitulatif des hypothèses & constantes

## 5.1 Sources opendata effectivement câblées

| # | Source | Producteur | Endpoint | Fréquence MAJ |
|---|---|---|---|---|
| 1 | eCO2mix national temps réel | RTE via ODRÉ | `eco2mix-national-tr` | 15 minutes |
| 2 | Parc national annuel ENR (éolien + solaire) | RTE via ODRÉ | `parc-national-annuel-prod-eolien-solaire` | Annuel |
| 3 | Bornes IRVE | Etalab via ODRÉ | `bornes-irve` | Quotidien |
| 4 | DPE logements existants | ADEME data-fair | `meg-83tjwtg8dyz4vv7h1dqe` | Continu |

## 5.2 Cibles 2030 / 2050 sourcées

| Indicateur | Cible 2030 | Cible 2050 | Source |
|---|---|---|---|
| Part bas-carbone du mix | 95 % | 100 % | SNBC |
| Capacité solaire installée | 54-60 GW | 100-200 GW | PPE 2 / ADEME Transition(s) 2050 |
| Capacité éolienne terrestre | 33-35 GW | ~50 GW | PPE 2 |
| Part VE parc VP | 15 % | ~100 % (UE 2035) | PPE 2 / Règlement UE 2023/851 |
| Bornes IRVE | 400 000 | — | Cible mobilité Plan d'électrification |
| Pompes à chaleur installées/an | 1 M/an | — | Mesure 4 Plan d'électrification |
| Intensité carbone kWh | ~30 gCO₂/kWh | ~10 gCO₂/kWh | SNBC |

## 5.3 Conventions techniques

| Convention | Choix |
|---|---|
| Composants UI | `<dsfr-data-source>` + `<dsfr-data-chart>` + `<dsfr-data-kpi>` + `<dsfr-data-a11y>` (objectif RGAA AA) |
| Accessibilité | `<dsfr-data-a11y>` systématique avec description et lien à la source |
| Sources CSP non-allowlistées | `use-proxy` (tunnel via `chartsbuilder.matge.com/cors-proxy`) |
| Sources lourdes statiques | internalisation locale (non utilisé dans ce dashboard, cf. `bornes-ve` pour les contours géo) |
| Filtre eCO2mix temps réel | `where="taux_co2 is not null"` pour exclure les enregistrements futurs où seules les prévisions sont renseignées |
| Tri ADEME data-fair | `sort=-count` (fréquence) ou `sort=key` (alphabétique, utile pour DPE A→G) |

---

# 6. Sources des données

| Donnée | Source officielle | Année / version | Référence |
|---|---|---|---|
| eCO2mix temps réel | RTE — service public d'opendata énergie via ODRÉ | continu | `odre.opendatasoft.com` |
| Parc national ENR annuel | RTE via ODRÉ | annuel | `odre.opendatasoft.com` |
| Bornes IRVE consolidées | Etalab (data.gouv.fr) → miroir ODRÉ | quotidien | `data.gouv.fr/datasets/base-nationale-des-irve` |
| DPE logements existants | ADEME data-fair | continu (DPE depuis juillet 2021) | `data.ademe.fr` |
| Cibles ENR / VE / PAC | PPE 2 (avril 2020), SNBC, Règlement UE 2023/851, Plan d'électrification (avril 2026) | divers | `ecologie.gouv.fr` · `legifrance.gouv.fr` |
| Scénarios ADEME Transition(s) 2050 | ADEME | 2021 | `librairie.ademe.fr/transition-2050` |

---

# 7. Limites connues

## 7.1 Hypothèses simplificatrices assumées

- **France entière uniquement** (métropole + DROM agrégés). Pas de décomposition régionale en v0.2.
- **Valeurs actuelles de l'onglet « Cap 2050 »** saisies en dur dans le HTML (pas branchées aux sources). À synchroniser avec les chiffres réels au moins une fois par trimestre.
- **Pas d'inflation / actualisation** des indicateurs monétaires (le dashboard est essentiellement physique : MW, GW, gCO₂/kWh, %).
- **Cibles PPE 2 (avril 2020)** : seront à mettre à jour quand la **PPE 3** sera publiée.
- **DPE non représentatif du parc total** : signalé en note de lecture mais le biais n'est pas corrigé.

## 7.2 Cas non traités (v0.2)

- **Cartographie régionale / départementale** (callout phase 2 sur onglets 2 et 3).
- **Scénarios prospectifs ADEME** S1 → S4 (callout phase 2 onglet 4).
- **Comparaisons UE** (Allemagne, Espagne, Pays-Bas) — utile pour le narratif Cap 2050.
- **Séries historiques 1948-2024** (EDF) sur la production électrique.
- **Données mensuelles SDES** (immatriculations VE, MaPrimeRénov').
- **Prix de l'électricité ménages / industrie** (Eurostat ou CRE).
- **Projets hydrogène** (quasi inexistant en opendata).

## 7.3 Points ouverts à arbitrer avec les experts

1. **Hotfix récent (commit `8ff0040`)** : ADEME bloquée par CSP → `use-proxy`. Vérifier que **toutes les sources non-allowlistées** passent par `use-proxy` — audit transverse à faire sur les 8 simulateurs *(todo dans la modale business)*.
2. **Mix électrique : production (TWh) ou capacité (GW) ?** Le message diffère (nucléaire dominant en énergie, ENR dominantes en capacité).
3. **Mobilité : parc VE roulant (cumul) ou ventes mensuelles ?** Les deux narratifs sont valides.
4. **Cap 2050 : SNBC 3 (à venir) vs SNBC 2 actuelle** — on attend la publication ou on positionne sur les cibles connues ? *(open dans la modale)*
5. **Si la donnée diverge entre RTE et SDES** (cas connu sur les ENR), quelle source prime ? *(open dans la modale)*
6. **Fraîcheur de la donnée** : à quel point afficher la date du dernier point de données disponible ?
7. **Accessibilité RGAA** : `<dsfr-data-a11y>` génère des alternatives texte / tableau — niveau d'audit confirmé AA ?
8. **Mention « données opendata officielles »** vs **« interprétations éditoriales DGEC »** : équilibre à valider.

---

# Annexe — Historique des versions

| Version | Date | Auteur | Modifications |
|---|---|---|---|
| 0.1 | 2026-05-20 | Bertrand Matge | Création initiale (5 onglets : mix électrique / mobilité / bâtiment / cap 2050 / brief & sources) |
