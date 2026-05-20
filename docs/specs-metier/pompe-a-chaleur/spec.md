---
title: "Simulateur Pompe à chaleur — Spécification métier"
simulateur: pompe-a-chaleur
version: 0.2
date: 2026-05-20
statut: brouillon — à valider
auteur: Bertrand Matge
destinataires: Anah, DGEC bâtiment, ADEME
---

# 1. Objectif & public visé

**Question à laquelle le simulateur répond :** « Combien me coûterait l'installation d'une pompe à chaleur dans mon logement après aides publiques (MaPrimeRénov' + CEE), et en combien d'années est-ce amorti par rapport à mon chauffage actuel ? »

**Public cible :** propriétaires occupants de maison individuelle, en réflexion sur le remplacement de leur chauffage (fioul, gaz, propane, convecteurs électriques) par une pompe à chaleur.

**Décision aidée :**

- estimer le **reste à charge** après aides cumulées (MPR + CEE + bonus fioul) selon le type de PAC et le profil de revenus ;
- mettre en regard les **économies annuelles** vs le chauffage actuel ;
- visualiser la **durée d'amortissement** sur 15 ans.

**Hors périmètre (v1) :**

- Copropriétés et logements collectifs.
- Locataires (seuls les aides Propriétaire Occupant sont modélisées).
- MaPrimeRénov' Parcours Rénovation Ampleur (anc. Sérénité) — *non géré*.
- ECS solaire / ballon thermodynamique en complément.
- Aides locales (région, département, EPCI).

---

# 2. Scénario par défaut — fil rouge des exemples

Tous les exemples chiffrés de ce document utilisent le **scénario chargé par défaut** au démarrage du simulateur.

| Catégorie | Valeurs par défaut |
|---|---|
| **Logement** | 120 m² chauffés, zone H2 (Ouest / Centre / Sud-Ouest), DPE D-E (isolation moyenne) |
| **Chauffage actuel** | Chaudière gaz |
| **Projet** | PAC air/eau (SCOP 3,8), profil revenus **Intermédiaire** (RFR 40–56 k€) |
| **Facture optionnelle** | Vide (calibrage par défaut sur surface × zone × isolation) |

> Le scénario par défaut donne (cf. §4) : besoin utile **13 200 kWh/an** → coût installation **14 000 €**, aides **7 000 €** (MPR 3 000 + CEE bonifié 4 000), **reste à charge 7 000 €** (50 % du coût), **économies annuelles 1 077 €/an** vs chaudière gaz.

---

# 3. Vue d'ensemble du parcours

L'outil est un **simulateur mono-page** sans wizard : tous les paramètres et tous les résultats sont visibles simultanément, le calcul est instantané à chaque modification.

Structure verticale (de haut en bas) :

1. **Hero** — titre + description + date des données
2. **Section « Formulaire »** — 2 cartes côte à côte : **« Mon logement »** + **« Mon projet »**
3. **Section « Estimation financière »** :
   - **bandeau 4 KPIs** (Coût installation / Aides mobilisables / Reste à charge / Économies annuelles)
   - **Spotlight État** « L'État finance X% de votre projet »
   - **2 cartes côte à côte** : Tableau « Détail du financement » + Graphique « Rentabilité du projet » (courbe d'amortissement 15 ans)
4. **Section « Comparaison avec les autres énergies »** — 2 cartes côte à côte : bar chart facture annuelle + bar chart TCO 15 ans + bloc hypothèses
5. **Footer DSFR**

Les 5 captures disponibles couvrent les zones de formulaire et le bandeau financier (§4). Les graphiques d'amortissement et de comparaison énergies (§5) n'ont **pas de capture en v0.2** — descriptions textuelles, captures à produire.

---

# 4. Détail par zone fonctionnelle (zones avec capture)

## 4.1 Zone — « Mon logement » (+ bloc « Affiner avec ma facture réelle »)

![](<images/pac - mon logement.png>){width=12cm}

**Présentation** : carte DSFR à gauche du formulaire, intitulée « Mon logement » (icône `fr-icon-home-4-line`). La capture montre l'état où le bloc dépliable **« Affiner avec ma facture réelle »** est **ouvert** en pied de carte.

**Champs saisis**

- **Surface chauffée** — slider 40 → 250 m², pas de 5 m². Défaut **120 m²**. Aide : « Pièces de vie effectivement chauffées ».
- **Zone climatique** — select. Défaut **H2 — Ouest, Centre, Sud-Ouest (climat tempéré)**. Aide : « Selon votre département (réglementation thermique) ». Options : H1 (Nord-est, montagne, climat froid) / H2 / H3 (Méditerranée, climat doux).
- **État de l'isolation** — select. Défaut **Isolation moyenne (DPE D-E)**. Aide : « Conditionne fortement la consommation ». Options : Passoire thermique (DPE F-G) / Isolation moyenne (DPE D-E) / Bonne isolation (DPE B-C).
- **Chauffage actuel** — select. Défaut **Chaudière gaz**. Aide : « Énergie principale du logement ». Options : Chaudière fioul / Chaudière gaz / Chaudière propane / GPL / Convecteurs électriques.

**Bloc dépliable « Affiner avec ma facture réelle »** (tag « optionnel »)

Aide générale : « Si renseigné, le simulateur recalibre l'estimation sur votre consommation réelle plutôt que sur la surface et la zone climatique. Indiquez si possible uniquement la part **chauffage** (hors eau chaude / cuisson). »

Deux champs **mutuellement exclusifs** (la saisie d'un vide l'autre) :

- **Montant annuel TTC** — input numérique (€/an), placeholder « ex. 2 100 ».
- **Consommation annuelle** — input numérique avec **unité dynamique** selon l'énergie actuelle :

| Énergie actuelle | Unité affichée | Aide |
|---|---|---|
| Chaudière fioul | L/an | « en litres livrés (1 L ≈ 10 kWh) » |
| Chaudière gaz | kWh/an | « en kWh sur votre facture (ou m³ × 11,2 pour le gaz naturel) » |
| Chaudière propane | kg/an | « en kg livrés (1 kg ≈ 13,8 kWh) » |
| Convecteurs électriques | kWh/an | « en kWh sur votre facture » |

Quand l'override est actif, un badge vert « ✓ Estimation calibrée sur vos données réelles » apparaît, et le sous-texte du KPI Économies devient « vs chauffage actuel · sur facture réelle ».

**Constantes mobilisées**

- **Besoin de chauffage de base** (kWh utiles/m²/an) selon zone : H1 = 130 · H2 = 110 · H3 = 90.
- **Facteur isolation** : Passoire = 1,5 · Moyen = 1,0 · Bon = 0,65.

**Formule — besoin utile (sans facture)**

$$
B_\text{utile} = S \times \text{Besoin}_\text{zone} \times f_\text{isolation}
$$

**Formule — besoin utile (avec facture en montant TTC)**

$$
B_\text{utile} = \frac{M_\text{facture}}{P_\text{énergie}} \times \eta_\text{énergie}
$$

**Formule — besoin utile (avec consommation brute)**

$$
B_\text{utile} = C_\text{brute} \times k_\text{conversion} \times \eta_\text{énergie}
$$

où $k_\text{conversion}$ vaut 10 (fioul L → kWh), 1 (gaz kWh), 13,8 (propane kg → kWh), 1 (élec kWh).

**Exemple — valeurs par défaut**

$B_\text{utile} = 120 \times 110 \times 1{,}0 =$ **13 200 kWh utiles/an**.

### Points à valider sur cette zone

- ☐ Les **besoins de base par zone** (130 / 110 / 90 kWh utiles/m²/an) sont-ils alignés avec la convention ADEME pour un logement DPE D-E ?
- ☐ Les **facteurs d'isolation** (1,5 / 1,0 / 0,65) reflètent-ils les écarts réels observés (DPE F-G vs B-C peut être un x3 — sous-estimé ?) ?
- ☐ L'**input « facture réelle »** : taux d'usage en conditions réelles ? Risque de saisie erronée (l'utilisateur saisit le total TTC incluant ECS et cuisson) ?
- ☐ L'**unité dynamique de la consommation annuelle** (L/an, kWh/an, kg/an) est-elle compréhensible sans aide complémentaire ?
- ☐ L'**énumération de chauffage actuel** est-elle exhaustive ? Manque biomasse, granulés bois, réseau de chaleur ?
- ☐ La **zone climatique** se déduit du département — faut-il poser la question via le département et déduire la zone, plutôt que demander à l'utilisateur de choisir ?
- ☐ Le bloc « facture réelle » est **dépliable** : par défaut ouvert ou fermé ? Quel impact pédagogique ?

---

## 4.2 Zone — « Mon projet »

![](<images/pac - mon projet.png>){width=12cm}

**Présentation** : carte DSFR à droite du formulaire, intitulée « Mon projet » (icône `fr-icon-settings-5-line`). 2 questions empilées.

**4.2.1 Type de pompe à chaleur** — 3 tuiles cliquables (radio exclusif). Aide : « SCOP : coefficient de performance saisonnier ».

| Tuile | SCOP | Coût installation TTC (pose incluse) | État par défaut |
|---|---|---|---|
| **Air / eau** | 3,8 | 14 000 € | **sélectionnée** |
| Géothermique | 4,5 | 28 000 € | — |
| Air / air | 3,5 | 9 000 € | — |

> ⚠️ Lorsque l'utilisateur sélectionne **Air / air**, une alerte DSFR `fr-icon-warning-line` apparaît juste en dessous des tuiles : « La PAC air/air n'est pas éligible à MaPrimeRénov' 2026 (parcours par geste). »

**4.2.2 Profil de revenus** — 4 tuiles cliquables (radio exclusif). Aide : « Plafonds ANAH 2026, revenu fiscal de référence (couple Île-de-France, indicatif) ».

| Tuile | Tranche RFR couple IDF | Code interne | État par défaut |
|---|---|---|---|
| Très modeste | < 33 k€ | `bleu` | — |
| Modeste | 33 – 40 k€ | `jaune` | — |
| **Intermédiaire** | 40 – 56 k€ | `violet` | **sélectionnée** |
| Supérieur | > 56 k€ | `rose` | — |

### Points à valider sur cette zone

- ☐ Les **SCOP par défaut** (3,8 / 4,5 / 3,5) sont-ils représentatifs du parc 2026 ? Faut-il les moduler selon la zone climatique (un SCOP air/eau à H1 sera plus bas) ?
- ☐ Les **coûts d'installation médians** (14 000 / 28 000 / 9 000 € TTC pose incluse) sont-ils à jour 2026 (FNCH, AFPAC, Observ'ER) ?
- ☐ Les **plafonds RFR par profil** sont calés sur un **couple Île-de-France** comme proxy pédagogique. Faut-il afficher les vraies tranches Anah par taille de ménage et zone (A/B/C) ?
- ☐ La **PAC air/air** est correctement exclue de MPR — mais elle reste éligible aux CEE standard. À renforcer dans le wording de l'alerte ?
- ☐ L'alerte « non éligible MPR » est-elle assez visible (placée juste sous les tuiles, mais peut être ignorée si l'utilisateur scrolle vite) ?

---

## 4.3 Zone — Bandeau « Estimation financière » (4 KPIs)

![](<images/pac - estimation.png>){width=14cm}

**Présentation** : bandeau de 4 KPIs côte à côte, fond gris clair, **bordure latérale colorée** (DSFR `border-left`) par KPI. Titre de section « Estimation financière » avec soulignement bleu.

| KPI | Valeur affichée (défaut) | Calcul | Sous-texte | Bordure |
|---|---|---|---|---|
| **Coût installation** | **14 000 €** | `COUT_PAC[type]` (constante) | « TTC, pose et matériel » | Grise |
| **Aides mobilisables** | **7 000 €** (bleu) | `MPR + CEE + bonusFioul` plafonné à 90 % du coût | Liste détaillée : MPR 3 000 € + CEE 4 000 €. Sous-texte : « MaPrimeRénov' + CEE bonifié » | Bleu DSFR |
| **Reste à charge** | **7 000 €** | `coutInstall − totalAides` (≥ 0) | « soit 50 % du coût » | Grise |
| **Économies annuelles** | **1 077 €** (vert) | `coutActuel − coutPAC` | « vs chauffage actuel » | Verte (ou rouge si négatif → surcoût annuel) |

**Détail injecté dans le KPI Aides** (liste `<ul class="kpi-aides-break">`)

Sous le montant 7 000 €, le simulateur liste les 1 à 3 aides actives **avec leur montant** :

```
MPR        3 000 €
CEE        4 000 €
[Cuve fioul   X €]   (uniquement si chauffage actuel = fioul ET PAC ≠ air/air)
```

Le sous-texte du KPI s'adapte :

- Si PAC = air/air : « CEE uniquement (MPR exclue) »
- Si éligible Coup de pouce (gaz / fioul / propane → PAC air/eau ou géo) : « MaPrimeRénov' + CEE bonifié » ← **scénario par défaut**
- Sinon : « MaPrimeRénov' + CEE »

**Formules — totaux**

$$
A_\text{total} = \min\left(\text{MPR} + \text{CEE} + \text{Bonus}_\text{fioul},\ 0{,}90 \times C_\text{install}\right)
$$

$$
R_\text{reste} = \max(0,\ C_\text{install} - A_\text{total})
\qquad
E_\text{annuelles} = C_\text{actuel} - C_\text{PAC}
$$

avec :

$$
C_\text{actuel} = \frac{B_\text{utile}}{\eta_\text{énergie}} \times P_\text{énergie}
\qquad
C_\text{PAC} = \frac{B_\text{utile}}{\text{SCOP}_\text{PAC}} \times P_\text{élec}
$$

**Exemple — valeurs par défaut (PAC air/eau, profil violet, chauffage gaz, 120 m² H2 D-E)**

- $C_\text{install}$ = 14 000 € (constante air/eau)
- MPR (air/eau, violet) = **3 000 €**
- CEE bonifié (remplacement gaz → PAC air/eau, violet) = **4 000 €**
- Bonus dépose cuve fioul = 0 (chauffage actuel = gaz)
- $A_\text{total}$ = 3 000 + 4 000 = **7 000 €** (plafond 90 % × 14 000 = 12 600 €, OK)
- $R_\text{reste}$ = 14 000 − 7 000 = **7 000 €** (50 % du coût)
- $C_\text{actuel}$ (gaz) = 13 200 / 0,95 × 0,126 ≈ **1 751 €/an**
- $C_\text{PAC}$ (air/eau SCOP 3,8) = 13 200 / 3,8 × 0,194 ≈ **674 €/an**
- $E_\text{annuelles}$ ≈ 1 751 − 674 ≈ **1 077 €/an** ✓ *(valeur affichée sur la capture)*

### Points à valider sur cette zone

- ☐ L'**ordre des 4 KPIs** (Coût → Aides → Reste → Économies) suit le fil narratif « combien je paie / combien l'État aide / combien il me reste / combien j'économise » — validé ?
- ☐ Le **plafond de cumul à 90 % du coût installation** correspond-il bien à la « pince 100 % du coût TTC » réglementaire ? Pour les très modestes, la règle est plutôt « reste à charge ≥ 10 % » — formellement identique mais à expliciter.
- ☐ Le **forfait CEE bonifié** est-il bien conditionné à « remplacement de chaudière **fossile** » (fioul / gaz / propane) ? Cas convecteurs électriques → CEE standard uniquement, est-ce correct ?
- ☐ La **liste détaillée des aides** dans le KPI Aides (MPR / CEE / Cuve fioul) : utile pour la transparence, ou redondante avec le tableau 4.5 ?
- ☐ Le **% « soit 50 % du coût »** dans le KPI Reste à charge : calcul `resteAcharge / coutInstall`. Faut-il plutôt afficher le complément (« 50 % financé par l'État ») ?
- ☐ Le **KPI Économies annuelles passe en rouge** si le PAC coûte plus cher en énergie que le chauffage actuel (cas convecteurs élec → PAC avec mauvais SCOP). Le message « surcoût annuel » est-il assez explicite ?

---

## 4.4 Zone — Spotlight État « L'État finance X% de votre projet »

![](<images/pac - aides.png>){width=14cm}

**Présentation** : encadré dédié situé **sous le bandeau des 4 KPIs**, structuré comme un « argument État ». Bande tricolore (bleu / blanc / rouge) en haut, fond bleu pâle DSFR (`--background-contrast-blue-france`).

**Structure verticale** :

1. **Eyebrow** (en majuscules bleu DSFR) : « République Française · Plan d'électrification 2026 »
2. **Titre principal** : « L'État finance **50%** de votre projet » (pourcentage en gros, gras, bleu DSFR — adapté dynamiquement)
3. **Sous-titre récapitulatif** : « Sur un investissement de **14 000 €**, vous mobilisez **7 000 €** d'aides publiques cumulables. Votre reste à charge tombe à **7 000 €**. »
4. **Liste des aides actives** — pour chaque aide mobilisée, une carte blanche avec bordure bleue :

| Aide | Montant | Source | Description courte |
|---|---|---|---|
| MaPrimeRénov' | 3 000 € | Agence nationale de l'habitat (Anah) | Aide principale de l'État à la rénovation énergétique. Le barème est modulé selon les revenus pour soutenir prioritairement les ménages modestes — fléchage renforcé vers l'électrification depuis le 1er septembre 2026 (Mesure 6 du Plan). |
| Coup de pouce Chauffage | 4 000 € | CEE bonifié — sortie fioul / gaz / propane | Bonification du dispositif CEE pour le remplacement d'une chaudière fossile par une PAC. Financé par les fournisseurs d'énergie sous régulation DGEC. |
| *(Bonus dépose cuve fioul)* | *(montant)* | *(Soutien spécifique sortie du fioul)* | *(affiché uniquement si chauffage actuel = fioul ET PAC ≠ air/air)* |

5. **Contexte** (encadré blanc à bordure bleue) : « Ces aides s'inscrivent dans le Plan d'électrification annoncé en avril 2026, qui vise **1 million de pompes à chaleur installées en 2030** pour réduire la dépendance de la France aux énergies fossiles importées. »
6. **CTA** (liens) : France Rénov' · Mes Aides Réno (simulateur officiel) · Plan d'électrification — suivi des 22 mesures.

**Calcul du % affiché**

$$
\%_\text{financé} = \frac{A_\text{total}}{C_\text{install}} \times 100
$$

Pour le scénario par défaut : 7 000 / 14 000 = **50 %** ✓ *(valeur affichée sur la capture)*.

**Cas dégénéré — aucune aide mobilisable**

Si $A_\text{total} = 0$ (ex. PAC air/air avec profil intermédiaire), la classe CSS `aide-spotlight--none` est ajoutée : la liste des aides et le % sont masqués, le titre devient « Pour ce profil, peu d'aides directes sont mobilisables » et le sous-titre adapté (PAC air/air → rappel exclusion MPR + suggestion CEE / Ampleur).

### Points à valider sur cette zone

- ☐ Le **wording « L'État finance X% de votre projet »** est-il politiquement validé ?
- ☐ Le dénominateur (`coutInstall`) est-il le bon, ou faut-il prendre le **surcoût** vs un changement à l'identique (chaudière gaz THPE) pour rester comparable à d'autres cas (passer-a-electrique, poids-lourd) ?
- ☐ La **liste des aides présentées** se limite aux 3 aides nationales (MPR, CEE, Bonus fioul). Manque l'éco-PTZ (prêt à taux zéro), la TVA 5,5 %, les aides Action Logement, les aides locales — à intégrer ?
- ☐ Le **lien CTA « Plan d'électrification — suivi des 22 mesures »** crée une boucle cohérente entre les 8 pages du portail — validé ?
- ☐ Le **rappel du contexte 1 M de PAC en 2030** est-il une formulation officielle (DGEC, dossier de presse avril 2026) ?
- ☐ Le **cas dégénéré « aucune aide »** doit-il rester aussi visible (pour assumer la transparence) ou pourrait-il être masqué pour éviter un effet décourageant ?

---

## 4.5 Zone — « Détail du financement » (tableau ligne à ligne)

![](<images/pac - detail.png>){width=12cm}

**Présentation** : carte blanche située à gauche **sous le spotlight État** (en parallèle de la carte « Rentabilité du projet »). Titre « Détail du financement », sous-titre « Décomposition du coût et des aides ».

**Contenu — tableau ligne à ligne** (dans le scénario par défaut)

| Ligne | Détail / sous-libellé | Montant | Style |
|---|---|---|---|
| Coût installation | TTC, pose comprise | **14 000 €** | — |
| MaPrimeRénov' | Profil violet *(ou « Non éligible » pour air/air)* | **−3 000 €** | bleu (négatif) |
| Prime CEE | badge bleu « Coup de pouce bonifié » *(ou « CEE standard »)* | **−4 000 €** | bleu (négatif) |
| Bonus dépose cuve fioul *(conditionnel)* | *(affiché uniquement si chauffage actuel = fioul ET PAC ≠ air/air)* | *(−montant)* | bleu (négatif) |
| **Reste à votre charge** | — | **7 000 €** | gras |

Le badge bleu « Coup de pouce bonifié » s'affiche **sur la ligne CEE** quand le scénario remplit la condition d'éligibilité (chauffage actuel = fioul / gaz / propane ET PAC = air/eau ou géo). Sinon, sous-libellé « CEE standard » en texte simple.

### Points à valider sur cette zone

- ☐ L'**ordre des aides** (MPR puis CEE puis Bonus) correspond-il à l'ordre administratif réel (qui se demande en premier) ?
- ☐ Faut-il afficher les **dates de validité des barèmes** ligne par ligne (ex. « MPR — barème en vigueur depuis le 1er sept 2026 ») ?
- ☐ Le badge **« Coup de pouce bonifié »** est-il assez visible pour justifier le doublement du forfait CEE ?
- ☐ Faut-il ajouter une ligne explicite **« Plafond cumul aides (90 %) »** quand celui-ci est atteint, plutôt que de seulement plafonner silencieusement le total ?
- ☐ Le tableau ne contient pas la **TVA 5,5 %** (déjà incluse dans le coût TTC) — à mentionner en pied pour éviter une question de l'utilisateur ?

---

# 5. Sections sans capture en v0.2 (à compléter)

Les deux sous-sections suivantes existent dans le simulateur mais **aucune capture n'a été déposée pour elles en v0.2**. Les descriptions ci-dessous sont basées sur le code source ; les captures seront à produire pour la v0.3.

## 5.1 Carte « Rentabilité du projet » (courbe d'amortissement 15 ans)

*Capture à fournir — actuellement non présente dans `images/`.*

**Présentation** : carte blanche située à droite **sous le spotlight État** (en parallèle du tableau « Détail du financement »). Titre « Rentabilité du projet », sous-titre dynamique « Point d'équilibre : **<X>** » (ex. « année 8,5 », « au-delà de 15 ans », « jamais rentabilisé (surcoût) »).

**Contenu — courbe linéaire Chart.js** sur **15 ans** :

- Axe X : An 0 → An 15
- Axe Y : cumul net en k€
- An 0 : `−resteAcharge` (l'utilisateur a payé)
- An *n+1* : cumul précédent + `economiesAn × (1 + 0,03)^n` (inflation énergie 3 %/an)
- Couleur de la courbe : bleu DSFR (`#000091`), remplissage léger, ligne de zéro renforcée en gris foncé

**Point d'équilibre** : interpolé linéairement à la première année où la courbe franchit zéro, affiché en sous-titre du graphique.

**Exemple — valeurs par défaut** (économies 1 077 €/an, reste à charge 7 000 €, inflation 3 %/an)

- An 0 : −7 000 €
- An 1 : −7 000 + 1 077 = −5 923 €
- An 2 : −5 923 + 1 077 × 1,03 = −4 814 €
- … point d'équilibre vers **année 5,9** (environ 5 ans et 11 mois).

### Points à valider sur cette zone

- ☐ **Fournir la capture** `pac - rentabilite.png` (ou similaire) pour la v0.3.
- ☐ L'**horizon 15 ans** correspond-il à la durée de vie moyenne d'une PAC ? Faut-il prévoir une provision remplacement compresseur à mi-vie ?
- ☐ L'**inflation énergie +3 %/an** est-elle conservatrice ? Faut-il distinguer inflation élec vs inflation gaz / fioul (corrélation politique et géopolitique différente) ?
- ☐ Le **point d'équilibre** ignore l'entretien annuel obligatoire (~200 €/an). À intégrer ?
- ☐ Affichage « jamais rentabilisé » si économies < 0 : message d'alerte plus visible (passoire thermique + PAC seule = mauvaise idée) ?

---

## 5.2 Section « Comparaison avec les autres énergies » (2 bar charts)

*Captures à fournir — actuellement non présentes dans `images/`.*

**Présentation** : section dédiée plus bas dans la page, titre « Comparaison avec les autres énergies » (soulignement bleu DSFR). 2 cartes côte à côte.

**5.2.1 Bar chart « Facture annuelle de chauffage »**

Sous-titre : « Coût en €/an pour le même besoin de chaleur »

5 barres : Fioul · Gaz · Propane · Élec. direct · PAC (type sélectionné).

- 4 barres grises (les autres énergies) + 1 verte (PAC, accent transition).
- L'**énergie actuelle** de l'utilisateur est mise en **orange** (`#CE614A`) pour rendre la comparaison saillante.

**5.2.2 Bar chart « Coût total sur 15 ans »**

Sous-titre : « Installation + énergie cumulée, inflation énergie 3 %/an »

TCO sur 15 ans pour chaque énergie : `coutInstall_énergie + Σ_15ans (coutAnnuel × (1,03)^n)`.

Coûts d'installation hypothétiques pour les autres énergies (remplacement chaudière) :

| Énergie | Coût install hypothétique |
|---|---|
| Fioul | 8 000 € |
| Gaz | 5 000 € |
| Propane | 7 000 € |
| Élec direct | 2 000 € |
| PAC (sélectionnée) | reste à charge utilisateur |

**5.2.3 Bloc « Hypothèses de calcul »**

Encadré gris en pied de section rappelant les hypothèses :

- Besoin de chauffage : 90 / 110 / 130 kWh utiles/m²/an en zones H3 / H2 / H1 (DPE D-E), ajusté selon isolation.
- Prix TTC mai 2026 : élec 0,194 €/kWh · gaz 0,126 €/kWh · fioul 0,11 €/kWh · propane 0,16 €/kWh.
- Rendements : fioul 80 % · gaz à condensation 95 % · propane 90 % · élec direct 100 %.
- SCOP : air/eau 3,8 · géo 4,5 · air/air 3,5.
- Coûts médians installation : PAC air/eau 14 000 € · géo 28 000 € · air/air 9 000 € (TVA 5,5 %, pose incluse).
- MaPrimeRénov' parcours par geste 2026, plafonds travaux 12 000 € (air/eau) et 20 000 € (géo).
- CEE Coup de pouce Chauffage bonifié si remplacement chaudière fioul / gaz / propane (hors PAC air/air).
- Inflation prix énergie : 3 %/an. Entretien annuel non intégré.

**Sources** mentionnées en pied : Anah (MPR), CRE, ADEME, arrêté du 20 mai 2022 modifié (CEE Coup de pouce Chauffage), loi de finances 2026.

### Points à valider sur cette zone

- ☐ **Fournir 2 captures** (1 par bar chart) pour la v0.3.
- ☐ Les **coûts d'installation hypothétiques** des autres énergies (8 000 / 5 000 / 7 000 / 2 000 €) sont-ils défendables comme « remplacement à l'identique » ?
- ☐ La **mise en avant orange de l'énergie actuelle** dans le bar chart : pertinente pédagogiquement ?
- ☐ Le **TCO 15 ans** intègre l'inflation énergie mais pas l'entretien annuel ni le remplacement de matériel à mi-vie — à signaler ?
- ☐ Le bloc « Hypothèses » en pied est-il assez visible, ou risque-t-il d'être ignoré ?

---

# 6. Récapitulatif des hypothèses & constantes

## 6.1 Prix de l'énergie (mai 2026, TTC)

| Énergie | Prix | Unité | Source |
|---|---|---|---|
| Fioul | 0,11 | €/kWh | CGDD hebdo |
| Gaz naturel (B1 / B2i) | 0,126 | €/kWh | CRE |
| Propane / GPL | 0,16 | €/kWh | indice professionnel |
| Électricité (tarif bleu base) | 0,194 | €/kWh | CRE / EDF 2026 |

## 6.2 Rendements et performances

| Équipement | Rendement / SCOP |
|---|---|
| Chaudière fioul (ancienne) | 80 % |
| Chaudière gaz à condensation | 95 % |
| Chaudière propane | 90 % |
| Convecteurs électriques | 100 % |
| PAC air / eau | SCOP **3,8** |
| PAC géothermique | SCOP **4,5** |
| PAC air / air | SCOP **3,5** |

## 6.3 Besoin de chauffage (par défaut, DPE D-E)

| Zone | kWh utiles/m²/an |
|---|---|
| H1 (Nord-est, froid) | 130 |
| H2 (Ouest/Centre/SO, tempéré) | 110 |
| H3 (Méditerranée, doux) | 90 |

Multiplié par le facteur isolation : **passoire 1,5** / **moyen 1,0** / **bon 0,65**.

## 6.4 Coûts d'installation médians TTC (pose incluse)

| Type de PAC | Coût |
|---|---|
| Air / eau | 14 000 € |
| Géothermique | 28 000 € |
| Air / air | 9 000 € |

## 6.5 Barèmes des aides 2026

**MaPrimeRénov' parcours par geste**

| PAC | Bleu | Jaune | Violet | Rose |
|---|---|---|---|---|
| Air/eau | 5 000 € | 4 000 € | **3 000 €** | 0 € |
| Géothermique | 11 000 € | 9 000 € | 6 000 € | 0 € |
| Air/air | 0 € | 0 € | 0 € | 0 € |

**Plafonds dépense éligible MPR** : 12 000 € (air/eau), 20 000 € (géo), 0 (air/air).

**CEE Coup de pouce Chauffage (bonifié — remplacement fioul / gaz / propane par PAC air/eau ou géo)**

| Profil | Bleu | Jaune | Violet | Rose |
|---|---|---|---|---|
| Montant | 5 000 € | 5 000 € | **4 000 €** | 2 500 € |

**CEE standard** (autres cas, dont PAC air/air)

| Profil | Bleu | Jaune | Violet | Rose |
|---|---|---|---|---|
| Montant | 1 000 € | 1 000 € | 800 € | 500 € |

**Bonus dépose cuve à fioul** (uniquement si chauffage actuel = fioul ET PAC ≠ air/air)

| Profil | Bleu | Jaune | Violet | Rose |
|---|---|---|---|---|
| Montant | 1 200 € | 800 € | 400 € | 0 € |

**Plafond cumul** : `totalAides ≤ 0,90 × coutInstall` (garde-fou règle des 10 % de reste à charge minimum).

## 6.6 Paramètres techniques

| Paramètre | Valeur |
|---|---|
| Horizon courbe d'amortissement | 15 ans |
| Inflation énergie | 3 % / an |
| Conversion fioul L → kWh | × 10 |
| Conversion propane kg → kWh | × 13,8 |
| Conversion gaz m³ → kWh (info utilisateur) | × 11,2 |

---

# 7. Sources des données

| Donnée | Source officielle | Année / version | Référence |
|---|---|---|---|
| Barème MaPrimeRénov' 2026 | Agence nationale de l'habitat (Anah) | 2026 | `maprimerenov.gouv.fr` |
| Forfaits CEE Coup de pouce Chauffage (BAR-TH-171, BAR-TH-172) | DGEC, registre EMMY | 2026 | `pncee.developpement-durable.gouv.fr` |
| Plafonds RFR par profil | Anah / loi de finances 2026 | 2026 | `anah.fr` |
| Tarifs réglementés électricité | CRE / EDF | mai 2026 | `cre.fr` |
| Prix moyen gaz naturel ménages | CRE | mai 2026 | `cre.fr` |
| Prix moyen fioul domestique | CGDD (hebdo) | mai 2026 | `statistiques.developpement-durable.gouv.fr` |
| Coûts médians installation PAC | ADEME, AFPAC, Observ'ER, FNCH | 2024–2025 | `ademe.fr` |
| SCOP saisonnier | NF EN 14825, NF Pompe à chaleur | continu | `afnor.org` |

---

# 8. Limites connues

## 8.1 Hypothèses simplificatrices assumées

- **Logement = maison individuelle propriétaire occupant.** Les locataires et copropriétés ne sont pas modélisés.
- **Prix énergie constants + inflation 3 %/an** sur tout l'horizon (pas de courbes différenciées par énergie).
- **SCOP figés** (3,8 / 4,5 / 3,5) — indépendants de la zone climatique et de la température de départ d'eau réelle.
- **Coût d'installation médian** indépendant de la puissance précise dimensionnée et de la complexité du chantier (rénovation lourde vs remplacement simple).
- **Entretien annuel obligatoire (~200 €/an)** non intégré dans la rentabilité.
- **MaPrimeRénov' Parcours Rénovation Ampleur** (anc. Sérénité) non pris en compte — uniquement le parcours par geste.

## 8.2 Cas non traités (v1)

- Copropriétés, logements collectifs.
- Locataires (MPR Locataire).
- Bonifications « rénovation globale » (MPR Ampleur).
- ECS solaire / ballon thermodynamique en complément.
- Aides locales (région, département, EPCI).
- Offres partenaires (EDF Pulse Habitat, Engie, etc.) — *en attente du modèle de données `partner-offers.json`*.

## 8.3 Points ouverts à arbitrer avec les experts

1. **Passoires thermiques (DPE F-G)** : PAC seule sans isolation préalable = inefficace. Bloquer ou alerter ? *(open dans la modale business)*
2. **RGE obligatoire** pour bénéficier des aides : à afficher comme prérequis ?
3. **Bruit PAC extérieur** : info à mentionner pour les acheteurs en pavillonnaire dense ?
4. **Coupures hivernales H1** : impact sur les économies réelles à intégrer ?
5. **Provision remplacement compresseur** à mi-vie : à inclure ?
6. **Captures manquantes en v0.2** : compléter avec une capture pour la courbe d'amortissement (§5.1) et une (ou deux) pour la comparaison énergies (§5.2).

---

# Annexe — Historique des versions

| Version | Date | Auteur | Modifications |
|---|---|---|---|
| 0.1 | 2026-05-20 | Bertrand Matge | Création initiale (5 zones logiques, mais captures mélangées dans la version) |
| 0.2 | 2026-05-20 | Bertrand Matge | Refonte structurelle : alignement strict des 5 captures et des descriptions. Section 4 redécoupée en 5 sous-sections (logement / projet / KPIs / spotlight État / détail financement), une capture par sous-section. La courbe d'amortissement et les 2 bar charts comparaison énergies sont déplacés en §5 « Sections sans capture en v0.2 ». Correction de la valeur économies annuelles (1 077 € observé en capture vs 1 076 € calculé) |
