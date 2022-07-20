#!/usr/bin/python

from typing import Dict, List, Tuple
from enum import Enum
from data_files.boosts import boosts
from data_files.player_stats import player_stats
from data_files.spells import spells


class Element(Enum):
    AIR = 1
    EAU = 2
    FEU = 3
    TERRE = 4


class DofusLigneDommage:
    def __init__(self, element: Element, dommage_min: int, dommage_max: int, critique_dommage_min: int, critique_dommage_max: int) -> None:
        self.element = element
        self.dommage_min = dommage_min
        self.dommage_max = dommage_max
        self.critique_dommage_min = critique_dommage_min
        self.critique_dommage_max = critique_dommage_max

    @property
    def get_element(self):
        return self.element


class DofusSpell:
    def __init__(self, nom: str, lignes_dommages: List) -> None:
        self.nom = nom
        self.lignes_dommages = [DofusLigneDommage(element=Element(ligne_dommage.pop("element")), **ligne_dommage) for ligne_dommage in lignes_dommages]

    @property
    def get_element_dommage(self) -> List:
        elements = []
        for ligne in self.lignes_dommages:
            elements.append(ligne.get_element)
        return elements


class DofusPlayer:
    def __init__(self, stats: Dict, spells: List) -> None:
        self.agilite = int(stats.get("agilite", 0))
        self.chance = int(stats.get("chance", 0))
        self.intelligence = int(stats.get("intelligence", 0))
        self.force = int(stats.get("force", 0))
        self.puissance = int(stats.get("puissance", 0))
        self.dommages_fixes = int(stats.get("dommages_fixes", 0))
        self.dommages_fixes_air = int(stats.get("dommages_fixes_air", 0))
        self.dommages_fixes_eau = int(stats.get("dommages_fixes_eau", 0))
        self.dommages_fixes_feu = int(stats.get("dommages_fixes_feu", 0))
        self.dommages_fixes_terre = int(stats.get("dommages_fixes_terre", 0))
        self.dommages_critiques = int(stats.get("dommages_critiques", 0))
        self.dommages_sort = int(stats.get("dommages_sort", 0))
        self.points_action = int(stats.get("points_action", 6))
        self.points_mouvement = int(stats.get("points_mouvement", 3))
        self.spells = {spell.nom: spell for spell in spells}
        self.boost_puissance = 0
        self.boost_dommages_fixes = 0
        self.boost_dommages_critiques = 0

    @property
    def get_boost_puissance(self) -> int:
        return self.boost_puissance

    def set_boost_puissance(self, boost_puissance: int) -> None:
        self.boost_puissance = boost_puissance

    @property
    def get_boost_dommages_fixes(self) -> int:
        return self.boost_dommages_fixes

    def set_boost_dommages_fixes(self, boost_dommages_fixes: int) -> None:
        self.boost_dommages_fixes = boost_dommages_fixes

    @property
    def get_boost_dommages_critiques(self) -> int:
        return self.boost_dommages_critiques

    def set_boost_dommages_critiques(self, boost_dommages_critiques: int) -> None:
        self.boost_dommages_critiques = boost_dommages_critiques

    @property
    def get_agilite(self) -> int:
        return self.agilite + self.puissance + self.boost_puissance

    @property
    def get_intelligence(self) -> int:
        return self.intelligence + self.puissance + self.boost_puissance

    @property
    def get_chance(self) -> int:
        return self.chance + self.puissance + self.boost_puissance

    @property
    def get_force(self) -> int:
        return self.force + self.puissance + self.boost_puissance

    @property
    def get_dommages_fixes_air(self) -> int:
        return self.dommages_fixes_air + self.dommages_fixes + self.get_boost_dommages_fixes

    @property
    def get_dommages_fixes_feu(self) -> int:
        return self.dommages_fixes_feu + self.dommages_fixes + self.get_boost_dommages_fixes

    @property
    def get_dommages_fixes_eau(self) -> int:
        return self.dommages_fixes_eau + self.dommages_fixes + self.get_boost_dommages_fixes

    @property
    def get_dommages_fixes_force(self) -> int:
        return self.dommages_fixes_force + self.dommages_fixes + self.get_boost_dommages_fixes

    @property
    def get_dommages_critiques(self) -> int:
        return self.dommages_critiques

    @property
    def get_dommages_sort(self) -> int:
        return self.dommages_sort

    @property
    def get_point_action(self) -> int:
        return self.point_action

    @property
    def get_point_mouvement(self) -> int:
        return self.point_mouvement

    def get_stats_by_element(self, element: Element) -> int:
        if element == Element.AIR:
            return self.get_agilite
        elif element == Element.EAU:
            return self.get_chance
        elif element == Element.TERRE:
            return self.get_force
        elif element == Element.FEU:
            return self.get_intelligence

    def get_dommages_fixes_by_element(self, element: Element) -> int:
        if element == Element.AIR:
            return self.get_dommages_fixes_air
        elif element == Element.EAU:
            return self.get_dommages_fixes_eau
        elif element == Element.TERRE:
            return self.get_dommages_fixes_force
        elif element == Element.FEU:
            return self.get_dommages_fixes_feu

    def get_spell_dommages_by_name(self, name: str) -> List:
        spell = self.spells.get(name)
        dommages = []
        for ligne in spell.lignes_dommages:
            dommages.append({
                "element": ligne.get_element,
                "stats": self.get_stats_by_element(ligne.get_element),
                "dommages_fixes": self.get_dommages_fixes_by_element(ligne.get_element),
                "dommages_critiques": self.get_dommages_critiques,
                "dommage_min": ligne.dommage_min,
                "dommage_max": ligne.dommage_max,
                "critique_dommage_min": ligne.critique_dommage_min,
                "critique_dommage_max": ligne.critique_dommage_max,
                "dommages_sort": self.get_dommages_sort
            })
        return dommages

    def get_all_spells_dommages(self) -> List:
        spells_dommages = []
        for spell_name in self.spells:
            dommages = self.get_spell_dommages_by_name(spell_name)
            spells_dommages.append({
                "nom": spell_name,
                "dommages": dommages
            })
        return spells_dommages


