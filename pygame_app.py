"""KITTEN FRONT — renderer Pygame, 60 FPS, carte de points + grande stratégie."""
from __future__ import annotations
import math
from pathlib import Path
import pygame
from game_model import GameState
from dot_warfare import DotBattlefield
from save_system import has_save, load_game, load_settings, save_game, save_settings

C={"bg":"#10130f","panel":"#171c16","panel2":"#222920","line":"#414a3c","paper":"#f3ecd5","muted":"#a0a994","acid":"#f2d45c","blue":"#3d91d3","blue2":"#21679e","red":"#e05249","red2":"#a33132","gold":"#f0c54a","grass":"#8da87b","grass2":"#749065","water":"#5a9eb0","road":"#342f27"}
EN={
"DOTS x GRANDE STRATÉGIE":"DOTS x GRAND STRATEGY","ÉDITION COMMANDEMENT":"COMMAND EDITION","CONTINUER":"CONTINUE","NOUVELLE PARTIE":"NEW GAME","TUTORIEL INTERACTIF":"INTERACTIVE TUTORIAL","PARAMÈTRES":"SETTINGS","CRÉDITS":"CREDITS","QUITTER":"QUIT","Une campagne est sauvegardée automatiquement tous les 5 jours.":"A campaign is automatically saved every 5 days.",
"CHOISIR UN MODE":"CHOOSE A MODE","Chaque mode conserve les combats de points et la ligne de front dynamique.":"Every mode keeps dot combat and the dynamic front line.","CAMPAGNE":"CAMPAIGN","ESCARMOUCHE":"SKIRMISH","SCÉNARIOS":"SCENARIOS","45 JOURS":"45 DAYS","PERSONNALISÉE":"CUSTOM","3 MISSIONS":"3 MISSIONS","Gérez la nation, la production et le front. Prenez 80 % des villes.":"Manage the nation, production and front. Capture 80% of the cities.","Choisissez la difficulté et livrez une guerre plus ouverte.":"Choose the difficulty and fight a more open war.","Des forces, délais et objectifs asymétriques.":"Asymmetric forces, deadlines and objectives.","CHOISIR  >":"SELECT  >","+ 4 MODES SPÉCIAUX":"+ 4 SPECIAL MODES","< RETOUR":"< BACK",
"Choisissez le niveau de réaction et la puissance de l'adversaire.":"Choose the enemy reaction speed and strength.","RECRUE":"ROOKIE","OFFICIER":"OFFICER","MARÉCHAL":"MARSHAL","IA plus lente, dégâts ennemis réduits.":"Slower AI and reduced enemy damage.","Expérience équilibrée recommandée.":"Recommended balanced experience.","Ordres rapides, puissance ennemie accrue.":"Faster orders and stronger enemy forces.","SÉLECTIONNÉ":"SELECTED","CHOISIR":"SELECT","LANCER L'ESCARMOUCHE":"START SKIRMISH",
"SCÉNARIOS DE GUERRE":"WAR SCENARIOS","Trois situations conçues pour des décisions immédiates.":"Three situations built for immediate decisions.","PERCÉE CENTRALE":"CENTRAL BREAKTHROUGH","25 JOURS":"25 DAYS","Renforts lourds et fonds élevés. Prenez Nova Kern.":"Heavy reinforcements and extra funds. Capture Nova Kern.","DERNIER REMPART":"LAST STAND","TENIR J30":"HOLD TO D30","Aurélia est presque encerclée. Survivez avec deux villes.":"Aurelia is nearly surrounded. Survive with two cities.","COURSE AUX CAPITALES":"CAPITAL RACE","35 JOURS":"35 DAYS","Production accélérée. La première capitale prise gagne.":"Faster production. The first captured capital decides the war.","DÉPLOYER  >":"DEPLOY  >",
"MODES SPÉCIAUX":"SPECIAL MODES","Des règles distinctes pour renouveler chaque bataille.":"Distinct rules to renew every battle.","CONQUÊTE TOTALE":"TOTAL CONQUEST","10 VILLES":"10 CITIES","Contrôlez presque toute la carte avant le jour 75.":"Control almost the whole map before day 75.","SURVIE":"SURVIVAL","VAGUES":"WAVES","Tenez Aurélia 30 jours face à des renforts tous les 5 jours.":"Hold Aurelia for 30 days against reinforcements every 5 days.","GUERRE ÉCLAIR":"BLITZ WAR","15 JOURS":"15 DAYS","Économie offensive : prenez Nova Kern au plus vite.":"Offensive economy: capture Nova Kern quickly.","BAC À SABLE":"SANDBOX","SANS LIMITE":"NO LIMIT","9999 ECO, production maximale et aucune condition de fin.":"9999 ECO, maximum production and no end condition.","JOUER  >":"PLAY  >",
"Les choix sont conservés entre les lancements.":"Your choices are kept between launches.","LANGUE":"LANGUAGE","PLEIN ÉCRAN":"FULLSCREEN","QUALITÉ DE LA LIGNE DE FRONT":"FRONT LINE QUALITY","AIDES DE COMMANDES":"CONTROL HINTS","SAUVEGARDE AUTOMATIQUE":"AUTOSAVE","DIFFICULTÉ PAR DÉFAUT":"DEFAULT DIFFICULTY","OUI":"YES","NON":"NO","ÉLEVÉE":"HIGH","MOYENNE":"MEDIUM","BASSE":"LOW","OPTIONS DE GAMEPLAY  >":"GAMEPLAY OPTIONS  >","REVOIR LA PRÉSENTATION":"REPLAY INTRODUCTION",
"OPTIONS DE GAMEPLAY":"GAMEPLAY OPTIONS","Ces réglages s'appliquent aux prochaines parties.":"These settings apply to new games.","RESSOURCES INITIALES":"STARTING RESOURCES","DENSITÉ DE POINTS":"DOT DENSITY","DURÉE D'UN JOUR":"DAY LENGTH","VITESSE DE CAPTURE":"CAPTURE SPEED","VITESSE AU DÉMARRAGE":"STARTING SPEED","PAUSE LORS D'UNE CAPTURE":"PAUSE ON CAPTURE","TOUJOURS AFFICHER LES BARRES":"ALWAYS SHOW HEALTH BARS","AFFICHER LA LIGNE DE FRONT":"SHOW FRONT LINE","NORMALES":"NORMAL","NORMALE":"NORMAL","NORMAL":"NORMAL","RÉDUITES":"REDUCED","ABONDANTES":"ABUNDANT","FAIBLE":"LOW","LENT":"SLOW","LENTE":"SLOW","RAPIDE":"FAST",
"Un jeu de stratégie original construit pour PC en Python.":"An original strategy game built for PC in Python.","CONCEPTION & DIRECTION":"DESIGN & DIRECTION","MOTEUR":"ENGINE","Inspiré par les jeux de points et la grande stratégie.":"Inspired by dot warfare and grand strategy.",
"BRIEFING DU COMMANDANT MOUSTACHE":"COMMANDER WHISKERS' BRIEFING","BIENVENUE DANS KITTEN FRONT":"WELCOME TO KITTEN FRONT","Le commandant Moustache vous confie le théâtre de Vardonne.":"Commander Whiskers entrusts you with the Vardonne theater.","UNE ARMÉE DE POINTS":"AN ARMY OF DOTS","Simple à lire, libre à diriger : chaque point est une unité.":"Easy to read, free to command: every dot is a unit.","LE FRONT EST VIVANT":"THE FRONT IS ALIVE","Villes, ravitaillement et encerclements redessinent la bataille.":"Cities, supply and encirclements reshape the battle.","COMMANDEZ TOUTE LA GUERRE":"COMMAND THE WHOLE WAR","Tactique immédiate et décisions nationales ne font qu'un.":"Immediate tactics and national decisions become one.","DEUX ARMÉES · UNE LIGNE · VOTRE PLAN":"TWO ARMIES · ONE LINE · YOUR PLAN","ENCERCLEZ · TRACEZ · ESPACE POUR EXÉCUTER":"ENCIRCLE · DRAW · SPACE TO EXECUTE","GARDEZ VOS POINTS RELIÉS AUX VILLES":"KEEP YOUR DOTS CONNECTED TO CITIES","Bienvenue, humain. Nos points comptent sur vous !":"Welcome, human. Our dots are counting on you!","Une boucle choisit la troupe. Un trait lance l'offensive.":"A loop selects the force. A line launches the offensive.","Une ligne fermée signifie souvent : encerclé !":"A closed line often means: surrounded!","Prêt ? Le quartier général vous attend.":"Ready? Headquarters is waiting.","PASSER":"SKIP","SUIVANT  >":"NEXT  >","ENTRER AU QG  >":"ENTER HQ  >",
"THÉÂTRE":"THEATER","POINTS ORION":"ORION DOTS","POINTS CARMIN":"CARMINE DOTS","GROUPES D'ARMÉES":"ARMY GROUPS","GROUPE NORD":"NORTH GROUP","GROUPE CENTRE":"CENTER GROUP","GROUPE SUD":"SOUTH GROUP","PRODUCTION DE POINTS":"DOT PRODUCTION","FONDS ECO":"ECO FUNDS","RAVITAILLEMENT":"SUPPLY","ROUTES · VILLES · FRONTS":"ROADS · CITIES · FRONTS","UNITÉS":"UNITS","TRACEZ UNE BOUCLE":"DRAW A LOOP","autour de vos points":"around your dots","LÉGERS":"LIGHT","LOURDS":"HEAVY","SANTÉ MOY.":"AVG HEALTH","MORAL":"MORALE","RAVITAILLÉS":"SUPPLIED","S · HALTE / MODE DÉFENSIF":"S · HALT / DEFENSIVE MODE","C · EFFACER LES ORDRES":"C · CLEAR ORDERS","COMMUNIQUÉS":"REPORTS","ANNÉE 1941":"YEAR 1941","SEPTEMBRE":"SEPTEMBER","OCTOBRE":"OCTOBER","NOVEMBRE":"NOVEMBER","? TUTO":"? HELP",
"NATION":"NATION","RECHERCHE":"RESEARCH","PRODUCTION":"PRODUCTION","ÉTAT-MAJOR DE L'ALLIANCE":"ALLIANCE HIGH COMMAND","NATION & FOCUS":"NATION & FOCUS","INDUSTRIE & LOGISTIQUE":"INDUSTRY & LOGISTICS","ALLIANCE D'ORION":"ORION ALLIANCE","République fédérale · Guerre défensive":"Federal Republic · Defensive war","STABILITÉ":"STABILITY","SOUTIEN À LA GUERRE":"WAR SUPPORT","BONUS DE PLANIFICATION":"PLANNING BONUS","FOCUS NATIONAL ACTIF":"ACTIVE NATIONAL FOCUS","MOBILISATION ACTIVE":"MOBILIZATION ACTIVE","MOBILISATION GÉNÉRALE · 35 CMD":"GENERAL MOBILIZATION · 35 CMD","BUREAUX DE RECHERCHE":"RESEARCH BUREAUS","LOGISTIQUE":"LOGISTICS","DOCTRINE":"DOCTRINE","INGÉNIERIE":"ENGINEERING","Guerre de mouvement":"Mobile warfare","Fortifications de campagne":"Field fortifications","USINES":"FACTORIES","ÉQUIPEMENT":"EQUIPMENT","RÉSERVES":"RESERVES","RAVITAIL.":"SUPPLY","LIGNES DE PRODUCTION":"PRODUCTION LINES","+ RÉAFFECTER UNE USINE AUX FUSILS":"+ ASSIGN A FACTORY TO RIFLES",
"Objectif : Nova Kern et 80 % des villes avant J45.":"Objective: Nova Kern and 80% of cities before D45.","Escarmouche : prenez la capitale ennemie avant J60.":"Skirmish: capture the enemy capital before D60.","Percée : prenez Nova Kern avant J25.":"Breakthrough: capture Nova Kern before D25.","Dernier rempart : tenez Aurélia jusqu'au jour 30.":"Last stand: hold Aurelia until day 30.","Course : la première capitale capturée décide de la guerre.":"Race: the first captured capital decides the war.","Conquête totale : contrôlez 10 villes avant J75.":"Total conquest: control 10 cities before D75.","Survie : tenez Aurélia 30 jours face aux renforts.":"Survival: hold Aurelia for 30 days against reinforcements.","Guerre éclair : prenez Nova Kern avant J15.":"Blitz: capture Nova Kern before D15.","Bac à sable : ressources illimitées, aucune limite de temps.":"Sandbox: unlimited resources and no time limit.",
"01 · SÉLECTIONNER":"01 · SELECT","Maintenez le clic et tracez une boucle autour de points bleus.":"Hold the mouse button and draw a loop around blue dots.","Tous les points dans la boucle seront sélectionnés.":"Every dot inside the loop will be selected.","02 · DESSINER L'OFFENSIVE":"02 · DRAW THE OFFENSIVE","Depuis un point sélectionné, dessinez un chemin vers l'ennemi.":"From a selected dot, draw a path toward the enemy.","Les chemins peuvent contourner collines et forêts.":"Paths can go around hills and forests.","03 · EXÉCUTER LES ORDRES":"03 · EXECUTE ORDERS","Appuyez sur ESPACE pour lancer tous les chemins préparés.":"Press SPACE to execute every prepared path.","Les points se désélectionnent après l'ordre.":"Dots are deselected after the order.","04 · DÉFENDRE":"04 · DEFEND","Sélectionnez des points puis pressez S ou HALTE.":"Select dots, then press S or HALT.","Une unité immobile perd moins de moral et subit moins de dégâts.":"A stationary unit loses less morale and takes less damage.","05 · PRODUIRE":"05 · PRODUCE","Cliquez sur CADENCE dans le panneau gauche.":"Click RATE in the left panel.","Léger : 200 ECO · Lourd : 400 ECO.":"Light: 200 ECO · Heavy: 400 ECO.","06 · TEMPS RÉEL":"06 · REAL TIME","Choisissez >, >> ou >>> en bas.":"Choose >, >> or >>> at the bottom.","La ligne de front suit la projection de puissance.":"The front line follows projected power.",
"PARTIE EN PAUSE":"GAME PAUSED","REPRENDRE":"RESUME","SAUVEGARDER":"SAVE","SAUVEGARDER ET MENU":"SAVE AND MENU","QUITTER LE JEU":"QUIT GAME","ÉCHAP · reprendre":"ESC · resume","VICTOIRE DÉCISIVE":"DECISIVE VICTORY","OPÉRATION PERDUE":"OPERATION LOST","REJOUER":"PLAY AGAIN","MENU PRINCIPAL":"MAIN MENU","Partie sauvegardée":"Game saved","Sauvegarde chargée":"Save loaded","Sauvegarde illisible":"Unreadable save","Capture détectée · jeu en pause":"Capture detected · game paused"
}
def col(name): return pygame.Color(C[name])

