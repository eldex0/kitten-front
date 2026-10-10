"""Combat continu inspiré des règles publiques de War of Dots."""
from __future__ import annotations
from dataclasses import dataclass, field
import math
import random

@dataclass
class DotUnit:
    uid: int; owner: str; kind: str; x: float; y: float
    health: float; morale: float = 100; path: list[tuple[float,float]] = field(default_factory=list)
    selected: bool = False; moving: bool = False; fighting: bool = False
    supplied: bool = True; last_order: float = 99; born: int = 0
    @property
    def max_health(self): return 200 if self.kind=="heavy" else 100
    @property
    def speed(self): return 33 if self.kind=="heavy" else 55
    @property
    def attack(self): return 18 if self.kind=="heavy" else 10

class DotBattlefield:
    def __init__(self, game, difficulty="Officier", spawn_initial=True, units_per_city=3, capture_duration=4.0):
        self.game=game; self.units=[]; self.next_uid=1; self.pending={}; self.eco={"blue":400.0,"red":400.0};self.production={"blue":.60,"red":.58};self.heavy_ratio={"blue":.30,"red":.34};self.production_clock={"blue":0.0,"red":0.0};self.capture={};self.ai_clock=0.0;self.difficulty=difficulty;self.capture_duration=capture_duration
        if spawn_initial:
            for city in game.provinces.values():
                for i in range(units_per_city):
                    angle=(i/max(1,units_per_city))*math.tau+(0 if city.owner=="blue" else .4);radius=18+(i%3)*4
                    self.spawn(city.owner,"heavy" if i==0 and city.capital else "light",city.x+math.cos(angle)*radius,city.y+math.sin(angle)*radius)

    def spawn(self,owner,kind,x,y):
        hp=200 if kind=="heavy" else 100;unit=DotUnit(self.next_uid,owner,kind,x,y,hp,born=self.next_uid);self.next_uid+=1;self.units.append(unit);return unit
    def own_units(self,owner="blue"):return [u for u in self.units if u.owner==owner and u.health>0]
    def selected(self):return [u for u in self.units if u.selected and u.owner=="blue"]
    def clear_selection(self):
        for u in self.units:u.selected=False
    def select_polygon(self,points,add=False):
        if not add:self.clear_selection()
        if len(points)<3:return []
        for u in self.own_units():
            if self._inside(u.x,u.y,points):u.selected=True
        return self.selected()
    def select_single(self,uid,add=False):
        if not add:self.clear_selection()
        for u in self.units:
            if u.uid==uid and u.owner=="blue":u.selected=True;return u
    @staticmethod
    def _inside(x,y,poly):
        inside=False;j=len(poly)-1
        for i in range(len(poly)):
            xi,yi=poly[i];xj,yj=poly[j]
            if ((yi>y)!=(yj>y)) and x<(xj-xi)*(y-yi)/(yj-yi+1e-9)+xi:inside=not inside
            j=i
        return inside
    def draft_order(self,path):
        selected=self.selected()
        if not selected or len(path)<2:return False
        cx=sum(u.x for u in selected)/len(selected);cy=sum(u.y for u in selected)/len(selected)
        for u in selected:self.pending[u.uid]=[(x+(u.x-cx),y+(u.y-cy)) for x,y in path]
        return True
    def commit_orders(self):
        count=0
        for u in self.units:
            if u.uid in self.pending:u.path=self.pending[u.uid];u.last_order=0;count+=1
        self.pending.clear();self.clear_selection();return count
    def clear_drafts(self):self.pending.clear()
    def halt_selected(self):
        for u in self.selected():u.path=[];u.moving=False;u.last_order=99

    def update(self,dt):
        self.ai_clock+=dt
        interval={"Recrue":5.2,"Officier":4.0,"Maréchal":2.8}.get(self.difficulty,4.0)
        if self.ai_clock>=interval:self.ai_clock=0;self._ai_orders()
        for u in self.units:u.fighting=False;u.last_order+=dt
        self._supply_and_economy(dt);self._movement(dt);self._combat(dt);self._capture_cities(dt);self._separate()
        self.units=[u for u in self.units if u.health>0]

    def _terrain(self,x,y):
        if (250<x<355 and 225<y<310) or (650<x<735 and 40<y<105) or (775<x<865 and 500<y<580):return "hill"
        if (90<x<205 and 55<y<140) or (620<x<725 and 365<y<445) or (820<x<910 and 190<y<275):return "forest"
        return "plain"
    def _movement(self,dt):
        for u in self.units:
            u.moving=bool(u.path)
            if not u.path:continue
            tx,ty=u.path[0];dx,dy=tx-u.x,ty-u.y;dist=math.hypot(dx,dy)
            terrain=self._terrain(u.x,u.y);modifier=.55 if u.kind=="heavy" and terrain!="plain" else (.82 if terrain!="plain" else 1)
            step=u.speed*modifier*dt
            if dist<=step:u.x,u.y=tx,ty;u.path.pop(0)
            elif dist:u.x+=dx/dist*step;u.y+=dy/dist*step
            u.x=max(15,min(965,u.x));u.y=max(15,min(605,u.y))

    def _combat(self,dt):
        handled=set()
        for a in self.units:
            enemies=[b for b in self.units if b.owner!=a.owner and b.health>0 and math.hypot(a.x-b.x,a.y-b.y)<27]
            if not enemies:continue
            b=min(enemies,key=lambda e:math.hypot(a.x-e.x,a.y-e.y));pair=tuple(sorted((a.uid,b.uid)))
            if pair in handled:continue
            handled.add(pair);a.fighting=b.fighting=True
            attacker,defender=(a,b) if a.moving or a.last_order<b.last_order else (b,a)
            terrain=self._terrain(defender.x,defender.y);terrain_bonus=1.18 if terrain in ("hill","forest") else 1
            atk_morale=.2+.8*attacker.morale/100;def_morale=.2+.8*defender.morale/100
            type_mod=.62 if attacker.kind=="heavy" and terrain!="plain" else 1
            ai_bonus={"Recrue":.82,"Officier":1.0,"Maréchal":1.18}.get(self.difficulty,1.0)
            defender.health-=attacker.attack*atk_morale*type_mod*dt*.52*(ai_bonus if attacker.owner=="red" else 1)
            attacker.health-=defender.attack*def_morale*terrain_bonus*dt*.78*(ai_bonus if defender.owner=="red" else 1)
            attacker.morale=max(0,attacker.morale-12*dt);defender.morale=max(0,defender.morale-5*dt)
            attacker.path=[]
        for u in self.units:
            if not u.fighting:
                near_enemy=any(e.owner!=u.owner and math.hypot(u.x-e.x,u.y-e.y)<120 for e in self.units)
                u.morale=min(100,u.morale+(18 if not near_enemy else 7)*dt)
                if not near_enemy:
                    in_city=any(c.owner==u.owner and math.hypot(u.x-c.x,u.y-c.y)<26 for c in self.game.provinces.values())
                    u.health=min(u.max_health,u.health+(4 if in_city else 2)*dt)

    def _supply_and_economy(self,dt):
        for owner in ("blue","red"):
            cities=[c for c in self.game.provinces.values() if c.owner==owner];units=self.own_units(owner)
            income=len(cities)*5;upkeep=0
            for u in units:
                garrison=any(math.hypot(u.x-c.x,u.y-c.y)<25 for c in cities)
                if not garrison:upkeep+=1
            self.eco[owner]+=max(-20,income-upkeep)*dt
            capacity=len(cities)*5;ordered=sorted(units,key=lambda u:u.born)
            for i,u in enumerate(ordered):
                local=self.power_at(u.x,u.y);inside_control=local>=-0.08 if owner=="blue" else local<=0.08
                u.supplied=(i<capacity and inside_control) or any(c.capital and math.hypot(u.x-c.x,u.y-c.y)<150 for c in cities)
                if not u.supplied:u.health-=12*dt;u.morale=max(0,u.morale-20*dt)
            self.production_clock[owner]+=dt*self.production[owner]
            if self.production_clock[owner]>=1:
                self.production_clock[owner]=0;kind="heavy" if random.random()<self.heavy_ratio[owner] else "light";cost=400 if kind=="heavy" else 200
                if self.eco[owner]>=cost and cities:
                    city=max(cities,key=lambda c:min((math.hypot(c.x-e.x,c.y-e.y) for e in self.own_units("red" if owner=="blue" else "blue")),default=999));self.eco[owner]-=cost;self.spawn(owner,kind,city.x+random.randint(-12,12),city.y+random.randint(-12,12))

    def _capture_cities(self,dt):
        for city in self.game.provinces.values():
            enemy="red" if city.owner=="blue" else "blue";occupiers=[u for u in self.own_units(enemy) if math.hypot(u.x-city.x,u.y-city.y)<28];defenders=[u for u in self.own_units(city.owner) if math.hypot(u.x-city.x,u.y-city.y)<38]
            if occupiers and not defenders:
                self.capture[city.key]=self.capture.get(city.key,0)+dt
                if self.capture[city.key]>=self.capture_duration:
                    city.owner=enemy;self.capture[city.key]=0;self.game.add_event(f"{city.name} est capturée par {'Orion' if enemy=='blue' else 'le Pacte'}.","good" if enemy=="blue" else "bad");self.game.captures+=enemy=="blue"
            else:self.capture[city.key]=max(0,self.capture.get(city.key,0)-dt*2)

    def _ai_orders(self):
        reds=[u for u in self.own_units("red") if not u.fighting];targets=[c for c in self.game.provinces.values() if c.owner=="blue"]
        if not reds or not targets:return
        idle=[u for u in reds if not u.path]
        for u in idle[:max(2,len(idle)//3)]:
            city=min(targets,key=lambda c:math.hypot(u.x-c.x,u.y-c.y));u.path=[(city.x+random.randint(-25,25),city.y+random.randint(-25,25))];u.last_order=0

    def _separate(self):
        for i,a in enumerate(self.units):
            for b in self.units[i+1:]:
                dx,dy=a.x-b.x,a.y-b.y;dist=math.hypot(dx,dy);minimum=12 if a.owner==b.owner else 9
                if 0<dist<minimum:
                    push=(minimum-dist)/2;nx,ny=dx/dist,dy/dist;a.x+=nx*push;a.y+=ny*push;b.x-=nx*push;b.y-=ny*push

    def power_at(self,x,y):
        """Positive is Orion control, negative is Carmin control."""
        power=0.0
        for city in self.game.provinces.values():
            sign=1 if city.owner=="blue" else -1;power+=sign*(4.2 if city.capital else 2.8)/(1+math.hypot(x-city.x,y-city.y)/95)
        for unit in self.units:
            sign=1 if unit.owner=="blue" else -1;weight=1.55 if unit.kind=="heavy" else 1
            power+=sign*weight*(unit.health/unit.max_health)/(1+math.hypot(x-unit.x,y-unit.y)/48)
        return power

    def front_segments(self,step=38):
        """Marching-squares contour where both factions project equal power."""
        xs=list(range(0,981,step));ys=list(range(0,621,step));values={(x,y):self.power_at(x,y) for y in ys for x in xs};segments=[]
        table={1:[(3,0)],2:[(0,1)],3:[(3,1)],4:[(1,2)],5:[(3,2),(0,1)],6:[(0,2)],7:[(3,2)],8:[(2,3)],9:[(0,2)],10:[(0,3),(1,2)],11:[(1,2)],12:[(1,3)],13:[(0,1)],14:[(3,0)]}
        for y in ys[:-1]:
            for x in xs[:-1]:
                corners=[(x,y),(x+step,y),(x+step,y+step),(x,y+step)];case=sum((1<<i) for i,p in enumerate(corners) if values[p]>0)
                edges=[(x+step/2,y),(x+step,y+step/2),(x+step/2,y+step),(x,y+step/2)]
                for a,b in table.get(case,[]):segments.append((edges[a],edges[b]))
        return segments