class DofusDamageCalculator:
    def __init__(self, player: DofusPlayer, boost_puissance: int, boost_dommages_fixes: int) -> None:
        self.player = player
        self.player.set_boost_dommages_fixes(boost_dommages_fixes)
        self.player.set_boost_puissance(boost_puissance)

    def dommages_formula(self, base_dommage: int, stats: int, dommages_fixes: int, dommages_sort: int) -> int:
        final_dommages = int(base_dommage + base_dommage * (stats/100) + dommages_fixes)
        return int(final_dommages + final_dommages * (dommages_sort/100))

    def calculate_dommages(self, spell_dommages: Dict) -> Tuple[int, int, int, int]:
        final_min_dommages = 0
        final_max_dommages = 0
        final_critique_min_dommages = 0
        final_critique_max_dommages = 0
        for dommage in spell_dommages:
            final_min_dommages += self.dommages_formula(dommage.get("dommage_min"), dommage.get("stats"), dommage.get("dommages_fixes"), dommage.get("dommages_sort"))
            final_max_dommages += self.dommages_formula(dommage.get("dommage_max"), dommage.get("stats"), dommage.get("dommages_fixes"), dommage.get("dommages_sort"))
            final_critique_min_dommages += self.dommages_formula(dommage.get("critique_dommage_min"), dommage.get("stats"), dommage.get("dommages_fixes") + dommage.get("dommages_critiques"), dommage.get("dommages_sort"))
            final_critique_max_dommages += self.dommages_formula(dommage.get("critique_dommage_max"), dommage.get("stats"), dommage.get("dommages_fixes") + dommage.get("dommages_critiques"), dommage.get("dommages_sort"))
        return (final_min_dommages, final_max_dommages, final_critique_min_dommages, final_critique_max_dommages)

    def display_dommages(self):
        spells_dommages = self.player.get_all_spells_dommages()
        for spell in spells_dommages:
            final_min_dommages, final_max_dommages, final_critique_min_dommages, final_critique_max_dommages = self.calculate_dommages(spell["dommages"])
            print(f"{spell['nom']} dommages:")
            print(f"\tMin: {final_min_dommages}")
            print(f"\tMax: {final_max_dommages}")
            print(f"Critique:")
            print(f"\tMin: {final_critique_min_dommages}")
            print(f"\tMax: {final_critique_max_dommages}")


player_spells = [DofusSpell(**spell) for spell in spells]
player = DofusPlayer(player_stats, player_spells)

calculator = DofusDamageCalculator(player=player, boost_puissance=boosts["boost_puissance"], boost_dommages_fixes=boosts["boost_dommages_fixes"])

calculator.display_dommages()
