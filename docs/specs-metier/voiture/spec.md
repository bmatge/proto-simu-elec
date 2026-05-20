---
title: "Simulateur « Voiture électrique » — Spécification métier (cas n°1 : VE vs Thermique neuf)"
simulateur: voiture
version: 0.2
date: 2026-05-20
statut: brouillon — à valider
auteur: Bertrand Matge
destinataires: DGEC mobilité, ADEME
---

# 1. Objectif & public visé

**Question à laquelle le simulateur répond (cas n°1) :** « J'achète une voiture neuve. Sur 5 à 10 ans, le véhicule électrique me revient-il moins cher qu'un thermique équivalent, en tenant compte de toutes les aides 2026 et des coûts d'usage ? »

**Public cible :** particuliers français en phase de décision d'achat d'une voiture neuve.

**Décision aidée :** comparer le **coût total de possession (TCO)** d'un VE et d'un thermique équivalent sur l'horizon de détention, identifier l'année de **point de bascule** où le VE devient rentable.

**Hors périmètre (cas n°1) :**

- Cas n°2 « Revendre mon thermique pour acheter un VE » — *spec à rédiger ultérieurement*.
- Cas n°3 « Acheter un VE d'occasion » — *spec à rédiger ultérieurement*.
- Usage professionnel : pas de TVS, pas de TAI, pas d'avantage en nature, pas d'amortissement fiscal.
- Coût de financement (crédit, LOA, leasing) non modélisé.
- Aides locales (région, département) non intégrées.
- Contraintes d'usage non chiffrées : temps de recharge longs trajets, ZFE, autonomie par grand froid.

---

# 2. Scénario par défaut — fil rouge des exemples

Tous les exemples chiffrés de ce document utilisent le **scénario chargé par défaut** au démarrage du simulateur (cas n°1 « Achat neuf VE vs thermique »).

| Catégorie | Valeurs par défaut |
|---|---|
| **Usage** | 13 000 km/an, durée de détention 5 ans |
| **Voiture électrique** | Prix catalogue **30 000 €**, consommation **16 kWh/100 km**, tranche RFR médiane (prime CEE **4 700 €**), surbonus batterie EU **1 500 €** (Oui médian), borne domicile **1 200 €** |
| **Voiture thermique** | Prix catalogue **23 000 €**, essence, consommation **6 L/100 km**, malus CO₂ + poids **0 €** |
| **Prix de l'énergie** | Élec HC 0,18 €/kWh, HP 0,24 €/kWh, borne rapide 0,60 €/kWh ; essence 1,75 €/L, diesel 1,65 €/L |
| **Mix de recharge VE** | **60 % HC / 30 % HP / 10 % borne rapide** → prix moyen pondéré **0,240 €/kWh** |
| **Entretien** | VE 250 €/an, TH 600 €/an |
| **Assurance** | VE 650 €/an, TH 600 €/an |
| **Décote à la revente** | VE **45 %** du prix conservé (= 13 500 €), TH **40 %** (= 9 200 €) |

> Avec ces valeurs, le simulateur affiche : **acquisition VE après aides 25 000 €** (vs TH 23 000 €), **économie d'énergie 866 €/an** (≈ 72 €/mois), **économie entretien/assurance 350 €/an**, **point de bascule à 1,7 an**, **TCO 5 ans VE 18 496 €** vs **TH 26 625 €** → **gagnant VE de 8 129 € sur 5 ans**.

---

# 3. Vue d'ensemble du parcours

Le simulateur s'ouvre sur un **point d'entrée à 3 cas d'usage** (« J'achète une voiture neuve » / « J'ai déjà une voiture, je veux la revendre pour un VE neuf » / « J'ai déjà une voiture, je veux passer à un VE d'occasion »). Le présent document décrit uniquement le cas n°1 « voiture neuve ».

Une fois le cas n°1 sélectionné, le simulateur propose **deux modes** qui utilisent les **mêmes formules** :

- **Mode guidé** : **7 étapes successives** (bienvenue / usage / cible VE / thermique / situation fiscale / habitudes de recharge / récapitulatif).
- **Mode expert** : tous les paramètres et résultats sur une seule page, organisée en **4 zones de paramètres** à gauche et **5 étapes de bilan** à droite (1 achat / 2 énergie mensuelle / 3 entretien et assurance / 4 valeur revente / 5 bilan année après année).

---

# 4. Mode guidé — détail étape par étape (cas n°1)

Le mode guidé enchaîne 7 écrans, chacun avec un eyebrow bleu (en haut), une question principale, des champs et 2 boutons « Retour » / « Continuer ».

## 4.1 Étape 1 — Choix du cas d'usage (« Bienvenue »)

![](<images/voiture-guide - etape 1.png>){width=11cm}

**Eyebrow** : « BIENVENUE » · **Question** : « Faut-il passer à l'électrique ? »

**Champs saisis** — 3 tuiles cliquables (radio exclusif) :

- *J'achète une voiture neuve, j'hésite entre les deux* — comparaison VE neuf vs thermique neuf équivalent. ← **objet du présent document**.
- *J'ai déjà une voiture, je veux la revendre pour un VE neuf* — évalue si le changement vaut le coup en tenant compte de la revente. *Spec à rédiger.*
- *J'ai déjà une voiture, je veux passer à un VE d'occasion* — plus accessible, mais sans aide nationale et avec un risque batterie à évaluer. *Spec à rédiger.*

