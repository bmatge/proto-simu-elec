---
title: "Simulateur « Passer à l'électrique » — Spécification métier"
simulateur: passer-a-electrique
version: 0.6
date: 2026-05-20
statut: brouillon — à valider
auteur: Bertrand Matge
destinataires: Anah, DGEC, ADEME
---

# 1. Objectif & public visé

**Question à laquelle le simulateur répond :** « Combien d'aides puis-je mobiliser pour électrifier mon logement et mon véhicule, et au bout de combien d'années cet investissement devient-il rentable ? »

**Public cible :** particuliers français — propriétaires occupants, bailleurs et locataires — envisageant un ou plusieurs projets d'électrification (véhicule électrique, pompe à chaleur, rénovation d'ampleur, photovoltaïque).

**Décision aidée :** identifier les solutions éligibles, estimer le reste à charge après aides, et visualiser le gain net cumulé sur un horizon de 15 à 25 ans.

**Hors périmètre :**

- Aides locales (région, département, commune) — non intégrées.
- Véhicules d'occasion — non traités (sauf prime à la conversion).
- Photovoltaïque > 9 kWc et injection totale — non traités.

---

# 2. Scénario par défaut — fil rouge des exemples

Tous les exemples chiffrés de ce document utilisent le **scénario chargé par défaut** au démarrage du simulateur. C'est le scénario que verra l'expert métier en ouvrant l'outil.

| Catégorie | Valeurs par défaut |
|---|---|
| **Profil foyer** | 3 personnes, RFR 32 000 €/an, hors Île-de-France |
| **Logement** | Propriétaire occupant, maison 90 m², DPE E, chauffage gaz, ECS sur même énergie |
| **Mobilité** | Véhicule essence, 12 000 km/an, mode domicile-travail |
| **Projets actifs (mode expert)** | PAC air/eau, VE neuf, borne domicile |
| **Horizon** | 20 ans, démarrage An 1 pour chaque chantier |

