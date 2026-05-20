---
title: "Suivi du Plan d'électrification — Spécification métier"
simulateur: plan-electrification
version: 0.1
date: 2026-05-20
statut: brouillon — à valider
auteur: Bertrand Matge
destinataires: DGEC, SGPE, cabinet MTE, équipes pilotage Matignon
---

# 1. Objectif & public visé

**Question à laquelle l'outil répond :** « Où en est-on de la mise en œuvre du Plan d'électrification de la France annoncé en avril 2026 ? Quelles mesures sont lancées, en préparation, en retard ? Quels jalons restent à franchir d'ici fin 2027 ? »

**Public cible :** pilotage interne (DGEC, SGPE, cabinet du MTE, Matignon), publics avertis (parlementaires, journalistes spécialisés, ONG). En l'état actuel (prototype), **pas destiné au grand public** tant que les valeurs courantes sont simulées.

**Décision aidée :**

- piloter l'avancement des 22 mesures (statut, % avancement, indicateurs cibles vs valeurs courantes) ;
- identifier les **mesures en retard** ou les **dispositifs en blocage réglementaire** (décret non publié, fiche CEE non révisée) ;
- arbitrer la communication publique (mesures déjà actives à mettre en avant vs mesures encore à instruire).

**Hors périmètre (v0.1 prototype) :**

- **Valeurs courantes réelles** des indicateurs : actuellement **simulées** (à brancher sur les remontées officielles, cf. §6).
- Suivi financier mesure par mesure (enveloppes budgétaires par mesure) — *à intégrer si la DGEC publie le détail*.
- Workflow validation / révision (édition collaborative) — outil en lecture seule.
- Export PDF / CSV pour revues cabinet — *à instruire*.

---

# 2. Scénario par défaut — fil rouge des exemples

Tous les exemples chiffrés et statuts de ce document utilisent les **valeurs initiales** du prototype (snapshot mi-mai 2026, ~1 mois après l'annonce du Plan).

| Catégorie | État au chargement |
|---|---|
| **Total mesures** | 22 (3 transversales + 5 bâtiments + 6 mobilités + 8 industrie/artisanat/agriculture) |
| **Statut majoritaire** | En préparation (la plupart sont en attente de leur décret ou fiche CEE) |
| **Mesures lancées / opérationnelles** | M02 (piquage RTE), M14 (schéma directeur bornes), M17 (AAP engins agricoles en cours), M21 (1re relève GPID) |
| **Mesures avec valeurs courantes simulées « plausibles »** | Toutes — explicitement signalé en callout d'alerte sur la page |
| **Onglet actif au chargement** | Transversal (3 mesures) |

> ⚠️ Le simulateur affiche un **callout d'alerte permanent** rappelant que les valeurs courantes sont simulées : « Ce tableau de bord est un **prototype**. Les valeurs cibles (« Quel objectif ? ») et les échéances (« Quand ? ») sont issues directement du dossier de presse d'avril 2026. En revanche, les valeurs courantes de chaque indicateur sont simulées tant que les remontées officielles ne sont pas branchées. »

---

# 3. Vue d'ensemble du parcours

Page unique structurée en **5 zones** verticales :

1. **En-tête** : titre + sous-titre + callout d'alerte « prototype ».
2. **KPIs globaux** : 4 KPIs comptant les mesures par grand statut.
3. **Légende** : 6 statuts colorés (attente / préparation / lancée / en cours / cible atteinte / en retard).
4. **Calendrier** : grille 5 colonnes (2026-Q2 / Q3 / Q4 / 2027 / long terme), une carte par mesure positionnée sur son jalon principal.
5. **Détail par mesure** : `fr-tabs` à 4 onglets (Transversal / Bâtiments / Mobilités / Industrie+artisanat+agriculture), chaque onglet contenant les cartes mesure de l'axe.

Suivi par une section **Méthodologie & sources** détaillant les 13 familles de données qu'il faudrait brancher pour piloter en temps réel.

![](<images/suivi-plan - global.png>){width=14cm}

Vue d'ensemble au chargement (KPIs globaux + légende, scénario par défaut).

### Points à valider sur la vue d'ensemble

- ☐ Le **callout d'alerte « prototype »** est-il suffisamment visible pour qu'aucun lecteur ne confonde valeurs simulées et valeurs officielles ?
- ☐ L'**ordre des zones** (KPIs → légende → calendrier → onglets détail) correspond-il au flux de lecture attendu pour le pilotage ?

---

# 4. Détail par zone fonctionnelle

## 4.1 Zone — KPIs globaux

![](<images/suivi-plan - global.png>){width=14cm}

Bandeau de 4 KPIs DSFR (border-left coloré) :

| KPI | Calcul | Couleur border |
|---|---|---|
| **Mesures au total** | `MEASURES.length` (= 22) | Bleu DSFR |
| **En préparation** | count des mesures avec `status === "preparation"` | Bleu info (`#0063cb`) |
| **Lancées / en cours** | count `status ∈ {lancee, encours}` | Orange warn (`#b34000`) |
| **Cibles atteintes** | count `status === "atteinte"` | Vert ok (`#18753c`) |

Chaque KPI a un sous-libellé d'aide à la lecture (« 3 transversales + 19 sectorielles » pour le total, « décrets, arrêtés, consultations » pour la préparation, etc.).

### Points à valider sur cette zone

- ☐ Les **4 KPIs choisis** (Total / Préparation / Lancées+En cours / Atteintes) sont-ils les bons indicateurs cardinaux ? Manque « En retard » qui mériterait peut-être son propre KPI ?
- ☐ Doit-on ajouter un KPI **% d'avancement global** (moyenne pondérée des % d'avancement par mesure) ?
- ☐ Doit-on ajouter un KPI **délai moyen restant** avant échéance ?

