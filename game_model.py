"""Moteur de simulation de KITTEN FRONT, sans dépendance graphique."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta
import random

@dataclass
class Province:
    key: str; name: str; x: int; y: int; owner: str
    strength: float; organisation: float; supply: float
    industry: int; victory_points: int; terrain: str
    links: tuple[str, ...]; capital: bool = False

@dataclass
class Battle:
    source: str; target: str; progress: float = 0.0; planning_bonus: float = 0.0

@dataclass
class Event:
    day: int; text: str; kind: str = "neutral"

@dataclass
class GameState:
    provinces: dict[str, Province] = field(default_factory=dict)
    battles: list[Battle] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)
    day: int = 1; command: float = 58; manpower: int = 86_000
    fuel: float = 74; equipment: float = 120; factories: int = 8
    captures: int = 0; losses: int = 0; weather: str = "Brume légère"
    stability: float = 72; war_support: float = 67; planning: float = 35
    focus_name: str = "Mobilisation industrielle"; focus_progress: float = 18
    research_name: str = "Logistique mécanisée"; research_progress: float = 24
    research_level: int = 0; mobilized: bool = False
    finished: bool = False; victory: bool | None = None

    @classmethod
    def new_campaign(cls) -> "GameState":
        rows = [
            ("aurelia","Aurélia",95,355,"blue",82,88,95,8,10,"Capitale",("belrive","montsac"),True),
            ("belrive","Belrive",200,165,"blue",64,78,86,5,4,"Plaines",("aurelia","montsac","valcroix"),False),
            ("montsac","Montsac",225,470,"blue",71,83,78,3,3,"Collines",("aurelia","belrive","rochefort","dornes"),False),
            ("valcroix","Valcroix",365,110,"blue",58,69,74,4,3,"Forêt",("belrive","rochefort","saint_lys"),False),
            ("rochefort","Rochefort",405,315,"blue",76,82,81,5,5,"Fortifié",("montsac","valcroix","dornes","saint_lys","verdance"),False),
            ("dornes","Dornes",365,535,"blue",53,67,65,2,2,"Marais",("montsac","rochefort","grisval"),False),
            ("saint_lys","Saint-Lys",555,125,"red",61,74,77,4,4,"Plaines",("valcroix","rochefort","verdance","nova"),False),
            ("verdance","Verdance",575,325,"red",72,79,72,4,4,"Forêt",("rochefort","saint_lys","grisval","nova","ostwald"),False),
            ("grisval","Grisval",545,540,"red",48,62,58,2,2,"Marais",("dornes","verdance","ostwald"),False),
            ("nova","Nova Kern",755,180,"red",88,91,94,9,10,"Capitale",("saint_lys","verdance","ostwald","karmin"),True),
            ("ostwald","Ostwald",745,455,"red",66,76,80,4,3,"Collines",("verdance","grisval","nova","karmin"),False),
            ("karmin","Karmin",890,320,"red",60,72,88,6,4,"Industriel",("nova","ostwald"),False),
        ]
        state = cls(provinces={r[0]: Province(*r) for r in rows})
        state.add_event("Le commandement du secteur vous est transféré.", "good")
        return state

    @property
    def current_date(self): return date(1941, 9, 11) + timedelta(days=self.day)
    def province(self, key): return self.provinces[key]
    def owned(self, faction): return [p for p in self.provinces.values() if p.owner == faction]
    def adjacent_enemies(self, key):
        p = self.province(key)
        return [self.province(k) for k in p.links if self.province(k).owner != p.owner]
    def add_event(self, text, kind="neutral"):
        self.events.insert(0, Event(self.day, text, kind)); del self.events[7:]

    def launch_attack(self, source, target):
        a, d = self.province(source), self.province(target)
        if a.owner != "blue" or d.owner != "red" or target not in a.links:
            return False, "La cible doit être rouge et adjacente."
        if self.command < 12 or self.fuel < 8: return False, "Ressources insuffisantes."
        if any(b.source == source or b.target == target for b in self.battles): return False, "Secteur déjà engagé."
        self.command -= 12; self.fuel -= 8; self.battles.append(Battle(source, target, planning_bonus=self.planning))
        self.planning = max(0, self.planning - 28)
        self.add_event(f"Offensive lancée : {a.name} → {d.name}.", "good")
        return True, "Offensive en cours"

    def reinforce(self, key):
        p = self.province(key)
        if p.owner != "blue": return False, "Secteur non contrôlé."
        if self.command < 15 or self.manpower < 3000 or self.equipment < 10: return False, "Réserves insuffisantes."
        self.command -= 15; self.manpower -= 3000; self.equipment -= 10
        p.strength = min(100, p.strength + 18); p.organisation = min(100, p.organisation + 14)
        self.add_event(f"{p.name} reçoit des renforts frais.", "good")
        return True, "Renforts déployés"

    def reorganise_factories(self):
        self.factories = 6 if self.factories >= 12 else self.factories + 1
        self.add_event(f"{self.factories} usines assignées à l'équipement.")

    def mobilize(self):
        if self.mobilized: return False, "La mobilisation est déjà active."
        if self.command < 35: return False, "Il faut 35 points de commandement."
        self.command -= 35; self.manpower += 20_000; self.war_support = min(100,self.war_support+12); self.stability=max(0,self.stability-7); self.mobilized=True
        self.add_event("La mobilisation générale est décrétée.","good")
        return True, "Mobilisation générale"

    def advance_day(self, tactical=True):
        if self.finished: return
        self.day += 1; self.command = min(100, self.command + 4)
        self.equipment += self.factories * (2.2+self.research_level*.25); self.fuel = min(100, self.fuel + 1.5)
        self.planning=min(100,self.planning+(1.5 if self.battles else 3.0)); self.focus_progress+=3.2; self.research_progress+=2.4
        if self.focus_progress>=100:
            self.focus_progress=0; self.command=min(100,self.command+18); self.manpower+=8_000; self.focus_name="Doctrine de défense active"; self.add_event("Focus national terminé : réserves libérées.","good")
        if self.research_progress>=100:
            self.research_progress=0; self.research_level+=1; self.research_name="Radio de campagne II" if self.research_level==1 else "Blindage amélioré"; self.add_event("Recherche terminée : production améliorée.","good")
        for p in self.provinces.values():
            p.organisation = min(100, p.organisation + p.supply / 50)
            if p.supply < 45: p.strength = max(5, p.strength - 1)
        if tactical:
            self._resolve_battles()
        if tactical and self.day % 4 == 0: self._enemy_ai()
        if self.day % 7 == 0: self._change_weather()
        if tactical:
            self._check_end()

    def _resolve_battles(self):
        survivors = []
        for b in self.battles:
            a, d = self.province(b.source), self.province(b.target)
            if a.owner == d.owner: continue
            terrain = {"Fortifié":.55,"Forêt":.78,"Marais":.70,"Collines":.85}.get(d.terrain, 1)
            attack = a.strength*a.organisation/100*a.supply/100*(1+b.planning_bonus/250)
            defence = d.strength*d.organisation/100*d.supply/100/terrain
            delta = attack - defence*.62
            d.strength -= max(.9, delta*.075); a.strength -= max(.45, (defence-attack*.35)*.028)
            a.organisation -= 2.3; d.organisation -= 3.1; b.progress += max(1.2, delta*.22)
            self.losses += max(1, int((attack+defence)/55))
            if d.strength <= 12 or d.organisation <= 8 or b.progress >= 100: self._capture(a, d)
            elif a.strength <= 14 or a.organisation <= 7:
                a.organisation = 25; self.add_event(f"L'offensive sur {d.name} s'est brisée.", "bad")
            else: survivors.append(b)
        self.battles = survivors

    def _capture(self, a, d):
        previous = d.owner; d.owner = a.owner; d.strength = max(24, a.strength*.42)
        d.organisation = 28; d.supply = max(35, d.supply-18)
        a.strength = max(18, a.strength*.72); a.organisation = 34
        if previous == "red": self.captures += 1; self.add_event(f"{d.name} est sous notre contrôle !", "good")
        else: self.add_event(f"{d.name} est tombée aux mains du Pacte.", "bad")

    def _enemy_ai(self):
        options = []
        for source in self.owned("red"):
            for target in self.adjacent_enemies(source.key):
                if not any(b.source == source.key or b.target == target.key for b in self.battles): options.append((source,target))
        options.sort(key=lambda pair: pair[0].strength-pair[1].strength, reverse=True)
        if options and options[0][0].strength > options[0][1].strength*.72:
            source,target = options[0]; self.battles.append(Battle(source.key,target.key))
            self.add_event(f"Attaque ennemie signalée à {target.name}.", "bad")

    def _change_weather(self):
        self.weather, delta = random.choice([("Brume légère",0),("Pluie battante",-8),("Ciel dégagé",5),("Vents d'ouest",-2)])
        for p in self.provinces.values(): p.supply = max(25,min(100,p.supply+delta))
        self.add_event(f"Bulletin météo : {self.weather.lower()}.")

    def _check_end(self):
        if self.province("nova").owner == "blue": self.finished,self.victory = True,True
        elif self.province("aurelia").owner == "red" or self.day > 45: self.finished,self.victory = True,False
