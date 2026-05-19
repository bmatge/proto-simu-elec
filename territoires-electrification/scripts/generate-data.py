#!/usr/bin/env python3
"""
Générateur de données factices pour les 100 territoires d'électrification (Mesure 1
du Plan d'électrification, avril 2026).

Produit data/territoires.json — consommé par <dsfr-data-source> comme s'il s'agissait
d'un endpoint API.

Quand la DGEC publiera la vraie liste (été 2026), remplacer le contenu du JSON :
le pipeline dsfr-data n'a aucune raison de changer.
"""
import json
import random
from pathlib import Path

random.seed(42)  # reproductible

# ============================================================
# Référentiel : 100 places réparties par région (poids ~ population)
# Coordonnées approchées des chefs-lieux / centroïdes EPCI.
# ============================================================

# Format : (slug_de_région, nom, type, lat, lon, dep_name, dep_code, pop_estim)
PLACES = [
    # ===== Île-de-France (18) =====
    ("Île-de-France", "Métropole du Grand Paris",                "métropole", 48.8566,  2.3522, "Paris",            "75", 7100000),
    ("Île-de-France", "EPT Plaine Commune",                      "EPCI",      48.9355,  2.3580, "Seine-Saint-Denis","93",  430000),
    ("Île-de-France", "EPT Est Ensemble",                        "EPCI",      48.8819,  2.4520, "Seine-Saint-Denis","93",  423000),
    ("Île-de-France", "CA Versailles Grand Parc",                "EPCI",      48.8014,  2.1301, "Yvelines",         "78",  267000),
    ("Île-de-France", "CA Cergy-Pontoise",                       "EPCI",      49.0480,  2.0784, "Val-d'Oise",       "95",  208000),
    ("Île-de-France", "CA Saint-Quentin-en-Yvelines",            "EPCI",      48.7800,  1.9700, "Yvelines",         "78",  227000),
    ("Île-de-France", "CA Plaine Vallée",                        "EPCI",      49.0250,  2.3000, "Val-d'Oise",       "95",  182000),
    ("Île-de-France", "CA Roissy Pays de France",                "EPCI",      49.0100,  2.5650, "Val-d'Oise",       "95",  351000),
    ("Île-de-France", "CA Grand Paris Sud",                      "EPCI",      48.6000,  2.4500, "Essonne",          "91",  354000),
    ("Île-de-France", "CA Marne et Gondoire",                    "EPCI",      48.8800,  2.7800, "Seine-et-Marne",   "77",  113000),
    ("Île-de-France", "Ville de Meaux",                          "commune",   48.9603,  2.8783, "Seine-et-Marne",   "77",   54000),
    ("Île-de-France", "Ville d'Évry-Courcouronnes",              "commune",   48.6293,  2.4416, "Essonne",          "91",   67000),
    ("Île-de-France", "Ville de Mantes-la-Jolie",                "commune",   48.9900,  1.7167, "Yvelines",         "78",   45000),
    ("Île-de-France", "Ville de Melun",                          "commune",   48.5400,  2.6600, "Seine-et-Marne",   "77",   41000),
    ("Île-de-France", "Ville de Trappes",                        "commune",   48.7755,  1.9919, "Yvelines",         "78",   32000),
    ("Île-de-France", "CC du Pays Houdanais",                    "EPCI",      48.7900,  1.6000, "Yvelines",         "78",   29000),
    ("Île-de-France", "CC Pays de l'Ourcq",                      "EPCI",      49.0500,  3.0500, "Seine-et-Marne",   "77",   18000),
    ("Île-de-France", "Département de l'Essonne",                "département",48.5900, 2.3800, "Essonne",          "91", 1300000),

    # ===== Auvergne-Rhône-Alpes (11) =====
    ("Auvergne-Rhône-Alpes", "Métropole de Lyon",                "métropole", 45.7640, 4.8357, "Rhône",            "69", 1411000),
    ("Auvergne-Rhône-Alpes", "Grenoble-Alpes Métropole",         "métropole", 45.1885, 5.7245, "Isère",            "38",  445000),
    ("Auvergne-Rhône-Alpes", "Saint-Étienne Métropole",          "métropole", 45.4397, 4.3872, "Loire",            "42",  408000),
    ("Auvergne-Rhône-Alpes", "Clermont Auvergne Métropole",      "métropole", 45.7772, 3.0870, "Puy-de-Dôme",      "63",  292000),
    ("Auvergne-Rhône-Alpes", "Grand Annecy",                     "EPCI",      45.8992, 6.1294, "Haute-Savoie",     "74",  213000),
    ("Auvergne-Rhône-Alpes", "Grand Chambéry",                   "EPCI",      45.5646, 5.9178, "Savoie",           "73",  138000),
    ("Auvergne-Rhône-Alpes", "Valence Romans Agglo",             "EPCI",      44.9333, 4.8917, "Drôme",            "26",  220000),
    ("Auvergne-Rhône-Alpes", "CA du Pays Voironnais",            "EPCI",      45.3653, 5.5814, "Isère",            "38",   95000),
    ("Auvergne-Rhône-Alpes", "Ville d'Aurillac",                 "commune",   44.9258, 2.4458, "Cantal",           "15",   25000),
    ("Auvergne-Rhône-Alpes", "Ville du Puy-en-Velay",            "commune",   45.0431, 3.8854, "Haute-Loire",      "43",   18000),
    ("Auvergne-Rhône-Alpes", "CC du Diois",                      "EPCI",      44.7500, 5.3700, "Drôme",            "26",   12000),

    # ===== Hauts-de-France (9) =====
    ("Hauts-de-France", "Métropole Européenne de Lille",         "métropole", 50.6292, 3.0573, "Nord",             "59", 1180000),
    ("Hauts-de-France", "CA Amiens Métropole",                   "EPCI",      49.8941, 2.2957, "Somme",            "80",  180000),
    ("Hauts-de-France", "CA d'Arras",                            "EPCI",      50.2929, 2.7811, "Pas-de-Calais",    "62",  108000),
    ("Hauts-de-France", "CA du Boulonnais",                      "EPCI",      50.7264, 1.6149, "Pas-de-Calais",    "62",  117000),
    ("Hauts-de-France", "CA de Saint-Quentinois",                "EPCI",      49.8480, 3.2876, "Aisne",            "02",   80000),
    ("Hauts-de-France", "CA de la Région de Compiègne",          "EPCI",      49.4179, 2.8260, "Oise",             "60",   83000),
    ("Hauts-de-France", "Ville de Maubeuge",                     "commune",   50.2786, 3.9722, "Nord",             "59",   30000),
    ("Hauts-de-France", "Ville de Soissons",                     "commune",   49.3814, 3.3236, "Aisne",            "02",   28000),
    ("Hauts-de-France", "CC Cœur d'Ostrevent",                   "EPCI",      50.3700, 3.2400, "Nord",             "59",   72000),

    # ===== Grand Est (8) =====
    ("Grand Est", "Eurométropole de Strasbourg",                 "métropole", 48.5734, 7.7521, "Bas-Rhin",         "67",  504000),
    ("Grand Est", "Métropole du Grand Nancy",                    "métropole", 48.6921, 6.1844, "Meurthe-et-Moselle","54", 257000),
    ("Grand Est", "Eurométropole de Metz",                       "métropole", 49.1193, 6.1757, "Moselle",          "57",  221000),
    ("Grand Est", "Mulhouse Alsace Agglomération",               "EPCI",      47.7508, 7.3359, "Haut-Rhin",        "68",  273000),
    ("Grand Est", "Grand Reims",                                 "EPCI",      49.2583, 4.0317, "Marne",            "51",  290000),
    ("Grand Est", "CA Troyes Champagne Métropole",               "EPCI",      48.2973, 4.0744, "Aube",             "10",  170000),
    ("Grand Est", "Ville de Charleville-Mézières",               "commune",   49.7714, 4.7197, "Ardennes",         "08",   46000),
    ("Grand Est", "CC du Pays de Bitche",                        "EPCI",      49.0500, 7.4300, "Moselle",          "57",   30000),

    # ===== Provence-Alpes-Côte d'Azur (7) =====
    ("Provence-Alpes-Côte d'Azur", "Métropole Aix-Marseille-Provence","métropole",43.2965,5.3698,"Bouches-du-Rhône","13",1880000),
    ("Provence-Alpes-Côte d'Azur", "Métropole Nice Côte d'Azur", "métropole", 43.7102, 7.2620, "Alpes-Maritimes",  "06",  537000),
    ("Provence-Alpes-Côte d'Azur", "Toulon Provence Méditerranée","EPCI",     43.1242, 5.9280, "Var",              "83",  448000),
    ("Provence-Alpes-Côte d'Azur", "CA du Grand Avignon",        "EPCI",      43.9493, 4.8055, "Vaucluse",         "84",  195000),
    ("Provence-Alpes-Côte d'Azur", "CA Cannes Pays de Lérins",   "EPCI",      43.5528, 7.0174, "Alpes-Maritimes",  "06",  159000),
    ("Provence-Alpes-Côte d'Azur", "Ville d'Aubagne",            "commune",   43.2925, 5.5703, "Bouches-du-Rhône", "13",   46000),
    ("Provence-Alpes-Côte d'Azur", "CC Sisteronais-Buëch",       "EPCI",      44.1937, 5.9445, "Hautes-Alpes",     "05",   24000),

    # ===== Occitanie (8) =====
    ("Occitanie", "Toulouse Métropole",                          "métropole", 43.6045, 1.4442, "Haute-Garonne",    "31",  815000),
    ("Occitanie", "Montpellier Méditerranée Métropole",          "métropole", 43.6108, 3.8767, "Hérault",          "34",  500000),
    ("Occitanie", "Nîmes Métropole",                             "EPCI",      43.8367, 4.3601, "Gard",             "30",  259000),
    ("Occitanie", "Perpignan Méditerranée Métropole",            "EPCI",      42.6886, 2.8946, "Pyrénées-Orientales","66",273000),
    ("Occitanie", "CA du Pays de l'Or",                          "EPCI",      43.5836, 4.0286, "Hérault",          "34",   46000),
    ("Occitanie", "CA Castres-Mazamet",                          "EPCI",      43.6064, 2.2414, "Tarn",             "81",   80000),
    ("Occitanie", "Ville de Cahors",                             "commune",   44.4475, 1.4408, "Lot",              "46",   19000),
    ("Occitanie", "CC Causses & Vallée de la Dordogne",          "EPCI",      44.8000, 1.7800, "Lot",              "46",   29000),

    # ===== Nouvelle-Aquitaine (9) =====
    ("Nouvelle-Aquitaine", "Bordeaux Métropole",                 "métropole", 44.8378,-0.5792, "Gironde",          "33",  814000),
    ("Nouvelle-Aquitaine", "Limoges Métropole",                  "EPCI",      45.8336, 1.2611, "Haute-Vienne",     "87",  208000),
    ("Nouvelle-Aquitaine", "CA Pau Béarn Pyrénées",              "EPCI",      43.2951,-0.3708, "Pyrénées-Atlantiques","64",162000),
    ("Nouvelle-Aquitaine", "Grand Poitiers",                     "EPCI",      46.5802, 0.3404, "Vienne",           "86",  194000),
    ("Nouvelle-Aquitaine", "CA La Rochelle",                     "EPCI",      46.1591,-1.1517, "Charente-Maritime","17",  170000),
    ("Nouvelle-Aquitaine", "CA Grand Angoulême",                 "EPCI",      45.6484, 0.1563, "Charente",         "16",  142000),
    ("Nouvelle-Aquitaine", "Ville de Périgueux",                 "commune",   45.1840, 0.7218, "Dordogne",         "24",   30000),
    ("Nouvelle-Aquitaine", "CC Médoc Atlantique",                "EPCI",      45.3500,-1.0700, "Gironde",          "33",   23000),
    ("Nouvelle-Aquitaine", "CC Lacq-Orthez",                     "EPCI",      43.4900,-0.7700, "Pyrénées-Atlantiques","64",53000),

    # ===== Bretagne (5) =====
    ("Bretagne", "Rennes Métropole",                             "métropole", 48.1173,-1.6778, "Ille-et-Vilaine",  "35",  457000),
    ("Bretagne", "Brest Métropole",                              "métropole", 48.3905,-4.4860, "Finistère",        "29",  214000),
    ("Bretagne", "CA Lorient Agglomération",                     "EPCI",      47.7482,-3.3702, "Morbihan",         "56",  205000),
    ("Bretagne", "CA Quimper Bretagne Occidentale",              "EPCI",      47.9960,-4.0975, "Finistère",        "29",  100000),
    ("Bretagne", "CC du Pays de Dol et Baie du Mont Saint-Michel","EPCI",     48.5450,-1.7500, "Ille-et-Vilaine",  "35",   20000),

    # ===== Pays de la Loire (6) =====
    ("Pays de la Loire", "Nantes Métropole",                     "métropole", 47.2184,-1.5536, "Loire-Atlantique", "44",  653000),
    ("Pays de la Loire", "Angers Loire Métropole",               "métropole", 47.4784,-0.5632, "Maine-et-Loire",   "49",  300000),
    ("Pays de la Loire", "Le Mans Métropole",                    "EPCI",      48.0061, 0.1996, "Sarthe",           "72",  210000),
    ("Pays de la Loire", "CA La Roche-sur-Yon Agglomération",    "EPCI",      46.6700,-1.4264, "Vendée",           "85",  100000),
    ("Pays de la Loire", "CA de Saumur Val de Loire",            "EPCI",      47.2606,-0.0793, "Maine-et-Loire",   "49",   97000),
    ("Pays de la Loire", "Ville de Cholet",                      "commune",   47.0590,-0.8779, "Maine-et-Loire",   "49",   53000),

    # ===== Normandie (5) =====
    ("Normandie", "Métropole Rouen Normandie",                   "métropole", 49.4432, 1.0993, "Seine-Maritime",   "76",  490000),
    ("Normandie", "Caen la Mer",                                 "EPCI",      49.1829,-0.3707, "Calvados",         "14",  267000),
    ("Normandie", "Le Havre Seine Métropole",                    "EPCI",      49.4944, 0.1079, "Seine-Maritime",   "76",  271000),
    ("Normandie", "CA du Cotentin",                              "EPCI",      49.6337,-1.6221, "Manche",           "50",  179000),
    ("Normandie", "Ville d'Évreux",                              "commune",   49.0269, 1.1500, "Eure",             "27",   46000),

    # ===== Bourgogne-Franche-Comté (4) =====
    ("Bourgogne-Franche-Comté", "Dijon Métropole",               "métropole", 47.3220, 5.0415, "Côte-d'Or",        "21",  254000),
    ("Bourgogne-Franche-Comté", "Grand Besançon Métropole",      "EPCI",      47.2378, 6.0241, "Doubs",            "25",  196000),
    ("Bourgogne-Franche-Comté", "CA du Grand Belfort",           "EPCI",      47.6380, 6.8628, "Territoire de Belfort","90",100000),
    ("Bourgogne-Franche-Comté", "CC Bresse Louhannaise Intercom","EPCI",      46.6300, 5.2200, "Saône-et-Loire",   "71",   30000),

    # ===== Centre-Val de Loire (4) =====
    ("Centre-Val de Loire", "Orléans Métropole",                 "métropole", 47.9029, 1.9039, "Loiret",           "45",  292000),
    ("Centre-Val de Loire", "Tours Métropole Val de Loire",      "métropole", 47.3941, 0.6848, "Indre-et-Loire",   "37",  300000),
    ("Centre-Val de Loire", "CA Bourges Plus",                   "EPCI",      47.0810, 2.3988, "Cher",             "18",  105000),
    ("Centre-Val de Loire", "Ville de Châteauroux",              "commune",   46.8108, 1.6918, "Indre",            "36",   44000),

    # ===== Corse (1) =====
    ("Corse", "CA du Pays Ajaccien",                             "EPCI",      41.9192, 8.7386, "Corse-du-Sud",     "2A",   84000),

    # ===== Outre-mer (5) =====
    ("Guadeloupe", "CA Cap Excellence",                          "EPCI",      16.2412,-61.5440,"Guadeloupe",       "971",100000),
    ("Martinique", "CA du Centre de la Martinique",              "EPCI",      14.6037,-61.0789,"Martinique",       "972",159000),
    ("Guyane", "CA du Centre Littoral",                          "EPCI",       4.9224,-52.3135,"Guyane",           "973",137000),
    ("La Réunion", "CA du Territoire de la Côte Ouest",          "EPCI",     -21.0419, 55.2293,"La Réunion",       "974",218000),
    ("Mayotte", "CC du Centre Ouest",                            "EPCI",     -12.8270, 45.1670,"Mayotte",          "976", 35000),
]

