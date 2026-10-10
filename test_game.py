import unittest
from pathlib import Path
from game_model import GameState
from dot_warfare import DotBattlefield
from save_system import load_game, load_settings, save_game, save_settings

class GameModelTests(unittest.TestCase):
    def test_campaign_starts_balanced(self):
        s=GameState.new_campaign(); self.assertEqual(len(s.owned("blue")),6); self.assertEqual(len(s.owned("red")),6)
    def test_valid_attack_spends_resources(self):
        s=GameState.new_campaign(); ok,_=s.launch_attack("rochefort","verdance"); self.assertTrue(ok); self.assertEqual(s.command,46); self.assertEqual(s.fuel,66)
    def test_invalid_non_adjacent_attack_is_rejected(self):
        s=GameState.new_campaign(); ok,_=s.launch_attack("aurelia","nova"); self.assertFalse(ok); self.assertFalse(s.battles)
    def test_reinforcement_has_cost(self):
        s=GameState.new_campaign(); ok,_=s.reinforce("dornes"); self.assertTrue(ok); self.assertEqual(s.manpower,83000)
    def test_capturing_enemy_capital_wins(self):
        s=GameState.new_campaign(); s.province("nova").owner="blue"; s.advance_day(); self.assertTrue(s.finished); self.assertTrue(s.victory)
    def test_mobilisation_trades_stability_for_reserves(self):
        s=GameState.new_campaign(); ok,_=s.mobilize(); self.assertTrue(ok); self.assertEqual(s.manpower,106000); self.assertEqual(s.stability,65); self.assertTrue(s.mobilized)
    def test_planning_bonus_is_stored_on_attack(self):
        s=GameState.new_campaign(); before=s.planning; ok,_=s.launch_attack("rochefort","verdance"); self.assertTrue(ok); self.assertEqual(s.battles[0].planning_bonus,before); self.assertLess(s.planning,before)

class DotWarfareTests(unittest.TestCase):
    def test_draw_then_commit_orders(self):
        s=GameState.new_campaign(); battle=DotBattlefield(s);unit=battle.own_units("blue")[0];battle.select_single(unit.uid);self.assertTrue(battle.draft_order([(unit.x,unit.y),(unit.x+80,unit.y)]));self.assertFalse(unit.path);self.assertEqual(battle.commit_orders(),1);self.assertTrue(unit.path);self.assertFalse(unit.selected)
    def test_stationary_defender_has_combat_advantage(self):
        s=GameState.new_campaign();battle=DotBattlefield(s);battle.units=[];attacker=battle.spawn("blue","light",400,300);defender=battle.spawn("red","light",420,300);attacker.path=[(500,300)];attacker.last_order=0;before_a=attacker.health;before_d=defender.health;battle._combat(1);self.assertGreater(before_a-attacker.health,before_d-defender.health);self.assertLess(attacker.morale,defender.morale)
    def test_front_line_is_generated_from_power_projection(self):
        battle=DotBattlefield(GameState.new_campaign());self.assertGreater(len(battle.front_segments()),5)
    def test_light_and_heavy_units_exist(self):
        battle=DotBattlefield(GameState.new_campaign());kinds={u.kind for u in battle.units};self.assertEqual(kinds,{"light","heavy"})
    def test_undefended_city_is_captured_by_occupation(self):
        s=GameState.new_campaign();battle=DotBattlefield(s);battle.units=[];city=s.province("verdance");battle.spawn("blue","light",city.x,city.y);battle._capture_cities(4.1);self.assertEqual(city.owner,"blue")
    def test_unit_density_changes_initial_armies(self):
        battle=DotBattlefield(GameState.new_campaign(),units_per_city=2);self.assertEqual(len(battle.units),24)
    def test_capture_duration_is_configurable(self):
        s=GameState.new_campaign();battle=DotBattlefield(s,capture_duration=2);battle.units=[];city=s.province("verdance");battle.spawn("blue","light",city.x,city.y);battle._capture_cities(2.1);self.assertEqual(city.owner,"blue")

class PersistenceTests(unittest.TestCase):
    def test_save_round_trip_preserves_campaign_and_units(self):
        path=Path(__file__).with_name("_test_save.json")
        try:
            game=GameState.new_campaign();field=DotBattlefield(game,"Maréchal",capture_duration=3);game.day=12;field.eco["blue"]=777;field.units[0].path=[(123,456)];save_game(game,field,{"mode":"scenario","scenario":"breakthrough"},path);loaded,battle,meta=load_game(path)
            self.assertEqual(loaded.day,12);self.assertEqual(battle.eco["blue"],777);self.assertEqual(battle.units[0].path,[(123,456)]);self.assertEqual(battle.difficulty,"Maréchal");self.assertEqual(battle.capture_duration,3);self.assertEqual(meta["scenario"],"breakthrough")
        finally:
            path.unlink(missing_ok=True);path.with_suffix(".json.tmp").unlink(missing_ok=True)
    def test_settings_merge_with_defaults(self):
        path=Path(__file__).with_name("_test_settings.json")
        try:
            save_settings({"fullscreen":True,"front_quality":"Basse","tooltips":False,"autosave":True,"default_difficulty":"Recrue"},path);settings=load_settings(path)
            self.assertTrue(settings["fullscreen"]);self.assertEqual(settings["front_quality"],"Basse");self.assertFalse(settings["tooltips"])
            self.assertEqual(settings["unit_density"],"Normale");self.assertTrue(settings["show_front"])
            self.assertFalse(settings["onboarding_complete"])
            self.assertEqual(settings["language"],"Français")
        finally:
            path.unlink(missing_ok=True);path.with_suffix(".json.tmp").unlink(missing_ok=True)
    def test_english_language_is_persisted(self):
        path=Path(__file__).with_name("_test_language.json")
        try:
            settings=load_settings(path);settings["language"]="English";save_settings(settings,path)
            self.assertEqual(load_settings(path)["language"],"English")
        finally:
            path.unlink(missing_ok=True);path.with_suffix(".json.tmp").unlink(missing_ok=True)

if __name__ == "__main__": unittest.main()