**Sortie de l'étape**

Sélection du **mode de calcul** (cas n°1 / 2 / 3). Le bouton « Continuer » est désactivé tant qu'un cas n'est pas choisi.

### Points à valider sur cette étape

- ☐ Les libellés des 3 cas sont-ils compréhensibles d'emblée pour un particulier ?
- ☐ Le sous-texte du cas n°3 (« sans aide nationale et avec un risque batterie ») est-il une formulation acceptable ou trop défavorable au marché de l'occasion ?
- ☐ Faut-il afficher dès cette étape une icône / pictogramme indiquant les cas non encore disponibles ?

---

## 4.2 Étape 2 — Votre usage

![](<images/voiture-guide - etape 2.png>){width=11cm}

**Eyebrow** : « VOTRE USAGE » · **Question** : « Comment utilisez-vous votre voiture ? »

**Champs saisis**

- **Kilométrage annuel** — slider 3 000 → 40 000 km/an, défaut **13 000 km/an**. Aide affichée : « La moyenne française est d'environ 13 000 km/an ». 4 presets cliquables sous le slider :
  - Petit rouleur — 6 000 km
  - Moyen — 13 000 km
  - Gros rouleur — 20 000 km
  - Très gros — 30 000 km
- **Durée de détention** — 4 tuiles cliquables (radio exclusif) : 3 / **5 ans (sélectionné par défaut)** / 7 / 10. Aide affichée : « La rentabilité d'un VE se calcule sur le moyen terme. En dessous de 4 ans, l'avantage est rarement décisif. »

**Sortie de l'étape**

Définit l'**horizon de comparaison** $N$ (années) et le **kilométrage annuel** $km$ utilisés dans toutes les formules de TCO.

**Exemple — valeurs par défaut**

13 000 km/an × 5 ans → **65 000 km cumulés** comparés.

### Points à valider sur cette étape

- ☐ La **moyenne française 13 000 km/an** est-elle bien le bon repère pédagogique (SDES 2024 ≈ 11 800 km/an, INSEE budget des familles ≈ 13 000 km/an) ?
- ☐ Les **4 presets** (6 / 13 / 20 / 30 k) couvrent-ils les profils types ? Faut-il un preset « < 4 000 km » (urbain, 2e voiture du foyer) ?
- ☐ Les **4 durées proposées** (3/5/7/10 ans) reflètent-elles la pratique réelle (durée moyenne 1er propriétaire VP ≈ 5-7 ans) ?
- ☐ Le message d'aide « En dessous de 4 ans, l'avantage est rarement décisif » est-il acceptable politiquement / pédagogiquement ?

---

## 4.3 Étape 3 — Votre cible (VE neuf)

![](<images/voiture-guide - etape 3.png>){width=11cm}

**Eyebrow** : « VOTRE CIBLE » · **Question** : « Quel VE neuf vous intéresse ? »

Aide générale : « Si vous n'avez pas encore choisi, les valeurs par défaut correspondent à une citadine européenne type Renault 5 / Peugeot e-208 / Citroën ë-C3. »

**Champs saisis**

- **Prix catalogue TTC** — input numérique, défaut **30 000 €**. Aide : « Pour bénéficier des aides, le prix doit être inférieur à 47 000 €. » 3 presets cliquables :
  - ~25 k€ (citadine)
  - ~32 k€ (compacte)
  - ~40 k€ (familiale)
- **Consommation** — input numérique, défaut **16 kWh/100 km**. Aide : « Compter 14-16 kWh/100 km pour une citadine, 18-22 pour un SUV. Cherchez la conso WLTP, ajoutez 10-15 % pour estimer le réel. »

**Sortie de l'étape**

$P_\text{VE}$ et $C_\text{VE}$ (kWh/100 km) utilisés dans toutes les formules en aval.

### Points à valider sur cette étape

- ☐ Le **prix par défaut 30 000 €** est-il pertinent pour une « citadine européenne » 2026 ?
- ☐ Le **plafond 47 000 €** pour les aides est-il à jour (CEE VPE 2026) ?
- ☐ Les **3 presets de prix** (~25 / ~32 / ~40 k€) couvrent-ils 80 % des segments accessibles VE ? Manque un preset SUV familial > 50 k€ (mais hors aides) ?
- ☐ Le **conseil WLTP +10-15 %** pour estimer la conso réelle est-il une convention officielle (ADEME) ou un retour d'usage ?
- ☐ Faut-il un preset SUV (~18-22 kWh/100 km) en plus des 2 valeurs textuelles dans l'aide ?

---

## 4.4 Étape 4 — Comparaison thermique

![](<images/voiture-guide - etape 4.png>){width=11cm}

**Eyebrow** : « COMPARAISON THERMIQUE » · **Question** : « Et le thermique équivalent ? »

Aide générale : « Pour comparer équitablement, prenez un modèle de gamme similaire au VE choisi. »

**Champs saisis**

- **Carburant** — 2 tuiles cliquables : **Essence (sélectionné par défaut)** / Diesel.
- **Prix catalogue TTC** — input numérique, défaut **23 000 €**.
- **Consommation** — input numérique, défaut **6 L/100 km**.
- **Malus écologique applicable** — input numérique, défaut **0 €**. Aide : « Le malus s'applique aux thermiques émetteurs ou lourds. Laissez 0 si le modèle est sobre, sinon vérifiez sur le site du constructeur. »

