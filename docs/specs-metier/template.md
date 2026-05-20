---
title: "Simulateur « TITRE » — Spécification métier"
simulateur: slug-du-simulateur
version: 0.1
date: AAAA-MM-JJ
statut: brouillon
auteur: Bertrand Matge
destinataires: à définir
---

> **Comment utiliser ce template**
>
> - Recopier ce fichier dans `<slug-du-simulateur>/spec.md`.
> - Créer `<slug-du-simulateur>/images/` et y déposer une capture par étape ou zone fonctionnelle.
> - Nomenclature suggérée : `mode guide - etape<N> - <slug>.png`, `mode expert - <zone>.png`. Les espaces dans les noms de fichier sont OK (les balises image utilisent `<...>`).
> - Format adopté : **séquentiel** — capture puis texte en dessous. Les grid tables pandoc → docx étant fragiles, on évite le 2 colonnes côte-à-côte.
> - Régénérer le `.docx` avec `./build.sh`. Le `reference.docx` à la racine applique automatiquement les styles utilisateur (polices, couleurs, numérotation auto des titres). Ne pas utiliser `--number-sections` dans build.sh.

# 1. Objectif & public visé

**Question à laquelle le simulateur répond :** _(1 phrase)_

**Public cible :** _(qui utilise l'outil)_

**Décision aidée :** _(quelle décision l'outil aide à prendre)_

**Hors périmètre :** _(ce que l'outil ne fait pas)_

---

# 2. Scénario par défaut — fil rouge des exemples

Tous les exemples chiffrés de ce document utilisent le **scénario chargé par défaut** au démarrage du simulateur.

| Catégorie | Valeurs par défaut |
|---|---|
| **_(catégorie 1)_** | _(valeurs)_ |
| **_(catégorie 2)_** | _(valeurs)_ |

> _(éventuelle précision sur la différence mode guidé / mode expert quant aux valeurs par défaut)_

---

# 3. Vue d'ensemble du parcours

_(1 paragraphe décrivant le flux global : nombre d'étapes, modes, etc.)_

## 3.1 Point d'entrée

![](<images/00-vue-ensemble.png>){width=10cm}

_(description courte du point d'entrée)_

### Points à valider sur ce point d'entrée

- ☐ _(question)_

---

# 4. Détail étape par étape

## 4.1 Étape 1 — _(nom)_

![](<images/01-etape-...png>){width=10cm}

**Champs saisis**

- _(champ 1)_ — _(type, unité, bornes éventuelles)_
- _(champ 2)_ — _(...)_

**Constantes mobilisées**

- _(variable)_ : _(valeur)_ _(unité)_ — _(source)_

**Formule — _(libellé métier)_**

$$\text{Sortie} = \ldots$$

**Exemple — valeurs par défaut**

_(calcul chiffré aboutissant à une valeur en gras)_

### Points à valider sur cette étape

- ☐ _(question précise posée à l'expert)_
- ☐ _(question précise posée à l'expert)_

---

## 4.2 Étape 2 — _(nom)_

_(répéter le pattern ci-dessus)_

---

# 5. _(facultatif)_ Mode expert — détail par zone fonctionnelle

À utiliser uniquement si le simulateur propose un mode expert distinct du mode guidé.

## 5.1 Vue complète

![](<images/mode-expert-complet.png>){width=14cm}

_(courte légende)_

### Points à valider sur la vue complète

- ☐ _(question)_

## 5.2 Zone — _(nom)_

![](<images/mode-expert-...png>){width=10cm}

_(description courte)_

**Valeurs par défaut**

_(valeurs initiales du simulateur dans cette zone)_

**Exemple — chiffré**

_(calcul aboutissant à une valeur en gras)_

### Points à valider sur cette zone

- ☐ _(question)_

---

# 6. Récapitulatif des hypothèses & constantes (toutes étapes)

Tableau consolidé pour relecture transversale.

## 6.1 _(catégorie 1, ex. Prix de l'énergie)_

| Variable | Valeur | Unité | Source |
|---|---|---|---|

## 6.2 _(catégorie 2, ex. Performance énergétique)_

| Variable | Valeur | Unité | Source |
|---|---|---|---|

## 6.3 _(catégorie 3, ex. Coûts des projets)_

| Projet | Coût TTC moyen |
|---|---|

## 6.4 _(catégorie 4, ex. Barèmes des aides)_

| Aide | Montant | Condition |
|---|---|---|

---

# 7. Sources des données

| Donnée | Source officielle | Année / version |
|---|---|---|

---

# 8. Limites connues

## 8.1 Hypothèses simplificatrices assumées

- _(liste)_

## 8.2 Cas non traités

- _(liste)_

---

# Annexe — Historique des versions

| Version | Date | Auteur | Modifications |
|---|---|---|---|
| 0.1 | AAAA-MM-JJ | | Création |