# ============================================================
# Génération
# ============================================================
STATUTS = [
    ("candidat",     "Candidature déposée", 40),
    ("retenu",       "Retenu",              35),
    ("conventionné", "Conventionné",        15),
    ("en_oeuvre",    "En œuvre",             8),
    ("abouti",       "Objectif atteint",     2),
]

# Plages de progression par statut
PROG_BY_STATUT = {
    "candidat":     (0,  5),
    "retenu":       (5, 18),
    "conventionné": (20, 40),
    "en_oeuvre":    (40, 75),
    "abouti":       (85, 98),
}

# Dates de sélection par statut (mai-décembre 2026)
DATE_BY_STATUT = {
    "candidat":     ("2026-04-15", "2026-06-30"),
    "retenu":       ("2026-05-15", "2026-07-31"),
    "conventionné": ("2026-06-01", "2026-09-30"),
    "en_oeuvre":    ("2026-07-01", "2026-11-30"),
    "abouti":       ("2025-09-01", "2026-03-31"),  # pilotes 2025
}

AXES_LIST = ["mobilite", "fioul", "gaz", "industrie", "agriculture"]
AXES_LABEL = {
    "mobilite":    "Mobilité",
    "fioul":       "Sortie fioul",
    "gaz":         "Sortie gaz",
    "industrie":   "Industrie",
    "agriculture": "Agriculture",
}