**Sortie de l'étape**

$P_\text{TH}$, $C_\text{TH}$ (L/100 km), $\text{Malus}_\text{TH}$, énergie utilisée pour le calcul d'usage.

### Points à valider sur cette étape

- ☐ Le **prix thermique par défaut 23 000 €** est-il représentatif d'une citadine essence équivalente à la cible VE 30 000 € (Renault Clio, Peugeot 208, etc.) ?
- ☐ La **conso 6 L/100 km essence** est-elle représentative d'une citadine 2026 (moteur 3-cyl 1.0 turbo) ?
- ☐ Le **malus par défaut à 0 €** est-il pertinent ou doit-on afficher la médiane parc neuf 2026 ?
- ☐ Faut-il intégrer la **vignette Crit'Air** / un coût ZFE indicatif côté thermique pour les zones concernées ?
- ☐ L'absence du **GPL / hybride non rechargeable / micro-hybride** est-elle assumée en cas n°1 ?

---

## 4.5 Étape 5 — Votre situation fiscale (RFR + batterie EU)

![](<images/voiture-guide - etape 5.png>){width=11cm}

**Eyebrow** : « VOTRE SITUATION FISCALE » · **Question** : « Quelles aides vous concernent ? »

Aide générale : « La prime "coup de pouce VPE" remplace l'ancien bonus écologique depuis juillet 2025. Son montant dépend de votre revenu fiscal. »

**Champs saisis** — 2 questions :

**5.5.1 Revenu fiscal de référence par part** — 3 tuiles cliquables (icône €) :

| Tranche RFR/part | Aide CEE | Cible |
|---|---|---|
| ≤ 16 300 € | jusqu'à **5 700 €** | Ménages modestes ou en précarité |
| Entre 16 301 € et 26 300 € (**sélectionné par défaut**) | jusqu'à **4 700 €** | Ménages intermédiaires |
| > 26 300 € | jusqu'à **3 500 €** | Autres ménages |

Aide : « Vous le trouvez en page 2 ou 3 de votre avis d'imposition. C'est le RFR divisé par le nombre de parts du foyer. »

**5.5.2 Le modèle visé a-t-il une batterie européenne ?** — 3 boutons :

- **Oui (1 500 €)** *(sélectionné par défaut)*
- Oui (2 000 €)
- Non éligible

Aide : « Un surbonus de 1 200 à 2 000 € est accordé pour les batteries fabriquées en Europe. La plupart des Renault, Peugeot, Citroën et Stellantis y sont éligibles. Vérifiez la liste ADEME. »

**Sortie de l'étape**

Montant total des aides CEE = `Prime CEE (RFR) + Surbonus batterie EU`.

### Points à valider sur cette étape

