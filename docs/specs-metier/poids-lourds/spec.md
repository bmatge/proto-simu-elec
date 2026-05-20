---
title: "Simulateur Poids lourd électrique vs diesel — Spécification métier"
simulateur: poids-lourds
version: 0.1
date: 2026-05-20
statut: brouillon — à valider
auteur: Bertrand Matge
destinataires: DGEC mobilité (service fret), DGITM, CNR, Avere-France PL
---

# 1. Objectif & public visé

**Question à laquelle le simulateur répond :** « Sur ma durée de détention prévisionnelle, mon poids lourd électrique me revient-il moins cher qu'un diesel équivalent, compte tenu de l'aide à l'achat (jusqu'à 100 000 € — Mesure 12 du Plan d'électrification) et des coûts d'exploitation ? »

**Public cible :** transporteurs (grandes flottes, PME, artisans), chargeurs qui suivent les coûts de transport, services DGEC / DGITM pour calibrer la Mesure 12.

**Décision aidée :**

- estimer le **surcoût net à l'achat** après aide (CEE bonifié) ;
- calculer le **point d'équilibre** (en années) à partir duquel l'électrique devient plus rentable que le diesel ;
- identifier le **kilométrage pivot annuel** au-delà duquel l'électrique gagne sur la durée de détention.

**Hors périmètre (v1) :**

