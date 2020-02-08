 ##  -*- coding: utf-8 -*-

"""
TODO LATER...:
-Properly display modified movement values on screen
-Create functional ability button
-Fix GlobalVars.gamelog on-screen text overflow

-START ADDING ATTACK EFFECTS
    Priorities:
    -Fly / Fly Away / Telekinesis effects
    -Knockback / Psychic Shove
    -Markers
    -Status Affliction
    -Respin (forced, tactical, Swords Dance, Fire Spin, etc)
    -Swap (Abra, Gardevoir)
    -Draco Meteor effects

    DONE:
    -Simple Wait effects (Purple / Blue; other colors' simple Wait effects in place but not implemented yet)

-PACKAGING / HOSTING
    -UUUGGGHHHH

"""
from glob import iglob
from os.path import abspath, expanduser, join
import tkinter as tk
from tkinter import ttk
import arcade, json, sys, os, random, time

class GlobalConstants():
    def __init__(self):
        self.SPRITE_SCALING = 2.5
        self.SCREEN_WIDTH = 1440
        self.SCREEN_HEIGHT = 1024
        self.SCREEN_TITLE = "PoDu ReDux v0.1.3"
        self.STATS_PATH = join(abspath(expanduser(sys.path[0])), "pkmn-stats.json")
        self.PKMN_STATS = json.load(open(self.STATS_PATH, "r"))
        self.BG_PATH = join(abspath(expanduser(sys.path[0])), "images", "board", "backgrounds")


class GlobalVars():
    def __init__(self):
        self.loop_counter = 0
        self.valid_moves = []
        self.checked_moves = []
        self.click_counter = 0
        self.in_transit = ''
        self.in_transit_loc = ''
        self.potential_targets = []
        self.checked_targets = []
        self.move_click = False
        self.attack_click = False
        self.turn_player = random.randint(1,2)
        self.first_turn = True
        self.gamelog = []
        self.player_1_win = False
        self.player_2_win = False
        self.stats_x = 0
        self.stats_y = 0
        self.background_select = ''
        self.player_1_select = ''
        self.player_2_select = ''
        self.game_mode = ''
        self.evo_complete = False
        self.unit_attacked = False
        self.unit_moved = False
        self.player_1_team = None
        self.player_2_team = None
        self.top_range = None
        self.bottom_range = None
        self.attacker_current_spin = None
        self.defender_current_spin = None

class BoardNeighbors():
    """Create generic board spaces and assign list of neighbor spaces"""
    def __init__(self, coords, neighbors = {}):
        self.neighbors = neighbors
        self.coords = coords
        self.force_stop = False
        self.force_attack = False
        self.occupied = False
        self.occupant = ''
        self.occupant_team = 0
        self.passable = True
        self.ctrl_player = 0
        self.player_1_entry = False
        self.player_1_goal = False
        self.player_2_entry = False
        self.player_2_goal = False

class ClassicBoardGenerator():
    """
    Create board object with space labels and adjusted bools for special spaces

        NOTES ABOUT VALUE OF NEIGHBOR KEYS (long overdue / overlooked):
        
        -Example: board.A1.neighbors['B1'] is 1, which means that
        B1 is directly north of A1. Moving clockwise, 2 is
        NE, 3 is E, 4 is SE, etc etc until 8 for NW.
        
        -Knockback path checking uses this number. The yet unused
        knockback function checks the direction of the target space
        from the point of attack initiation for consideration of
        effects like Psychic Shove or my custom Donphan's
        charging mechanics.
    """
    def __init__(self):
        self.A1 = BoardNeighbors({'x': 290, 'y': 294}, {"B1":1, "B2":2, "A2":3})
        self.A1.player_1_entry = True
        self.A2 = BoardNeighbors({'x': 365, 'y': 293}, {"A1":7, "A3":3})
        self.A3 = BoardNeighbors({'x': 436, 'y': 293}, {"A2":7, "A4":3})
        self.A4 = BoardNeighbors({'x': 512, 'y': 293}, {"A3":7, "A5":3})
        self.A4.player_1_goal = True
        self.A5 = BoardNeighbors({'x': 586, 'y': 293}, {"A4":7, "A6":3, "B4":1})
        self.A6 = BoardNeighbors({'x': 658, 'y': 293}, {"A5":7, "A7":3})
        self.A7 = BoardNeighbors({'x': 732, 'y': 293}, {"A6":7, "B6":8, "B7":1})
        self.A7.player_1_entry = True
        
        self.B1 = BoardNeighbors({'x': 290, 'y': 414}, {"A1":5, "C1":1})
        self.B2 = BoardNeighbors({'x': 400, 'y': 414}, {"A1":6, "B4":3, "C2":1})
        self.B4 = BoardNeighbors({'x': 512, 'y': 414}, {"B2":7, "A5":5, "B6":3})
        self.B6 = BoardNeighbors({'x': 625, 'y': 414}, {"B4":7, "A7":5, "C6":1})
        self.B7 = BoardNeighbors({'x': 732, 'y': 414}, {"A7":5, "C7":1}) 
        
        self.C1 = BoardNeighbors({'x': 290, 'y': 514}, {"B1":5, "D1":1}) 
        self.C2 = BoardNeighbors({'x': 400, 'y': 514}, {"B2":5, "D2":1})
        self.C6 = BoardNeighbors({'x': 625, 'y': 514}, {"B6":5, "D6":1}) 
        self.C7 = BoardNeighbors({'x': 732, 'y': 514}, {"B7":5, "D7":1})
        
        self.D1 = BoardNeighbors({'x': 290, 'y': 614}, {"E1":1, "C1":5})
        self.D2 = BoardNeighbors({'x': 400, 'y': 614}, {"E1":8, "D4":3, "C2":5})
        self.D4 = BoardNeighbors({'x': 512, 'y': 614}, {"D2":7, "E3":1, "D6":3})
        self.D6 = BoardNeighbors({'x': 625, 'y': 614}, {"D4":7, "E7":2, "C6":5})
        self.D7 = BoardNeighbors({'x': 732, 'y': 614}, {"C7":5, "E7":1})
        
        self.E1 = BoardNeighbors({'x': 290, 'y': 731}, {"D1":5, "E2":3, "D2":4})
        self.E1.player_2_entry = True
        self.E2 = BoardNeighbors({'x': 365, 'y': 731}, {"E1":7, "E3":3})
        self.E3 = BoardNeighbors({'x': 436, 'y': 731}, {"E2":7, "E4":3, "D4":5})
        self.E4 = BoardNeighbors({'x': 512, 'y': 731}, {"E3":7, "E5":3})
        self.E4.player_2_goal = True
        self.E5 = BoardNeighbors({'x': 586, 'y': 731}, {"E4":7, "E6":3})
        self.E6 = BoardNeighbors({'x': 658, 'y': 731}, {"E5":7, "E7":3})
        self.E7 = BoardNeighbors({'x': 732, 'y': 731}, {"E6":7, "D6":6, "D7":5})
        self.E7.player_2_entry = True
        
        self.player_1_bench_1 = BoardNeighbors({'x': 311, 'y': 183}, {'A1':None, 'A7':None})
        self.player_1_bench_1.occupant = GlobalVars.player_1_team.pkmn1
        self.player_1_bench_1.occupant_team = 1
        self.player_1_bench_1.occupied = True
        self.player_1_bench_2 = BoardNeighbors({'x': 411, 'y': 183}, {'A1':None, 'A7':None})
        self.player_1_bench_2.occupant = GlobalVars.player_1_team.pkmn2
        self.player_1_bench_2.occupant_team = 1
        self.player_1_bench_2.occupied = True
        self.player_1_bench_3 = BoardNeighbors({'x': 511, 'y': 183}, {'A1':None, 'A7':None})
        self.player_1_bench_3.occupant = GlobalVars.player_1_team.pkmn3
        self.player_1_bench_3.occupant_team = 1
        self.player_1_bench_3.occupied = True
        self.player_1_bench_4 = BoardNeighbors({'x': 360, 'y': 110}, {'A1':None, 'A7':None})
        self.player_1_bench_4.occupant = GlobalVars.player_1_team.pkmn4
        self.player_1_bench_4.occupant_team = 1
        self.player_1_bench_4.occupied = True
        self.player_1_bench_5 = BoardNeighbors({'x': 460, 'y': 110}, {'A1':None, 'A7':None})
        self.player_1_bench_5.occupant = GlobalVars.player_1_team.pkmn5
        self.player_1_bench_5.occupant_team = 1
        self.player_1_bench_5.occupied = True
        self.player_1_bench_6 = BoardNeighbors({'x': 560, 'y': 110}, {'A1':None, 'A7':None})
        self.player_1_bench_6.occupant = GlobalVars.player_1_team.pkmn6
        self.player_1_bench_6.occupant_team = 1
        self.player_1_bench_6.occupied = True
        
        self.player_2_bench_1 = BoardNeighbors({'x': 715, 'y': 845}, {'E1':None, 'E7':None})
        self.player_2_bench_1.occupant = GlobalVars.player_2_team.pkmn1
        self.player_2_bench_1.occupant_team = 2
        self.player_2_bench_1.occupied = True
        self.player_2_bench_2 = BoardNeighbors({'x': 615, 'y': 845}, {'E1':None, 'E7':None})
        self.player_2_bench_2.occupant = GlobalVars.player_2_team.pkmn2
        self.player_2_bench_2.occupant_team = 2
        self.player_2_bench_2.occupied = True
        self.player_2_bench_3 = BoardNeighbors({'x': 515, 'y': 845}, {'E1':None, 'E7':None})
        self.player_2_bench_3.occupant = GlobalVars.player_2_team.pkmn3
        self.player_2_bench_3.occupant_team = 2
        self.player_2_bench_3.occupied = True
        self.player_2_bench_4 = BoardNeighbors({'x': 661, 'y': 921}, {'E1':None, 'E7':None})
        self.player_2_bench_4.occupant = GlobalVars.player_2_team.pkmn4
        self.player_2_bench_4.occupant_team = 2
        self.player_2_bench_4.occupied = True
        self.player_2_bench_5 = BoardNeighbors({'x': 561, 'y': 921}, {'E1':None, 'E7':None})
        self.player_2_bench_5.occupant = GlobalVars.player_2_team.pkmn5
        self.player_2_bench_5.occupant_team = 2
        self.player_2_bench_5.occupied = True
        self.player_2_bench_6 = BoardNeighbors({'x': 461, 'y': 921}, {'E1':None, 'E7':None})
        self.player_2_bench_6.occupant = GlobalVars.player_2_team.pkmn6
        self.player_2_bench_6.occupant_team = 2
        self.player_2_bench_6.occupied = True
        
        self.player_1_ultra_space_1 = BoardNeighbors({'x': 900, 'y': 280})
        self.player_1_ultra_space_2 = BoardNeighbors({'x': 975, 'y': 240})
        self.player_1_ultra_space_3 = BoardNeighbors({'x': 900, 'y': 185})
        self.player_1_ultra_space_4 = BoardNeighbors({'x': 975, 'y': 100})
        self.player_1_ultra_space_5 = BoardNeighbors({'x': 900, 'y': 140})
        self.player_1_ultra_space_6 = BoardNeighbors({'x': 975, 'y': 55})
        
        self.player_2_ultra_space_1 = BoardNeighbors({'x': 124, 'y': 752})
        self.player_2_ultra_space_2 = BoardNeighbors({'x': 50, 'y': 794})
        self.player_2_ultra_space_3 = BoardNeighbors({'x': 124, 'y': 843})
        self.player_2_ultra_space_4 = BoardNeighbors({'x': 50, 'y': 886})
        self.player_2_ultra_space_5 = BoardNeighbors({'x': 124, 'y': 940})
        self.player_2_ultra_space_6 = BoardNeighbors({'x': 50, 'y': 975})
        
        self.player_1_eliminated_1 = BoardNeighbors({'x': 124, 'y': 280})
        self.player_1_eliminated_2 = BoardNeighbors({'x': 50, 'y': 240})
        self.player_1_eliminated_3 = BoardNeighbors({'x': 124, 'y': 185})
        self.player_1_eliminated_4 = BoardNeighbors({'x': 50, 'y': 100})
        self.player_1_eliminated_5 = BoardNeighbors({'x': 124, 'y': 140})
        self.player_1_eliminated_6 = BoardNeighbors({'x': 50, 'y': 55})
        
        self.player_2_eliminated_1 = BoardNeighbors({'x': 900, 'y': 752})
        self.player_2_eliminated_2 = BoardNeighbors({'x': 975, 'y': 794})
        self.player_2_eliminated_3 = BoardNeighbors({'x': 900, 'y': 843})
        self.player_2_eliminated_4 = BoardNeighbors({'x': 975, 'y': 886})
        self.player_2_eliminated_5 = BoardNeighbors({'x': 900, 'y': 940})
        self.player_2_eliminated_6 = BoardNeighbors({'x': 975, 'y': 975})
        
        self.player_1_PC_1 = BoardNeighbors({'x': 645, 'y': 185})
        self.player_1_PC_2 = BoardNeighbors({'x': 727, 'y': 185})
        
        self.player_2_PC_1 = BoardNeighbors({'x': 380, 'y': 840})
        self.player_2_PC_2 = BoardNeighbors({'x': 297, 'y': 840})