- ☐ Les **3 montants CEE** (5 700 / 4 700 / 3 500 €) sont-ils à jour 2026 ?
- ☐ Les **2 seuils RFR/part** (16 300 € / 26 300 €) correspondent-ils bien aux tranches officielles 2026 ?
- ☐ Le **surbonus batterie EU** : pourquoi proposer 1 500 € comme défaut médian vs 2 000 € (palier haut) ? Sur quel critère ADEME ?
- ☐ Doit-on intégrer la **prime à la conversion** (mise au rebut d'un diesel) comme 3e levier d'aide dans cette étape ?

---

## 4.6 Étape 6 — Vos habitudes de recharge

![](<images/voiture-guide - etape 6.png>){width=11cm}

**Eyebrow** : « VOS HABITUDES DE RECHARGE » · **Question** : « Où rechargerez-vous principalement ? »

Aide générale : « C'est le facteur qui fait le plus varier le coût de l'énergie. Recharger en heures creuses chez soi coûte 3 à 4× moins cher qu'en borne rapide. »

**Champs saisis** — 4 tuiles cliquables (radio exclusif) :

| Profil | Icône | Mix de recharge | Prix moyen kWh |
|---|---|---|---|
| À domicile, surtout en heures creuses | 🌙 | ~100 % HC | ~0,18 €/kWh |
| À domicile, sans toujours optimiser **(par défaut)** | 🏠 | mix dominant HC + un peu HP | ~0,20 €/kWh moyen |
| Mix domicile + bornes publiques | ⬛ | mix domicile + publique | ~0,25 €/kWh moyen |
| Surtout en borne publique | ⚡ | ~100 % borne rapide | — (avertissement : économies très réduites) |

Le profil sélectionné pilote en interne les 3 ratios HC/HP/Borne rapide, et donc le **prix moyen pondéré du kWh** utilisé dans la formule d'énergie VE.

> En mode expert, les 3 ratios sont ajustables individuellement (cf. §6.4). Le scénario par défaut en mode expert utilise **60 % HC / 30 % HP / 10 % Borne rapide** → prix moyen **0,240 €/kWh**.

### Points à valider sur cette étape

- ☐ Les **prix moyens annoncés** (0,18 / 0,20 / 0,25 €/kWh) reflètent-ils bien les profils proposés ?
- ☐ Le **profil par défaut « À domicile, sans toujours optimiser »** est-il le bon point de départ pédagogique (vs « surtout en HC » plus optimiste) ?
- ☐ Le **profil « Surtout en borne publique »** affiche un avertissement « économies très réduites » : message politiquement acceptable / aligné avec la stratégie d'incitation à la borne domestique ?
- ☐ Doit-on proposer un profil **« Sans borne à domicile (copropriété) »** distinct du « Surtout en borne publique » ?
- ☐ Faut-il afficher le **mix HC/HP/Borne rapide réel** sous-jacent à chaque profil pour transparence ?

---

## 4.7 Étape 7 — Récapitulatif

![](<images/voiture-guide - etape 7.png>){width=11cm}

**Eyebrow** : « RÉCAPITULATIF » · **Question** : « On y est ! »

Sous-titre : « Voici vos réponses. Cliquez sur **Lancer la simulation** pour voir le résultat détaillé. »

**Contenu** — un tableau synthétique organisé en 6 rubriques :

| Rubrique | Champs récapitulés (valeurs par défaut) |
|---|---|
| **VOTRE SITUATION** | Mode : Achat neuf VE vs thermique |
| **USAGE** | Kilométrage annuel : 13 000 km · Durée de détention : 5 ans |
| **VE NEUF VISÉ** | Prix catalogue : 30 000 € · Consommation : 16 kWh/100 km |
| **THERMIQUE COMPARÉ** | Type & prix : essence · 23 000 € · Consommation : 6 L/100 km |
| **AIDES** | Prime CEE : 4 700 € · Surbonus batterie EU : 1 500 € |
| **RECHARGE** | Profil : À domicile, mix standard |

Pied de page : « Une fois la simulation lancée, vous pourrez ajuster finement chaque paramètre dans le panneau de gauche, ou relancer le guide à tout moment via le bouton "Repasser en mode guidé" dans le bandeau supérieur. »

Boutons : **Retour** (revenir à l'étape 6) · **Lancer la simulation** (bascule sur le mode expert pré-rempli avec les réponses).

### Points à valider sur cette étape

- ☐ L'**ordre des 6 rubriques** suit l'ordre des 6 étapes précédentes (situation / usage / VE / thermique / aides / recharge) — cohérent ?
- ☐ La rubrique **AIDES** affiche les 2 lignes (Prime CEE + Surbonus). Faut-il ajouter une **3e ligne « Total aides » = 6 200 €** pour préparer la lecture du bilan ?
- ☐ La transition « Lancer la simulation » bascule sur le **mode expert pré-rempli** : suffisamment expliqué dans le pied de page ?
- ☐ Faut-il proposer un export (PDF / impression) du récapitulatif à cette étape ?

---

# 5. Résultat final — bilan TCO (formules partagées guidé / expert)

À l'issue des 7 étapes (mode guidé) ou en temps réel (mode expert), le simulateur calcule :

**Coût d'acquisition net**

$$
A_\text{VE} = P_\text{VE} - \text{Prime CEE} - \text{Surbonus batterie EU} + \text{Borne domicile}
$$

$$
A_\text{TH} = P_\text{TH} + \text{Malus}_\text{TH}
$$

**Coût d'énergie annuel**

$$
\bar{P}_\text{kWh} = \alpha_\text{HC} \cdot P_\text{HC} + \alpha_\text{HP} \cdot P_\text{HP} + \alpha_\text{DC} \cdot P_\text{DC}
$$

$$
E_\text{VE} = \frac{C_\text{VE}}{100} \times km \times \bar{P}_\text{kWh}
\qquad
E_\text{TH} = \frac{C_\text{TH}}{100} \times km \times P_\text{carburant}
$$

**Coût d'usage annuel**

$$
U_\text{VE} = E_\text{VE} + \text{Entretien}_\text{VE} + \text{Assurance}_\text{VE}
\qquad
U_\text{TH} = E_\text{TH} + \text{Entretien}_\text{TH} + \text{Assurance}_\text{TH}
$$

**Valeur résiduelle**

$$
V_\text{résiduelle} = P_\text{catalogue} \times \tau_\text{conservé}
$$

**TCO sur N ans**

$$
\text{TCO} = A + N \times U - V_\text{résiduelle}
$$

**Différentiel et point de bascule**

$$
\Delta = \text{TCO}_\text{TH} - \text{TCO}_\text{VE}
\qquad
n_\text{bascule} = \frac{A_\text{VE} - A_\text{TH}}{U_\text{TH} - U_\text{VE}}
$$

**Exemple complet — valeurs par défaut (5 ans, 13 000 km/an, mix 60/30/10)**

| Étape | VE | Thermique |
|---|---|---|
| Acquisition nette | 30 000 − 4 700 − 1 500 + 1 200 = **25 000 €** | 23 000 + 0 = **23 000 €** |
| Prix moyen kWh | 0,6×0,18 + 0,3×0,24 + 0,1×0,60 = **0,240 €/kWh** | — |
| Énergie / an | 16 × 130 × 0,240 = **499 €/an** | 6 × 130 × 1,75 = **1 365 €/an** |
| Entretien / an | 250 € | 600 € |
| Assurance / an | 650 € | 600 € |
| **Usage total / an** | **1 399 €/an** | **2 565 €/an** |
| Usage cumulé sur 5 ans | 6 995 € | 12 825 € |
| Valeur résiduelle (5 ans) | 30 000 × 0,45 = **13 500 €** | 23 000 × 0,40 = **9 200 €** |
| **TCO 5 ans** | **18 496 €** | **26 625 €** |
| **Différentiel** | | **VE gagnant de 8 129 €** |
| **Point de bascule** | $2\,000 / 1\,166$ ≈ **1,7 an** | |

---

# 6. Mode expert — détail par zone fonctionnelle

Une fois la simulation lancée, le mode expert affiche tous les paramètres à gauche et tous les résultats à droite **sur une seule page**. Il y a **4 zones de paramètres** (votre usage, voiture électrique, voiture thermique, réglages avancés) et **5 étapes de bilan numérotées** (achat, énergie mensuelle, entretien et assurance, valeur revente, bilan année après année).

## 6.1 Zone — Votre usage

![](<images/expert-scenario1 - usage.png>){width=8cm}

Zone compacte avec icône cible. Reprend les 2 champs de l'étape 2 du mode guidé.

**Champs**

- Kilométrage annuel — input numérique, défaut **13 000 km/an**.
- Durée de détention — input numérique, défaut **5 ans**.

Aide affichée : « Plus vous roulez, plus l'électrique devient avantageux. »

### Points à valider sur cette zone

- ☐ Faut-il conserver le **slider** (mode guidé) ou un simple **input** est plus efficace en mode expert ?
- ☐ Une borne haute implicite (40 000 km/an, 20 ans) doit-elle être visible ?

---

## 6.2 Zone — Voiture électrique

![](<images/expert-scenario1 - voiture electrique.png>){width=8cm}

Zone avec icône éclair, regroupant les paramètres VE et l'éligibilité aux aides.

**Champs**

- **Prix catalogue TTC** — input, défaut **30 000 €**.
- **Consommation** — input, défaut **16 kWh/100 km**. Aide : « Citadine ~14 kWh, SUV 18-22 ».
- **Tranche RFR/part** — select, défaut **16 301-26 300 € — 4 700 €** (RFR médian). Aide : « Avis d'imposition, dernière page ». Options : 5 700 € (≤ 16 300), 4 700 € (16 301-26 300), 3 500 € (> 26 300).
- **Surbonus batterie EU** — select, défaut **Oui (médian) — 1 500 €**. Options : 0 / 1 500 / 2 000 €.
- **Borne domicile** — input numérique, défaut **1 200 €**.

### Points à valider sur cette zone

- ☐ Le **regroupement « paramètres VE + éligibilité aides »** dans une seule zone est-il intuitif, ou faut-il une zone « Aides » séparée ?
- ☐ La **borne domicile à 1 200 €** est-elle la médiane du marché 2026 (Wallbox, Enphase, Schneider EVlink) ? Faut-il un select preset (sans borne / 800 € / 1 200 € / 1 800 €) ?
- ☐ Faut-il ajouter un champ **prime à la conversion** ou **aide locale** ici ?

---

## 6.3 Zone — Voiture thermique

![](<images/expert-scenario1 - voiture thermique.png>){width=8cm}

Zone avec icône pompe à essence, reprend les champs de l'étape 4 du mode guidé.

**Champs**

- **Prix catalogue TTC** — input, défaut **23 000 €**.
- **Carburant** — select, défaut **Essence**. Options : Essence / Diesel.
- **Consommation** — input, défaut **6 L/100 km**.
- **Malus CO₂ + poids** — input, défaut **0 €**.

### Points à valider sur cette zone

- ☐ Faut-il un **slider de malus** avec des paliers (0 / 500 / 1 500 / 5 000 / 20 000 €) plutôt qu'un input libre ?
- ☐ Doit-on ajouter le **gabarit / poids** du véhicule pour pré-calculer le malus selon la grille DGEC ?

---

## 6.4 Zone — Réglages avancés (énergie, entretien, décote)

![](<images/expert-scenario1 - reglages.png>){width=8cm}

Bloc dépliable (par défaut ouvert en capture) regroupant 3 sous-sections :

**Prix de l'énergie** (5 champs)

| Variable | Défaut | Unité |
|---|---|---|
| Élec. heures creuses | 0,18 | €/kWh |
| Élec. heures pleines | 0,24 | €/kWh |
| Élec. borne rapide | 0,60 | €/kWh |
| Prix essence | 1,75 | €/L |
| Prix diesel | 1,65 | €/L |

**Mix de recharge VE** (3 champs en %, total = 100)

| Variable | Défaut |
|---|---|
| Heures creuses | **60 %** |
| Heures pleines | **30 %** |
| Borne rapide | **10 %** |

> ⚠️ Le **mix par défaut 60/30/10** diffère des 4 profils du mode guidé (cf. §4.6) — il correspond approximativement au profil « À domicile, mix standard » mais avec des valeurs explicites. À harmoniser avec les libellés guidés.

**Entretien & assurance** (4 champs €/an)

| Variable | Défaut |
|---|---|
| Entretien VE | 250 €/an |
| Entretien thermique | 600 €/an |
| Assurance VE | 650 €/an |
| Assurance thermique | 600 €/an *(non visible sur la capture, en bas du panneau)* |

> La capture est tronquée en bas : **Décote à la revente** (% conservé VE et TH) figure également dans cette zone — cf. captures 6.8 pour les valeurs (45 % VE / 40 % TH).

### Points à valider sur cette zone

- ☐ Le **mix par défaut 60/30/10** (mode expert) vs **profils nominaux** (mode guidé) : à aligner. Risque d'écart de résultat entre les 2 modes pour le même utilisateur.
- ☐ Les **prix énergie 2026** (0,18 / 0,24 / 0,60 €/kWh ; 1,75 €/L ; 1,65 €/L) sont-ils à actualiser à quelle fréquence et par qui ?
- ☐ Le bloc « Réglages avancés » est dépliable : par défaut **ouvert ou fermé** ? Quel impact pédagogique ?

---

## 6.5 Bilan ① — Combien coûtent ces voitures à l'achat ?

![](<images/expert-scenario1 - cout achat.png>){width=14cm}

**Présentation** : 2 barres horizontales comparatives.

- Barre verte (Électrique après aides) : **25 000 €**
- Barre orange (Thermique) : **23 000 €**

**Message conclusif** dans un encadré vert : « Sur le prix d'achat seul, **le thermique reste 2 000 € moins cher**, malgré les 6 200 € d'aides sur le VE. »

**Détail des aides** : 4 700 € (Prime CEE) + 1 500 € (Surbonus batterie EU) = **6 200 €** d'aides. Ajout de 1 200 € (borne domicile) au coût VE → 30 000 − 6 200 + 1 200 = **25 000 €**.

Lien dépliable « ▶ Voir le détail du calcul » pour exposer la formule complète.

### Points à valider sur cette étape

- ☐ Le **message « le thermique reste 2 000 € moins cher »** est-il acceptable politiquement, ou faut-il éviter de mettre en avant le surcoût d'achat VE ?
- ☐ Faut-il inclure la **borne domicile (1 200 €)** dans le coût d'acquisition VE, ou la traiter comme un poste à part (« infrastructure ») ?
- ☐ La barre horizontale est-elle plus lisible qu'un tableau ? Affichage en valeur absolue ou en % du prix catalogue ?

---

## 6.6 Bilan ② — Combien ça coûte de rouler chaque mois ?

![](<images/expert-scenario1 - cout energie.png>){width=14cm}

**Présentation** : 2 cartes côte à côte (VE / TH) avec le coût en €/mois.

| Carte | Coût mensuel | Détail |
|---|---|---|
| **Recharge électrique** | **42 €/mois** (soit 499 €/an) | Conso 16 kWh/100 km · Prix moyen kWh **0,240 €** |
| **Carburant essence** | **114 €/mois** (soit 1 365 €/an) | Conso 6 L/100 km · Prix au L **1,75 €** |

**Message conclusif** dans un encadré vert : « **Économie : 72 €/mois** avec l'électrique sur l'énergie seule (soit 866 €/an, et **4 329 € sur 5 ans**). »

**Phrase d'introduction** : « L'énergie est le poste où l'électrique fait le plus gros écart. Pour vos 13 000 km par an : »

Lien dépliable « ▶ Voir le détail du calcul » pour exposer la formule.

### Points à valider sur cette étape

- ☐ L'affichage **en €/mois** est plus parlant qu'en €/an : confirmé par les retours utilisateurs ?
- ☐ Le **prix moyen kWh 0,240 €** est-il systématiquement affiché en sous-texte pour transparence ?
- ☐ Doit-on afficher aussi le **TCO énergie sur N ans** (4 329 € pour 5 ans) directement dans la carte VE, ou réserver cela au bilan final ?
- ☐ La distinction « énergie seule » est importante (le reste arrive dans les étapes 3 et 4) : assez explicite ?

---

## 6.7 Bilan ③ — L'entretien et l'assurance

![](<images/expert-scenario1 - cout assurance.png>){width=14cm}

**Présentation** : 2 cartes côte à côte (VE / TH) avec le coût annuel.

| Carte | Coût annuel | Détail |
|---|---|---|
| **VE — entretien + assurance** | **900 €/an** | Entretien 250 € + Assurance 650 € |
| **Thermique — entretien + assurance** | **1 200 €/an** | Entretien 600 € + Assurance 600 € |

**Message conclusif** dans un encadré vert : « L'électrique économise **350 €/an sur l'entretien**, soit **1 750 € sur 5 ans**. »

**Phrase d'introduction** : « Un moteur électrique a beaucoup moins de pièces qui s'usent (pas de vidange, pas de courroie, freins préservés grâce à la récupération d'énergie). L'assurance est globalement comparable. »

### Points à valider sur cette étape

- ☐ La formulation **« économise 350 €/an sur l'entretien »** est imprécise (en réalité c'est entretien + assurance combinés, avec entretien −350 et assurance +50). Faut-il clarifier ?
- ☐ Les **écarts entretien VE/TH (250 vs 600 €/an)** et **assurance VE/TH (650 vs 600 €/an)** sont-ils défendables (UFC-Que Choisir 2024, ADEME Verdir ma flotte) ?
- ☐ Faut-il intégrer un **coût de remplacement de batterie** à mi-vie pour le VE (rare en pratique, mais à signaler) ?

---

## 6.8 Bilan ④ — Combien ça vaudra à la revente ?

![](<images/expert-scenario1 - valeur revente.png>){width=14cm}

**Présentation** : 2 cartes côte à côte (VE / TH) avec la valeur résiduelle estimée.

| Carte | Valeur après 5 ans | % du prix neuf conservé |
|---|---|---|
| **Valeur VE après 5 ans** | **13 500 €** | **45 %** |
| **Valeur thermique après 5 ans** | **9 200 €** | **40 %** |

**Avertissement** dans un encadré orange pâle : « Ces hypothèses sont des moyennes de marché. Selon le modèle, l'écart réel peut être de **± 25 %**. C'est le poste qui peut le plus faire basculer le résultat — à ajuster avec une cote Argus du modèle précis. »

**Phrase d'introduction** : « Toute voiture perd de la valeur. Cette perte fait partie du coût réel. Pour les VE, c'est l'incertitude principale : le marché de l'occasion est jeune et la technologie évolue. »

### Points à valider sur cette étape

- ☐ La **décote VE 45 %** est-elle réaliste pour un marché jeune avec incertitude sur la durée de vie batterie ? *(point critique)*
- ☐ La **décote TH 40 %** est-elle alignée avec la cote Argus moyenne pour un horizon 5 ans ?
- ☐ L'**avertissement ± 25 %** est important — assez visible pour éviter qu'un utilisateur prenne le bilan TCO pour argent comptant ?
- ☐ Faut-il intégrer un **lien direct vers la cote Argus** du modèle saisi pour permettre l'ajustement ?
- ☐ Doit-on adapter la décote en fonction du **kilométrage cumulé** plutôt qu'un % fixe sur le prix neuf ?

---

## 6.9 Bilan ⑤ — Le bilan année après année

![](<images/expert-scenario1 - bilan tco.png>){width=14cm}

**Présentation** : graphique linéaire **cumul VE (vert) vs cumul thermique (orange)** sur la durée de détention, axe X = années depuis l'achat, axe Y = coût cumulé en k€.

**Annotations sur le graphique**

- Ligne verticale bleue à l'année du point de bascule, label **« Bascule : an 1.7 »**.
- Points finaux : VE **31 996 €** / TH **35 825 €** (somme cumulée Acquisition + N×U, **sans soustraction de la valeur résiduelle**).
- Légende : Coût cumulé VE · Coût cumulé thermique · ▼ Point de bascule.

**Texte explicatif sous le graphique** : « Au début, l'électrique part plus cher (le surcoût d'achat est de 2 000 €). Mais l'économie de 1 166 €/an sur l'usage rattrape ce surcoût en **1.7 ans**. Après ce point, chaque année supplémentaire creuse l'écart. »

**Message conclusif** dans un encadré vert : « **L'électrique est gagnant de 8 129 € sur 5 ans** — Soit 135 €/mois d'économie en moyenne. Coût total VE : **18 496 €** · coût total thermique : **26 625 €**. »

> Le coût total mentionné dans l'encadré final (**18 496 € VE / 26 625 € TH**) intègre la valeur résiduelle (TCO « net »). Le graphique, lui, affiche le cumul des dépenses **hors revente** (31 996 € VE / 35 825 € TH), d'où l'écart visuel. À clarifier dans le wording.

### Points à valider sur cette étape

- ☐ Le **point de bascule (1.7 an)** est calculé sur le surcoût d'achat (2 000 €) ÷ économie usage/an (1 166 €/an). Convention claire pour l'utilisateur ?
- ☐ Le **graphique cumule sans soustraire la revente**, alors que le **message final inclut la revente**. Risque de confusion : faut-il afficher la valeur résiduelle comme un crédit en fin de courbe ?
- ☐ Le **chiffre final 8 129 €** : doit-on aussi le proposer **par mois** (135 €/mois) **et par km** (0,125 €/km parcouru) ?
- ☐ Le **message « creuse l'écart »** après le point de bascule : pédagogiquement clair ?
- ☐ Le graphique ne montre que **2 courbes cumulées** : faut-il une 3e courbe « écart cumulé » pour matérialiser le gain ?

---

# 7. Récapitulatif des hypothèses & constantes

## 7.1 Prix de l'énergie (2026)

| Variable | Valeur | Unité | Source |
|---|---|---|---|
| Électricité — heures creuses (HC) | 0,18 | €/kWh | tarif réglementé EDF 2026 |
| Électricité — heures pleines (HP) | 0,24 | €/kWh | tarif réglementé EDF 2026 |
| Électricité — borne rapide (DC) | 0,60 | €/kWh | relevés Chargemap / Fastned / Ionity |
| Essence (SP95) | 1,75 | €/L | tarif station moyen 2026 |
| Diesel | 1,65 | €/L | tarif station moyen 2026 |

## 7.2 Performance énergétique

| Variable | Valeur | Unité | Source |
|---|---|---|---|
| Consommation VE défaut | 16 | kWh/100 km | citadine ~14, SUV 18-22 |
| Consommation thermique défaut | 6 | L/100 km | essence citadine moyenne |
| Mix de recharge défaut (expert) | **60 / 30 / 10** | % HC / HP / DC | profil « À domicile, mix standard » |

## 7.3 Coûts d'usage annuels

| Poste | VE | TH | Source |
|---|---|---|---|
| Entretien | 250 €/an | 600 €/an | UFC-Que Choisir, ADEME |
| Assurance | 650 €/an | 600 €/an | hypothèse marché 2026 |

## 7.4 Acquisition & aides

| Variable | Valeur | Unité | Source |
|---|---|---|---|
| Prix VE catalogue défaut | **30 000** | € | citadine européenne 2026 (Renault 5, Peugeot e-208, Citroën ë-C3) |
| Prix TH catalogue défaut | **23 000** | € | essence équivalente (citadine 3-cyl turbo) |
| Plafond éligibilité aide CEE VPE | 47 000 | € | DGEC 2026 |
| Prime CEE VPE (RFR ≤ 16 300 / 16 301-26 300 / > 26 300) | **5 700 / 4 700 / 3 500** | € | DGEC 2026, « coup de pouce VPE » depuis juillet 2025 |
| Surbonus batterie EU | 1 500 ou 2 000 | € | score ADEME (médian 1 500, palier haut 2 000) |
| Borne domicile (installation) | 1 200 | € | marché 2026 |
| Malus CO₂ + poids défaut | 0 | € | dépend du modèle |

## 7.5 Valeur de revente

| Variable | Valeur | Source |
|---|---|---|
| Décote VE — % conservé à 5 ans | 45 % | hypothèse marché jeune |
| Décote TH — % conservé à 5 ans | 40 % | cote Argus indicative |

---

# 8. Sources des données

| Donnée | Source officielle | Année / version | Référence |
|---|---|---|---|
| Prime CEE « Coup de pouce VPE » | DGEC / economie.gouv.fr | 2026 (depuis juillet 2025) | ecologie.gouv.fr |
| Score environnemental batterie | ADEME | 2026 (liste mensuelle) | score-environnemental-bonus.ademe.fr |
| Méthodologie TCO | Automobile-Propre, Freshmile, UFC-Que Choisir, ADEME « Verdir ma flotte » | — | — |
| Prix électricité réglementés | EDF / CRE | 2026 | edf.fr |
| Prix carburants | Pégase (DGEC) | 2026 | developpement-durable.gouv.fr |
| Prix bornes publiques | Chargemap / Fastned / Ionity | 2026 | relevés terrain |
| Décote véhicules | Argus, La Centrale | indicatif | argus.fr |
| Tranches RFR/part | Avis d'imposition / DGFiP | 2026 | impots.gouv.fr |

---

# 9. Limites connues

## 9.1 Hypothèses simplificatrices assumées

- **Prix de l'énergie constants** sur tout l'horizon (pas d'indexation, pas d'inflation).
- **Prime CEE volatile** : dépend du cours des certificats, les montants par défaut sont indicatifs.
- **Consommations forfaits** (16 kWh/100 km, 6 L/100 km) indépendantes du style de conduite, du relief et de la météo.
- **Décote à la revente** modélisée comme un % fixe, indépendant du kilométrage cumulé.
- **Mix de recharge** supposé constant sur l'horizon (pas d'évolution des comportements).
- **Borne domicile** comptée comme un poste unique d'acquisition (pas d'amortissement, pas de prime CEE associée).