---

## 4.2 Zone — Calendrier (grille 5 colonnes)

![](<images/suivi-plan - calendrier.png>){width=14cm}

Grille HTML 5 colonnes :

| Colonne | Période | Libellé affiché |
|---|---|---|
| 1 | `2026-Q2` | 2026 · Q2 (mai-juin) |
| 2 | `2026-Q3` | 2026 · Q3 (juil-sept) |
| 3 | `2026-Q4` | 2026 · Q4 (oct-déc) |
| 4 | `2027` | 2027 |
| 5 | `longterme` | 2030 → 2035 (long terme) |

Chaque mesure est positionnée dans **une seule colonne** correspondant à son **principal jalon opérationnel** (publication du texte, ouverture du dispositif, entrée en vigueur). Plusieurs mesures ont des jalons intermédiaires : seul le plus structurant figure ici.

Chaque carte mesure dans le calendrier contient : badge `M01`, libellé court, pastille colorée de statut.

**Au clic** sur une carte calendrier, l'utilisateur :

1. bascule sur l'onglet de l'axe correspondant ;
2. la page scrolle automatiquement sur la carte mesure détaillée (`scrollIntoView`).

### Points à valider sur cette zone

- ☐ Le **découpage 2026-Q2 / Q3 / Q4 / 2027 / long terme** est-il le bon ? Faut-il faire apparaître **2028 / 2029** explicitement ?
- ☐ Le **choix d'un jalon unique par mesure** est-il un parti pris acceptable, ou faut-il représenter une mesure avec plusieurs jalons (ex. par une barre) ?
- ☐ L'interaction **clic calendrier → bascule onglet + scroll** est-elle assez intuitive ? Faut-il une animation visuelle de la carte au scroll ?

---

## 4.3 Zone — Détail par mesure (4 onglets, 22 cartes au total)

L'outil utilise `fr-tabs` DSFR à 4 onglets, chacun contenant les cartes mesure de son axe :

| Onglet | Axe | Nombre |
|---|---|---|
| Transversal | `transversal` | 3 |
| Bâtiments | `batiments` | 5 |
| Mobilités | `mobilites` | 6 |
| Industrie, artisanat, agriculture | `industrie` | 8 |

### 4.3.1 Structure d'une carte mesure

![](<images/suivi-plan - detail1.png>){width=12cm}

Chaque carte (`<article class="measure">`) contient :

1. **Header** : badge `M0X` (fond bleu), titre de la mesure, badge statut (couleur = statut)
2. **Méta** : icône calendrier + échéance · icône cible + objectif officiel (issu du DP)
3. **Barre de progression** : `progress` en %, couleur = statut
4. **Indicateurs** (grille auto-fit, mini 220 px) : pour chaque indicateur :
   - libellé + hint éventuel
   - valeur courante / cible (format `12 345 / 50 000`)
   - mini-barre de progression (sauf indicateurs « texte » comme un statut juridique)
5. **Bloc dépliable** « Données à brancher pour suivre en réel » (fond jaune `#fef7da`)

### 4.3.2 Statuts (couleurs et codes)