class TvTBoardGenerator():
    ## 3v3 Board
    """Create board object with space labels and adjusted bools for special spaces"""
    def __init__(self):
        self.A1 = BoardNeighbors({'x': 290, 'y': 294}, {"B1":1, "B2":2, "A2":3})
        self.A1.player_1_entry = True
        self.A2 = BoardNeighbors({'x': 365, 'y': 293}, {"A1":7, "A3":3})
        self.A3 = BoardNeighbors({'x': 436, 'y': 293}, {"A2":7, "A4":3})
        self.A4 = BoardNeighbors({'x': 512, 'y': 293}, {"A3":7, "A5":3})
        self.A4.player_1_goal = True
        self.A5 = BoardNeighbors({'x': 586, 'y': 293}, {"A4":7, "A6":3})
        self.A6 = BoardNeighbors({'x': 658, 'y': 293}, {"A5":7, "A7":3})
        self.A6.player_1_entry = True
        self.A7 = BoardNeighbors({'x': 732, 'y': 293}, {"A6":7, "B6":8, "B7":1})
        
        self.B1 = BoardNeighbors({'x': 290, 'y': 414}, {"A1":5, "C1":1})
        self.B2 = BoardNeighbors({'x': 400, 'y': 414}, {"A1":6, "C2":1})
        self.B6 = BoardNeighbors({'x': 625, 'y': 414}, {"A7":5, "C6":1})
        self.B7 = BoardNeighbors({'x': 732, 'y': 414}, {"A7":5, "C7":1})
        
        self.C1 = BoardNeighbors({'x': 290, 'y': 514}, {"B1":5, "D1":1})
        self.C2 = BoardNeighbors({'x': 400, 'y': 514}, {"B2":5, "D2":1, "C4":3})
        self.C4 = BoardNeighbors({'x': 512, 'y': 512}, {"C2":7, "C6":3})
        self.C6 = BoardNeighbors({'x': 625, 'y': 514}, {"B6":5, "D6":1, "C4":7})
        self.C7 = BoardNeighbors({'x': 732, 'y': 514}, {"B7":5, "D7":1})
        
        self.D1 = BoardNeighbors({'x': 290, 'y': 614}, {"E1":1, "C1":5})
        self.D2 = BoardNeighbors({'x': 400, 'y': 614}, {"E1":8, "C2":5})
        self.D6 = BoardNeighbors({'x': 625, 'y': 614}, {"E7":2, "C6":5})
        self.D7 = BoardNeighbors({'x': 732, 'y': 614}, {"C7":5, "E7":1})
        
        self.E1 = BoardNeighbors({'x': 290, 'y': 731}, {"D1":5, "E2":3, "D2":4})
        self.E2 = BoardNeighbors({'x': 365, 'y': 731}, {"E1":7, "E3":3})
        self.E2.player_2_entry = True
        self.E3 = BoardNeighbors({'x': 436, 'y': 731}, {"E2":7, "E4":3})
        self.E4 = BoardNeighbors({'x': 512, 'y': 731}, {"E3":7, "E5":3})
        self.E4.player_2_goal = True
        self.E5 = BoardNeighbors({'x': 586, 'y': 731}, {"E4":7, "E6":3})
        self.E6 = BoardNeighbors({'x': 658, 'y': 731}, {"E5":7, "E7":3})
        self.E7 = BoardNeighbors({'x': 732, 'y': 731}, {"E6":7, "D6":6, "D7":5})
        self.E7.player_2_entry = True
        
        self.player_1_bench_1 = BoardNeighbors({'x': 311, 'y': 183}, {'A1':None, 'A6':None})
        self.player_1_bench_1.occupant = GlobalVars.player_1_team.pkmn1
        self.player_1_bench_1.occupant_team = 1
        self.player_1_bench_1.occupied = True
        self.player_1_bench_2 = BoardNeighbors({'x': 411, 'y': 183}, {'A1':None, 'A6':None})
        self.player_1_bench_2.occupant = GlobalVars.player_1_team.pkmn2
        self.player_1_bench_2.occupant_team = 1
        self.player_1_bench_2.occupied = True
        self.player_1_bench_3 = BoardNeighbors({'x': 511, 'y': 183}, {'A1':None, 'A6':None})
        self.player_1_bench_3.occupant = GlobalVars.player_1_team.pkmn3
        self.player_1_bench_3.occupant_team = 1
        self.player_1_bench_3.occupied = True
        
        self.player_2_bench_1 = BoardNeighbors({'x': 715, 'y': 845}, {'E2':None, 'E7':None})
        self.player_2_bench_1.occupant = GlobalVars.player_2_team.pkmn1
        self.player_2_bench_1.occupant_team = 2
        self.player_2_bench_1.occupied = True
        self.player_2_bench_2 = BoardNeighbors({'x': 615, 'y': 845}, {'E2':None, 'E7':None})
        self.player_2_bench_2.occupant = GlobalVars.player_2_team.pkmn2
        self.player_2_bench_2.occupant_team = 2
        self.player_2_bench_2.occupied = True
        self.player_2_bench_3 = BoardNeighbors({'x': 515, 'y': 845}, {'E2':None, 'E7':None})
        self.player_2_bench_3.occupant = GlobalVars.player_2_team.pkmn3
        self.player_2_bench_3.occupant_team = 2
        self.player_2_bench_3.occupied = True
        
        self.player_1_ultra_space_1 = BoardNeighbors({'x': 900, 'y': 280})
        self.player_1_ultra_space_2 = BoardNeighbors({'x': 975, 'y': 240})
        self.player_1_ultra_space_3 = BoardNeighbors({'x': 900, 'y': 185})
        
        self.player_2_ultra_space_1 = BoardNeighbors({'x': 124, 'y': 752})
        self.player_2_ultra_space_2 = BoardNeighbors({'x': 50, 'y': 794})
        self.player_2_ultra_space_3 = BoardNeighbors({'x': 124, 'y': 843})
        
        self.player_1_eliminated_1 = BoardNeighbors({'x': 124, 'y': 280})
        self.player_1_eliminated_2 = BoardNeighbors({'x': 50, 'y': 240})
        self.player_1_eliminated_3 = BoardNeighbors({'x': 124, 'y': 185})
        
        self.player_2_eliminated_1 = BoardNeighbors({'x': 900, 'y': 752})
        self.player_2_eliminated_2 = BoardNeighbors({'x': 975, 'y': 794})
        self.player_2_eliminated_3 = BoardNeighbors({'x': 900, 'y': 843})
        
        self.player_1_PC_1 = BoardNeighbors({'x': 681, 'y': 185})
        
        self.player_2_PC_1 = BoardNeighbors({'x': 336, 'y': 840})