class FrontlineGame:
    def __init__(self):
        pygame.init(); pygame.display.set_caption("KITTEN FRONT — War of Dots × grande stratégie")
        self.settings=load_settings();flags=pygame.FULLSCREEN if self.settings["fullscreen"] else pygame.RESIZABLE
        self.screen=pygame.display.set_mode((1440,900),flags); self.clock=pygame.time.Clock(); self.running=True
        self.logo=None;logo_path=Path(__file__).with_name("assets")/"kitten-front-logo.png"
        try:
            self.logo=pygame.image.load(str(logo_path)).convert_alpha();pygame.display.set_icon(self.logo)
            self.logo_header=pygame.transform.smoothscale(self.logo,(52,52));self.logo_menu=pygame.transform.smoothscale(self.logo,(82,82))
        except (pygame.error,OSError):self.logo=None
        self.game=GameState.new_campaign(); self.battlefield=DotBattlefield(self.game); self.speed=0; self.day_clock=0; self.anim=0
        self.scene="menu" if self.settings["onboarding_complete"] else "presentation";self.return_scene="menu";self.presentation_return="menu";self.presentation_page=0;self.pause_menu=False;self.mode="campaign";self.scenario="campaign";self.difficulty=self.settings["default_difficulty"];self.last_autosave_day=0;self.last_wave_day=0
        self.tutorial=-1; self.strategy=None; self.buttons={}; self.toast=""; self.toast_time=0
        self.gesture=None;self.drag_points=[]
        self.fonts={k:pygame.font.SysFont("bahnschrift",s,bold=b) for k,s,b in [("tiny",10,True),("small",12,False),("label",12,True),("body",15,False),("strong",16,True),("title",22,True),("big",30,True),("hero",46,True)]}

    def tr(self,value):
        text=str(value)
        if self.settings.get("language")!="English":return text
        if text in EN:return EN[text]
        replacements=(("LIGNE DE BRAISE","EMBER LINE"),("PERCÉE CENTRALE","CENTRAL BREAKTHROUGH"),("DERNIER REMPART","LAST STAND"),("COURSE AUX CAPITALES","CAPITAL RACE"),("CONQUÊTE TOTALE","TOTAL CONQUEST"),("GUERRE ÉCLAIR","BLITZ WAR"),("BAC À SABLE","SANDBOX"),("OPÉRATION ","OPERATION "),("SEPTEMBRE","SEPTEMBER"),("OCTOBRE","OCTOBER"),("NOVEMBRE","NOVEMBER"),("ESPACE : EXÉCUTER","SPACE: EXECUTE"),(" ·  C : ANNULER"," · C: CANCEL"),(" ·  S : HALTE"," · S: HALT"),(" ORDRE(S) EN ATTENTE"," ORDER(S) PENDING"),(" ordre(s) exécuté(s)"," order(s) executed"),(" ORDRE(S)"," ORDER(S)"),("POINTS SÉLECTIONNÉS","DOTS SELECTED"),("% moral","% morale"),("CADENCE :","RATE:"),("LOURDS :","HEAVY:"),("LÉGER 200 · LOURD 400 ECO","LIGHT 200 · HEAVY 400 ECO"),("JOUR ","DAY "),(" jours · "," days · "),(" prises · "," captures · "),(" points survivants"," surviving dots"),("/jour","/day"),("ASTUCE · ","TIP · "))
        for source,target in replacements:text=text.replace(source,target)
        return text
    def text(self,text,pos,font="body",color="paper",anchor="topleft",surface=None):
        surf=self.fonts[font].render(self.tr(text),True,col(color)); rect=surf.get_rect(); setattr(rect,anchor,pos); (surface or self.screen).blit(surf,rect); return rect
    def panel(self,rect,color="panel",border="line",radius=0):
        pygame.draw.rect(self.screen,col(color),rect,border_radius=radius); pygame.draw.rect(self.screen,col(border),rect,1,border_radius=radius)
    def bar(self,rect,value,color="acid"):
        pygame.draw.rect(self.screen,col("line"),rect); fill=rect.copy(); fill.width=int(rect.width*max(0,min(100,value))/100); pygame.draw.rect(self.screen,col(color),fill)
    def button(self,key,rect,label,accent=False,disabled=False,font="tiny"):
        mouse=pygame.mouse.get_pos(); hover=rect.collidepoint(mouse) and not disabled; bg="acid" if accent else "panel2"; fg="bg" if accent else "paper"
        if disabled:bg="panel";fg="muted"
        if hover:bg="paper";fg="bg"
        pygame.draw.rect(self.screen,col(bg),rect,border_radius=2); pygame.draw.rect(self.screen,col("line"),rect,1,border_radius=2)
        self.text(label,rect.center,font,fg,"center"); self.buttons[key]=(rect,disabled)
    def star(self,center,outer=13,inner=6,color="gold"):
        pts=[]
        for i in range(10):
            angle=-math.pi/2+i*math.pi/5; radius=outer if i%2==0 else inner
            pts.append((center[0]+math.cos(angle)*radius,center[1]+math.sin(angle)*radius))
        pygame.draw.polygon(self.screen,col(color),pts);pygame.draw.polygon(self.screen,pygame.Color("#594b20"),pts,2)

    def layout(self):
        w,h=self.screen.get_size(); header=68; footer=58; left=214; right=250
        return pygame.Rect(0,0,w,header),pygame.Rect(0,header,left,h-header-footer),pygame.Rect(left,header,w-left-right,h-header-footer),pygame.Rect(w-right,header,right,h-header-footer),pygame.Rect(0,h-footer,w,footer)

    def loop(self):
        while self.running:
            dt=self.clock.tick(60)/1000; self.anim+=dt
            for e in pygame.event.get():
                if e.type==pygame.QUIT:self.running=False
                elif e.type==pygame.VIDEORESIZE and not self.settings["fullscreen"]:self.screen=pygame.display.set_mode((max(1100,e.w),max(700,e.h)),pygame.RESIZABLE)
                elif e.type==pygame.KEYDOWN:self.key(e.key)
                elif e.type==pygame.MOUSEBUTTONDOWN and e.button==1:self.mouse_down(e.pos)
                elif e.type==pygame.MOUSEMOTION and self.gesture:self.mouse_drag(e.pos)
                elif e.type==pygame.MOUSEBUTTONUP and e.button==1:self.mouse_up(e.pos)
            self.update(dt); self.draw(); pygame.display.flip()
        pygame.quit()

    def key(self,key):
        if self.scene!="game":
            if self.scene=="presentation":
                if key in (pygame.K_SPACE,pygame.K_RETURN,pygame.K_RIGHT):self.advance_presentation()
                elif key==pygame.K_LEFT:self.presentation_page=max(0,self.presentation_page-1)
                elif key==pygame.K_ESCAPE:self.finish_presentation()
            elif key==pygame.K_ESCAPE and self.scene!="menu":self.scene="menu"
            return
        if key==pygame.K_ESCAPE:
            if self.strategy:self.strategy=None
            elif self.tutorial>=0:self.finish_tutorial()
            elif self.pause_menu:self.pause_menu=False;self.speed=1
            else:self.pause_menu=True;self.speed=0
        elif self.pause_menu:return
        elif key==pygame.K_SPACE:
            count=self.battlefield.commit_orders();self.toast=f"{count} ordre(s) exécuté(s)";self.toast_time=2
            if count:self.tutorial_event("commit")
        elif key==pygame.K_p:self.set_speed(0 if self.speed else 1)
        elif key==pygame.K_c:self.battlefield.clear_drafts()
        elif key==pygame.K_s:self.battlefield.halt_selected();self.tutorial_event("halt")
        elif key in (pygame.K_1,pygame.K_2,pygame.K_3):self.set_speed(key-pygame.K_0)

    def mouse_down(self,pos):
        if self.scene!="game":
            for key in list(self.buttons):
                if self._hit(key,pos):self.menu_action(key);return
            return
        if self.pause_menu or self.game.finished:
            for key in list(self.buttons):
                if self._hit(key,pos):self.menu_action(key);return
            return
        if self.strategy:
            for key in ("close_strategy","tab_nation","tab_research","tab_production","mobilize","strategy_factory"):
                if self._hit(key,pos):self.action(key);return
            return
        for key in ("nation","research","production","pause","speed1","speed2","speed3","production_rate","production_type","halt","clear_orders","help","tutorial_skip"):
            if self._hit(key,pos):self.action(key);return
        _,_,mapr,_,_=self.layout()
        if not mapr.collidepoint(pos):return
        world=self.screen_to_world(pos,mapr);unit=self.unit_at(pos,mapr,"blue")
        if unit:
            if not unit.selected:self.battlefield.select_single(unit.uid,pygame.key.get_mods()&pygame.KMOD_SHIFT)
            self.gesture="order";self.drag_points=[world]
        else:
            self.gesture="lasso";self.drag_points=[world]

    def mouse_drag(self,pos):
        _,_,mapr,_,_=self.layout()
        if mapr.collidepoint(pos):
            point=self.screen_to_world(pos,mapr)
            if not self.drag_points or math.dist(point,self.drag_points[-1])>5:self.drag_points.append(point)

    def mouse_up(self,pos):
        if not self.gesture:return
        if self.gesture=="order" and len(self.drag_points)>1:
            if self.battlefield.draft_order(self.drag_points):self.tutorial_event("draft")
        elif self.gesture=="lasso" and len(self.drag_points)>2:
            selected=self.battlefield.select_polygon(self.drag_points,pygame.key.get_mods()&pygame.KMOD_SHIFT)
            if selected:self.tutorial_event("select_units")
        self.gesture=None;self.drag_points=[]

    def _hit(self,key,pos):
        item=self.buttons.get(key); return bool(item and not item[1] and item[0].collidepoint(pos))
    def action(self,key):
        if key in ("nation","research","production"):self.strategy=key
        elif key=="close_strategy":self.strategy=None
        elif key.startswith("tab_"):self.strategy=key[4:]
        elif key=="pause":self.set_speed(0)
        elif key.startswith("speed"):self.set_speed(int(key[-1]))
        elif key=="production_rate":
            current=self.battlefield.production["blue"];self.battlefield.production["blue"]={.25:.60,.60:1.0,1.0:.25}.get(round(current,2),.60);self.tutorial_event("production")
        elif key=="production_type":self.battlefield.heavy_ratio["blue"]=(self.battlefield.heavy_ratio["blue"]+.25)%1.01
        elif key=="strategy_factory":self.game.reorganise_factories()
        elif key=="halt":self.battlefield.halt_selected();self.tutorial_event("halt")
        elif key=="clear_orders":self.battlefield.clear_drafts()
        elif key=="mobilize":
            ok,msg=self.game.mobilize();self.toast=msg;self.toast_time=2
        elif key=="help":self.tutorial=0;self.speed=0
        elif key=="tutorial_skip":self.finish_tutorial()

    def menu_action(self,key):
        if key=="continue":self.load_current_game()
        elif key=="new_game":self.scene="modes"
        elif key=="mode_campaign":self.start_game("campaign","campaign")
        elif key=="mode_skirmish":self.scene="skirmish"
        elif key=="mode_scenarios":self.scene="scenarios"
        elif key=="mode_specials":self.scene="specials"
        elif key=="tutorial":self.start_game("tutorial","campaign",tutorial=True)
        elif key.startswith("difficulty_"):
            self.difficulty={"rookie":"Recrue","officer":"Officier","marshal":"Maréchal"}[key.split("_")[1]]
        elif key=="launch_skirmish":self.start_game("skirmish","skirmish")
        elif key.startswith("scenario_"):self.start_game("scenario",key.removeprefix("scenario_"))
        elif key.startswith("special_"):self.start_game("special",key.removeprefix("special_"))
        elif key=="settings":self.return_scene=self.scene;self.scene="settings"
        elif key=="gameplay_settings":self.scene="gameplay_settings"
        elif key=="credits":self.scene="credits"
        elif key=="presentation_next":self.advance_presentation()
        elif key=="presentation_previous":self.presentation_page=max(0,self.presentation_page-1)
        elif key=="presentation_skip":self.finish_presentation()
        elif key=="replay_presentation":self.presentation_page=0;self.presentation_return="settings";self.scene="presentation"
        elif key=="back":
            if self.scene=="gameplay_settings":self.scene="settings"
            elif self.scene=="settings":self.scene=self.return_scene
            elif self.scene in ("skirmish","scenarios","specials"):self.scene="modes"
            else:self.scene="menu"
        elif key=="quit":self.running=False
        elif key=="resume":self.pause_menu=False;self.speed=1
        elif key=="save":self.save_current_game("Partie sauvegardée")
        elif key=="main_menu":
            if not self.game.finished:self.save_current_game()
            self.pause_menu=False;self.scene="menu"
        elif key=="replay":self.start_game(self.mode,self.scenario,self.mode=="tutorial")
        elif key=="setting_language":
            self.settings["language"]="English" if self.settings["language"]=="Français" else "Français";save_settings(self.settings)
        elif key=="setting_fullscreen":
            self.settings["fullscreen"]=not self.settings["fullscreen"];self.apply_display();save_settings(self.settings)
        elif key=="setting_quality":
            values=["Basse","Moyenne","Élevée"];self.settings["front_quality"]=values[(values.index(self.settings["front_quality"])+1)%3];save_settings(self.settings)
        elif key in ("setting_tooltips","setting_autosave"):
            name=key.removeprefix("setting_");self.settings[name]=not self.settings[name];save_settings(self.settings)
        elif key=="setting_default_difficulty":
            values=["Recrue","Officier","Maréchal"];self.settings["default_difficulty"]=values[(values.index(self.settings["default_difficulty"])+1)%3];self.difficulty=self.settings["default_difficulty"];save_settings(self.settings)
        elif key=="setting_resources":self.cycle_setting("starting_resources",["Réduites","Normales","Abondantes"])
        elif key=="setting_density":self.cycle_setting("unit_density",["Faible","Normale","Élevée"])
        elif key=="setting_day_length":self.cycle_setting("day_length",["Lent","Normal","Rapide"])
        elif key=="setting_capture_speed":self.cycle_setting("capture_speed",["Lente","Normale","Rapide"])
        elif key=="setting_default_speed":self.cycle_setting("default_speed",[1,2,3])
        elif key in ("setting_pause_capture","setting_health_bars","setting_show_front"):
            name={"setting_pause_capture":"pause_on_capture","setting_health_bars":"always_health_bars","setting_show_front":"show_front"}[key];self.settings[name]=not self.settings[name];save_settings(self.settings)

    def cycle_setting(self,name,values):
        current=self.settings.get(name,values[0]);self.settings[name]=values[(values.index(current)+1)%len(values)];save_settings(self.settings)

    def advance_presentation(self):
        if self.presentation_page<3:self.presentation_page+=1
        else:self.finish_presentation()

    def finish_presentation(self):
        self.settings["onboarding_complete"]=True;save_settings(self.settings);self.scene=self.presentation_return;self.presentation_page=0

    def apply_display(self):
        flags=pygame.FULLSCREEN if self.settings["fullscreen"] else pygame.RESIZABLE
        self.screen=pygame.display.set_mode((1440,900),flags)

    def start_game(self,mode="campaign",scenario="campaign",tutorial=False):
        self.game=GameState.new_campaign();self.mode=mode;self.scenario=scenario;self.difficulty=self.difficulty;self.day_clock=0;self.last_autosave_day=0;self.last_wave_day=0
        if scenario=="last_stand":
            for key in ("belrive","valcroix","rochefort","dornes"):self.game.province(key).owner="red"
        density={"Faible":2,"Normale":3,"Élevée":5}.get(self.settings["unit_density"],3);capture_time={"Lente":6.0,"Normale":4.0,"Rapide":2.5}.get(self.settings["capture_speed"],4.0);self.battlefield=DotBattlefield(self.game,self.difficulty,units_per_city=density,capture_duration=capture_time)
        resources={"Réduites":.55,"Normales":1.0,"Abondantes":2.0}.get(self.settings["starting_resources"],1.0);self.battlefield.eco={"blue":400*resources,"red":400*resources}
        if scenario=="breakthrough":
            self.battlefield.eco["blue"]=900
            c=self.game.province("rochefort")
            for dy in (-35,0,35):self.battlefield.spawn("blue","heavy",c.x+25,c.y+dy)
        elif scenario=="capital_race":
            self.battlefield.eco={"blue":1000.0,"red":1000.0};self.battlefield.production={"blue":.9,"red":.9}
        elif scenario=="last_stand":
            for key in ("aurelia","montsac"):
                c=self.game.province(key)
                for i in range(3):self.battlefield.spawn("blue","heavy" if i==0 else "light",c.x+25,c.y-24+i*24)
        elif scenario=="survival":self.battlefield.eco["red"]*=1.5
        elif scenario=="blitz":
            self.battlefield.eco["blue"]*=1.8;self.battlefield.production["blue"]=1.0
        elif scenario=="sandbox":
            self.battlefield.eco={"blue":9999.0,"red":9999.0};self.battlefield.production={"blue":1.0,"red":1.0}
        elif mode=="skirmish":self.battlefield.eco={"blue":700.0,"red":700.0}
        self.scene="game";self.pause_menu=False;self.strategy=None;self.tutorial=0 if tutorial else -1;self.speed=0 if tutorial else self.settings["default_speed"]
        self.game.events=[];self.game.add_event(self.objective_text(),"good")

    def objective_text(self):
        return {"campaign":"Objectif : Nova Kern et 80 % des villes avant J45.","skirmish":"Escarmouche : prenez la capitale ennemie avant J60.","breakthrough":"Percée : prenez Nova Kern avant J25.","last_stand":"Dernier rempart : tenez Aurélia jusqu'au jour 30.","capital_race":"Course : la première capitale capturée décide de la guerre.","conquest":"Conquête totale : contrôlez 10 villes avant J75.","survival":"Survie : tenez Aurélia 30 jours face aux renforts.","blitz":"Guerre éclair : prenez Nova Kern avant J15.","sandbox":"Bac à sable : ressources illimitées, aucune limite de temps."}.get(self.scenario,"Prenez la capitale ennemie.")

    def save_current_game(self,message=None):
        save_game(self.game,self.battlefield,{"mode":self.mode,"scenario":self.scenario,"difficulty":self.difficulty,"day_clock":self.day_clock,"last_wave_day":self.last_wave_day})
        if message:self.toast=message;self.toast_time=2

    def load_current_game(self):
        try:
            self.game,self.battlefield,meta=load_game();self.mode=meta.get("mode","campaign");self.scenario=meta.get("scenario","campaign");self.difficulty=meta.get("difficulty","Officier");self.day_clock=meta.get("day_clock",0);self.last_wave_day=meta.get("last_wave_day",0);self.scene="game";self.pause_menu=False;self.speed=0;self.toast="Sauvegarde chargée";self.toast_time=2
        except (OSError,ValueError,KeyError,TypeError):
            self.scene="menu";self.toast="Sauvegarde illisible";self.toast_time=3

    def set_speed(self,n):
        self.speed=n
        if n:self.tutorial_event("speed")
    def tutorial_event(self,event):
        expected=("select_units","draft","commit","halt","production","speed")
        if 0<=self.tutorial<len(expected) and event==expected[self.tutorial]:
            self.tutorial+=1
            if self.tutorial==len(expected):self.finish_tutorial()
    def finish_tutorial(self):
        if self.tutorial>=0:self.game.add_event("Instruction terminée. Vous avez le commandement.","good")
        self.tutorial=-1
        if self.speed==0:self.speed=1

    def update(self,dt):
        if self.toast_time>0:self.toast_time-=dt
        if self.scene=="game" and self.speed and not self.game.finished and not self.pause_menu:
            owners=tuple(p.owner for p in self.game.provinces.values());self.battlefield.update(dt*self.speed)
            if self.settings["pause_on_capture"] and owners!=tuple(p.owner for p in self.game.provinces.values()):self.speed=0;self.toast="Capture détectée · jeu en pause";self.toast_time=3
            self.day_clock+=dt*self.speed
            day_seconds={"Lent":3.0,"Normal":2.0,"Rapide":1.2}.get(self.settings["day_length"],2.0)
            if self.day_clock>=day_seconds:
                self.day_clock=0;self.game.advance_day(tactical=False);self.check_dot_victory()
                if self.scenario=="survival" and self.game.day%5==0 and self.last_wave_day!=self.game.day:self.spawn_survival_wave();self.last_wave_day=self.game.day
                if self.settings["autosave"] and self.game.day%5==0 and self.last_autosave_day!=self.game.day:self.save_current_game();self.last_autosave_day=self.game.day
                if self.game.finished:self.speed=0

    def check_dot_victory(self):
        cities=list(self.game.provinces.values());blue=len([c for c in cities if c.owner=="blue"]);red=len(cities)-blue
        if self.scenario=="sandbox":return
        if self.scenario in ("last_stand","survival"):
            if self.game.day>=30:self.game.finished=True;self.game.victory=True
            elif self.game.province("aurelia").owner=="red":self.game.finished=True;self.game.victory=False
        elif self.scenario=="breakthrough":
            if self.game.province("nova").owner=="blue":self.game.finished=True;self.game.victory=True
            elif self.game.day>25 or self.game.province("aurelia").owner=="red":self.game.finished=True;self.game.victory=False
        elif self.scenario=="capital_race":
            if self.game.province("nova").owner=="blue":self.game.finished=True;self.game.victory=True
            elif self.game.province("aurelia").owner=="red" or self.game.day>35:self.game.finished=True;self.game.victory=False
        elif self.scenario=="conquest":
            if blue>=10:self.game.finished=True;self.game.victory=True
            elif red>=10 or self.game.day>75:self.game.finished=True;self.game.victory=False
        elif self.scenario=="blitz":
            if self.game.province("nova").owner=="blue":self.game.finished=True;self.game.victory=True
            elif self.game.day>15 or self.game.province("aurelia").owner=="red":self.game.finished=True;self.game.victory=False
        else:
            limit=60 if self.mode=="skirmish" else 45
            if self.game.province("nova").owner=="blue" and (self.mode=="skirmish" or blue/len(cities)>=.8):self.game.finished=True;self.game.victory=True
            elif self.game.province("aurelia").owner=="red" or self.game.day>limit:self.game.finished=True;self.game.victory=False

    def spawn_survival_wave(self):
        for key in ("nova","ostwald","karmin"):
            c=self.game.province(key)
            self.battlefield.spawn("red","heavy",c.x-20,c.y);self.battlefield.spawn("red","light",c.x,c.y+24)
        self.game.add_event("Une nouvelle vague du Pacte entre sur le théâtre.","bad")

    def draw(self):
        self.buttons={}; self.screen.fill(col("bg"))
        if self.scene!="game":self.draw_menu_scene();return
        header,left,mapr,right,footer=self.layout()
        self.draw_header(header); self.draw_left(left); self.draw_map(mapr); self.draw_right(right); self.draw_footer(footer)
        if self.tutorial>=0:self.draw_tutorial(mapr)
        if self.strategy:self.draw_strategy(mapr)
        if self.game.finished:self.draw_end()
        elif self.pause_menu:self.draw_pause()
        if self.toast_time>0:self.draw_toast()

    def draw_header(self,r):
        pygame.draw.rect(self.screen,col("bg"),r);pygame.draw.line(self.screen,col("line"),r.bottomleft,r.bottomright)
        if self.logo:self.screen.blit(self.logo_header,(2,8))
        else:pygame.draw.circle(self.screen,col("acid"),(27,34),13,3);pygame.draw.circle(self.screen,col("acid"),(27,34),4)
        self.text("KITTEN FRONT",(58,15),"title");self.text("DOTS x GRANDE STRATÉGIE",(59,42),"tiny","muted")
        names={"campaign":"LIGNE DE BRAISE","skirmish":"ESCARMOUCHE","breakthrough":"PERCÉE CENTRALE","last_stand":"DERNIER REMPART","capital_race":"COURSE AUX CAPITALES","conquest":"CONQUÊTE TOTALE","survival":"SURVIE","blitz":"GUERRE ÉCLAIR","sandbox":"BAC À SABLE"};cx=r.centerx-80;pygame.draw.circle(self.screen,col("red"),(cx-91,18),3);self.text("OPÉRATION "+names.get(self.scenario,"KITTEN FRONT"),(cx,12),"tiny","red","midtop")
        for i,(key,label) in enumerate((("nation","NATION"),("research","RECHERCHE"),("production","PRODUCTION"))):self.button(key,pygame.Rect(cx-145+i*98,31,94,27),label)
        vals=[("ECO",round(self.battlefield.eco["blue"]),"gold"),("UNIT",len(self.battlefield.own_units("blue")),"paper"),("CAR",f"{round(self.game.fuel)}%","paper"),("CMD",round(self.game.command),"acid")]
        x=r.right-310
        for label,value,color in vals:
            self.text(label,(x,14),"tiny","muted");self.text(value,(x,31),"strong",color);x+=72

    def draw_left(self,r):
        pygame.draw.rect(self.screen,col("panel"),r);pygame.draw.line(self.screen,col("line"),r.topright,r.bottomright)
        x=r.x+14;y=r.y+14;self.text("01",(x,y),"tiny","acid");self.text("THÉÂTRE",(x+30,y-5),"title");y+=40
        box=pygame.Rect(x,y,r.width-28,78);self.panel(box,"bg");blue=len(self.battlefield.own_units("blue"));red=len(self.battlefield.own_units("red"));self.text(blue,(box.x+10,box.y+9),"big","blue");self.text(red,(box.right-10,box.y+9),"big","red","topright");self.bar(pygame.Rect(box.x+10,box.y+48,box.width-20,7),blue/max(1,blue+red)*100,"blue");self.text("POINTS ORION",(box.x+10,box.bottom-14),"tiny","blue");self.text("POINTS CARMIN",(box.right-10,box.bottom-14),"tiny","red","topright");y+=96
        self.text("GROUPES D'ARMÉES",(x,y),"tiny","muted");y+=19
        groups=[("I","NORD",lambda u:u.y<220),("II","CENTRE",lambda u:220<=u.y<420),("III","SUD",lambda u:u.y>=420)]
        for mark,name,test in groups:
            own=[u for u in self.battlefield.own_units("blue") if test(u)];card=pygame.Rect(x,y,r.width-28,55);self.panel(card,"panel2");self.text(mark,(card.x+12,card.centery),"strong","gold","midleft");self.text("GROUPE "+name,(card.x+50,card.y+9),"label");morale=round(sum(u.morale for u in own)/len(own)) if own else 0;self.text(f"{morale}% moral",(card.x+50,card.y+31),"tiny","muted");self.text(len(own),(card.right-12,card.centery),"big","paper","midright");y+=61
        y+=10;self.text("PRODUCTION DE POINTS",(x,y),"tiny","muted");y+=18;card=pygame.Rect(x,y,r.width-28,133);self.panel(card,"bg");self.text("FONDS ECO",(card.x+10,card.y+10),"tiny","muted");self.text(round(self.battlefield.eco["blue"]),(card.right-10,card.y+8),"strong","gold","topright")
        rate=self.battlefield.production["blue"];self.button("production_rate",pygame.Rect(card.x+10,card.y+36,card.width-20,30),f"CADENCE : {round(rate*100)}%")
        heavy=self.battlefield.heavy_ratio["blue"];self.button("production_type",pygame.Rect(card.x+10,card.y+72,card.width-20,30),f"LOURDS : {round(heavy*100)}%")
        self.text("LÉGER 200 · LOURD 400 ECO",(card.centerx,card.bottom-19),"tiny","muted","center")
        y+=148;self.text("RAVITAILLEMENT",(x,y),"tiny","muted");supplied=sum(u.supplied for u in self.battlefield.own_units("blue"));total=max(1,len(self.battlefield.own_units("blue")));self.text(f"{supplied}/{total}",(r.right-14,y),"label","acid","topright");self.bar(pygame.Rect(x,y+19,r.width-28,7),supplied/total*100,"acid")

    def world_to_screen(self,p,r):
        x,y=(p if isinstance(p,tuple) else (p.x,p.y));return (r.x+x/980*r.width,r.y+y/620*r.height)
    def screen_to_world(self,p,r):return ((p[0]-r.x)/r.width*980,(p[1]-r.y)/r.height*620)
    def unit_at(self,pos,r,owner=None):
        units=[u for u in self.battlefield.units if owner is None or u.owner==owner]
        return min(units,key=lambda u:math.dist(pos,self.world_to_screen(u,r)),default=None) if units and min(math.dist(pos,self.world_to_screen(u,r)) for u in units)<15 else None
    def draw_map(self,r):
        pygame.draw.rect(self.screen,col("grass"),r);pygame.draw.polygon(self.screen,pygame.Color("#a2b47e"),[(r.x,r.bottom),(r.x,r.y+r.height*.72),(r.x+r.width*.35,r.y+r.height*.8),(r.x+r.width*.43,r.bottom)]);pygame.draw.polygon(self.screen,col("grass2"),[(r.x+r.width*.72,r.y),(r.right,r.y),(r.right,r.bottom),(r.x+r.width*.82,r.bottom)])
        river=[(520,-20),(455,105),(570,200),(510,320),(430,445),(525,650)];pts=[self.world_to_screen(p,r) for p in river];pygame.draw.lines(self.screen,pygame.Color("#376f7d"),False,pts,24);pygame.draw.lines(self.screen,col("water"),False,pts,15)
        for hx,hy in [(300,265),(690,70),(810,535)]:
            x,y=self.world_to_screen((hx,hy),r)
            for ring in range(3):pygame.draw.ellipse(self.screen,pygame.Color("#64755e"),pygame.Rect(x-25-ring*10,y-15-ring*7,50+ring*20,30+ring*14),2)
        for fx,fy in [(120,90),(150,115),(180,88),(650,390),(680,420),(705,390),(850,245),(875,220)]:
            x,y=self.world_to_screen((fx,fy),r);pygame.draw.circle(self.screen,pygame.Color("#3d6244"),(int(x),int(y)),8);pygame.draw.line(self.screen,pygame.Color("#4a3b29"),(x,y+5),(x,y+13),2)
        seen=set()
        for p in self.game.provinces.values():
            for key in p.links:
                pair=tuple(sorted((p.key,key)))
                if pair in seen:continue
                seen.add(pair);q=self.game.province(key);a=self.world_to_screen(p,r);b=self.world_to_screen(q,r);pygame.draw.line(self.screen,pygame.Color("#b6a582"),a,b,8);pygame.draw.line(self.screen,col("gold" if self.mode_supply() else "road"),a,b,4)
        # Living front: equal-power contour from every city and every dot.
        if self.settings["show_front"]:
            step={"Basse":56,"Moyenne":38,"Élevée":26}.get(self.settings["front_quality"],38)
            for a,b in self.battlefield.front_segments(step):
                sa,sb=self.world_to_screen(a,r),self.world_to_screen(b,r);pygame.draw.line(self.screen,pygame.Color("#f6efd8"),sa,sb,7);pygame.draw.line(self.screen,pygame.Color("#22241e"),sa,sb,3)
        for p in self.game.provinces.values():self.draw_city(p,r)
        for u in self.battlefield.units:self.draw_unit(u,r)
        for uid,path in self.battlefield.pending.items():
            unit=next((u for u in self.battlefield.units if u.uid==uid),None)
            if unit:
                pts=[self.world_to_screen(unit,r)]+[self.world_to_screen(p,r) for p in path]
                if len(pts)>1:pygame.draw.lines(self.screen,col(unit.owner),False,pts,2)
        if self.drag_points:
            pts=[self.world_to_screen(p,r) for p in self.drag_points]
            if len(pts)>1:pygame.draw.lines(self.screen,col("acid" if self.gesture=="order" else "paper"),self.gesture=="lasso",pts,2)
        self.text("VARDONNE",(r.x+18,r.bottom-48),"big","line");self.text("ROUTES · VILLES · FRONTS",(r.x+20,r.bottom-19),"tiny","bg")

    def mode_supply(self):return self.strategy=="production"
    def draw_city(self,p,r):
        x,y=self.world_to_screen(p,r);pygame.draw.circle(self.screen,col(p.owner),(int(x),int(y)),23,3);pygame.draw.circle(self.screen,col("gold"),(int(x),int(y)),15);pygame.draw.circle(self.screen,pygame.Color("#5b4d21"),(int(x),int(y)),15,2)
        if p.capital:self.star((x,y),12,5)
        else:pygame.draw.circle(self.screen,pygame.Color("#584b20"),(int(x),int(y)),5)
        capture=self.battlefield.capture.get(p.key,0)
        if capture:pygame.draw.arc(self.screen,col("acid"),pygame.Rect(x-29,y-29,58,58),-math.pi/2,-math.pi/2+math.tau*capture/4,4)
        self.text(p.name.upper(),(x,y+25),"tiny","bg","midtop")

    def draw_unit(self,u,r):
        x,y=self.world_to_screen(u,r);shake=math.sin(self.anim*24+u.uid)*2.5 if u.fighting else 0;x+=shake
        radius=10 if u.kind=="heavy" else 8
        if u.selected:pygame.draw.circle(self.screen,col("acid"),(int(x),int(y)),radius+6,2)
        if not u.supplied:pygame.draw.circle(self.screen,col("red"),(int(x),int(y)),radius+4,2)
        pygame.draw.circle(self.screen,col(u.owner),(int(x),int(y)),radius);pygame.draw.circle(self.screen,col("paper"),(int(x),int(y)),radius,1)
        if u.kind=="heavy":pygame.draw.rect(self.screen,col("bg"),pygame.Rect(x-3,y-3,6,6))
        if self.settings["always_health_bars"] or u.selected or u.fighting or u.health<u.max_health*.7:
            width=22;pygame.draw.rect(self.screen,pygame.Color("#342f2a"),pygame.Rect(x-width/2,y-radius-9,width,3));pygame.draw.rect(self.screen,pygame.Color("#71c66c"),pygame.Rect(x-width/2,y-radius-9,width*u.health/u.max_health,3));pygame.draw.rect(self.screen,col("blue"),pygame.Rect(x-width/2,y-radius-5,width*u.morale/100,2))

    def draw_right(self,r):
        pygame.draw.rect(self.screen,col("panel"),r);pygame.draw.line(self.screen,col("line"),r.topleft,r.bottomleft);x=r.x+14;y=r.y+14;self.text("02",(x,y),"tiny","acid");self.text("UNITÉS",(x+30,y-5),"title");y+=42;selected=self.battlefield.selected()
        if not selected:self.text("O",(r.centerx,y+50),"big","muted","center");self.text("TRACEZ UNE BOUCLE",(r.centerx,y+92),"tiny","muted","center");self.text("autour de vos points",(r.centerx,y+111),"small","muted","center")
        else:
            lights=sum(u.kind=="light" for u in selected);heavies=len(selected)-lights;hp=round(sum(u.health/u.max_health for u in selected)/len(selected)*100);morale=round(sum(u.morale for u in selected)/len(selected));supplied=sum(u.supplied for u in selected)
            self.text(f"{len(selected)} POINTS SÉLECTIONNÉS",(x,y),"title");y+=38
            for name,value in [("LÉGERS",lights),("LOURDS",heavies),("SANTÉ MOY.",f"{hp}%"),("MORAL",f"{morale}%"),("RAVITAILLÉS",f"{supplied}/{len(selected)}")]:self.text(name,(x,y),"tiny","muted");self.text(value,(r.right-14,y),"label","paper","topright");y+=24
            y+=8;self.button("halt",pygame.Rect(x,y,r.width-28,38),"S · HALTE / MODE DÉFENSIF",True);y+=44;self.button("clear_orders",pygame.Rect(x,y,r.width-28,34),"C · EFFACER LES ORDRES")
        y=max(y+55,r.y+345);self.text("COMMUNIQUÉS",(x,y),"tiny","muted");y+=20
        for event in self.game.events[:5]:
            color="blue" if event.kind=="good" else "red" if event.kind=="bad" else "muted";pygame.draw.line(self.screen,col(color),(x,y),(x,y+42),3);self.text(f"J{event.day:02d}",(x+9,y),"tiny",color);lines=self.wrap(event.text,26);self.text(lines[0],(x+9,y+16),"small");y+=50

    def wrap(self,text,limit):
        words=self.tr(text).split();lines=[""]
        for word in words:
            if len(lines[-1])+len(word)+1>limit:lines.append(word)
            else:lines[-1]=(lines[-1]+" "+word).strip()
        return lines

    def draw_footer(self,r):
        pygame.draw.rect(self.screen,col("bg"),r);pygame.draw.line(self.screen,col("line"),r.topleft,r.topright);d=self.game.current_date;months={9:"SEPTEMBRE",10:"OCTOBRE"};self.text("ANNÉE 1941",(18,r.y+8),"tiny","muted");self.text(f"{d.day:02d} {months.get(d.month,'NOVEMBRE')}",(18,r.y+25),"strong")
        x=210;self.button("pause",pygame.Rect(x,r.y+11,38,36),"P",self.speed==0);x+=43
        for n,label in ((1,">"),(2,">>"),(3,">>>")):self.button("speed"+str(n),pygame.Rect(x,r.y+11,46,36),label,self.speed==n);x+=51
        pending=len(self.battlefield.pending);hint=f"ESPACE : EXÉCUTER {pending} ORDRE(S)  ·  C : ANNULER  ·  S : HALTE" if self.settings["tooltips"] else f"{pending} ORDRE(S) EN ATTENTE";self.text(hint,(430,r.y+10),"tiny","acid" if pending else "muted");limit={"skirmish":60,"breakthrough":25,"last_stand":30,"capital_race":35,"conquest":75,"survival":30,"blitz":15,"sandbox":999}.get(self.scenario,45);self.bar(pygame.Rect(430,r.y+30,max(100,r.width-620),7),self.game.day/limit*100,"acid");deadline="∞" if self.scenario=="sandbox" else str(limit);self.text(f"JOUR {self.game.day} / {deadline}",(r.right-92,r.y+12),"label","paper","topright");self.button("help",pygame.Rect(r.right-82,r.y+11,66,36),"? TUTO")

    def draw_menu_scene(self):
        w,h=self.screen.get_size();self.draw_menu_background(w,h)
        if self.logo:self.screen.blit(self.logo_menu,(w//2-300,52))
        self.text("KITTEN FRONT",(w//2,72),"hero","paper","midtop");self.text("WAR OF DOTS × GRANDE STRATÉGIE",(w//2,128),"label","acid","midtop");self.text("ÉDITION COMMANDEMENT",(w//2,151),"tiny","muted","midtop")
        if self.scene=="menu":
            x=w//2-170;y=210
            items=[("continue","CONTINUER",True,not has_save()),("new_game","NOUVELLE PARTIE",True,False),("tutorial","TUTORIEL INTERACTIF",False,False),("settings","PARAMÈTRES",False,False),("credits","CRÉDITS",False,False),("quit","QUITTER",False,False)]
            for key,label,accent,disabled in items:self.button(key,pygame.Rect(x,y,340,48),label,accent,disabled,"label");y+=58
            self.text("Une campagne est sauvegardée automatiquement tous les 5 jours.",(w//2,h-54),"small","muted","center")
        elif self.scene=="modes":self.draw_modes(w,h)
        elif self.scene=="skirmish":self.draw_skirmish(w,h)
        elif self.scene=="scenarios":self.draw_scenarios(w,h)
        elif self.scene=="specials":self.draw_specials(w,h)
        elif self.scene=="settings":self.draw_settings(w,h)
        elif self.scene=="gameplay_settings":self.draw_gameplay_settings(w,h)
        elif self.scene=="credits":self.draw_credits(w,h)
        elif self.scene=="presentation":self.draw_presentation(w,h)
        if self.toast_time>0:self.draw_toast()

    def draw_menu_background(self,w,h):
        pygame.draw.circle(self.screen,pygame.Color("#1b241b"),(w//2,h//2+50),min(w,h)//2-30)
        for i in range(18):
            x=int(w*.12+i*w*.045);y=int(h*.28+math.sin(i*.8+self.anim*.25)*115);pygame.draw.circle(self.screen,col("blue"),(x,y),5)
            xr=w-x;yr=int(h*.65+math.sin(i*.73+self.anim*.2)*105);pygame.draw.circle(self.screen,col("red"),(xr,yr),5)
        pts=[(int(w*.18+i*w*.04),int(h*.48+math.sin(i*.72+self.anim*.35)*42)) for i in range(17)]
        if len(pts)>1:pygame.draw.lines(self.screen,col("paper"),False,pts,2)
        pygame.draw.line(self.screen,col("line"),(0,178),(w,178));pygame.draw.line(self.screen,col("line"),(0,h-82),(w,h-82))

    def menu_title(self,title,subtitle):
        w,_=self.screen.get_size();self.text(title,(w//2,202),"big","paper","midtop");self.text(subtitle,(w//2,241),"small","muted","midtop")

    def draw_modes(self,w,h):
        self.menu_title("CHOISIR UN MODE","Chaque mode conserve les combats de points et la ligne de front dynamique.");cw=286;gap=16;x=w//2-(cw*3+gap*2)//2;y=295
        cards=[("mode_campaign","CAMPAGNE","45 JOURS","Gérez la nation, la production et le front. Prenez 80 % des villes."),("mode_skirmish","ESCARMOUCHE","PERSONNALISÉE","Choisissez la difficulté et livrez une guerre plus ouverte."),("mode_scenarios","SCÉNARIOS","3 MISSIONS","Des forces, délais et objectifs asymétriques.")]
        for i,(key,title,tag,body) in enumerate(cards):
            r=pygame.Rect(x+i*(cw+gap),y,cw,235);self.panel(r,"panel");self.text(f"0{i+1}",(r.x+18,r.y+16),"label","acid");self.text(tag,(r.right-18,r.y+17),"tiny","muted","topright");self.text(title,(r.x+18,r.y+52),"title");lines=self.wrap(body,32)
            for j,line in enumerate(lines):self.text(line,(r.x+18,r.y+92+j*21),"small","muted")
            self.button(key,pygame.Rect(r.x+18,r.bottom-56,r.width-36,38),"CHOISIR  >",i==0)
        self.button("mode_specials",pygame.Rect(w//2-150,y+250,300,40),"+ 4 MODES SPÉCIAUX",True);self.button("back",pygame.Rect(w//2-90,y+300,180,34),"< RETOUR")

    def draw_skirmish(self,w,h):
        self.menu_title("ESCARMOUCHE","Choisissez le niveau de réaction et la puissance de l'adversaire.");x=w//2-360;y=302
        data=[("rookie","RECRUE","IA plus lente, dégâts ennemis réduits."),("officer","OFFICIER","Expérience équilibrée recommandée."),("marshal","MARÉCHAL","Ordres rapides, puissance ennemie accrue.")]
        for i,(key,title,body) in enumerate(data):
            r=pygame.Rect(x+i*250,y,230,150);self.panel(r,"panel2");self.text(title,(r.centerx,r.y+25),"title","acid" if self.difficulty==title.title() else "paper","midtop")
            for j,line in enumerate(self.wrap(body,28)):self.text(line,(r.x+15,r.y+63+j*18),"small","muted")
            self.button("difficulty_"+key,pygame.Rect(r.x+15,r.bottom-43,200,29),"SÉLECTIONNÉ" if self.difficulty==title.title() else "CHOISIR",self.difficulty==title.title())
        self.button("launch_skirmish",pygame.Rect(w//2-180,y+190,360,48),"LANCER L'ESCARMOUCHE",True);self.button("back",pygame.Rect(w//2-90,y+250,180,36),"< RETOUR")

    def draw_scenarios(self,w,h):
        self.menu_title("SCÉNARIOS DE GUERRE","Trois situations conçues pour des décisions immédiates.");x=w//2-410;y=288;data=[("breakthrough","PERCÉE CENTRALE","25 JOURS","Renforts lourds et fonds élevés. Prenez Nova Kern."),("last_stand","DERNIER REMPART","TENIR J30","Aurélia est presque encerclée. Survivez avec deux villes."),("capital_race","COURSE AUX CAPITALES","35 JOURS","Production accélérée. La première capitale prise gagne.")]
        for i,(key,title,tag,body) in enumerate(data):
            r=pygame.Rect(x+i*280,y,260,215);self.panel(r,"panel");self.text(tag,(r.x+16,r.y+16),"tiny","gold");self.text(title,(r.x+16,r.y+44),"strong");
            for j,line in enumerate(self.wrap(body,29)):self.text(line,(r.x+16,r.y+82+j*20),"small","muted")
            self.button("scenario_"+key,pygame.Rect(r.x+16,r.bottom-50,r.width-32,34),"DÉPLOYER  >",i==0)
        self.button("back",pygame.Rect(w//2-90,y+244,180,36),"< RETOUR")

    def draw_specials(self,w,h):
        self.menu_title("MODES SPÉCIAUX","Des règles distinctes pour renouveler chaque bataille.");x=w//2-390;y=278;data=[("conquest","CONQUÊTE TOTALE","10 VILLES","Contrôlez presque toute la carte avant le jour 75."),("survival","SURVIE","VAGUES","Tenez Aurélia 30 jours face à des renforts tous les 5 jours."),("blitz","GUERRE ÉCLAIR","15 JOURS","Économie offensive : prenez Nova Kern au plus vite."),("sandbox","BAC À SABLE","SANS LIMITE","9999 ECO, production maximale et aucune condition de fin.")]
        for i,(key,title,tag,body) in enumerate(data):
            row=i//2;column=i%2;r=pygame.Rect(x+column*400,y+row*180,380,160);self.panel(r,"panel");self.text(tag,(r.x+16,r.y+15),"tiny","gold");self.text(title,(r.x+16,r.y+39),"title")
            for j,line in enumerate(self.wrap(body,43)):self.text(line,(r.x+16,r.y+76+j*18),"small","muted")
            self.button("special_"+key,pygame.Rect(r.right-125,r.bottom-42,109,28),"JOUER  >",key=="conquest")
        self.button("back",pygame.Rect(w//2-90,y+375,180,34),"< RETOUR")

    def draw_settings(self,w,h):
        self.menu_title("PARAMÈTRES","Les choix sont conservés entre les lancements.");x=w//2-285;y=272;rows=[("setting_language","LANGUE",self.settings["language"].upper()),("setting_fullscreen","PLEIN ÉCRAN","OUI" if self.settings["fullscreen"] else "NON"),("setting_quality","QUALITÉ DE LA LIGNE DE FRONT",self.settings["front_quality"].upper()),("setting_tooltips","AIDES DE COMMANDES","OUI" if self.settings["tooltips"] else "NON"),("setting_autosave","SAUVEGARDE AUTOMATIQUE","OUI" if self.settings["autosave"] else "NON"),("setting_default_difficulty","DIFFICULTÉ PAR DÉFAUT",self.settings["default_difficulty"].upper())]
        for key,label,value in rows:self.panel(pygame.Rect(x,y,570,48),"panel2");self.text(label,(x+16,y+16),"label");self.button(key,pygame.Rect(x+355,y+9,198,30),value,True);y+=57
        self.button("gameplay_settings",pygame.Rect(w//2-180,y+12,360,40),"OPTIONS DE GAMEPLAY  >",True);self.button("replay_presentation",pygame.Rect(w//2-180,y+61,360,34),"REVOIR LA PRÉSENTATION");self.button("back",pygame.Rect(w//2-90,y+104,180,34),"< RETOUR")

    def draw_gameplay_settings(self,w,h):
        self.menu_title("OPTIONS DE GAMEPLAY","Ces réglages s'appliquent aux prochaines parties.");x=w//2-315;y=262;rows=[("setting_resources","RESSOURCES INITIALES",self.settings["starting_resources"].upper()),("setting_density","DENSITÉ DE POINTS",self.settings["unit_density"].upper()),("setting_day_length","DURÉE D'UN JOUR",self.settings["day_length"].upper()),("setting_capture_speed","VITESSE DE CAPTURE",self.settings["capture_speed"].upper()),("setting_default_speed","VITESSE AU DÉMARRAGE",">"*self.settings["default_speed"]),("setting_pause_capture","PAUSE LORS D'UNE CAPTURE","OUI" if self.settings["pause_on_capture"] else "NON"),("setting_health_bars","TOUJOURS AFFICHER LES BARRES","OUI" if self.settings["always_health_bars"] else "NON"),("setting_show_front","AFFICHER LA LIGNE DE FRONT","OUI" if self.settings["show_front"] else "NON")]
        for key,label,value in rows:self.panel(pygame.Rect(x,y,630,42),"panel2");self.text(label,(x+15,y+13),"label");self.button(key,pygame.Rect(x+420,y+6,194,30),value,True);y+=49
        self.button("back",pygame.Rect(w//2-90,y+10,180,34),"< RETOUR")

    def draw_credits(self,w,h):
        self.menu_title("CRÉDITS","Un jeu de stratégie original construit pour PC en Python.");box=pygame.Rect(w//2-310,292,620,255);self.panel(box,"panel");self.text("CONCEPTION & DIRECTION",(box.centerx,box.y+28),"tiny","acid","midtop");self.text("OPEN KITTEN",(box.centerx,box.y+54),"big","paper","midtop");self.text("MOTEUR",(box.centerx,box.y+111),"tiny","muted","midtop");self.text("Python · Pygame · simulation KITTEN FRONT",(box.centerx,box.y+134),"strong","paper","midtop");self.text("Inspiré par les jeux de points et la grande stratégie.",(box.centerx,box.y+184),"small","muted","midtop");self.button("back",pygame.Rect(w//2-90,575,180,38),"< RETOUR")

    def draw_kitten_commander(self,center,scale=1.0):
        x,y=center;s=scale;fur=pygame.Color("#d6a45f");dark=pygame.Color("#6a472d");cream=pygame.Color("#f3dfb3")
        pygame.draw.polygon(self.screen,fur,[(x-46*s,y-38*s),(x-30*s,y-94*s),(x-5*s,y-56*s)]);pygame.draw.polygon(self.screen,fur,[(x+46*s,y-38*s),(x+30*s,y-94*s),(x+5*s,y-56*s)])
        pygame.draw.polygon(self.screen,pygame.Color("#c87873"),[(x-37*s,y-48*s),(x-29*s,y-79*s),(x-14*s,y-53*s)]);pygame.draw.polygon(self.screen,pygame.Color("#c87873"),[(x+37*s,y-48*s),(x+29*s,y-79*s),(x+14*s,y-53*s)])
        pygame.draw.circle(self.screen,fur,(int(x),int(y)),int(58*s));pygame.draw.ellipse(self.screen,cream,pygame.Rect(x-31*s,y+2*s,62*s,40*s))
        pygame.draw.ellipse(self.screen,col("bg"),pygame.Rect(x-29*s,y-15*s,13*s,18*s));pygame.draw.ellipse(self.screen,col("bg"),pygame.Rect(x+16*s,y-15*s,13*s,18*s));pygame.draw.circle(self.screen,col("acid"),(int(x-22*s),int(y-8*s)),int(3*s));pygame.draw.circle(self.screen,col("acid"),(int(x+22*s),int(y-8*s)),int(3*s))
        pygame.draw.polygon(self.screen,dark,[(x,y+5*s),(x-6*s,y+13*s),(x+6*s,y+13*s)]);pygame.draw.arc(self.screen,dark,pygame.Rect(x-15*s,y+9*s,15*s,16*s),0,math.pi,2);pygame.draw.arc(self.screen,dark,pygame.Rect(x,y+9*s,15*s,16*s),0,math.pi,2)
        for side in (-1,1):
            pygame.draw.line(self.screen,cream,(x+side*18*s,y+15*s),(x+side*67*s,y+7*s),2);pygame.draw.line(self.screen,cream,(x+side*18*s,y+21*s),(x+side*67*s,y+25*s),2)
        pygame.draw.rect(self.screen,col("panel2"),pygame.Rect(x-57*s,y-58*s,114*s,15*s));pygame.draw.polygon(self.screen,col("panel2"),[(x-38*s,y-58*s),(x-24*s,y-78*s),(x+27*s,y-78*s),(x+42*s,y-58*s)]);pygame.draw.circle(self.screen,col("acid"),(int(x),int(y-65*s)),int(5*s))

    def draw_presentation(self,w,h):
        page=self.presentation_page;box=pygame.Rect(w//2-480,205,960,545);self.panel(box,"panel","acid",4);self.text("BRIEFING DU COMMANDANT MOUSTACHE",(box.x+28,box.y+20),"tiny","acid");self.text(f"{page+1} / 4",(box.right-28,box.y+20),"label","muted","topright")
        titles=["BIENVENUE DANS KITTEN FRONT","UNE ARMÉE DE POINTS","LE FRONT EST VIVANT","COMMANDEZ TOUTE LA GUERRE"];subs=["Le commandant Moustache vous confie le théâtre de Vardonne.","Simple à lire, libre à diriger : chaque point est une unité.","Villes, ravitaillement et encerclements redessinent la bataille.","Tactique immédiate et décisions nationales ne font qu'un."]
        self.text(titles[page],(box.x+36,box.y+56),"big","paper");self.text(subs[page],(box.x+38,box.y+101),"body","muted")
        area=pygame.Rect(box.x+35,box.y+145,box.width-300,285);self.panel(area,"bg")
        if page==0:
            for i in range(13):
                px=area.x+35+i*43;py=area.centery+math.sin(i*.75)*48;pygame.draw.circle(self.screen,col("blue" if i<6 else "red"),(int(px),int(py)),7)
            pygame.draw.lines(self.screen,col("paper"),False,[(area.x+20,area.centery+15),(area.x+150,area.centery-25),(area.x+285,area.centery+24),(area.x+430,area.centery-35),(area.right-20,area.centery+5)],3)
            self.text("DEUX ARMÉES · UNE LIGNE · VOTRE PLAN",(area.centerx,area.bottom-33),"label","gold","center")
        elif page==1:
            for i in range(12):pygame.draw.circle(self.screen,col("blue"),(area.x+75+(i%4)*38,area.y+72+(i//4)*38),8)
            pygame.draw.ellipse(self.screen,col("acid"),pygame.Rect(area.x+45,area.y+42,175,145),3);pygame.draw.lines(self.screen,col("acid"),False,[(area.x+150,area.y+120),(area.x+300,area.y+85),(area.x+455,area.y+150),(area.right-35,area.y+80)],4)
            for px,py in ((area.x+455,area.y+150),(area.right-35,area.y+80)):pygame.draw.circle(self.screen,col("red"),(px,py),9)
            self.text("ENCERCLEZ · TRACEZ · ESPACE POUR EXÉCUTER",(area.centerx,area.bottom-30),"label","acid","center")
        elif page==2:
            pygame.draw.lines(self.screen,col("paper"),False,[(area.x+280,area.y+18),(area.x+245,area.y+70),(area.x+310,area.y+120),(area.x+260,area.y+185),(area.x+300,area.bottom-18)],7)
            pygame.draw.lines(self.screen,col("bg"),False,[(area.x+280,area.y+18),(area.x+245,area.y+70),(area.x+310,area.y+120),(area.x+260,area.y+185),(area.x+300,area.bottom-18)],3)
            for px,py,owner in ((90,70,"blue"),(155,175,"blue"),(425,65,"red"),(510,170,"red")):
                pygame.draw.circle(self.screen,col(owner),(area.x+px,area.y+py),13);pygame.draw.circle(self.screen,col("gold"),(area.x+px,area.y+py),6)
            self.text("GARDEZ VOS POINTS RELIÉS AUX VILLES",(area.centerx,area.bottom-30),"label","gold","center")
        else:
            labels=[("NATION","Stabilité · mobilisation"),("RECHERCHE","Doctrine · logistique"),("PRODUCTION","Légers · lourds"),("9 MODES","Campagne · survie · bac à sable")]
            for i,(title,body) in enumerate(labels):
                r=pygame.Rect(area.x+18+(i%2)*315,area.y+20+(i//2)*105,295,88);self.panel(r,"panel2");self.text(title,(r.x+14,r.y+14),"strong","acid");self.text(body,(r.x+14,r.y+47),"small","muted")
        self.draw_kitten_commander((box.right-145,box.y+285),1.15);bubble=pygame.Rect(box.right-260,box.y+395,230,66);self.panel(bubble,"paper","paper",8);say=["Bienvenue, humain. Nos points comptent sur vous !","Une boucle choisit la troupe. Un trait lance l'offensive.","Une ligne fermée signifie souvent : encerclé !","Prêt ? Le quartier général vous attend."][page]
        for i,line in enumerate(self.wrap(say,30)):self.text(line,(bubble.x+12,bubble.y+11+i*18),"small","bg")
        self.button("presentation_skip",pygame.Rect(box.x+35,box.bottom-57,130,32),"PASSER")
        self.button("presentation_previous",pygame.Rect(box.centerx-130,box.bottom-57,110,32),"< RETOUR",False,page==0)
        self.button("presentation_next",pygame.Rect(box.centerx-8,box.bottom-57,235,32),"ENTRER AU QG  >" if page==3 else "SUIVANT  >",True)

    def draw_tutorial(self,mapr):
        steps=[("01 · SÉLECTIONNER","Maintenez le clic et tracez une boucle autour de points bleus.","Tous les points dans la boucle seront sélectionnés."),("02 · DESSINER L'OFFENSIVE","Depuis un point sélectionné, dessinez un chemin vers l'ennemi.","Les chemins peuvent contourner collines et forêts."),("03 · EXÉCUTER LES ORDRES","Appuyez sur ESPACE pour lancer tous les chemins préparés.","Les points se désélectionnent après l'ordre."),("04 · DÉFENDRE","Sélectionnez des points puis pressez S ou HALTE.","Une unité immobile perd moins de moral et subit moins de dégâts."),("05 · PRODUIRE","Cliquez sur CADENCE dans le panneau gauche.","Léger : 200 ECO · Lourd : 400 ECO."),("06 · TEMPS RÉEL","Choisissez >, >> ou >>> en bas.","La ligne de front suit la projection de puissance.")]
        title,body,tip=steps[self.tutorial];box=pygame.Rect(mapr.centerx-245,mapr.y+16,490,118);self.panel(box,"bg","acid",3);self.text(title,(box.x+14,box.y+12),"strong","acid");self.text(f"{self.tutorial+1}/6",(box.right-14,box.y+13),"label","muted","topright");self.text(body,(box.x+14,box.y+43),"body");self.text("ASTUCE · "+tip,(box.x+14,box.y+73),"tiny","muted");self.button("tutorial_skip",pygame.Rect(box.right-82,box.bottom-31,68,22),"PASSER")

    def draw_strategy(self,mapr):
        box=pygame.Rect(mapr.x+mapr.width*.06,mapr.y+mapr.height*.07,mapr.width*.88,mapr.height*.86);box=pygame.Rect(*map(int,box));self.panel(box,"bg","gold",2);self.text("ÉTAT-MAJOR DE L'ALLIANCE",(box.x+18,box.y+15),"title");self.button("close_strategy",pygame.Rect(box.right-44,box.y+10,30,30),"X")
        tabs=(("nation","NATION & FOCUS"),("research","RECHERCHE"),("production","INDUSTRIE & LOGISTIQUE"));tx=box.x+18;tw=(box.width-74)//3
        for key,label in tabs:self.button("tab_"+key,pygame.Rect(tx,box.y+54,tw,34),label,self.strategy==key);tx+=tw+5
        area=pygame.Rect(box.x+18,box.y+103,box.width-36,box.height-121)
        if self.strategy=="nation":self.strategy_nation(area)
        elif self.strategy=="research":self.strategy_research(area)
        else:self.strategy_production(area)

    def strategy_nation(self,a):
        g=self.game;left=pygame.Rect(a.x,a.y,a.width//2-6,a.height);right=pygame.Rect(a.centerx+6,a.y,a.width//2-6,a.height);self.panel(left,"panel2");self.panel(right,"panel2");self.text("ALLIANCE D'ORION",(left.x+18,left.y+18),"big");self.text("République fédérale · Guerre défensive",(left.x+18,left.y+53),"tiny","muted");y=left.y+90
        for name,val,color in (("STABILITÉ",g.stability,"blue"),("SOUTIEN À LA GUERRE",g.war_support,"red"),("BONUS DE PLANIFICATION",g.planning,"acid")):self.text(name,(left.x+18,y),"tiny","muted");self.text(f"{round(val)}%",(left.right-18,y),"label",color,"topright");self.bar(pygame.Rect(left.x+18,y+20,left.width-36,8),val,color);y+=65
        self.text("FOCUS NATIONAL ACTIF",(right.x+18,right.y+18),"tiny","gold");self.text(g.focus_name.upper(),(right.x+18,right.y+43),"title");self.bar(pygame.Rect(right.x+18,right.y+81,right.width-36,10),g.focus_progress,"gold");self.text("+18 commandement · +8 000 hommes",(right.x+18,right.y+106),"small","muted");label="MOBILISATION ACTIVE" if g.mobilized else "MOBILISATION GÉNÉRALE · 35 CMD";self.button("mobilize",pygame.Rect(right.x+18,right.bottom-58,right.width-36,40),label,not g.mobilized,g.mobilized)

    def strategy_research(self,a):
        g=self.game;self.text("BUREAUX DE RECHERCHE",(a.x,a.y),"title");rows=[("01","LOGISTIQUE",g.research_name,g.research_progress),("02","DOCTRINE","Guerre de mouvement",g.planning),("03","INGÉNIERIE","Fortifications de campagne",62)];y=a.y+40
        for num,kind,name,progress in rows:
            card=pygame.Rect(a.x,y,a.width,78);self.panel(card,"panel2");self.text(num,(card.x+14,card.centery),"big","gold","midleft");self.text(kind,(card.x+70,card.y+13),"tiny","muted");self.text(name,(card.x+70,card.y+34),"strong");self.bar(pygame.Rect(card.right-180,card.y+31,120,9),progress,"acid");self.text(f"{round(progress)}%",(card.right-16,card.y+27),"label","acid","topright");y+=87

    def strategy_production(self,a):
        g=self.game;avg=sum(p.supply for p in g.owned("blue"))/max(1,len(g.owned("blue")));cards=[("USINES",g.factories,"gold"),("ÉQUIPEMENT",round(g.equipment),"paper"),("RÉSERVES",f"{round(g.manpower/1000)}K","blue"),("RAVITAIL.",f"{round(avg)}%","acid")];cw=(a.width-18)//4
        for i,(name,val,color) in enumerate(cards):card=pygame.Rect(a.x+i*(cw+6),a.y,cw,78);self.panel(card,"panel2");self.text(name,(card.centerx,card.y+13),"tiny","muted","midtop");self.text(val,(card.centerx,card.y+38),"big",color,"midtop")
        y=a.y+105;self.text("LIGNES DE PRODUCTION",(a.x,y),"tiny","muted");y+=25
        for name,used,total,out in (("Fusils M41",g.factories,12,round(g.factories*(2.2+g.research_level*.25),1)),("Camions V-8",3,8,4.5),("Artillerie 90 mm",2,7,2.1)):
            card=pygame.Rect(a.x,y,a.width,48);self.panel(card,"panel2");self.text(name,(card.x+14,card.centery),"strong","paper","midleft");self.text("●"*min(used,12)+"○"*max(0,min(total-used,12)),(card.centerx,card.centery),"label","gold","center");self.text(f"+{out}/jour",(card.right-14,card.centery),"strong","acid","midright");y+=55
        self.button("strategy_factory",pygame.Rect(a.x,y+8,a.width,39),"+ RÉAFFECTER UNE USINE AUX FUSILS",True)

    def draw_toast(self):
        w,h=self.screen.get_size();box=pygame.Rect(w//2-180,h-105,360,42);self.panel(box,"bg","acid",3);self.text(self.toast,box.center,"label","paper","center")
    def draw_pause(self):
        shade=pygame.Surface(self.screen.get_size(),pygame.SRCALPHA);shade.fill((5,7,5,215));self.screen.blit(shade,(0,0));w,h=self.screen.get_size();box=pygame.Rect(w//2-245,h//2-250,490,500);self.panel(box,"bg","gold",3);self.text("PARTIE EN PAUSE",(box.centerx,box.y+42),"big","paper","center");self.text(self.objective_text(),(box.centerx,box.y+82),"small","muted","center");y=box.y+125
        for key,label,accent in (("resume","REPRENDRE",True),("save","SAUVEGARDER",False),("settings","PARAMÈTRES",False),("main_menu","SAUVEGARDER ET MENU",False),("quit","QUITTER LE JEU",False)):
            self.button(key,pygame.Rect(box.x+65,y,box.width-130,44),label,accent);y+=55
        self.text("ÉCHAP · reprendre",(box.centerx,box.bottom-27),"tiny","muted","center")
    def draw_end(self):
        shade=pygame.Surface(self.screen.get_size(),pygame.SRCALPHA);shade.fill((5,7,5,215));self.screen.blit(shade,(0,0));w,h=self.screen.get_size();box=pygame.Rect(w//2-300,h//2-190,600,380);self.panel(box,"bg","acid" if self.game.victory else "red",3);title="VICTOIRE DÉCISIVE" if self.game.victory else "OPÉRATION PERDUE";self.text(title,(box.centerx,box.y+55),"hero","acid" if self.game.victory else "red","center");self.text(f"{self.game.day} jours · {self.game.captures} prises · {len(self.battlefield.own_units('blue'))} points survivants",(box.centerx,box.y+130),"strong","paper","center");self.text(self.objective_text(),(box.centerx,box.y+164),"small","muted","center");self.button("replay",pygame.Rect(box.x+55,box.bottom-105,235,46),"REJOUER",True);self.button("main_menu",pygame.Rect(box.x+310,box.bottom-105,235,46),"MENU PRINCIPAL");self.button("quit",pygame.Rect(box.centerx-85,box.bottom-46,170,28),"QUITTER")

def run(): FrontlineGame().loop()