| Statut | Libellé | Couleur |
|---|---|---|
| `attente` | En attente | `#6a6af4` (violet pâle) |
| `preparation` | En préparation | `#a558a0` (mauve) |
| `lancee` | Lancée / opérationnelle | `#009081` (turquoise) |
| `encours` | En cours (résultats partiels) | `#d1b781` (jaune-or) |
| `atteinte` | Cible atteinte | `#18753c` (vert succès) |
| `retard` | En retard | `#ce0500` (rouge danger) |

### 4.3.3 Exemple — Mesure 9 « 50 000 véhicules électriques en location sociale (leasing) »

![](<images/suivi-plan - detail2.png>){width=12cm}

Carte complète :

- **Statut** : En préparation, 30 % avancement
- **Échéance** : Mi-juillet 2026 (ouverture commandes)
- **Objectif officiel (DP)** : « 50 000 véhicules électriques neufs loués à des ménages modestes en 2026. »
- **Indicateurs** :
  - Véhicules loués (édition 2026) : 0 / 50 000 (mini-barre 0 %)
  - Offres concessionnaires disponibles : 0 / — (pas de cible chiffrée)
  - Statut dispositif : « Préparation appel d'offres » → « Ouvert »
- **Données à brancher** : « Pilote ASP/DGEC : remontée mensuelle du nombre de contrats signés. Pour les éditions précédentes (2024/2025), le compteur public était mis à jour irrégulièrement — à fiabiliser. »

### Points à valider sur cette zone

- ☐ Les **6 statuts** sont-ils les bons ? Faut-il distinguer **« En attente d'arbitrage »** vs **« En préparation »** (les deux sont souvent confondus en pratique) ?
- ☐ Le **% d'avancement** est aujourd'hui un **jugement qualitatif unique par mesure**. Faut-il le calculer comme moyenne pondérée des indicateurs (quand tous chiffrés), ou conserver le jugement ?
- ☐ Les **indicateurs « texte »** (ex. « Statut décret : Rédaction → Publié ») affichent une transition mais pas de barre. Faut-il une iconographie dédiée (étapes 1/2/3) ?
- ☐ Le **bloc « Données à brancher »** explicite mesure par mesure : utile pour la note technique, ou à déplacer dans une annexe ?
- ☐ Les **objectifs officiels** issus du DP sont-ils tous repris textuellement (sans paraphrase) ?

---

# 5. Le contenu des 22 mesures (cibles & échéances DP avril 2026)

Tous les chiffres et libellés ci-dessous sont **issus directement du dossier de presse** d'avril 2026.

## 5.1 Transversal (3 mesures)

| # | Titre | Échéance | Objectif |
|---|---|---|---|
| M01 | Lancer 100 territoires d'électrification | Été 2026 | 100 territoires sélectionnés, accompagnés sur objectifs chiffrés |
| M02 | Faciliter l'accès au réseau électrique | Avril → fin 2026 | Piquage 400 kV opérationnel, surréservation, « premier prêt premier servi » avant fin 2026 |
| M03 | Interdire la publicité pour les énergies fossiles | Décret avant fin 2026 | Décret pris en application de la loi Climat & Résilience (2021) |

## 5.2 Bâtiments (5 mesures)

| # | Titre | Échéance | Objectif |
|---|---|---|---|
| M04 | Offre « clés en main » de pompes à chaleur | Labellisation automne 2026 | 25 000 ménages bénéficiaires court terme · 1 M PAC en 2030 |
| M05 | Fin du gaz dans la construction neuve | 1er janvier 2027 (logements) | Aucun bâtiment neuf consommant du gaz dès 2030 |
| M06 | Flécher aides rénovation vers l'électrification | 1er sept 2026 (MPR) · 1er janv 2027 (éco-PLS) | Plus aucune rénovation d'ampleur MPR conservant un chauffage gaz |
| M07 | Rendre les bâtiments de l'État exemplaires | Décret été 2026 | ~80 GWh/an de gaz évités · 20 sites prioritaires |
| M08 | Limiter les nouveaux raccordements gaz pour les bâtiments | 1er janvier 2027 | Aucune nouvelle consommation de gaz pour les bâtiments à terme |

## 5.3 Mobilités (6 mesures)