PRENOMS_F = ["Marie", "Sophie", "Anne", "Catherine", "Christine", "Isabelle", "Hélène", "Nathalie", "Caroline", "Émilie"]
PRENOMS_H = ["Pierre", "Jean", "Michel", "Philippe", "Bernard", "Christophe", "Patrick", "Olivier", "Laurent", "Stéphane"]
NOMS = ["Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand", "Dubois", "Moreau", "Laurent",
        "Simon", "Michel", "Lefebvre", "Leroy", "Roux", "David", "Bertrand", "Morel", "Fournier", "Girard"]

ROLES_BY_TYPE = {
    "métropole":   ["Président de la métropole", "Présidente de la métropole"],
    "EPCI":        ["Président d'EPCI", "Présidente d'EPCI"],
    "commune":     ["Maire", "Maire"],
    "département": ["Président du Conseil départemental", "Présidente du Conseil départemental"],
}

DISPOSITIFS = [
    "MaPrimeRénov' (ANAH)",
    "CEE Bâtiment",
    "CEE Transports (E-Trans)",
    "Programme Advenir",
    "AAP DECARB FLASH",
    "AO Grands Projets Industriels (GPID)",
    "Fonds chaleur (Ademe)",
    "Prêt Action élec ta boîte (Bpifrance)",
]