> En **mode guidé**, aucune solution n'est cochée par défaut à l'étape 5 — l'utilisateur doit les sélectionner. En **mode expert**, les trois projets ci-dessus sont chargés d'emblée et le gain net affiché par défaut est **38 105 € sur 20 ans, ROI 4 ans 3 mois** (référence d'alignement, commit `e70985c`).

---

# 3. Vue d'ensemble du parcours

Le simulateur propose **deux modes** qui utilisent les **mêmes formules** et produisent les **mêmes résultats** à entrées équivalentes :

- **Mode guidé** : 6 étapes successives.
- **Mode expert** : tous les paramètres et hypothèses sur une seule page, par zones.

## 3.1 Point d'entrée — choix du mode

![](<images/mode guide - etape0 - choix du mode.png>){width=10cm}

L'utilisateur choisit entre le mode guidé (parcours pas à pas) et le mode expert (toutes les valeurs accessibles immédiatement). Les données et formules sont identiques entre les deux modes.

### Points à valider sur ce point d'entrée

- ☐ Le libellé de chaque mode est clair.
- ☐ Le public visé par chaque mode est expliqué.

---

# 4. Mode guidé — détail étape par étape

## 4.1 Étape 1 — Foyer

![](<images/mode guide - etape1 - foyer.png>){width=10cm}

**Champs saisis**

- Nombre de personnes — entier, 1 à 6
- RFR (€/an) — nombre ≥ 0
- Zone — Île-de-France / Hors Île-de-France

**Sortie de l'étape**

Profil de revenu Anah (bleu / jaune / violet / rose), calculé depuis RFR, nombre de parts et zone. Conditionne tous les barèmes MaPrimeRénov' ensuite.

**Exemple — valeurs par défaut**

Entrées : 3 personnes, RFR 32 000 €, hors IDF. Sortie attendue : profil Anah à valider (probable **jaune** ou **violet** selon le barème 2026).

### Points à valider sur cette étape

- ☐ Les seuils RFR → profil Anah utilisés sont conformes aux barèmes 2026.
- ☐ La règle « 1 personne = 1 part » utilisée pour le calcul des parts est correcte.
- ☐ Le profil affiché pour le scénario par défaut (3 pers., 32 000 €, hors IDF) est le bon.

---

## 4.2 Étape 2 — Logement

![](<images/mode guide - etape2 - logement.png>){width=10cm}

**Champs saisis**

- Statut — propriétaire occupant / bailleur / locataire
- Type — maison / appartement
- Surface — 20 à 200 m²
- DPE actuel — A à G
- Énergie chauffage — gaz / fioul / élec / bois

**Constantes mobilisées**

- Conso par DPE (A→G) : 50 → 600 kWh/m²/an (3CL-DPE)
- Prix gaz : 0,1162 €/kWh (CRE 2026)
- Prix fioul : 0,135 €/kWh (Pégase)
- Prix élec HP : 0,2516 €/kWh (CRE 2026)
- Prix bois : 0,075 €/kWh (ADEME)

**Formule — coût chauffage actuel**

$$C_\text{chauffage} = C_\text{DPE} \times S \times P_\text{énergie}$$

**Exemple — valeurs par défaut**

Maison 90 m², DPE E (≈ 250 kWh/m²/an), gaz :
$C = 250 \times 90 \times 0{,}1162 \approx$ **2 615 €/an**

### Points à valider sur cette étape

- ☐ Les valeurs de consommation par classe DPE sont conformes à la méthode 3CL-DPE 2026.
- ☐ Les prix unitaires de l'énergie sont à jour (CRE / Pégase 2026).
- ☐ La non-éligibilité des locataires à la majorité des aides logement est confirmée.

---

## 4.3 Étape 3 — Déplacement

![](<images/mode guide - etape3 - deplacement.png>){width=10cm}

**Champs saisis**

- Véhicule actuel — essence / diesel / hybride / aucun
- Kilométrage annuel — 0 à 30 000 km/an
- Type de trajets — domicile-travail / mixte / urbain

**Constantes mobilisées**

- Conso thermique forfait : 6,5 L/100 km
- Conso VE forfait : 17 kWh/100 km
- Prix essence : 1,95 €/L — diesel : 1,80 €/L
- Prix élec HC domicile : 0,2068 €/kWh
- Mode mixte/urbain : 70 % HC domicile + 30 % public
- Mode domicile-travail : 100 % HC domicile

**Formule — coût carburant actuel**

$$C_\text{carburant} = (km/100) \times C_\text{therm} \times P_\text{carburant}$$

**Exemple — valeurs par défaut**

12 000 km, essence : $C = 120 \times 6{,}5 \times 1{,}95 =$ **1 521 €/an**

### Points à valider sur cette étape

- ☐ Le forfait 6,5 L/100 km est représentatif du parc thermique français.
- ☐ Le forfait 17 kWh/100 km est représentatif d'un VE moyen acheté en 2026.
- ☐ La répartition 70 % HC / 30 % public en mode mixte/urbain est plausible.
- ☐ Le **prix moyen de la recharge publique** (actuellement implicite) doit être expliqué et sourcé. **Point ouvert.**

---

## 4.4 Étape 4 — Votre situation

![](<images/mode guide - etape4 - votre situation.png>){width=10cm}

**Affichage** (lecture seule)

- Coût annuel chauffage actuel
- Coût annuel carburant actuel
- Part de l'énergie dans le RFR

**Formule — part énergie dans le RFR**

$$\text{part} = (C_\text{chauffage} + C_\text{carburant}) / RFR$$

**Exemple — valeurs par défaut**

$C_\text{chauffage} = 2\,615$ € + $C_\text{carburant} = 1\,521$ € → $\text{part} = 4\,136 / 32\,000 \approx$ **12,9 % du RFR**

### Points à valider sur cette étape

- ☐ Le mode de calcul de la « part énergie dans le RFR » est pertinent pour la communication (vs. revenu disponible, vs. revenu après impôts).

---

## 4.5 Étape 5 — Solutions

L'étape 5 a deux états visuels : vue initiale (toutes les solutions éligibles affichées) et vue après sélection (récapitulatif des solutions retenues).

### 4.5.1 Vue initiale — solutions éligibles

![](<images/mode guide - etape5 - solutions.png>){width=10cm}

Solutions cumulables affichées :

- PAC air/eau ou géothermique
- Rénovation d'ampleur
- Véhicule électrique neuf (+ borne domicile)
- Photovoltaïque 3 kWc en autoconsommation

Pour chaque solution : aides mobilisables, économie annuelle, reste à charge.

### 4.5.2 Vue récapitulative — solutions choisies

![](<images/mode guide - etape5 - solutions choisies.png>){width=10cm}

Affichage du cumul pour les solutions sélectionnées :

- Total des aides reçues
- Total des économies annuelles
- Total des coûts projets
- Gain net cumulé sur l'horizon 20 ans

### Coûts des projets

| Solution | Coût TTC | À valider |
|---|---|---|
| PAC air/eau (remplacement chauffage) | 14 000 € | ☐ |
| PAC géothermique | 22 000 € | ☐ |
| Rénovation d'ampleur (isolation + équipement) | 45 000 € | ☐ |
| Véhicule électrique neuf — **surcoût compté** | 9 000 € (32 000 − 23 000) | ☐ |
| Borne de recharge domicile | 1 200 € | ☐ |
| Photovoltaïque 3 kWc | 9 000 € | ☐ |

> ⚠️ **Hypothèse structurante** : seul le **surcoût** du VE est compté comme dépense (pas le prix total), au motif que le ménage achèterait un véhicule de toute façon. *À arbitrer avec la DGEC mobilité.*

### Barèmes des aides

**MaPrimeRénov'** — montants par profil Anah, à valider sur la base des barèmes Anah 2026.

**Véhicule électrique :**

| Aide | Montant | Condition | À valider |
|---|---|---|---|
| Prime VPE (Coup de pouce) | 4 000 → 1 000 € | dégressif selon RFR/part | ☐ |
| Surbonus batterie EU | +1 500 € | score ADEME ≥ seuil | ☐ |
| Prime à la conversion | 1 500 € | mise au rebut diesel + revenus modestes | ☐ |
| Prime borne domicile | 75 %, plafond 500 € | propriétaire | ☐ |
| Prime ADVENIR copropriété | 1 200 € / point de charge | copropriété | ☐ |
| Gain leasing social | 2 400 €/an | (300 − 100) × 12 | ☐ |

**Photovoltaïque :**

| Aide | Montant | Condition | À valider |
|---|---|---|---|
| Prime à l'investissement (≤ 3 kWc) | 230 €/kWc | autoconsommation | ☐ |
| Prime à l'investissement (≤ 9 kWc) | 170 €/kWc | autoconsommation | ☐ |
| Tarif OA — surplus injecté | 0,13 €/kWh | autoconsommation | ☐ |

### Formules déclenchées à cette étape

**Économie annuelle de chauffage après PAC :**

$$
\text{Éco}_\text{chauffage} = (C_\text{DPE} \times S \times P_\text{actuelle}) - \left(\frac{C_\text{DPE} \times S}{\text{COP}} \times P_\text{élec,HP}\right)
$$

avec COP = 3,5 (air/eau) ou 4,5 (géothermique).

*Exemple — valeurs par défaut, PAC air/eau (COP 3,5) :*

- Coût actuel = 250 × 90 × 0,1162 ≈ **2 615 €/an**
- Coût après PAC = (250 × 90 / 3,5) × 0,2516 ≈ **1 618 €/an**
- **Économie ≈ 997 €/an**

**Économie annuelle de carburant après VE :**

$$
\text{Éco}_\text{carburant} = \frac{km}{100} \times \left( C_\text{therm} \times P_\text{carburant} - C_\text{VE} \times P_\text{élec,mix} \right)
$$

avec $P_\text{élec,mix} = 0{,}7 \times P_\text{HC} + 0{,}3 \times P_\text{public}$ en mode mixte/urbain (100 % HC en mode domicile-travail).

*Exemple — valeurs par défaut, mode domicile-travail :*

- Coût essence = 120 × 6,5 × 1,95 = **1 521 €/an**
- Coût VE = 120 × 17 × 0,2068 ≈ **422 €/an**
- **Économie ≈ 1 099 €/an**

**Gain net par solution :**

$$
\text{Gain net}_\text{solution} = \sum \text{Aides} + N \times \text{Économie annuelle} - \text{Coût projet}
$$

avec N = horizon défini à l'étape 6 (défaut 20 ans).

### Points à valider sur cette étape

- ☐ Le **surcoût VE** plutôt que le prix total est la bonne convention comptable.
- ☐ Les coûts TTC moyens des projets (14 000 / 22 000 / 45 000 €…) sont représentatifs du marché 2026.
- ☐ Les COP retenus pour les PAC (3,5 et 4,5) sont alignés avec le baromètre PAC 2025.
- ☐ La règle de cumul **bonus écologique + prime à la conversion + leasing social** est correcte.
- ☐ Le **seuil ADEME** pour le surbonus batterie EU est à confirmer.

---

## 4.6 Étape 6 — Bilan détaillé

![](<images/mode guide - etape6 - bilan détaillé.png>){width=10cm}

**Champs saisis**

- Horizon de projection — défaut 20 ans
- Année de démarrage de chaque chantier

**Formule — Gain net cumulé**

(identique à l'étape 5 et au mode expert, alignement commit `e70985c`)

$$\text{Gain net} = \sum \text{Aides} + N \sum \text{Économies} - \sum \text{Coûts}$$

**Formule — Courbe d'amortissement**

$$\text{Cumul}_\text{statu quo}(n) = n \times C_\text{énergie actuelle}$$

$$\text{Cumul}_\text{scénario}(n) = I_\text{net}(n) + n \times (C_\text{énergie actuelle} - E_\text{cumulée}(n))$$

**ROI** = première année où $\text{Cumul}_\text{scénario}(n) \leq \text{Cumul}_\text{statu quo}(n)$

**Exemple — valeurs par défaut**

Avec PAC air/eau + VE + borne, horizon 20 ans : **Gain net = 38 105 €, ROI = 4 ans 3 mois.**

### Points à valider sur cette étape

- ☐ L'horizon par défaut (20 ans) est cohérent avec la durée de vie économique des équipements.
- ☐ Hypothèse « prix de l'énergie constants en euros 2026 sur tout l'horizon » : pertinente, ou faut-il une trajectoire ?
- ☐ Hypothèse « aides 2026 figées sur tout l'horizon » pour les chantiers démarrant dans les 10 ans : pertinente ?

---

# 5. Mode expert — détail par zone fonctionnelle

Le mode expert affiche toutes les hypothèses et tous les résultats sur **une seule page**, organisée en zones fonctionnelles. Les valeurs présentées ici sont les **valeurs par défaut** chargées au démarrage — l'utilisateur expert peut les modifier et restaurer les défauts d'un clic.

## 5.1 Vue complète

![](<images/mode expert - complet.png>){width=14cm}

Vue d'ensemble de la page — sert de référence visuelle pour situer les zones détaillées ci-dessous.

### Points à valider sur la vue complète

- ☐ L'organisation des zones (foyer → logement → mobilité → … → amortissement) suit un flux logique pour un utilisateur métier.
- ☐ Les libellés de zones sont compréhensibles sans formation préalable.

---

## 5.2 Zone — Foyer

![](<images/mode expert - foyer.png>){width=10cm}

Mêmes champs qu'à l'étape 1 du mode guidé, accessibles directement.

**Valeurs par défaut**

3 personnes, RFR 32 000 €, hors IDF.

**Sortie**

Profil de revenu Anah recalculé à la volée.

### Points à valider sur cette zone

- ☐ Les bornes des champs éditables sont cohérentes avec celles du mode guidé.

---

## 5.3 Zone — Logement

![](<images/mode expert - logement.png>){width=10cm}

Mêmes champs qu'à l'étape 2 du mode guidé. Les utilisateurs experts peuvent ajuster directement les hypothèses de consommation par DPE (§ 6.2).

**Valeurs par défaut**

PO, maison 90 m², DPE E, gaz, ECS sur même énergie, projet **PAC air/eau** présélectionné.

**Exemple — coût chauffage actuel**

$250 \times 90 \times 0{,}1162 \approx$ **2 615 €/an**

### Points à valider sur cette zone

- ☐ Les hypothèses de consommation par DPE éditables affichent bien les valeurs par défaut listées en § 6.2.

---

## 5.4 Zone — Mobilité

![](<images/mode expert - mobilite.png>){width=10cm}

Mêmes champs qu'à l'étape 3 du mode guidé. Paramètres ajustables :

- forfaits de consommation thermique et VE
- prix unitaires (carburants, électricité)
- répartition recharge domicile / publique

**Valeurs par défaut**

Essence, 12 000 km, mode domicile-travail, projet **VE neuf + borne domicile** présélectionné.

**Exemple — coût carburant actuel**

$120 \times 6{,}5 \times 1{,}95 =$ **1 521 €/an**

### Points à valider sur cette zone

- ☐ La liste des paramètres éditables couvre les leviers d'arbitrage attendus (et pas plus).

---

## 5.5 Zone — Situation actuelle

![](<images/mode expert - situation actuelle.png>){width=10cm}

Lecture seule, équivalent de l'étape 4 du mode guidé, mais visible en même temps que les autres zones.

**Affichage — valeurs par défaut**

- Coût chauffage actuel : ≈ **2 615 €/an**
- Coût carburant actuel : **1 521 €/an**
- Total : **4 136 €/an**
- Part dans le RFR : **12,9 %**

### Points à valider sur cette zone

- ☐ Les chiffres affichés sont strictement les mêmes que dans le mode guidé pour les mêmes entrées.

---

## 5.6 Zone — Dispositifs mobilisables

![](<images/mode expert - dispositifs mobilisables.png>){width=10cm}

Liste des dispositifs (aides et solutions techniques) auxquels l'utilisateur est **éligible** compte tenu de son profil. Chaque dispositif peut être activé / désactivé pour tester différents scénarios.

**Valeurs par défaut**

Dispositifs activés : PAC air/eau, VE neuf, borne domicile.

### Points à valider sur cette zone

- ☐ La liste des dispositifs éligibles est exhaustive (rien d'oublié vs barèmes 2026).
- ☐ Les règles d'éligibilité affichées correspondent aux conditions réglementaires officielles.
- ☐ Les dispositifs non éligibles sont affichés désactivés, avec le motif d'inéligibilité visible.

---

## 5.7 Zone — Aides publiques

![](<images/mode expert - aides publiques.png>){width=10cm}

Détail du montant de chaque aide mobilisable pour le scénario en cours :

- MaPrimeRénov' par solution (selon profil Anah)
- Aides VE : VPE, surbonus batterie EU, conversion, borne, ADVENIR, leasing social
- Aides PV : prime à l'investissement, tarif OA surplus

Barèmes détaillés : voir § 6.4.

### Points à valider sur cette zone

- ☐ Le total des aides affiché correspond bien à la somme des aides individuelles (pas de double comptage).
- ☐ Les règles de cumul entre aides sont respectées (ex. cumul ou non du leasing social avec la prime à la conversion).

---

## 5.8 Zone — Économie annuelle

![](<images/mode expert - economie annuelle.png>){width=10cm}

Décomposition de l'économie annuelle :

- économie chauffage (PAC + rénovation)
- économie carburant (VE)
- gain photovoltaïque (autoconsommation + revente)

**Formules** : voir étape 5 du mode guidé.

**Gain PV autoconsommation :**

$$
\text{Éco}_\text{PV} = P_\text{kWc} \times \text{Prod} \times (\alpha P_\text{HP} + (1-\alpha) P_\text{OA})
$$

avec $\alpha$ = part autoconsommée, $P_\text{OA}$ = 0,13 €/kWh.

**Exemple — valeurs par défaut (sans PV)**

Éco chauffage ≈ 997 €/an + Éco carburant ≈ 1 099 €/an = **≈ 2 096 €/an**

### Points à valider sur cette zone

- ☐ La part d'autoconsommation $\alpha$ retenue par défaut est précisée et sourcée.
- ☐ Les économies sont calculées en euros 2026 constants (pas d'indexation sur l'horizon).

---

## 5.9 Zone — Gain estimé

![](<images/mode expert - gain estime.png>){width=10cm}

Gain net cumulé sur l'horizon — formule identique aux étapes 5 et 6 du mode guidé.

$$\text{Gain net} = \sum \text{Aides} + N \sum \text{Économies} - \sum \text{Coûts}$$

**Valeur affichée par défaut**

Scénario PAC air/eau + VE + borne, horizon 20 ans : **Gain net = 38 105 €**.

(Cette valeur est le test d'alignement entre les 3 vues depuis le commit `e70985c`.)

### Points à valider sur cette zone

- ☐ La valeur affichée converge bien avec celle des étapes 5 et 6 pour les mêmes entrées.
- ☐ Le découpage visuel (aides, économies, coûts) est lisible pour un expert.

---

## 5.10 Zone — Amortissement

![](<images/mode expert - amortissement.png>){width=10cm}

Graphique d'amortissement (cumul statu quo vs scénario) et ROI affiché.

**Formules** : identiques à l'étape 6 du mode guidé.

**ROI affiché par défaut**

**4 ans 3 mois** (scénario PAC air/eau + VE + borne).

### Points à valider sur cette zone

- ☐ La courbe d'amortissement converge avec celle de l'étape 6 pour les mêmes entrées.
- ☐ Le ROI affiché est arrondi de la même manière qu'à l'étape 6 (cohérence de présentation).

---

# 6. Récapitulatif des hypothèses & constantes (toutes étapes)

Tableau consolidé pour relecture transversale.

## 6.1 Prix de l'énergie (2026)

| Variable | Valeur | Unité | Source |
|---|---|---|---|
| Électricité — heures pleines | 0,2516 | €/kWh | CRE 2026 |
| Électricité — heures creuses | 0,2068 | €/kWh | CRE 2026 |
| Gaz naturel | 0,1162 | €/kWh PCS | CRE 2026 |
| Fioul domestique | 0,135 | €/kWh | Pégase |
| Bois bûches | 0,075 | €/kWh | ADEME |
| Essence (SP95) | 1,95 | €/L | Pégase |
| Diesel | 1,80 | €/L | Pégase |

## 6.2 Performance énergétique

| Variable | Valeur | Unité | Source |
|---|---|---|---|
| Consommation thermique forfait | 6,5 | L/100 km | hypothèse parc |
| Consommation VE forfait | 17 | kWh/100 km | WLTP moyen 2025 |
| COP PAC air/eau | 3,5 | — | ADEME / Uniclima |
| COP PAC géothermique | 4,5 | — | ADEME |
| COP chauffe-eau thermodynamique | 2,8 | — | BAR-TH-148 |
| Consommation par DPE (A → G) | 50 → 600 | kWh/m²/an | 3CL-DPE |
| Réduction conso après rénovation d'ampleur | −45 % | — | Anah |
| Productible PV (France métropolitaine) | 1 100 | kWh/kWc/an | PVGIS |

## 6.3 Coûts des projets

| Projet | Coût TTC moyen |
|---|---|
| PAC air/eau | 14 000 € |
| PAC géothermique | 22 000 € |
| Rénovation d'ampleur | 45 000 € |
| Photovoltaïque 3 kWc | 9 000 € |
| Borne de recharge domicile | 1 200 € |
| Surcoût VE neuf vs thermique équivalent | 9 000 € |

## 6.4 Barèmes des aides (extraits)

| Aide | Montant | Condition |
|---|---|---|
| MaPrimeRénov' | par solution × profil Anah (2026) | propriétaire occupant / bailleur |
| Prime VPE (Coup de pouce) | 4 000 → 1 000 € | dégressif selon RFR/part |
| Surbonus batterie EU | +1 500 € | score ADEME ≥ seuil |
| Prime à la conversion | 1 500 € | mise au rebut diesel + revenus modestes |
| Prime borne domicile | 75 %, plafond 500 € | propriétaire |
| Prime ADVENIR copropriété | 1 200 € / point de charge | copropriété |
| Gain leasing social | 2 400 €/an | (300 − 100) × 12 |
| Prime PV (≤ 3 kWc) | 230 €/kWc | autoconsommation |
| Prime PV (≤ 9 kWc) | 170 €/kWc | autoconsommation |
| Tarif OA — surplus | 0,13 €/kWh | autoconsommation |

---

# 7. Sources des données

| Donnée | Source officielle | Année / version |
|---|---|---|
| Barèmes MaPrimeRénov' | Anah | 2026 |
| Coup de pouce chauffage, VPE, CEE | DGEC | 2026 |
| Fiche CEE BAR-TH-148 (CET) | ATEE | en vigueur |
| Tarif OA photovoltaïque | CRE | 2026 |
| Prix gaz / électricité réglementés | CRE | 2026 |
| Prix carburants | Pégase (DGEC) | 2025 |
| Score environnemental batterie VE | ADEME | 2025 |
| COP PAC | ADEME / Uniclima / Baromètre PAC | 2025 |
| Consommation par DPE | méthode 3CL-DPE | en vigueur |

---

# 8. Limites connues

## 8.1 Hypothèses simplificatrices assumées

- Consommation thermique 6,5 L/100 km et VE 17 kWh/100 km : forfaits indépendants du modèle.
- Réduction post-rénovation fixée à −45 %, indépendante du DPE initial.
- PV limité à l'autoconsommation avec vente du surplus, ≤ 9 kWc.
- Pas d'aides locales (région / département / commune).
- Locataires exclus de la plupart des aides logement.
- Prix de l'énergie supposés constants en euros 2026 sur tout l'horizon.
- Barèmes d'aides 2026 figés pour tous les chantiers démarrant dans les 10 ans.

## 8.2 Cas non traités

- Véhicules d'occasion (hors prime à la conversion).
- Logements collectifs hors copropriété simple.
- Projets financés via prêt — coût du crédit non modélisé.

---

# Annexe — Historique des versions

| Version | Date | Auteur | Modifications |
|---|---|---|---|
| 0.1 | 2026-05-20 | Bertrand Matge | Création — format à plat |
| 0.2 | 2026-05-20 | Bertrand Matge | Restructuration étape par étape, emplacements pour captures |
| 0.3 | 2026-05-20 | Bertrand Matge | Captures intégrées (mode guidé + mode expert détaillé par zone) |
| 0.4 | 2026-05-20 | Bertrand Matge | Layout 2 colonnes (grid tables), captures réduites, exemple chiffré systématique avec scénario par défaut |
| 0.5 | 2026-05-20 | Bertrand Matge | Adoption du `reference.docx` (styles utilisateur), suppression des plages paramétrables à l'étape 6, précision « horizon 20 ans » dans le récap solutions |
| 0.6 | 2026-05-20 | Bertrand Matge | Layout séquentiel (capture puis texte) pour rendu Word fiable, suppression de `--number-sections` (numérotation auto via styles du `reference.docx`) |