| # | Titre | Échéance | Objectif |
|---|---|---|---|
| M09 | 50 000 VE en location sociale (« leasing ») | Mi-juillet 2026 (ouverture) | 50 000 VE loués à des ménages modestes en 2026 |
| M10 | Soutien à l'achat pour les « gros rouleurs » | Sept 2026 → 31 déc 2026 | 50 000 VE additionnels achetés d'ici fin 2026 |
| M11 | Renforcer le soutien à l'achat de VUL électriques | 1er juin 2026 (fiches CEE) | 50 000 VUL VE en 2026 · 70 000 en 2027 |
| M12 | Renforcer le soutien à l'achat de poids lourds électriques | 1er juin 2026 (fiches CEE) | 2 000 PL neufs VE en 2026 · 4 000 en 2027 |
| M13 | Rendre les flottes de l'État exemplaires | 1er janvier 2027 (circulaire) | 100 % renouvellements VE dès que possible · ~60 000 véhicules concernés |
| M14 | Planifier les bornes de recharge sur le réseau routier national | Schéma directeur actif · cibles 2035 | 22 000 points VL sur 900 aires (×5) · 8 000 points PL sur 560 aires |

## 5.4 Industrie, artisanat, agriculture (8 mesures)

| # | Titre | Échéance | Objectif |
|---|---|---|---|
| M15 | Soutenir l'électrification des artisans | Bpifrance 1er mai 2026 · AAP été 2026 | 1 000 projets artisans (DECARB FLASH, 16 M€) |
| M16 | Accompagner l'électrification des engins de chantier | 1re relève juin 2026 (10 M€) · 2e relève fin 2026 (40 M€) | 1 000 engins fabriqués en Europe |
| M17 | Développer l'offre d'engins agricoles électriques | AAP en cours · 2e relève fin 2026 | 150 engins agricoles (phase exploratoire) |
| M18 | Pompes à chaleur pour serres maraîchères et horticoles | Révision fiche CEE d'ici sept 2026 | 400 ha de serres équipées en PAC d'ici 2030 |
| M19 | Favoriser l'électrification des navires de pêche | Fiche CEE déployée fin 2026 | 500 navires de pêche équipés d'ici 2030 |
| M20 | Renforcer les aides PAC / chaudières élec. / CMV industrielles | Mai (PAC) · Juillet (chaudières) · Octobre (CMV) 2026 | ~10 TWhc/an pour les PAC industrielles |
| M21 | Décarboner et électrifier les grands sites industriels | Lancement AAP été 2026 · lauréats fin 2026 | ~2 TWh électrifiés d'ici 2030 (AO GPID + DECARB-IND) |
| M22 | Nouveaux contrats d'électricité long terme (8 à 10 ans) | Mise en vente premiers volumes 2027 | Dizaines de MW, puis 1 GW dans les prochaines années |

### Points à valider sur cette section

- ☐ Tous les libellés sont-ils **identiques au DP officiel** (vérification verbatim) ?
- ☐ Y a-t-il eu des **fusions / scissions** depuis l'annonce du DP (avril 2026) ? Si oui, comment versionner ?
- ☐ Les **dates précises** (1er juin 2026 pour M11/M12, 1er janvier 2027 pour M05/M08, etc.) sont-elles consolidées par la DGEC ?

---

# 6. Sources de données qui permettraient un suivi temps réel

Le tableau ci-dessous, présent dans l'outil sous l'intitulé « Sources de données qui permettraient un suivi temps réel », recense les **13 familles de données** identifiées comme nécessaires pour piloter en temps réel les 22 mesures.

| Famille | Producteur | Format / accès | Mesures |
|---|---|---|---|
| Aides à l'achat de véhicules (VP/VUL/PL) | ASP, DGEC | Pas d'API publique aujourd'hui | M09, M10, M11, M12, M13 |
| Immatriculations VE | SDES (MTE), AAA Data | Bulletin SDES mensuel · data.gouv.fr | M09, M10, M11, M12, M13 |
| Bornes de recharge publiques | Avere-France / GIREVE / IRVE | Base IRVE data.gouv.fr (quotidien) | M14 |
| Pompes à chaleur installées | Observ'ER, Uniclima, AFPAC | Études annuelles ; ou registre CEE | M04, M18, M20 |
| Certificats d'économie d'énergie (CEE) | DGEC — registre EMMY (PNCEE) | Export public mensuel | M04, M11, M12, M15, M16, M17, M18, M19, M20 |
| MaPrimeRénov' & rénovation | ANAH | Bilan trimestriel | M06 |
| Bâtiments / chaudières installées | Sit@del, CSTB, Observatoire BBC | Sit@del (PC) ; pas de granularité énergie sans croisement DPE | M05, M06, M07, M08 |
| Raccordement réseau / file d'attente | RTE, Enedis | Bilan prévisionnel RTE annuel · opendata.rte-france.com | M02 |
| Décrets, arrêtés, fiches CEE | Légifrance, JORF | API Légifrance (piste.gouv.fr), flux RSS JO | M03, M05, M06, M07, M08, M11, M12, M13, M18, M19, M20 |
| Bâtiments de l'État | DIE (Direction de l'immobilier de l'État), OSFi | Pas de portail public — données internes | M07, M13 |
| Appels à projets décarbonation industrie | Ademe, DGE | Annonces des lauréats publiées au cas par cas | M15, M16, M21 |
| Engins agricoles, navires de pêche | Ministère Agriculture, FranceAgriMer, DPMA | Pas de portail dédié — à construire | M17, M19 |
| Territoires d'électrification | DGEC, ANCT | Liste à publier sur ecologie.gouv.fr | M01 |
| Contrats d'électricité long terme | CRE, EDF | Annonces ad-hoc, à formaliser | M22 |