class PlayerTeam():
    """Instantiate class that contains player 1 team and base stats."""
    ## WORKAROUND IMPLEMENTED DUE TO TEAM INSTANTIATION ISSUES BETWEEN PLAYERS
    def __init__(self, ctrl_player):

        team_file = eval(f"GlobalVars.player_{ctrl_player}_select")

        if GlobalVars.game_mode == "Classic":
            selected_team_path = join(abspath(expanduser(sys.path[0])), "saves", "classic_teams", f"{team_file}")
            GlobalVars.top_range = 1
            GlobalVars.bottom_range = 7
        elif GlobalVars.game_mode == "3v3":
            selected_team_path = join(abspath(expanduser(sys.path[0])), "saves", "3v3_teams", f"{team_file}")
            GlobalVars.top_range = 1
            GlobalVars.bottom_range = 4
        
        for x in range(GlobalVars.top_range, GlobalVars.bottom_range):
            exec(f"self.pkmn{x} = dict()")
            exec(f"self.pkmn{x}['loc'] = f'player_{ctrl_player}_bench_{x}'")
            exec(f"self.pkmn{x}['orig_loc'] = f'player_{ctrl_player}_bench_{x}'")
            exec(f"self.pkmn{x}['knocked_out'] = False")
            exec(f"self.pkmn{x}['is_surrounded'] = False")
            exec(f"self.pkmn{x}['to_PC'] = False")
            exec(f"self.pkmn{x}['to_eliminated'] = False")
            exec(f"self.pkmn{x}['to_ultra_space'] = False")
            exec(f"self.pkmn{x}['to_bench'] = False")
            exec(f"self.pkmn{x}['wait'] = int(0)")
            exec(f"self.pkmn{x}['in-play'] = False")
            exec(f"self.pkmn{x}['status'] = 'clear'")
            exec(f"self.pkmn{x}['markers'] = 'clear'")
            exec(f"self.pkmn{x}['ctrl'] = ctrl_player")
            exec(f"self.pkmn{x}['stage'] = 0")
            exec(f"self.pkmn{x}['final_song_count'] = None")
        
        custom_team = open(selected_team_path)
        custom_team = custom_team.read().splitlines()
        line_counter = 1
        GlobalVars.gamelog.append(f"Player {ctrl_player}'s team:")
        GlobalVars.gamelog.append(str("-"*8 + team_file[:-4] + "-"*8))
        for line in custom_team:
            exec(f"self.pkmn{line_counter}.update(GlobalConstants.PKMN_STATS['{line}'])")
            GlobalVars.gamelog.append(eval(f"GlobalConstants.PKMN_STATS['{line}']['name']"))
            line_counter += 1
            if GlobalVars.game_mode == "Classic" and line_counter == 7:
                break
            elif GlobalVars.game_mode == "3v3" and line_counter == 4:
                break
            else:
                continue
        for x in range(GlobalVars.top_range, GlobalVars.bottom_range):
            if eval(f"self.pkmn{x}['name']") == 'Reshiram' or eval(f"self.pkmn{x}['name']") == 'Zekrom':
                exec(f"self.pkmn{x}['wait'] = 9")
            for y in range(1,10):
                if eval(f"self.pkmn{x}['attack{y}power']") != 'null':
                    exec(f"self.pkmn{x}['attack{y}origpower'] = self.pkmn{x}['attack{y}power']")
                else:
                    exec(f"self.pkmn{x}['attack{y}origpower'] = 'null'")

def write_log():
    log_stamp = time.ctime()
    log_stamp = log_stamp.replace(' ', '_')
    log_stamp = log_stamp.replace(':', '-')
    LOG_PATH = join(abspath(expanduser(sys.path[0])), "saves", "gamelogs", "PoDuReDux_Log_" + f"{log_stamp}" + ".txt")
    LOG_FILE = open(LOG_PATH, "a+")
    for lines in GlobalVars.gamelog:
        lines = lines + "\n"
        LOG_FILE.write(lines)
    LOG_FILE.close()

#DRAFT EFFECTS
"""
def send_to_bench(target):
    target['loc']
    target['loc'] = target['orig_loc']
    target['status'] = 'clear'
    target['marker'] = 'clear'

def attack_respin():
    #For optional respinning like Deoxy-A or Double Chance
    pass

def attack_spin_effect():
    #For Fire Spin, Swords Dance, etc
    pass

def apply_marker():
    #For MP-X, Curse, Disguise, etc
    pass

def fly():
    #For selectable flight pathing (i.e. fly to space 1-2 spaces behind opponent)
    pass

def fly_away():
    #For pre-determined flight pathing (i.e. fly to space behind opponent)
    pass
    
def knockback():
    #For knockback resolution; implements knockback_pathing()
    pass

def knockback_pathing():
    #Check pathing for directional knockback effects
    direction = board.B2.neighbors["C2"]
    GlobalVars.valid_moves = []

    for x in board.C2.neighbors.keys():
        if board.C2.neighbors[x] == direction:
            GlobalVars.valid_moves.append(x)
        else:
            continue
    return GlobalVars.valid_moves
                    
    ## output -> ['D2']
"""

def pc_rotate(target):

    for pkmns in range(GlobalVars.top_range, GlobalVars.bottom_range):
        rotate_target = eval(f"GlobalVars.player_{target['ctrl']}_team.pkmn{pkmns}")
        if 'PC' in eval(f"GlobalVars.player_{target['ctrl']}_team.pkmn{pkmns}['loc']"):
            if rotate_target['loc'][-1] == str(2):
                rotate_target['loc'] = f"player_{target['ctrl']}_PC_1"
            else:
                rotate_target['loc'] = rotate_target['orig_loc']
                if rotate_target['wait'] >= 1:
                    rotate_target['wait'] += 1
                else:
                    rotate_target['wait'] += 2

def apply_wait(target, duration = 2):
    if target['wait'] > 0:
        target['wait'] += duration - 1
        GlobalVars.gamelog.append(f"{target['name']} gained Wait {duration - 1}.")
    else:
        target['wait'] += duration
        GlobalVars.gamelog.append(f"{target['name']} gained Wait {duration - 1}.")

def wait_tickdown():
    for x in range(1,3):
        for pkmns in range(GlobalVars.top_range, GlobalVars.bottom_range):
            if eval(f"GlobalVars.player_{x}_team.pkmn{pkmns}['wait']") != 0:
                exec(f"GlobalVars.player_{x}_team.pkmn{pkmns}['wait'] -= int(1)")

def apply_status(target, status_type = 'clear'):
    target['status'] = status_type

def surround_check(focal_unit):
    """Checks for surround conditions of a target space"""
    surround_counter = len(eval(f"board.{focal_unit['loc']}.neighbors.keys()"))
    for x in eval(f"board.{focal_unit['loc']}.neighbors.keys()"):
        if eval(f"board.{x}.occupied") == True and eval(f"board.{focal_unit['loc']}.ctrl_player") != eval(f"board.{x}.ctrl_player"):
            surround_counter -= 1
        else:
            continue
    if surround_counter == 0:
        return True
    else:
        return False