- Catégories autres que tracteur routier 40 t et porteur urbain 19-26 t (pas de 12 t / 7,5 t logistique urbaine en v1).
- Comparaison vs BioGNV (uniquement strict diesel).
- Valeur résiduelle des véhicules (mise à zéro — marché de l'occasion VE PL quasi inexistant en 2026).
- CAPEX de l'infrastructure de recharge au dépôt (transformateur, bornes HPC).
- Réductions de péages Eurovignette PL électriques.
- Fiscalité spécifique (TVS, taxe à l'essieu, suramortissement 39 decies A).
- Crédit / leasing / coût d'opportunité du capital.

---

# 2. Scénario par défaut — fil rouge des exemples

Tous les exemples chiffrés de ce document utilisent le **scénario chargé par défaut** au démarrage du simulateur.

| Catégorie | Valeurs par défaut |
|---|---|
| **Type de PL** | Tracteur routier 40 t (longue distance) |
| **Exploitation** | 85 000 km/an, durée de détention 5 ans |
| **Diesel** | 110 000 € HT · 30 L/100 km · 7 000 €/an maintenance |
| **Électrique** | 285 000 € HT · 130 kWh/100 km · 4 000 €/an maintenance |
| **Prix énergie** | Gazole pro 1,85 €/L · Électricité recharge mix 0,28 €/kWh |
| **Aide à l'achat** | 100 000 € (CEE bonifié, plafond tracteur, fabrication EU) |

> Avec ces valeurs, le simulateur affiche : surcoût net à l'achat ≈ **75 000 €**, économie annuelle ≈ **17 200 €/an**, point d'équilibre ≈ **4,4 ans**, gain TCO sur 5 ans ≈ **+11 000 €** vs diesel (cohérent avec l'ordre de grandeur cité dans le dossier de presse d'avril 2026 : pivot 85 000 km/an, ~15 000 € d'économies annuelles).

---

# 3. Vue d'ensemble du parcours

L'outil est un **simulateur mono-page** structuré en 4 strates verticales (de haut en bas) :

1. **Hero** — titre + rappel pivot DGEC (85 000 km/an, ~15 000 €/an d'économies)
2. **3 cartes de formulaire côte à côte** — « Mon véhicule » (preset tracteur/porteur) · « Mon exploitation » (km/an, durée) · « Prix de l'énergie » (gazole, électricité, aide)
3. **4 KPIs** — surcoût net, économie annuelle, point d'équilibre, gain TCO sur la durée de détention
4. **Spotlight État** « L'État finance **X%** du surcoût » + **2 graphiques** (TCO cumulé année par année · Gain TCO selon kilométrage annuel) + **tableau détail** + **bloc méthodologie**

![](<images/poids-lourds - global.png>){width=14cm}

Vue d'ensemble au chargement (scénario par défaut : tracteur 40 t, 85 000 km/an, 5 ans).

### Points à valider sur la vue d'ensemble

- ☐ La **hiérarchie « préset → KPIs → spotlight État → graphiques → détail »** correspond-elle au flux de lecture attendu par un transporteur ?
- ☐ Le **rappel du pivot DGEC 85 000 km/an** en hero : message politiquement validé ?

---

# 4. Détail par zone fonctionnelle

## 4.1 Zone — « Mon véhicule » (preset tracteur / porteur)

![](<images/poids-lourds - mon vehicule.png>){width=11cm}

**Champ saisi**

- **Type de poids lourd** — 2 tuiles radio :

| Type | Prix diesel HT | Prix élec HT | Conso diesel | Conso élec | Maint. diesel | Maint. élec | Aide max |
|---|---|---|---|---|---|---|---|
| Tracteur routier 40 t (défaut) | 110 000 € | 285 000 € | 30 L/100km | 130 kWh/100km | 7 000 €/an | 4 000 €/an | 100 000 € |
| Porteur urbain 19-26 t | 80 000 € | 195 000 € | 25 L/100km | 100 kWh/100km | 5 000 €/an | 3 000 €/an | 50 000 € |

À la sélection d'un type, le preset complet est appliqué (toutes les valeurs ci-dessus + le champ « Aide » sont remis à zéro et synchronisés sur les inputs).

**Bloc dépliable « Prix d'achat et maintenance »**

Permet à un utilisateur expert d'écraser les valeurs preset (4 inputs : prix diesel HT, prix élec HT, maintenance diesel €/an, maintenance élec €/an).

### Points à valider sur cette zone

- ☐ Les **deux catégories** (tracteur 40 t / porteur 19-26 t) couvrent-elles 90 % du parc TRM concerné par la Mesure 12 ?
- ☐ Faut-il ajouter une catégorie **12 t** (logistique urbaine) ou **7,5 t** (livraison dernier km) ?
- ☐ Les **prix catalogue 2026** (110 / 80 k€ diesel · 285 / 195 k€ électrique) sont-ils alignés avec les grilles constructeurs (Renault Trucks, Volvo, Daimler, DAF, MAN, Scania, Iveco) ? Qui maintient la grille ?
- ☐ Les **écarts maintenance** (−43 % en tracteur, −40 % en porteur) sont-ils étayés par des retours flottes pilotes (FM Logistic, Schneider, DB Schenker, etc.) ?
- ☐ Le **dépliable expert** est-il assez visible, ou faut-il afficher les valeurs preset en lecture seule à côté ?

---

## 4.2 Zone — « Mon exploitation »

![](<images/poids-lourds - mon exploitation.png>){width=11cm}

**Champs saisis**

- **Kilométrage annuel** — slider 20 000 → 200 000 km, pas de 5 000. Défaut **85 000 km** (pivot DGEC).
- **Durée de détention** — slider 3 → 10 ans, pas de 1. Défaut **5 ans**.

**Bloc dépliable « Consommations »**

- **Consommation diesel** — input nombre, pas 0,5. Défaut 30 L/100 km (tracteur) / 25 L/100 km (porteur) — *IRU / FCM 2024-2025*.
- **Consommation électrique** — input nombre, pas 1. Défaut 130 kWh/100 km (tracteur) / 100 kWh/100 km (porteur) — *T&E 2024 en exploitation réelle*.

### Points à valider sur cette zone

- ☐ Le **pivot 85 000 km/an** comme valeur par défaut est-il pédagogiquement bon (l'utilisateur démarre exactement au point de bascule annoncé) ?
- ☐ La borne haute du slider à **200 000 km/an** couvre-t-elle les usages exceptionnels (longue distance international, transport frigorifique 24/7) ?
- ☐ Les **consommations par défaut** sont-elles validées par les transporteurs (CNR) ? Faut-il intégrer un facteur correctif `conditions sévères` pour le frigo (+30 %), le relief, le froid (−25 à −35 % d'autonomie VE) ?
- ☐ La **durée de détention** maxi 10 ans : pertinente vs la pratique TRM (5-7 ans en 1er propriétaire) ?

---

## 4.3 Zone — « Prix de l'énergie » + Aide à l'achat

![](<images/poids-lourds - prix energie.png>){width=11cm}

**Champs saisis**

- **Prix gazole pro** — input nombre €/L. Défaut **1,85 €/L** (TTC pro, après remboursement TICPE partiel).
- **Prix électricité recharge** — input nombre €/kWh. Défaut **0,28 €/kWh** (mix dépôt nocturne ~0,20 + hub itinérance jour ~0,40).
- **Aide à l'achat mobilisable** — input nombre €. Défaut **100 000 € (tracteur)** / **50 000 € (porteur)**. CEE bonifié, conditionné à une fabrication du véhicule en Europe.

L'aide saisie est **plafonnée** en interne par `PRESETS[type].aideMax` (sécurité : si l'utilisateur saisit 150 000 € sur un porteur, le calcul prend 50 000 €).

### Points à valider sur cette zone

- ☐ Le **prix gazole pro 1,85 €/L** (TTC après TICPE) est-il à jour mai 2026 ? Source CGDD / DGEC ?
- ☐ Le **mix recharge 0,28 €/kWh** (dépôt + hub itinérance) est-il représentatif d'un transporteur routier longue distance ? Plus bas (~0,15 €/kWh) si transporteur urbain 100 % dépôt ?
- ☐ Le **plafond d'aide 100 k€ tracteur / 50 k€ porteur** est-il l'arbitrage Mesure 12 définitif ? Date d'entrée en vigueur **1er juin 2026** confirmée ?
- ☐ Le **critère « fabrication EU »** est-il vérifiable par le bénéficiaire au moment du dépôt de demande ?

---

## 4.4 Zone — Résumé KPIs (4 indicateurs)

![](<images/poids-lourds - resume.png>){width=14cm}

| KPI | Calcul | Couleur |
|---|---|---|
| **Surcoût net à l'achat** | `(prixElec − aide) − prixDiesel` | Orange (`#b34000`) si > 0 |
| **Économie annuelle** | `(carbDiesel + maintDiesel) − (carbElec + maintElec)` | Verte (`#18753c`) si > 0 |
| **Point d'équilibre** | `surcout / economieAnnuelle` (en années) | Bleu DSFR |
| **Gain TCO sur la période** | `tcoDiesel − tcoElec` (sur durée de détention) | Bleu DSFR si > 0, orange si < 0 |

**Formules détaillées**

$$
\text{Acquisition élec.} = \max(0,\ P_\text{VE} - A_\text{aide})
$$

$$
\text{Carb./an (\$énergie\$)} = \frac{km_\text{an} \times C_\text{conso}}{100} \times P_\text{énergie}
$$

$$
\text{TCO (T ans)} = \text{Acquisition} + T \times (\text{Carb./an} + \text{Maint./an})
$$

$$
\text{Économie annuelle} = (\text{Carb. diesel/an} + \text{Maint. diesel}) - (\text{Carb. élec/an} + \text{Maint. élec})
$$

$$
n_\text{bascule} = \frac{\text{Surcoût net à l'achat}}{\text{Économie annuelle}}\quad\text{(si économie > 0)}
$$

**Exemple — valeurs par défaut (tracteur, 85 000 km/an, 5 ans)**

- Acquisition diesel = **110 000 €**
- Acquisition élec = max(0, 285 000 − 100 000) = **185 000 €**
- Surcoût net à l'achat = 185 000 − 110 000 = **75 000 €**
- Carb diesel/an = 85 000 × 30 / 100 × 1,85 ≈ **47 175 €/an**
- Carb élec/an = 85 000 × 130 / 100 × 0,28 ≈ **30 940 €/an**
- Économie annuelle = (47 175 + 7 000) − (30 940 + 4 000) ≈ **19 235 €/an**
- Point d'équilibre = 75 000 / 19 235 ≈ **3,9 ans**
- TCO diesel 5 ans = 110 000 + 5 × 54 175 = **380 875 €**
- TCO élec 5 ans = 185 000 + 5 × 34 940 = **359 700 €**
- Gain TCO sur 5 ans = 380 875 − 359 700 ≈ **+21 175 €** (en faveur de l'électrique)

### Points à valider sur cette zone

- ☐ Le **wording « Surcoût net à l'achat »** est-il compris par les transporteurs (vs « surcoût d'investissement », « delta CAPEX ») ?
- ☐ Affichage en **k€** automatique au-delà de 1 000 € (`12,5 k€` au lieu de `12 500 €`) : pédagogique ?
- ☐ Le **point d'équilibre en années** est plus parlant qu'en km cumulés pour un patron de PME — confirmé ?
- ☐ Le **gain TCO sur la période** signe les choix d'horizon : à 5 ans, la décote VE est ignorée. Faut-il un avertissement explicite ?

---

## 4.5 Zone — Spotlight État « L'État finance X% du surcoût »

![](<images/poids-lourds - financement etat.png>){width=14cm}

Encadré dédié à l'aide, structuré comme un « argument État » :

- Eyebrow « République Française · Plan d'électrification 2026 · Mesure 12 »
- Titre : « L'État finance **X%** du surcoût de votre véhicule »
- Sous-titre : « Sur un surcoût brut de **B**, vous mobilisez **A** d'aide publique. Le reste à charge tombe à **C**. »
- Liste avec le détail de l'aide (montant, nom : « CEE bonifié — Tracteur routier électrique » / « CEE bonifié — Porteur électrique », source DGEC, description)
- Contexte : cible 2 000 PL 2026 / 4 000 PL 2027, fabrication EU
- CTA : ecologie.gouv.fr · ADEME E-Trans · /plan-electrification/#m12

**Formule — % financé**

$$
\text{\%\,financé} = \min\left(100,\ \frac{A_\text{aide}}{P_\text{VE} - P_\text{diesel}}\right)
$$

Pour le scénario par défaut tracteur : surcoût brut = 285 000 − 110 000 = **175 000 €**, aide 100 000 € → **57 % financé par l'État**.

### Points à valider sur cette zone

- ☐ Le **wording « L'État finance X% du surcoût »** est-il politiquement validé ?
- ☐ Le dénominateur (`surcoutBrut = prixElec − prixDiesel`) est-il le bon, ou faut-il prendre `prixElec` seul (« l'État finance 35 % du véhicule ») ?
- ☐ La **description de l'aide** mentionne 100 k€ vs 60 k€ en 2025 — chiffre 2025 à confirmer.

---

## 4.6 Zone — Graphique « TCO cumulé année par année »

![](<images/poids-lourds - tco.png>){width=11cm}

Graphique linéaire avec 2 séries (Diesel orange-brun, Électrique vert) :

- Axe X : Achat, 1 an, 2 ans, …, durée de détention
- Axe Y : coût cumulé en k€

Le **point de croisement** des deux courbes = moment où l'électrique devient moins cher cumulé que le diesel (point d'équilibre lu visuellement).

### Points à valider sur cette zone

- ☐ Le graphique linéaire avec 2 séries est-il plus lisible qu'un graphique de différentiel (gain VE cumulé année par année) ?
- ☐ Faut-il **annoter visuellement** le point d'équilibre sur le graphique (ligne verticale + label) ?

---

## 4.7 Zone — Graphique « Compétitivité selon le kilométrage »

![](<images/poids-lourds - competitivite.png>){width=11cm}

Bar chart sur l'axe X = kilométrages annuels de 20 000 à 200 000 km (pas 10 000). Axe Y = gain TCO vs diesel sur la durée de détention (en k€).

- Barres vertes si gain > 0 (électrique gagnant)
- Barres oranges si gain < 0 (diesel gagnant)
- Titre dynamique « Pivot ≈ X km/an » (calculé par `kmPivot()`)

**Formule — kilométrage pivot**

$$
km_\text{pivot} = \frac{\text{Surcoût net} - T \times (\text{Maint. diesel} - \text{Maint. élec})}{T \times \left[\frac{C_\text{diesel} \times P_\text{gazole} - C_\text{élec} \times P_\text{kWh}}{100}\right]}
$$

(si dénominateur > 0, sinon non rentable quel que soit le km).

**Exemple — valeurs par défaut**

- Numérateur : 75 000 − 5 × (7 000 − 4 000) = 75 000 − 15 000 = **60 000 €**
- Dénominateur : 5 × ((30 × 1,85 − 130 × 0,28) / 100) = 5 × ((55,5 − 36,4) / 100) = 5 × 0,191 = **0,955 €/km**
- $km_\text{pivot}$ ≈ 60 000 / 0,955 / 5 ≈ **62 800 km/an** *(pour le scénario par défaut : le pivot annoncé DGEC est 85 000 km/an, l'écart vient des hypothèses ; à expliciter)*

### Points à valider sur cette zone

- ☐ Le **pivot calculé** par le simulateur dans le scénario par défaut **diverge du pivot annoncé DGEC** (85 000 km/an dans le DP avril 2026). Quelle hypothèse cale les chiffres officiels ?
- ☐ Affichage **par pas de 10 000 km** : assez fin, ou faut-il un slider continu ?
- ☐ Coloration **vert/orange** : alternative pour accessibilité (RGAA) ?

---

## 4.8 Zone — Tableau « Détail du coût annuel »

![](<images/poids-lourds - details cout.png>){width=14cm}

Tableau ligne à ligne pour comprendre le coût total :

| Ligne | Détail | Montant |
|---|---|---|
| Acquisition diesel | — | `110 000 €` |
| Acquisition électrique | `prix 285 000 € − aide 100 000 €` | `185 000 €` (bleu) |
| Carburant diesel | `85 000 km × 30 L/100km × 1,85 €/L` | `47 175 €/an` |
| Carburant électrique | `85 000 km × 130 kWh/100km × 0,28 €/kWh` | `30 940 €/an` (bleu) |
| Maintenance diesel | — | `7 000 €/an` |
| Maintenance électrique | — | `4 000 €/an` (bleu) |
| **TCO 5 ans — diesel** | — | **`380 875 €`** |
| **TCO 5 ans — électrique** | — | **`359 700 €`** (bleu) |

### Points à valider sur cette zone

- ☐ Le **détail des unités** dans la colonne 2 (`85 000 km × 30 L/100km × 1,85 €/L`) est-il utile pour un expert métier qui veut tracer le calcul, ou trop chargé ?
- ☐ Faut-il ajouter une ligne **« Économie annuelle »** synthétique entre maintenance et TCO total ?

---

# 5. Récapitulatif des hypothèses & constantes

## 5.1 Prix d'achat HT (2026 indicatif marché)

| Véhicule | Diesel | Électrique | Source |
|---|---|---|---|
| Tracteur 40 t | 110 000 € | 285 000 € | Renault T / Volvo FH / Iveco S-Way · fourchette diesel 95-130 k€ ; Renault E-Tech T / Volvo FH Electric · fourchette élec 250-340 k€ |
| Porteur 19-26 t | 80 000 € | 195 000 € | Indicatif |

## 5.2 Consommations (défaut)

| Véhicule | Diesel | Électrique | Source |
|---|---|---|---|
| Tracteur 40 t | 30 L/100 km | 130 kWh/100 km | IRU / FCM 2024-2025 · T&E 2024 |
| Porteur 19-26 t | 25 L/100 km | 100 kWh/100 km | Estimation |

## 5.3 Maintenance annuelle

| Véhicule | Diesel | Électrique | Source |
|---|---|---|---|
| Tracteur 40 t | 7 000 €/an | 4 000 €/an | CNR (référentiel pneumatiques + entretien) · −40 % vs diesel (estimation) |
| Porteur 19-26 t | 5 000 €/an | 3 000 €/an | Estimation |

## 5.4 Prix énergie (mai 2026)

| Énergie | Prix | Source |
|---|---|---|
| Gazole pro | 1,85 €/L | TTC pro après remboursement TICPE partielle |
| Électricité recharge mix | 0,28 €/kWh | Dépôt nocturne ~0,20 + hub itinérance jour ~0,40 |

## 5.5 Aides à l'achat (Mesure 12, DP avril 2026)

| Véhicule | Aide max | Source |
|---|---|---|
| Tracteur routier électrique | 100 000 € | CEE bonifié, fabrication EU, applicable 1er juin 2026 |
| Porteur urbain électrique | 50 000 € | Estimation (« quasi doublement » des aides porteur, base 25-30 k€ en 2025) |

## 5.6 Paramètres techniques

| Paramètre | Valeur |
|---|---|
| Slider km/an min / max | 20 000 / 200 000 |
| Slider km/an pas | 5 000 |
| Slider durée min / max | 3 / 10 ans |
| Pas du graphique pivot | 10 000 km |
| Plage tranche affichage k€ | ≥ 1 000 € |

---

# 6. Sources des données

| Donnée | Source officielle | Année / version | Référence |
|---|---|---|---|
| Mesure 12 (aide PL électrique) | Plan d'électrification — DP avril 2026 | 2026 | DGEC |
| Prix gazole professionnel | CGDD (hebdomadaire) | mai 2026 | `statistiques.developpement-durable.gouv.fr` |
| Consommation tracteur diesel | International Road Transport Union (IRU) · FCM | 2024-2025 | iru.org |
| Consommation tracteur électrique | Transport & Environment | 2024 | transportenvironment.org |
| Référentiel coûts CNR | Comité national routier | continu | cnr.fr |
| Programme ADEME E-Trans (engins) | Ademe | 2026 | ademe.fr |
| Tarif électricité B2B | CRE | mai 2026 | cre.fr |

---

# 7. Limites connues

## 7.1 Hypothèses simplificatrices assumées

- **Aucune valeur résiduelle** retenue (marché VE PL occasion quasi inexistant en 2026). Le diesel et l'électrique sont tous deux remis à zéro à la revente — pratique conservatrice.
- **TCO calculé en euros constants** (pas d'inflation ni d'indexation des prix énergie sur la durée).
- **CAPEX infrastructure de recharge dépôt** (transformateur, bornes HPC, 20-80 k€ selon flotte) **non inclus** — à mentionner dans l'aide.
- **Coût d'opportunité du capital** immobilisé (financement, leasing) non pris en compte.
- **Maintenance −40 % VE** : ordre de grandeur extrapolé des flottes pilotes, à confirmer.

## 7.2 Cas non traités (v1)

- Catégorie **12 t** et **7,5 t** (logistique urbaine, dernier km).
- Transport **frigorifique** (consommation électrique +30 %).
- Comparaison vs **BioGNV / biocarburants HVO**.
- **Conditions sévères** (relief, froid, charge max) qui dégradent l'autonomie VE de 25-35 %.
- **Réductions de péages PL électrique** (directive Eurovignette à venir).
- **Fiscalité** : TVS, taxe à l'essieu, suramortissement 39 decies A, crédit d'impôt.
- **Aides locales** (région, EPCI) et programmes spécifiques (Plan Air).
- **Formation conducteur** VE (coût ponctuel) — exclu.

## 7.3 Points ouverts à arbitrer avec les experts

1. **Pivot annoncé DGEC** (85 000 km/an) vs **pivot calculé** par le simulateur (~63 000 km/an au scénario par défaut). Quelle hypothèse cale la communication officielle ?
2. **Crédit d'impôt + suramortissement** (art. 39 decies A) : régime 2026 confirmé ? *(open dans la modale business)*
3. **TVS / taxe à l'essieu** : exemption VE confirmée jusque quand ?
4. **Accès aux bornes publiques HPC** : maillage encore très lacunaire — comment matérialiser ce risque dans l'outil ?
5. **Confidentialité** : les patrons saisiraient-ils leur kilométrage réel sans crainte de fuite concurrentielle ? Rappeler que rien n'est stocké côté serveur.

---

# Annexe — Historique des versions

| Version | Date | Auteur | Modifications |
|---|---|---|---|
| 0.1 | 2026-05-20 | Bertrand Matge | Création initiale (préset tracteur/porteur, KPIs, spotlight État Mesure 12, 2 graphiques TCO + pivot km) |