def random_date(start_iso, end_iso):
    import datetime as dt
    start = dt.date.fromisoformat(start_iso)
    end = dt.date.fromisoformat(end_iso)
    delta = (end - start).days
    return (start + dt.timedelta(days=random.randint(0, delta))).isoformat()

def generate_territoire(idx, place):
    region, nom, type_, lat, lon, dep, dep_code, pop = place

    # Statut tiré selon pondération
    status_weights = [s[2] for s in STATUTS]
    status_choices = [s[0] for s in STATUTS]
    statut = random.choices(status_choices, weights=status_weights)[0]
    statut_label = dict([(s[0], s[1]) for s in STATUTS])[statut]

    # Date de sélection
    d_start, d_end = DATE_BY_STATUT[statut]
    date_selection = random_date(d_start, d_end) if statut != "candidat" else random_date(d_start, d_end)

    # Progression
    prog_min, prog_max = PROG_BY_STATUT[statut]
    progression_pct = random.randint(prog_min, prog_max)

    # Axes prioritaires (1 à 3, biaisé sur mobilité/fioul/gaz)
    n_axes = random.choices([1, 2, 3], weights=[20, 50, 30])[0]
    base_axes = ["mobilite", "fioul", "gaz"]
    extra_axes = ["industrie", "agriculture"]
    axes = random.sample(base_axes, k=min(n_axes, 3))
    # Ajoute peut-être industrie/agriculture
    if random.random() < 0.2 and len(axes) < 3:
        axes.append(random.choice(extra_axes))
    axes = sorted(set(axes), key=lambda a: AXES_LIST.index(a))

    # Engagements scalés à la population
    # Échelles : bornes ≈ 0.8-2.5 PDC / 1000 hab ; PAC ≈ 8-18 / 1000 ; fioul ≈ 3-8 / 1000
    bornes_cible = max(8, int(pop / 1000 * random.uniform(0.8, 2.5)))
    pac_cible    = max(40, int(pop / 1000 * random.uniform(8, 18)))
    log_cible    = max(15, int(pop / 1000 * random.uniform(2.5, 7)))

    # Actuels = cible × progression × bruit
    noise = lambda: random.uniform(0.7, 1.3)
    bornes_actuel = int(bornes_cible * progression_pct / 100 * noise())
    pac_actuel    = int(pac_cible    * progression_pct / 100 * noise())
    log_actuel    = int(log_cible    * progression_pct / 100 * noise())

    ve_cible = random.choice([25, 30, 35, 40, 45, 50])
    ve_actuel = round(ve_cible * progression_pct / 100 * noise(), 1)
    ve_actuel = max(2.0, min(ve_actuel, ve_cible - 1.0))

    # Élu référent
    is_f = random.random() < 0.4
    prenom = random.choice(PRENOMS_F if is_f else PRENOMS_H)
    nom_elu = random.choice(NOMS)
    role = ROLES_BY_TYPE[type_][1 if is_f else 0]
    civ = "Mme" if is_f else "M."
    elu_referent = f"{civ} {prenom} {nom_elu}, {role}"

    # Direction État référente
    direction_etat = f"DGEC · ADEME {region}"

    # Financements (3 à 6 dispositifs)
    n_disp = random.randint(3, 6)
    dispositifs = random.sample(DISPOSITIFS, k=n_disp)
    financements = []
    for d in dispositifs:
        # Montant fonction de la population et de la nature
        base = pop * random.uniform(2, 40)  # 2-40 €/hab
        montant = int(round(base, -3))  # arrondi millier
        financements.append({"dispositif": d, "montant": montant})
    financement_total = sum(f["montant"] for f in financements)
    financements_resume = " · ".join(
        f"{f['dispositif'].split('(')[0].strip()} {f['montant']//1000} k€"
        for f in financements[:3]
    )
    if len(financements) > 3:
        financements_resume += f" · +{len(financements)-3} autres"

    # Jalons
    jalons_phrases = [
        "Délibération adoptée par le conseil",
        "Audit énergétique du parc public lancé",
        "Plan local de déploiement IRVE adopté",
        "Convention CEE signée avec un obligé",
        "Recensement des chaudières fioul ménages",
        "Cartographie des bâtiments publics au gaz",
        "Première phase de leasing social livrée",
        "Réunion publique d'information tenue",
        "AMO France Rénov' mobilisée",
        "Plan climat-air-énergie territorial révisé",
    ]
    dernier_jalon = random.choice(jalons_phrases) + " — " + random_date("2026-04-01", "2026-09-30")
    prochain_jalon = random.choice(jalons_phrases) + " — Q" + str(random.randint(1, 4)) + "/2027"

    # ID
    pk = f"T{idx:03d}"
    code_insee = dep_code + str(random.randint(100, 999)).zfill(3) if type_ == "commune" else "20" + str(random.randint(10000000, 99999999))
    if type_ == "département":
        code_insee = dep_code

    return {
        "id": pk,
        "nom": nom,
        "type": type_,
        "code_insee": code_insee,
        "lat": round(lat + random.uniform(-0.05, 0.05), 4),
        "lon": round(lon + random.uniform(-0.05, 0.05), 4),
        "region": region,
        "departement": dep,
        "dep_code": dep_code,
        "population": pop,

        "statut": statut,
        "statut_label": statut_label,
        "date_selection": date_selection,
        "progression_pct": progression_pct,

        "axes_codes": ",".join(axes),
        "axes_label": ", ".join(AXES_LABEL[a] for a in axes),
        "axe_mobilite":   1 if "mobilite"    in axes else 0,
        "axe_fioul":      1 if "fioul"       in axes else 0,
        "axe_gaz":        1 if "gaz"         in axes else 0,
        "axe_industrie":  1 if "industrie"   in axes else 0,
        "axe_agriculture":1 if "agriculture" in axes else 0,

        "elu_referent": elu_referent,
        "direction_etat": direction_etat,

        "bornes_cible": bornes_cible,
        "bornes_actuel": bornes_actuel,
        "bornes_pct": min(100, round(bornes_actuel / bornes_cible * 100)) if bornes_cible else 0,
        "pac_cible": pac_cible,
        "pac_actuel": pac_actuel,
        "pac_pct": min(100, round(pac_actuel / pac_cible * 100)) if pac_cible else 0,
        "logements_fioul_cible": log_cible,
        "logements_fioul_actuel": log_actuel,
        "logements_fioul_pct": min(100, round(log_actuel / log_cible * 100)) if log_cible else 0,
        "ve_part_cible_pct": ve_cible,
        "ve_part_actuel_pct": ve_actuel,
        "ve_pct": min(100, round(ve_actuel / ve_cible * 100)) if ve_cible else 0,

        "financement_total_eur": financement_total,
        "financement_total_keur": financement_total // 1000,
        "financements": financements,
        "financements_resume": financements_resume,

        "convention_url": f"https://www.ecologie.gouv.fr/territoires-electrification/{pk.lower()}",
        "dernier_jalon": dernier_jalon,
        "prochain_jalon": prochain_jalon,
    }


def main():
    if len(PLACES) > 100:
        sample = PLACES[:100]
    else:
        sample = PLACES
    territoires = [generate_territoire(i + 1, p) for i, p in enumerate(sample)]
    out = Path(__file__).resolve().parent.parent / "data" / "territoires.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        json.dump(territoires, f, ensure_ascii=False, indent=2)
    print(f"✓ {len(territoires)} territoires écrits dans {out}")
    print(f"  Taille fichier : {out.stat().st_size // 1024} KB")
    # Petites stats
    by_status = {}
    by_region = {}
    for t in territoires:
        by_status[t["statut"]] = by_status.get(t["statut"], 0) + 1
        by_region[t["region"]] = by_region.get(t["region"], 0) + 1
    print("  Par statut :")
    for k, v in sorted(by_status.items()):
        print(f"    {k:15s} {v}")
    print("  Par région :")
    for k, v in sorted(by_region.items(), key=lambda x: -x[1]):
        print(f"    {k:35s} {v}")


if __name__ == "__main__":
    main()