def path_check(loc, move, modifier = 0):
    """Check all possible paths for various purposes, including movement and teleports"""

    del GlobalVars.valid_moves[:]
    if GlobalVars.first_turn == True:
        modifier = -1
        GlobalVars.gamelog.append("First turn: Movement reduced by 1.")
    else:
        pass

    def path_iter(loc, move, modifier):
        next_moves = []
        for x in loc:
            if move + modifier == 0:
                break
            if eval(f"board.{x}.passable") == True:
                GlobalVars.valid_moves.append(x)
                for y in eval(f"board.{x}.neighbors.keys()"):
                    next_moves.append(y)
            else:
                continue
        GlobalVars.loop_counter += 1
        if GlobalVars.loop_counter < move + modifier:
            path_iter(next_moves, modifier, move)

    path_iter(loc, move, modifier)
    GlobalVars.checked_moves = set(GlobalVars.valid_moves)
    to_remove = []
    for possible_moves in GlobalVars.checked_moves:
        if eval(f"board.{possible_moves}.occupied") == True:
            to_remove.append(possible_moves)
        else:
            continue
    for invalid_move in to_remove:
        GlobalVars.checked_moves.remove(invalid_move)
    GlobalVars.valid_moves.clear()
    GlobalVars.loop_counter = 0
    
def spin(combatant):
    """Perform SPIN action for selected unit. Can be applied to effects and battles."""

    ## Perform number randomization for spin
    combatant_spin = random.randint(1,24)
    
    ## Iterate over wheel for maximum number of possible wheel segments for any unit (9)
    for wheel_numbers in range(1,10):
        ## Check if wheel segment is valid
        if eval(f"{combatant}['attack{wheel_numbers}range']") != "null":
            ## Pull wheel information from unit data and find segment
            ## ranges to check against combatant_spin
            if combatant_spin <= combatant[f'attack{wheel_numbers}range']:
                combatant_attack = wheel_numbers
                ## Returns segment number of SPIN result (wheel_numbers at correct iteration)
                return combatant_attack
                break
            else:
                continue
        else:
            break

def target_finder(combatant_loc, control_player, combatant_targets, attack_distance = 1):
    """
    Checks adjacent spaces for valid attack targets
    """
    
    def target_iter(combatant_targets, attack_distance):
        next_targets = []
        for x in combatant_targets:
            GlobalVars.potential_targets.append(x)
            for y in eval(f"board.{x}.neighbors.keys()"):
                next_targets.append(y)
            else:
                continue
        GlobalVars.loop_counter += 1
        if GlobalVars.loop_counter < attack_distance:
            target_iter(next_targets, attack_distance)

    if len(combatant_loc) == 2:
        GlobalVars.potential_targets = []
        target_iter(combatant_targets, attack_distance)
        to_remove = []
        for x in GlobalVars.potential_targets:
            if eval(f"board.{x}.occupied") == False:
                to_remove.append(x)
            elif eval(f"board.{x}.ctrl_player") == control_player:
                to_remove.append(x)
            elif eval(f"board.{x}.ctrl_player") == 0:
                to_remove.append(x)
        GlobalVars.potential_targets = set(GlobalVars.potential_targets).difference(to_remove)
    else:
        GlobalVars.potential_targets = []
    GlobalVars.loop_counter = 0

def battle_spin_compare(combatant_1, combatant_2):
    """
    Compare the SPIN of two battling units.

    'If' blocks check for color matchups, then nest down to check power stats when
    relevant (i.e. White vs. Gold)

    Returns the following for win checks:
        Tie: 0
        Attacker Win: 1
        Defender Win: 2
        Attacker Gold beats Purple: 3
        Defender Gold beats Purple: 4
        Attacker Purple or Blue Win: 5
        Defender Purple or Blue Win: 6
        Purple or Blue Tie: 7
    """

    combatant_1_attack = spin(combatant_1)
    GlobalVars.attacker_current_spin = combatant_1_attack
    combatant_2_attack = spin(combatant_2)
    GlobalVars.defender_current_spin = combatant_2_attack
    GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}'s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) attacked Player {combatant_2['ctrl']}'s {combatant_2['name']} ({combatant_2['orig_loc'][-1]})")
    
    if combatant_1['status'] != 'frozen':
        combatant_1_color = eval(f"combatant_1['attack{combatant_1_attack}color']")
    else:
        combatant_1_color = "Red"
        GlobalVars.gamelog.append(f"Player {combatant_1['ctrl']}s {combatant_1['name']} {combatant_1['orig_loc'][-1]} is frozen. Wheel has become Miss.")
    if not combatant_1_color == "Red" and not combatant_1_color == "Blue":
        combatant_1_power = eval(f"combatant_1['attack{combatant_1_attack}power']")
        if combatant_1_color == "White" or combatant_1_color == "Gold":
            if combatant_1['status'] == "poisoned" or combatant_1['status'] == "burned":
                combatant_1_power -= 20
            elif combatant_1['status'] == "noxious":
                combatant_1_power -= 40

    #Need to rework code to prevent procs of burned/paralyzed attack effects. Delphox miss effects need to be taken into heavy consideration
    #
    #Need to add check for attacks with same name
    if combatant_1['status'] == "paralyzed" or combatant_1['status'] == "burned":
        baseline_size = 24
        miss_candidates = []
        for x in range(1,10):
            if eval(f"combatant_1['attack{x}size']") != None:
                if eval(f"combatant_1['attack{x}color']") != "Red":
                    atk_size = eval(f"combatant_1['attack{x}size']")
                    if atk_size <= baseline_size:
                        baseline_size = atk_size
                        for y in miss_candidates:
                            if eval(f"combatant_1['attack{y}size']") > baseline_size:
                                miss_candidates.remove(y)
                        miss_candidates.append(x)
        miss_check = miss_candidates[random.randint(0, len(miss_candidates) - 1)]
        if miss_check == combatant_1_attack:
            combatant_1_color = "Red"
            combatant_1_miss_check = True
            if combatant_1['status'] == "burned":
                GlobalVars.gamelog.append(f"Player {combatant_1['ctrl']}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) is burned. Smallest segment has become Miss and attack power reduced by -20.")
            elif combatant_1['status'] == "paralyzed":
                GlobalVars.gamelog.append(f"Player {combatant_1['ctrl']}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) is paralyzed. Smallest segment has become Miss.")
        else:
            combatant_1_miss_check = False
    ## Checks for Confusion status and returns next available attack segment
    if combatant_1['status'] == 'confused':
        GlobalVars.gamelog.append(f"Player {combatant_1['ctrl']}s {combatant_1['name']} {combatant_1['orig_loc'][-1]} is confused. Attack has shifted one segment from {combatant_1[f'attack{combatant_1_attack}name']}.")
        combatant_1_attack += 1
        if eval(f"{combatant_1}['attack{combatant_1_attack}name']") == "null":
            combatant_1_attack = 1
    
    if combatant_2['status'] != 'frozen':
        combatant_2_color = eval(f"combatant_2['attack{combatant_2_attack}color']")
    else:
        combatant_2_color = 'Red'
        GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) is frozen. Wheel has become Miss.")
    if not combatant_2_color == "Red" and not combatant_2_color == "Blue":
        combatant_2_power = eval(f"combatant_2['attack{combatant_2_attack}power']")
        if combatant_2_color == "White" or combatant_2_color == "Gold":
            if combatant_2['status'] == "poisoned" or combatant_2['status'] == "burned":
                combatant_2_power -= 20
            elif combatant_2['status'] == "noxious":
                combatant_2_power -= 40

    if combatant_2['status'] == "paralyzed" or combatant_2['status'] == "burned":
        baseline_size = 24
        miss_candidates = []
        for x in range(1,10):
            if eval(f"combatant_2['attack{x}size']") != None:
                if eval(f"combatant_2['attack{x}color']") != "Red":
                    atk_size = eval(f"combatant_2['attack{x}size']")
                    if atk_size <= baseline_size:
                        baseline_size = atk_size
                        for y in miss_candidates:
                            if eval(f"combatant_2['attack{y}size']") > baseline_size:
                                miss_candidates.remove(y)
                        miss_candidates.append(x)
        miss_check = miss_candidates[random.randint(0, len(miss_candidates) - 1)]
        if miss_check == combatant_2_attack:
            combatant_2_color = "Red"
            combatant_2_miss_check = True
            if combatant_2['status'] == "burned":
                GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) is burned. Smallest segment has become Miss and attack power reduced by -20.")
            elif combatant_2['status'] == "paralyzed":
                GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) is paralyzed. Smallest segment has become Miss.")
        else:
            combatant_2_miss_check = False

    if combatant_2['status'] == 'confused':
        GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) is confused. Attack has shifted one segment from {combatant_2[f'attack{combatant_2_attack}name']}.")
        combatant_2_attack += 1
        if eval(f"{combatant_2}['attack{combatant_2_attack}name']") == "null":
            combatant__2_attack = 1
    
    if combatant_1['status'] == 'frozen':
        GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}'s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) spun Miss")
        GlobalVars.gamelog.append("    " + "Color: Red ----- Power: None")
    elif combatant_1['status'] == 'paralyzed' or combatant_1['status'] == 'burned':
        if combatant_1_miss_check == True:
            GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}'s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) spun Miss")
            GlobalVars.gamelog.append("    " + "Color: Red ----- Power: None")
        else:
            GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}'s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) spun {combatant_1[f'attack{combatant_1_attack}name']}")
            GlobalVars.gamelog.append("    " + f"Color: {combatant_1[f'attack{combatant_1_attack}color']} ----- Power: {combatant_1[f'attack{combatant_1_attack}power']}")
    else:
        GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}'s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) spun {combatant_1[f'attack{combatant_1_attack}name']}")
        GlobalVars.gamelog.append("    " + f"Color: {combatant_1[f'attack{combatant_1_attack}color']} ----- Power: {combatant_1[f'attack{combatant_1_attack}power']}")

    if combatant_2['status'] == 'frozen':
        GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}'s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) spun Miss")
        GlobalVars.gamelog.append("    " + "Color: Red ----- Power: None")
    elif combatant_2['status'] == 'paralyzed' or combatant_2['status'] == 'burned':
        if combatant_2_miss_check == True:
            GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}'s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) spun Miss")
            GlobalVars.gamelog.append("    " + "Color: Red ----- Power: None")
        else:
            GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}'s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) spun {combatant_2[f'attack{combatant_2_attack}name']}")
            GlobalVars.gamelog.append("    " + f"Color: {combatant_2[f'attack{combatant_2_attack}color']} ----- Power: {combatant_2[f'attack{combatant_2_attack}power']}")
    else:
        GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}'s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) spun {combatant_2[f'attack{combatant_2_attack}name']}")
        GlobalVars.gamelog.append("    " + f"Color: {combatant_2[f'attack{combatant_2_attack}color']} ----- Power: {combatant_2[f'attack{combatant_2_attack}power']}")
    
    if combatant_1_color == "White":
        if combatant_2_color == "White" or combatant_2_color == "Gold":
            if combatant_1_power > combatant_2_power:
                #Update other log entries here to this format
                GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
                return 1
            elif combatant_1_power < combatant_2_power:
                GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
                return 2
            elif combatant_1_power == combatant_2_power:
                GlobalVars.gamelog.append("Tie!")
                return 0
        elif combatant_2_color == "Purple":
            GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 6
        elif combatant_2_color == "Red":
            GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
            return 1
        elif combatant_2_color == "Blue":
            GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 6
        
    elif combatant_1_color == "Gold":
        if combatant_2_color == "White" or combatant_2_color == "Gold":
            if combatant_1_power > combatant_2_power:
                GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
                return 1
            elif combatant_1_power < combatant_2_power:
                GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
                return 2
            elif combatant_1_power == combatant_2_power:
                GlobalVars.gamelog.append("Tie!")
                return 0
        elif combatant_2_color == "Purple":
            GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
            return 3
        elif combatant_2_color == "Red":
            GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
            return 1
        elif combatant_2_color == "Blue":
            GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 6
        
    elif combatant_1_color == "Purple":
        if combatant_2_color == "Purple":
            if combatant_1_power > combatant_2_power:
                GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
                return 5
            elif combatant_1_power < combatant_2_power:
                GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
                return 6
            elif combatant_1_power == combatant_2_power:
                GlobalVars.gamelog.append("Tie!")
                return 7
        elif combatant_2_color == "White":
            GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
            return 5
        elif combatant_2_color == "Gold":
            GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 4
        elif combatant_2_color == "Red":
            GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
            return 5
        elif combatant_2_color == "Blue":
            GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 6

    elif combatant_1_color == "Blue":
        if combatant_2_color != "Blue":
            GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
            return 6
        else:
            GlobalVars.gamelog.append("Tie!")
            return 7

    elif combatant_1_color == "Red":
        if combatant_2_color == "White" or combatant_2_color == "Gold":
            GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 2
        elif combatant_2_color == "Purple" or combatant_2_color == "Blue":
            GlobalVars.gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 6
        elif combatant_2_color == "Red":
            GlobalVars.gamelog.append("Tie!")
            return 0