### Points à valider sur cette section

- ☐ Cette liste de **13 familles** est-elle exhaustive ?
- ☐ Pour chaque famille, qui (DGEC ? prestataire ?) prend en charge l'intégration ?
- ☐ Quelles familles sont **prioritaires** pour un MVP de pilotage réel ?
- ☐ Le **passage par le registre EMMY** (CEE) couvrirait à lui seul ~10 mesures — démarche déjà entamée par la DGEC ?

---

# 7. Récapitulatif des paramètres techniques

| Paramètre | Valeur |
|---|---|
| Nombre total de mesures | 22 |
| Nombre d'axes | 4 (transversal, bâtiments, mobilités, industrie) |
| Nombre de statuts | 6 (attente, préparation, lancée, encours, atteinte, retard) |
| Nombre de colonnes calendrier | 5 (Q2 / Q3 / Q4 / 2027 / long terme) |
| Indicateurs moyens par mesure | 2 à 4 |
| Type d'indicateur | numérique (avec cible et mini-barre) ou textuel (transition) |
| Stockage des données mesures | objet JS `MEASURES` inline (pas de fetch externe) |

---

# 8. Limites connues

## 8.1 Hypothèses simplificatrices assumées

- **Valeurs courantes simulées** dans la v0.1 prototype. Aucun branchement réel.
- **% d'avancement par mesure** = jugement qualitatif unique (pas calculé automatiquement à partir des indicateurs).
- **Statut « en retard »** : pas encore appliqué à aucune mesure (déclaration manuelle, pas de détection automatique d'un jalon dépassé).
- **Un jalon par mesure** dans le calendrier (le plus structurant). Les sous-jalons existent dans le DP mais ne sont pas représentés.
- **Pas de versioning** : si une mesure est fusionnée ou scindée, on perd l'historique.

## 8.2 Cas non traités (v1)

- Suivi **financier** mesure par mesure (enveloppe budgétaire).
- **Workflow validation** (édition collaborative, révisions).
- **Export PDF / CSV** pour revues cabinet.
- **Comparaison avec d'autres plans** (Stratégie nationale bas-carbone, Plan d'investissement France 2030).
- **Vue chronologique inversée** (chronique des annonces / décrets publiés).

## 8.3 Points ouverts à arbitrer avec les experts

1. **Affichage public d'une mesure « en retard »** avant arbitrage cabinet : politiquement sensible — qui valide l'autorisation d'affichage ? *(open dans la modale business)*
2. **Gouvernance** : qui édite ce dashboard ? Workflow de validation avant chaque mise à jour ? *(open)*
3. **Audit RGAA** : timeline / calendrier 5 colonnes ont-ils une alternative lecture séquentielle ?
4. **Auto-déclaration biaisée** : les indicateurs « réalisé » sans backing data précis : qui contrôle ?
5. **Versioning de la liste** : si une mesure est fusionnée / scindée, on garde la trace dans un journal ?
6. **Liens croisés** :
   - Mesure 1 (100 territoires) → `/territoires-electrification/`
   - Mesure 12 (PL aide achat) → `/poids-lourd/`
   - Mesure 4 (PAC) → `/pompe-a-chaleur/`
   - Mesure 14 (bornes) → `/bornes-ve/`
   Cohérence des chiffres entre les 5 outils à maintenir explicitement.

---

# Annexe — Historique des versions

| Version | Date | Auteur | Modifications |
|---|---|---|---|
| 0.1 | 2026-05-20 | Bertrand Matge | Création initiale (KPIs globaux, calendrier 5 colonnes, 4 onglets × 22 cartes mesure, table 13 sources de données) |