## 9.2 Cas non traités

- **Cas n°2** « Revendre mon thermique pour acheter un VE » (à venir).
- **Cas n°3** « Acheter un VE d'occasion » (à venir).
- **Usage pro** : TVS, TAI, avantage en nature, amortissement fiscal — non modélisés.
- **Financement** : crédit, LOA, leasing — coût d'intérêts non inclus.
- **Aides locales** (région, département) non intégrées.
- **Prime à la conversion** (mise au rebut d'un diesel) : intégrée au cas n°1 ? *À clarifier.*
- **Contraintes d'usage** : temps de recharge longs trajets, ZFE, autonomie par grand froid.
- **Coût de remplacement de batterie** à mi-vie : non modélisé.

## 9.3 Points ouverts à arbitrer avec les experts

1. **Cohérence guidé / expert sur le mix de recharge** : le mode guidé propose 4 profils qualitatifs (HC / mix standard / mix dom+publique / publique), le mode expert affiche 60/30/10 par défaut. Préciser le mapping exact.
2. **Décote VE** (inconnue n°1) : le marché VE d'occasion est jeune, la durée de vie batterie reste un sujet → confronter le 45 % par défaut à la cote Argus actualisée 2026.
3. **Borne domicile** dans le coût d'acquisition : à conserver dans le bilan ① « Achat » ou à isoler en poste « infrastructure » ?
4. **Mix de recharge** par défaut : représentatif d'un particulier avec borne, mais à mettre en regard d'un profil sans borne (qui aurait un coût d'énergie nettement supérieur).
5. **Prime CEE VPE** : le montant peut varier en cours d'année ; affiche-t-on un avertissement de date de mise à jour ?
6. **Vignette Crit'Air / ZFE** : faut-il intégrer un coût de non-conformité côté TH dans les zones concernées ?
7. **Graphique bilan ⑤** : valeur résiduelle visible ou intégrée ? Aligner le wording du graphe et le message final.

---

# Annexe — Historique des versions

| Version | Date | Auteur | Modifications |
|---|---|---|---|
| 0.1 | 2026-05-20 | Bertrand Matge | Création — cas n°1 (VE vs Thermique neuf) uniquement |
| 0.2 | 2026-05-20 | Bertrand Matge | Refonte structurelle : alignement strict des captures et des descriptions ; ajout de l'étape 1 « Bienvenue / choix du cas d'usage » manquante ; correction des valeurs par défaut (prix VE 30 000 €, TH 23 000 €, RFR médian 16 301-26 300 € → 4 700 €, mix recharge 60/30/10) ; restructuration du mode expert en 4 zones de paramètres + 5 étapes de bilan |