class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        
        self.background = None
        self.ClassicBoard = None
        self.TvTBoard = None

        #Create initial state of sprites for both teams
        for x in range(1,3):
            for y in range(GlobalVars.top_range, GlobalVars.bottom_range):
                exec(f"self.player_{x}_pkmn_{y} = None")

        self.pkmn_list = None
        
    def on_show(self):
        # Create your sprites and sprite lists here
        self.pkmn_list = arcade.SpriteList()
        
        for x in range(1,3):
            for y in range(GlobalVars.top_range,GlobalVars.bottom_range):
                pkmn_ref = eval(f"GlobalVars.player_{x}_team.pkmn{y}")
                pkmn_ref_x = eval(f"board.{pkmn_ref['loc']}.coords['x']")
                pkmn_ref_y = eval(f"board.{pkmn_ref['loc']}.coords['y']")
                sprite_file_name = pkmn_ref['spritefile']
                sprite_path = f"images/Sprites/{sprite_file_name}"
                exec(f"self.player_{x}_pkmn_{y} = arcade.Sprite('{sprite_path}', GlobalConstants.SPRITE_SCALING)")
                exec(f"self.player_{x}_pkmn_{y}.center_x = pkmn_ref_x")
                exec(f"self.player_{x}_pkmn_{y}.center_y = pkmn_ref_y")
                exec(f"self.pkmn_list.append(self.player_{x}_pkmn_{y})")

        self.background = arcade.load_texture(GlobalVars.background_select)
        if GlobalVars.game_mode == "Classic":
            self.ClassicBoard = arcade.load_texture("images/board/overlays/classic_duel_overlay.png")
        elif GlobalVars.game_mode == "3v3":
            self.TvTBoard = arcade.load_texture("images/board/overlays/3v3_duel_overlay.png")
    

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.

        text_offset_x = -20
        text_offset_y = 35
        circle_offset_x = -25
        circle_offset_y = 27
        
        arcade.start_render()
        arcade.draw_texture_rectangle(GlobalConstants.SCREEN_HEIGHT // 2, GlobalConstants.SCREEN_HEIGHT // 2,
                                      GlobalConstants.SCREEN_HEIGHT, GlobalConstants.SCREEN_HEIGHT, self.background)
        if GlobalVars.game_mode == "Classic":
            arcade.draw_texture_rectangle(GlobalConstants.SCREEN_HEIGHT // 2, GlobalConstants.SCREEN_HEIGHT // 2,
                                          GlobalConstants.SCREEN_HEIGHT, GlobalConstants.SCREEN_HEIGHT, self.ClassicBoard)
            center_text_x = 450
            center_text_y = 500
            
        elif GlobalVars.game_mode == "3v3":
            arcade.draw_texture_rectangle(GlobalConstants.SCREEN_HEIGHT // 2, GlobalConstants.SCREEN_HEIGHT // 2,
                                          GlobalConstants.SCREEN_HEIGHT, GlobalConstants.SCREEN_HEIGHT, self.TvTBoard)
            center_text_x = 450
            center_text_y = 369

        #draw unit bases
        for x in range(1,3):
            if x == 1:
                cir_color = arcade.color.AZURE
            elif x == 2:
                cir_color = arcade.color.RASPBERRY
            for y in range(GlobalVars.top_range, GlobalVars.bottom_range):
                pkmn_ref = eval(f"GlobalVars.player_{x}_team.pkmn{y}")
                pkmn_ref_loc = pkmn_ref['loc']
                pkmn_ref_x = eval(f"board.{pkmn_ref_loc}.coords['x']")
                pkmn_ref_y = eval(f"board.{pkmn_ref_loc}.coords['y']")
                exec(f"self.player_{x}_pkmn_{y}.center_x = pkmn_ref_x")
                exec(f"self.player_{x}_pkmn_{y}.center_y = pkmn_ref_y")
                exec(f"arcade.draw_circle_filled(self.player_{x}_pkmn_{y}.center_x, self.player_{x}_pkmn_{y}.center_y, 40, cir_color)")
                exec(f"arcade.draw_circle_filled(self.player_{x}_pkmn_{y}.center_x - circle_offset_x, self.player_{x}_pkmn_{y}.center_y - circle_offset_y, 12, arcade.color.BLUE_SAPPHIRE)")
                exec(f"arcade.draw_text(str(GlobalVars.player_{x}_team.pkmn{y}['move']), self.player_{x}_pkmn_{y}.center_x - text_offset_x, self.player_{x}_pkmn_{y}.center_y - text_offset_y, arcade.color.WHITE, 16)")

                #Wait circle and text draw
                if pkmn_ref['wait'] > 0:
                    exec(f"arcade.draw_circle_filled(self.player_{x}_pkmn_{y}.center_x + circle_offset_x, self.player_{x}_pkmn_{y}.center_y - circle_offset_y, 12, arcade.color.PURPLE)")
                    exec(f"arcade.draw_text(str(GlobalVars.player_{x}_team.pkmn{y}['wait']), self.player_{x}_pkmn_{y}.center_x + text_offset_x - 10, self.player_{x}_pkmn_{y}.center_y - text_offset_y, arcade.color.WHITE, 16)")

        line_counter = 0
        for lines in GlobalVars.gamelog[::-1]:
            lines_text = '\n'.join(lines[i:i+45] for i in range(0, len(lines), 45))
            line_counter += len(lines_text.split('\n'))
            arcade.draw_text(lines_text, 1030, 40 + line_counter*20, arcade.color.WHITE, font_name = "Arial")
            line_counter += 1
            if line_counter == 70:
                break

        if GlobalVars.player_1_win == True:
            center_text = "Player 1 Wins!"
        elif GlobalVars.player_2_win == True:
            center_text = "Player 2 Wins!"
        else:
            center_text = f"Player {GlobalVars.turn_player} turn."

        arcade.draw_text(center_text, center_text_x, center_text_y, arcade.color.YELLOW, 18)
        if GlobalVars.move_click == True:
            arcade.draw_text("Click this unit again\nto attack without moving,\nif able.", center_text_x - 15, center_text_y - 45, arcade.color.YELLOW, 12, align='center')
                
        if len(GlobalVars.checked_moves) > 0:
            for moves in GlobalVars.checked_moves:
                arcade.draw_circle_outline(eval(f"board.{moves}.coords['x']"), eval(f"board.{moves}.coords['y']"), 40, arcade.color.AMAZON, 5)
        if len(GlobalVars.potential_targets) > 0:
            for targets in GlobalVars.potential_targets:
                arcade.draw_circle_outline(eval(f"board.{targets}.coords['x']"), eval(f"board.{targets}.coords['y']"), 40, arcade.color.YELLOW , 5)
        # Call draw() on all your sprite lists below
        self.pkmn_list.draw()
            
    def evolution_check(self, winner):
        
        def evolution_popup(winner_name, evo_list):

            root = tk.Tk()
            root.title(f"Select Evolution for {winner_name}")

            def close_window():
                root.destroy()
            
            def evolution_submit(selection):
                GlobalVars.evo_complete = selection
                root.destroy()

            evo_cb = ttk.Combobox(root, values = evo_list)
            evo_cb.pack()
            evo_cb.set(evo_list[0])
            
            confirm_button = ttk.Button(root, text = "Select", command = lambda: evolution_submit(evo_cb.get()))
            confirm_button.pack()
            
            done_button = ttk.Button(root, text = "Cancel", command = close_window)
            done_button.pack()
            
            root.mainloop()

        evo_skip = False
        evo_list = []
        GlobalVars.evo_complete = False
        
        if eval(f"{winner}['evolutions']"):
            if len(eval(f"{winner}['evolutions']")) > 0:
                for evos in eval(f"{winner}['evolutions']"):
                    if ", Mega" in evos:
                        evo_skip = True
                if evo_skip == False:
                    winner_name = eval(f"{winner}['name']")
                    
                    self.pkmn_list.update()   
                    for evos in eval(f"{winner}['evolutions']"):
                        if ", Mega" not in evos:
                            evo_list.append(evos)
                    if len(evo_list) != 0:
                        evolution_popup(winner_name, evo_list)
                        if GlobalVars.evo_complete != False:
                            GlobalVars.gamelog.append(f"{winner_name} evolving to {GlobalVars.evo_complete}")
    
    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """

        if button == arcade.MOUSE_BUTTON_LEFT:
            if not GlobalVars.move_click and not GlobalVars.attack_click:
                if GlobalVars.turn_player == 1:
                    for units in dir(GlobalVars.player_1_team):
                        if units.startswith("pkmn"):
                            unit = eval(f"GlobalVars.player_1_team.{units}")
                            if unit['wait'] > 0:
                                continue
                            elif unit['status'] == 'sleep' or unit['status'] == 'frozen':
                                continue
                            else:
                                units_loc_str = unit['loc']
                                if x in range(eval(f"board.{units_loc_str}.coords['x']") - 40,
                                              eval(f"board.{units_loc_str}.coords['x']") + 40
                                              ) and y in range(
                                                  eval(f"board.{units_loc_str}.coords['y']") - 40,
                                                  eval(f"board.{units_loc_str}.coords['y']") + 40):
                                    GlobalVars.move_click = True
                                    GlobalVars.in_transit = unit
                                    GlobalVars.in_transit_combatant = GlobalVars.in_transit
                                    GlobalVars.in_transit_loc = GlobalVars.in_transit['loc']
                                    path_check(eval(f"board.{units_loc_str}.neighbors.keys()"), unit['move'])
                                    break
                elif GlobalVars.turn_player == 2:
                    for units in dir(GlobalVars.player_2_team):
                        if units.startswith("pkmn"):
                            unit = eval(f"GlobalVars.player_2_team.{units}")
                            if unit['wait'] > 0:
                                continue
                            elif unit['status'] == 'sleep' or unit['status'] == 'frozen':
                                continue
                            else:
                                units_loc_str = unit['loc']
                                if x in range(eval(f"board.{units_loc_str}.coords['x']") - 40,
                                              eval(f"board.{units_loc_str}.coords['x']") + 40
                                              ) and y in range(
                                                  eval(f"board.{units_loc_str}.coords['y']") - 40,
                                                  eval(f"board.{units_loc_str}.coords['y']") + 40):
                                    GlobalVars.move_click = True
                                    GlobalVars.in_transit = unit
                                    GlobalVars.in_transit_combatant = GlobalVars.in_transit
                                    GlobalVars.in_transit_loc = GlobalVars.in_transit['loc']
                                    path_check(eval(f"board.{units_loc_str}.neighbors.keys()"), unit['move'])
                                    break

                        
            elif GlobalVars.move_click:
                for moves in GlobalVars.checked_moves:
                    #Make space clearing its own function?
                    if x in range(eval(f"board.{moves}.coords['x']") - 40, eval(f"board.{moves}.coords['x']") + 40) and y in range(
                                        eval(f"board.{moves}.coords['y']") - 40, eval(f"board.{moves}.coords['y']") + 40) and eval(
                                        f"board.{moves}.occupied") == False:
                        GlobalVars.unit_moved = True
                        GlobalVars.gamelog.append(f"Player {GlobalVars.turn_player}'s " +  eval(f"{GlobalVars.in_transit}['name']") +  " (" + str(eval(f"{GlobalVars.in_transit}['orig_loc'][-1]")) + ") "+ f"moved to {moves}.")
                        exec(f"board.{GlobalVars.in_transit_loc}.occupied = False")
                        exec(f"board.{GlobalVars.in_transit_loc}.occupant = ''")
                        exec(f"board.{GlobalVars.in_transit_loc}.occupant_team = 0")
                        exec(f"board.{GlobalVars.in_transit_loc}.ctrl_player = 0")
                        exec(f"board.{GlobalVars.in_transit_loc}.passable = True")
                        exec(f"board.{moves}.occupied = True")
                        exec(f"board.{moves}.occupant = GlobalVars.in_transit")
                        exec(f"board.{moves}.occupant_team = GlobalVars.in_transit['ctrl']")
                        exec(f"board.{moves}.ctrl_player = GlobalVars.in_transit['ctrl']")
                        exec(f"board.{moves}.passable = False")
                        GlobalVars.in_transit['loc'] = moves
                        GlobalVars.in_transit_loc = GlobalVars.in_transit['loc']
                        for surround_neighbors in dir(board):
                            if len(surround_neighbors) == 2:
                                surround_target = eval(f"board.{surround_neighbors}.occupant")
                                if surround_target:
                                    surround_target['is_surrounded'] = surround_check(surround_target)
                        for team in range(1,3):
                            for surround_resolve_target in eval(f"dir(GlobalVars.player_{team}_team)"):
                                if surround_resolve_target.startswith('pkmn'):
                                    surround_resolve = eval(f"GlobalVars.player_{team}_team.{surround_resolve_target}")
                                    winner_ctrl = surround_resolve['loc']
                                    if surround_resolve['is_surrounded'] == True:
                                        GlobalVars.gamelog.append(str(f"SURROUNDED:    Player {team}'s " +
                                              surround_resolve['name'] + " (" +
                                                f"{surround_resolve}"[-1] +
                                                ") " +
                                              f" was sent to Player {team}'s PC."))
                                        exec(f"board.{surround_resolve['loc']}.occupied = False")
                                        exec(f"board.{surround_resolve['loc']}.occupant = ''")
                                        exec(f"board.{surround_resolve['loc']}.occupant_team = 0")
                                        exec(f"board.{surround_resolve['loc']}.ctrl_player = 0")
                                        exec(f"board.{surround_resolve['loc']}.passable = True")
                                        pc_rotate(surround_resolve)
                                        if GlobalVars.game_mode == "Classic":
                                            surround_resolve['loc'] = f'player_{team}_PC_2'
                                        elif GlobalVars.game_mode == "3v3":
                                            surround_resolve['loc'] = f'player_{team}_PC_1'
                                        surround_resolve['is_surrounded'] = False
                        target_finder(GlobalVars.in_transit['loc'], GlobalVars.in_transit['ctrl'], eval(f"board.{GlobalVars.in_transit['loc']}.neighbors.keys()"))
                        if len(GlobalVars.potential_targets) > 0:
                            GlobalVars.attack_click = True
                        else:
                            linebreak_text = '='*5
                            if GlobalVars.turn_player == 1:
                                GlobalVars.turn_player = 2
                                GlobalVars.gamelog.append(f"{linebreak_text} Player {GlobalVars.turn_player} Turn {linebreak_text}")
                                wait_tickdown()
                                if GlobalVars.first_turn:
                                    if len(GlobalVars.in_transit_loc) == 2:
                                        GlobalVars.first_turn = False
                            elif GlobalVars.turn_player == 2:
                                GlobalVars.turn_player = 1
                                GlobalVars.gamelog.append(f"{linebreak_text} Player {GlobalVars.turn_player} Turn {linebreak_text}")
                                wait_tickdown()
                                if GlobalVars.first_turn:
                                    if len(GlobalVars.in_transit_loc) == 2:
                                        GlobalVars.first_turn = False
                            GlobalVars.in_transit = ''
                            GlobalVars.in_transit_loc = ''
                            GlobalVars.unit_moved = False
                            GlobalVars.unit_attacked = False

                    elif len(GlobalVars.in_transit_loc) == 2 and x in range(eval(f"board.{GlobalVars.in_transit_loc}.coords['x']") - 40,
                                                                      eval(f"board.{GlobalVars.in_transit_loc}.coords['x']") + 40) and y in range(
                                                                        eval(f"board.{GlobalVars.in_transit_loc}.coords['y']") - 40,
                                                                        eval(f"board.{GlobalVars.in_transit_loc}.coords['y']") + 40):
                        target_finder(GlobalVars.in_transit['loc'], GlobalVars.in_transit['ctrl'], eval(f"board.{GlobalVars.in_transit['loc']}.neighbors.keys()"))
                        if len(GlobalVars.potential_targets) > 0:
                            GlobalVars.attack_click = True
                        else:
                            GlobalVars.in_transit = ''
                            GlobalVars.in_transit_loc = ''
                            GlobalVars.move_click = False
                            GlobalVars.potential_targets = []
                        

                GlobalVars.move_click = False
                GlobalVars.checked_moves = []
                
                self.pkmn_list.update()

            elif GlobalVars.attack_click:
                for targets in GlobalVars.potential_targets:
                    if x in range(eval(f"board.{targets}.coords['x']") - 40, eval(f"board.{targets}.coords['x']") + 40) and y in range(
                                        eval(f"board.{targets}.coords['y']") - 40, eval(f"board.{targets}.coords['y']") + 40):
                        GlobalVars.unit_attacked = True
                        winner_check = battle_spin_compare(GlobalVars.in_transit_combatant, eval(f'board.{targets}.occupant'))
                        #Add effects checks
                        if winner_check == 0:
                            pass
                        
                        if winner_check == 1:
                            winner_ctrl = GlobalVars.in_transit['ctrl']
                            loser_ctrl_temp = eval(f"board.{targets}.occupant")
                            loser_ctrl = loser_ctrl_temp['ctrl']
                            GlobalVars.gamelog.append(f"Player {loser_ctrl}s {loser_ctrl_temp['name']} was sent to the PC.")
                            exec(f"board.{targets}.occupied = False")
                            exec(f"board.{targets}.occupant = ''")
                            exec(f"board.{targets}.occupant_team = 0")
                            exec(f"board.{targets}.ctrl_player = 0")
                            exec(f"board.{targets}.passable = True")
                            pc_rotate(loser_ctrl_temp)
                            if GlobalVars.game_mode == "Classic":
                                exec(f"loser_ctrl_temp['loc'] = 'player_{loser_ctrl}_PC_2'")
                            elif GlobalVars.game_mode == "3v3":
                                exec(f"loser_ctrl_temp['loc'] = 'player_{loser_ctrl}_PC_1'")
                            self.evolution_check(GlobalVars.in_transit)
                            if GlobalVars.evo_complete:
                                GlobalVars.in_transit.update(GlobalConstants.PKMN_STATS[f'{GlobalVars.evo_complete}'])
                                new_evo_path = GlobalVars.in_transit['spritefile']
                                GlobalVars.in_transit['stage'] += 1

                                for x in range(1,10):
                                    if type(GlobalVars.in_transit[f'attack{x}power']) == int:
                                        if GlobalVars.in_transit[f'attack{x}color'] == 'White' or GlobalVars.in_transit[f'attack{x}color'] == 'Gold':
                                            GlobalVars.in_transit[f'attack{x}power'] += 10*GlobalVars.in_transit['stage']
                                        elif GlobalVars.in_transit[f'attack{x}color'] == 'Purple':
                                            GlobalVars.in_transit[f'attack{x}power'] += 1*GlobalVars.in_transit['stage']
                                    else:
                                        continue
                                    
                                exec(f"self.pkmn_list.remove(self.player_{winner_ctrl}_pkmn_{GlobalVars.in_transit['orig_loc'][-1]})")
                                exec(f"self.player_{winner_ctrl}_pkmn_{GlobalVars.in_transit['orig_loc'][-1]} = arcade.Sprite('images/sprites/{new_evo_path}', GlobalConstants.SPRITE_SCALING)")
                                exec(f"self.pkmn_list.append(self.player_{winner_ctrl}_pkmn_{GlobalVars.in_transit['orig_loc'][-1]})")
                                self.pkmn_list.update()
                        elif winner_check == 2:
                            winner_ctrl_temp = eval(f"board.{targets}.occupant")
                            winner_ctrl = winner_ctrl_temp['ctrl']
                            loser_ctrl = GlobalVars.in_transit['ctrl']
                            GlobalVars.gamelog.append(f"Player {loser_ctrl}s {GlobalVars.in_transit['name']} was sent to the PC.")
                            exec(f"board.{GlobalVars.in_transit_loc}.occupied = False")
                            exec(f"board.{GlobalVars.in_transit_loc}.occupant = ''")
                            exec(f"board.{GlobalVars.in_transit_loc}.occupant_team = 0")
                            exec(f"board.{GlobalVars.in_transit_loc}.ctrl_player = 0")
                            exec(f"board.{GlobalVars.in_transit_loc}.passable = True")
                            pc_rotate(GlobalVars.in_transit)
                            if GlobalVars.game_mode == "Classic":
                                GlobalVars.in_transit['loc'] = f'player_{loser_ctrl}_PC_2'
                            elif GlobalVars.game_mode == "3v3":
                                GlobalVars.in_transit['loc'] = f'player_{loser_ctrl}_PC_1'
                            self.evolution_check(winner_ctrl_temp)
                            if GlobalVars.evo_complete:
                                winner_ctrl_temp.update(GlobalConstants.PKMN_STATS[f'{GlobalVars.evo_complete}'])
                                new_evo_path = winner_ctrl_temp['spritefile']
                                winner_ctrl_temp['stage'] += 1

                                for x in range(1,10):
                                    if type(winner_ctrl_temp[f'attack{x}power']) == int:
                                        if winner_ctrl_temp[f'attack{x}color'] == 'White' or winner_ctrl_temp[f'attack{x}color'] == 'Gold':
                                            winner_ctrl_temp[f'attack{x}power'] += 10*winner_ctrl_temp['stage']
                                        elif winner_ctrl_temp[f'attack{x}color'] == 'Purple':
                                            winner_ctrl_temp[f'attack{x}power'] += 1*winner_ctrl_temp['stage']
                                    else:
                                        continue
                                    
                                exec(f"self.pkmn_list.remove(self.player_{winner_ctrl}_pkmn_{winner_ctrl_temp['orig_loc'][-1]})")
                                exec(f"self.player_{winner_ctrl}_pkmn_{winner_ctrl_temp['orig_loc'][-1]} = arcade.Sprite('images/sprites/{new_evo_path}', GlobalConstants.SPRITE_SCALING)")
                                exec(f"self.pkmn_list.append(self.player_{winner_ctrl}_pkmn_{winner_ctrl_temp['orig_loc'][-1]})")
                                self.pkmn_list.update()
                        elif winner_check == 3:
                            pass
                        elif winner_check == 4:
                            pass
                        elif winner_check == 5:
                            effect_user = GlobalVars.in_transit
                            target_opponent = eval(f"board.{targets}.occupant")
                            if len(effect_user[f'attack{GlobalVars.attacker_current_spin}funcs']) != 0:
                                for effects in effect_user[f'attack{GlobalVars.attacker_current_spin}funcs']:
                                    exec(effects)
                        elif winner_check == 6:
                            effect_user = eval(f"board.{targets}.occupant")
                            target_opponent = GlobalVars.in_transit
                            if len(effect_user[f'attack{GlobalVars.defender_current_spin}funcs']) != 0:
                                for effects in effect_user[f'attack{GlobalVars.defender_current_spin}funcs']:
                                    exec(effects)
                        elif winner_check == 7:
                            pass

                if GlobalVars.unit_moved or GlobalVars.unit_attacked:
                    linebreak_text = "="*5
                    if GlobalVars.turn_player == 1:
                        GlobalVars.turn_player = 2
                        GlobalVars.gamelog.append(f"{linebreak_text} Player {GlobalVars.turn_player} Turn {linebreak_text}")
                        wait_tickdown()
                    elif GlobalVars.turn_player == 2:
                        GlobalVars.turn_player = 1
                        GlobalVars.gamelog.append(f"{linebreak_text} Player {GlobalVars.turn_player} Turn {linebreak_text}")
                        wait_tickdown()
                GlobalVars.attack_click = False
                GlobalVars.in_transit = ''
                GlobalVars.in_transit_loc = ''
                GlobalVars.potential_targets = []
                GlobalVars.unit_moved = False
                GlobalVars.unit_attacked = False
                GlobalVars.attack_click = False
                
                self.pkmn_list.update()

            if GlobalVars.player_1_win == True or GlobalVars.player_2_win == True:
                arcade.close_window()
                exit()
            
            if board.A4.ctrl_player == 2:
                GlobalVars.player_2_win = True
                GlobalVars.gamelog.append("Player 2 wins! Click anywhere to exit.")
                write_log()
                self.pkmn_list.update()
                
            elif board.E4.ctrl_player == 1:
                GlobalVars.player_1_win = True
                GlobalVars.gamelog.append("Player 1 wins! Click anywhere to exit.")
                write_log()
                self.pkmn_list.update()

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            for team in range(1,3):
                for units in dir(eval(f"GlobalVars.player_{team}_team")):
                    if units.startswith("pkmn"):
                        unit = eval(f"GlobalVars.player_{team}_team.{units}")
                        units_loc_str = unit['loc']
                        if x in range(eval(f"board.{units_loc_str}.coords['x']") - 40,
                                      eval(f"board.{units_loc_str}.coords['x']") + 40
                                      ) and y in range(
                                          eval(f"board.{units_loc_str}.coords['y']") - 40,
                                          eval(f"board.{units_loc_str}.coords['y']") + 40):
                            stats_window(unit)
                            break

def main():
    """ Main method """
    window = arcade.Window(GlobalConstants.SCREEN_WIDTH, GlobalConstants.SCREEN_HEIGHT, "Game Start")
    game = GameView()
    window.show_view(game)  
    arcade.run()

def on_select_team(player_num, event = None):

    if event:
        if player_num == 1:
            GlobalVars.player_1_select = event.widget.get()
        elif player_num == 2:
            GlobalVars.player_2_select = event.widget.get()

def mode_select():
    
    def button_click():
        if var.get() == '3v3':
            GlobalVars.game_mode = '3v3'

        elif var.get() == 'Classic':
            GlobalVars.game_mode = 'Classic'

        GlobalVars.background_select = f"images/board/backgrounds/{bg_cb.get()}.png"
        root.destroy()
    
    root = tk.Tk()
    root.title("PoDuReDux: Game Mode Select")

    var = tk.StringVar()
    var.set('1')

    try:
        fn = lambda x: x.split('/')[-1][:-4]
        background_textures = {fn(k) : k for k in iglob(GlobalConstants.BG_PATH + "/**/*.png", recursive=True)}
        
    except:
        pass

    background_list = []
    
    for items in background_textures.values():
        background_list.append(items[len(GlobalConstants.BG_PATH)+1:-4])

    bg_label = ttk.Label(root, text = "Choose Background image from drop-down:")
    bg_label.pack()

    bg_cb = ttk.Combobox(root, values = background_list)
    bg_cb.set(background_list[0])
    bg_cb.pack()
    
    mode_select_label = ttk.Label(root, text = "Choose Game Mode:")
    mode_select_label.pack()

    mode_select_classic_radio = ttk.Radiobutton(root, text = "Classic", variable = var, value = "Classic")
    mode_select_classic_radio.pack()
    mode_select_classic_radio.invoke()

    mode_select_3v3_radio = ttk.Radiobutton(root, text = "3v3", variable = var, value = "3v3")
    mode_select_3v3_radio.pack()
    
    mode_select_confirm = ttk.Button(root, text = "Confirm", command = button_click)
    mode_select_confirm.pack()

    root.mainloop()

def startup_window():

    def button_click():
        
        GlobalVars.player_1_select = p1team_cb.get()
        GlobalVars.player_2_select = p2team_cb.get()
        root.destroy()
    
    root = tk.Tk()
    root.title(f"PoDuReDux: Team Select ({GlobalVars.game_mode})")

    p1team_label = ttk.Label(root, text = "Player 1 Team:")
    p1team_label.grid(row = 0, column = 0, padx = 30, pady = (30, 10))

    p2team_label = ttk.Label(root, text = "Player 2 Team:")
    p2team_label.grid(row = 0, column = 2, padx = 30, pady = (30, 10))
    
    p1team_cb = ttk.Combobox(root, values = team_list)
    p1team_cb.set(team_list[0])
    p1team_cb.grid(row=1, column=0, padx = 30, pady = 10)
    p1team_cb.bind('<<ComboboxSelected>>', on_select_team(1))

    p2team_cb = ttk.Combobox(root, values = team_list)
    p2team_cb.set(team_list[0])
    p2team_cb.grid(row=1, column=2, padx = 30, pady = 10)
    p2team_cb.bind('<<ComboboxSelected>>', on_select_team(2))
    
    gamestart_button = ttk.Button(root, text = "Start Game", command = button_click)
    gamestart_button.grid(row=3, column=1, padx = 30, pady = (10, 30))
    
    root.mainloop()
def stats_window(target_figure):

    root = tk.Tk()
    root.title("Stats Window")

    GlobalVars.loop_counter = 0
    column_var = 0
    for attribute in target_figure.keys():
        if attribute.startswith("attack") == False:
            attr_val = target_figure[attribute]
            if attribute == 'ability':
                attr_val = '\n'.join(attr_val[i:i+30] for i in range(0, len(attr_val), 30))
            if attr_val != None:
                attr_str = str(attribute)
                attr_str = attr_str.replace('-', "_")
                exec(f"{attr_str}_label = ttk.Label(root, text = attr_str)")
                exec(f"{attr_str}_label.grid(row = GlobalVars.loop_counter, column = column_var)")
                exec(f"{attr_str}_content = ttk.Label(root, text = attr_val)")
                exec(f"{attr_str}_content.grid(row = GlobalVars.loop_counter, column = column_var + 1)")
        GlobalVars.loop_counter += 1
    
    for attr_index in range(1,10):
        if target_figure[f'attack{attr_index}name'] != None:

            effect_text = target_figure[f'attack{attr_index}effect']
            if effect_text != None:
                effect_text = '\n'.join(effect_text[i:i+30] for i in range(0, len(effect_text), 30))
            
            
            #Name
            exec(f"attack{attr_index}name_label = ttk.Label(root, text = f'Attack {attr_index} Name:')")
            exec(f"attack{attr_index}name_label.grid(row = GlobalVars.loop_counter, column = 0)")
            exec(f"attack{attr_index}name_content = ttk.Label(root, text = target_figure['attack{attr_index}name'])")
            exec(f"attack{attr_index}name_content.grid(row = GlobalVars.loop_counter + 1, column = 0)")

            #Color
            exec(f"attack{attr_index}color_label = ttk.Label(root, text = f'Attack {attr_index} Color:')")
            exec(f"attack{attr_index}color_label.grid(row = GlobalVars.loop_counter, column = 1)")
            exec(f"attack{attr_index}color_content = ttk.Label(root, text = target_figure['attack{attr_index}color'])")
            exec(f"attack{attr_index}color_content.grid(row = GlobalVars.loop_counter + 1, column = 1)")

            #Size
            exec(f"attack{attr_index}size_label = ttk.Label(root, text = f'Attack {attr_index} Size:')")
            exec(f"attack{attr_index}size_label.grid(row = GlobalVars.loop_counter, column = 2)")
            exec(f"attack{attr_index}size_content = ttk.Label(root, text = target_figure['attack{attr_index}size'])")
            exec(f"attack{attr_index}size_content.grid(row = GlobalVars.loop_counter + 1, column = 2)")

            #Power
            exec(f"attack{attr_index}power_label = ttk.Label(root, text = f'Attack {attr_index} Power:')")
            exec(f"attack{attr_index}power_label.grid(row = GlobalVars.loop_counter, column = 3)")
            exec(f"attack{attr_index}power_content = ttk.Label(root, text = target_figure['attack{attr_index}power'])")
            exec(f"attack{attr_index}power_content.grid(row = GlobalVars.loop_counter + 1, column = 3)")

            #Effect
            exec(f"attack{attr_index}effect_label = ttk.Label(root, text = f'Attack {attr_index} Effect:')")
            exec(f"attack{attr_index}effect_label.grid(row = GlobalVars.loop_counter, column = 4)")
            exec(f"attack{attr_index}effect_content = ttk.Label(root, text = effect_text)")
            exec(f"attack{attr_index}effect_content.grid(row = GlobalVars.loop_counter + 1, column = 4)")

            GlobalVars.loop_counter += 2

    GlobalVars.loop_counter = 0

    display_img = tk.PhotoImage(file = f"images/Sprites/{target_figure['spritefile']}")
    img_label = ttk.Label(root, image = display_img)
    img_label.grid(row = 2, column = 4)
    root.mainloop()
if __name__ == "__main__":

    GlobalConstants = GlobalConstants()
    GlobalVars = GlobalVars()

    mode_select()
    
    team_list = []
    if GlobalVars.game_mode == "Classic":
        for x in os.listdir(join(abspath(expanduser(sys.path[0])), "saves", "classic_teams")):
            team_list.append(x)
    elif GlobalVars.game_mode == "3v3":
        for x in os.listdir(join(abspath(expanduser(sys.path[0])), "saves", "3v3_teams")):
            team_list.append(x)
    
    startup_window()
    
    GlobalVars.player_1_team = PlayerTeam(1)
    GlobalVars.player_2_team = PlayerTeam(2)

    if GlobalVars.game_mode == "Classic":
        board = ClassicBoardGenerator()
    elif GlobalVars.game_mode == "3v3":
        board = TvTBoardGenerator()

    main()
