#!/usr/bin/python

# Elements: 
# 1 = AIR
# 2 = EAU
# 3 = FEU
# 4 = TERRE

spells = [
    {
        "nom": "Symbiose",
        "lignes_dommages": [
            {
                "element": 1,
                "dommage_min": 26,
                "dommage_max": 29,
                "critique_dommage_min": 31,
                "critique_dommage_max": 36
            },
            {
                "element": 2, 
                "dommage_min": 26,
                "dommage_max": 29,
                "critique_dommage_min": 31,
                "critique_dommage_max": 36
            }
        ]
    },
    {
        "nom": "Tique",
        "lignes_dommages": [
            {
                "element": 2,
                "dommage_min": 28,
                "dommage_max": 32,
                "critique_dommage_min": 28,
                "critique_dommage_max": 32
            }
        ]
    },
    {
        "nom": "Tique T2",
        "lignes_dommages": [
            {
                "element": 2,
                "dommage_min": 34,
                "dommage_max": 38,
                "critique_dommage_min": 34,
                "critique_dommage_max": 38
            }
        ]
    },
    {
        "nom": "Nématode",
        "lignes_dommages": [
            {
                "element": 1,
                "dommage_min": 27,
                "dommage_max": 31,
                "critique_dommage_min": 32,
                "critique_dommage_max": 37
            }
        ]
    }
]