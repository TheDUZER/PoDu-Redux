 ##  -*- coding: utf-8 -*-

"""
CURRENT TODO:

-Update file pathing for various filesystems
-Add ability and stat previews to main view on click (or possibly hover? TK popup? do something with hover)


TODO LATER...:
-Properly display modified movement values on screen
-Create functional ability button
-Fix gamelog on-screen text overflow
-Write gamelog to file

-START ADDING ATTACK EFFECTS
    Priorities:
    -Wait effects and wait after PC move
    -Fly / Fly Away / Telekinesis effects
    -Knockback / Psychic Shove
    -Wait / Markers
    -Status Affliction
    -Respin (forced, tactical, Swords Dance, Fire Spin, etc)
    -Swap (Abra, Gardevoir)
    -Draco Meteor effects

-PACKAGING / HOSTING
    -UUUGGGHHHH

"""
from glob import iglob
from os.path import abspath, expanduser, join
import tkinter as tk
from tkinter import ttk
import arcade, json, sys, os, random, time

SPRITE_SCALING = 2.5

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 1024
SCREEN_TITLE = "PoDu ReDux v0.1.1"
STATS_PATH = os.path.join(sys.path[0], "pkmn-stats.json")

PKMN_STATS = json.load(open(STATS_PATH, "r"))

valid_moves = []
first_loop = 0
checked_moves = []
click_counter = 0
in_transit = ''
in_transit_loc = ''
potential_targets = []
move_click = False
attack_click = False
turn_player = random.randint(1,2)
first_turn = True
gamelog = []
player_1_win = False
player_2_win = False
stats_x = 0
stats_y = 0
background_select = ''
player_1_select = ''
player_2_select = ''
game_mode = ''
evo_complete = False
unit_attacked = False
unit_moved = False

BG_PATH = join(abspath(expanduser(sys.path[0])), "images", "board", "backgrounds")

def write_log():
    log_stamp = time.ctime()
    log_stamp = log_stamp.replace(' ', '_')
    log_stamp = log_stamp.replace(':', '-')
    LOG_PATH = sys.path[0] + "\saves\gamelogs\PoDuReDux_Log_" + f"{log_stamp}" + ".txt"
    LOG_FILE = open(LOG_PATH, "a+")
    for lines in gamelog:
        lines = lines + "\n"
        LOG_FILE.write(lines)
    LOG_FILE.close()

class BoardNeighbors():
    """Create generic board spaces and assign list of neighbor spaces"""
    def __init__(self, neighbors = {}):
        self.neighbors = neighbors
        self.coords = {}
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
    """Create board object with space labels and adjusted bools for special spaces"""
    def __init__(self):
        self.A1 = BoardNeighbors({"B1":1, "B2":2, "A2":3})
        self.A1.player_1_entry = True
        self.A1.coords = {'x': 290, 'y': 294}
        self.A2 = BoardNeighbors({"A1":7, "A3":3})
        self.A2.coords = {'x': 365, 'y': 293}
        self.A3 = BoardNeighbors({"A2":7, "A4":3})
        self.A3.coords = {'x': 436, 'y': 293}
        self.A4 = BoardNeighbors({"A3":7, "A5":3})
        self.A4.player_1_goal = True
        self.A4.coords = {'x': 512, 'y': 293}
        self.A5 = BoardNeighbors({"A4":7, "A6":3, "B4":1})
        self.A5.coords = {'x': 586, 'y': 293}
        self.A6 = BoardNeighbors({"A5":7, "A7":3})
        self.A6.coords = {'x': 658, 'y': 293}
        self.A7 = BoardNeighbors({"A6":7, "B6":8, "B7":1})
        self.A7.player_1_entry = True
        self.A7.coords = {'x': 732, 'y': 293}
        
        self.B1 = BoardNeighbors({"A1":5, "C1":1})
        self.B1.coords = {'x': 290, 'y': 414}
        self.B2 = BoardNeighbors({"A1":6, "B4":3, "C2":1})
        self.B2.coords = {'x': 400, 'y': 414}
        self.B4 = BoardNeighbors({"B2":7, "A5":5, "B6":3})
        self.B4.coords = {'x': 512, 'y': 414}
        self.B6 = BoardNeighbors({"B4":7, "A7":5, "C6":1})
        self.B6.coords = {'x': 625, 'y': 414}
        self.B7 = BoardNeighbors({"A7":5, "C7":1})
        self.B7.coords = {'x': 732, 'y': 414}
        
        self.C1 = BoardNeighbors({"B1":5, "D1":1})
        self.C1.coords = {'x': 290, 'y': 514}
        self.C2 = BoardNeighbors({"B2":5, "D2":1})
        self.C2.coords = {'x': 400, 'y': 514}
        self.C6 = BoardNeighbors({"B6":5, "D6":1})
        self.C6.coords = {'x': 625, 'y': 514}
        self.C7 = BoardNeighbors({"B7":5, "D7":1})
        self.C7.coords = {'x': 732, 'y': 514}
        
        self.D1 = BoardNeighbors({"E1":1, "C1":5})
        self.D1.coords = {'x': 290, 'y': 614}
        self.D2 = BoardNeighbors({"E1":8, "D4":3, "C2":5})
        self.D2.coords = {'x': 400, 'y': 614}
        self.D4 = BoardNeighbors({"D2":7, "E3":1, "D6":3})
        self.D4.coords = {'x': 512, 'y': 614}
        self.D6 = BoardNeighbors({"D4":7, "E7":2, "C6":5})
        self.D6.coords = {'x': 625, 'y': 614}
        self.D7 = BoardNeighbors({"C7":5, "E7":1})
        self.D7.coords = {'x': 732, 'y': 614}
        
        self.E1 = BoardNeighbors({"D1":5, "E2":3, "D2":4})
        self.E1.player_2_entry = True
        self.E1.coords = {'x': 290, 'y': 731}
        self.E2 = BoardNeighbors({"E1":7, "E3":3})
        self.E2.coords = {'x': 365, 'y': 731}
        self.E3 = BoardNeighbors({"E2":7, "E4":3, "D4":5})
        self.E3.coords = {'x': 436, 'y': 731}
        self.E4 = BoardNeighbors({"E3":7, "E5":3})
        self.E4.player_2_goal = True
        self.E4.coords = {'x': 512, 'y': 731}
        self.E5 = BoardNeighbors({"E4":7, "E6":3})
        self.E5.coords = {'x': 586, 'y': 731}
        self.E6 = BoardNeighbors({"E5":7, "E7":3})
        self.E6.coords = {'x': 658, 'y': 731}
        self.E7 = BoardNeighbors({"E6":7, "D6":6, "D7":5})
        self.E7.player_2_entry = True
        self.E7.coords = {'x': 732, 'y': 731}
        
        self.player_1_bench_1 = BoardNeighbors({'A1':None, 'A7':None})
        self.player_1_bench_1.occupant = player_1_team.pkmn1
        self.player_1_bench_1.occupant_team = 1
        self.player_1_bench_1.occupied = True
        self.player_1_bench_1.coords = {'x': 311, 'y': 183}
        self.player_1_bench_2 = BoardNeighbors({'A1':None, 'A7':None})
        self.player_1_bench_2.occupant = player_1_team.pkmn2
        self.player_1_bench_2.occupant_team = 1
        self.player_1_bench_2.occupied = True
        self.player_1_bench_2.coords = {'x': 411, 'y': 183}
        self.player_1_bench_3 = BoardNeighbors({'A1':None, 'A7':None})
        self.player_1_bench_3.occupant = player_1_team.pkmn3
        self.player_1_bench_3.occupant_team = 1
        self.player_1_bench_3.occupied = True
        self.player_1_bench_3.coords = {'x': 511, 'y': 183}
        self.player_1_bench_4 = BoardNeighbors({'A1':None, 'A7':None})
        self.player_1_bench_4.occupant = player_1_team.pkmn4
        self.player_1_bench_4.occupant_team = 1
        self.player_1_bench_4.occupied = True
        self.player_1_bench_4.coords = {'x': 360, 'y': 110}
        self.player_1_bench_5 = BoardNeighbors({'A1':None, 'A7':None})
        self.player_1_bench_5.occupant = player_1_team.pkmn5
        self.player_1_bench_5.occupant_team = 1
        self.player_1_bench_5.occupied = True
        self.player_1_bench_5.coords = {'x': 460, 'y': 110}
        self.player_1_bench_6 = BoardNeighbors({'A1':None, 'A7':None})
        self.player_1_bench_6.occupant = player_1_team.pkmn6
        self.player_1_bench_6.occupant_team = 1
        self.player_1_bench_6.occupied = True
        self.player_1_bench_6.coords = {'x': 560, 'y': 110}
        
        self.player_2_bench_1 = BoardNeighbors({'E1':None, 'E7':None})
        self.player_2_bench_1.occupant = player_1_team.pkmn1
        self.player_2_bench_1.occupant_team = 2
        self.player_2_bench_1.occupied = True
        self.player_2_bench_1.coords = {'x': 715, 'y': 845}
        self.player_2_bench_2 = BoardNeighbors({'E1':None, 'E7':None})
        self.player_2_bench_2.occupant = player_1_team.pkmn2
        self.player_2_bench_2.occupant_team = 2
        self.player_2_bench_2.occupied = True
        self.player_2_bench_2.coords = {'x': 615, 'y': 845}
        self.player_2_bench_3 = BoardNeighbors({'E1':None, 'E7':None})
        self.player_2_bench_3.occupant = player_1_team.pkmn3
        self.player_2_bench_3.occupant_team = 2
        self.player_2_bench_3.occupied = True
        self.player_2_bench_3.coords = {'x': 515, 'y': 845}
        self.player_2_bench_4 = BoardNeighbors({'E1':None, 'E7':None})
        self.player_2_bench_4.occupant = player_1_team.pkmn4
        self.player_2_bench_4.occupant_team = 2
        self.player_2_bench_4.occupied = True
        self.player_2_bench_4.coords = {'x': 661, 'y': 921}
        self.player_2_bench_5 = BoardNeighbors({'E1':None, 'E7':None})
        self.player_2_bench_5.occupant = player_1_team.pkmn5
        self.player_2_bench_5.occupant_team = 2
        self.player_2_bench_5.occupied = True
        self.player_2_bench_5.coords = {'x': 561, 'y': 921}
        self.player_2_bench_6 = BoardNeighbors({'E1':None, 'E7':None})
        self.player_2_bench_6.occupant = player_1_team.pkmn6
        self.player_2_bench_6.occupant_team = 2
        self.player_2_bench_6.occupied = True
        self.player_2_bench_6.coords = {'x': 461, 'y': 921}
        
        self.player_1_ultra_space_1 = BoardNeighbors()
        self.player_1_ultra_space_1.coords = {'x': 900, 'y': 280}
        self.player_1_ultra_space_2 = BoardNeighbors()
        self.player_1_ultra_space_2.coords = {'x': 975, 'y': 240}
        self.player_1_ultra_space_3 = BoardNeighbors()
        self.player_1_ultra_space_3.coords = {'x': 900, 'y': 185}
        self.player_1_ultra_space_4 = BoardNeighbors()
        self.player_1_ultra_space_4.coords = {'x': 975, 'y': 100}
        self.player_1_ultra_space_5 = BoardNeighbors()
        self.player_1_ultra_space_5.coords = {'x': 900, 'y': 140}
        self.player_1_ultra_space_6 = BoardNeighbors()
        self.player_1_ultra_space_6.coords = {'x': 975, 'y': 55}
        
        self.player_2_ultra_space_1 = BoardNeighbors()
        self.player_2_ultra_space_1.coords = {'x': 124, 'y': 752}
        self.player_2_ultra_space_2 = BoardNeighbors()
        self.player_2_ultra_space_2.coords = {'x': 50, 'y': 794}
        self.player_2_ultra_space_3 = BoardNeighbors()
        self.player_2_ultra_space_3.coords = {'x': 124, 'y': 843}
        self.player_2_ultra_space_4 = BoardNeighbors()
        self.player_2_ultra_space_4.coords = {'x': 50, 'y': 886}
        self.player_2_ultra_space_5 = BoardNeighbors()
        self.player_2_ultra_space_5.coords = {'x': 124, 'y': 940}
        self.player_2_ultra_space_6 = BoardNeighbors()
        self.player_2_ultra_space_6.coords = {'x': 50, 'y': 975}
        
        self.player_1_eliminated_1 = BoardNeighbors()
        self.player_1_eliminated_1.coords = {'x': 124, 'y': 280}
        self.player_1_eliminated_2 = BoardNeighbors()
        self.player_1_eliminated_2.coords = {'x': 50, 'y': 240}
        self.player_1_eliminated_3 = BoardNeighbors()
        self.player_1_eliminated_3.coords = {'x': 124, 'y': 185}
        self.player_1_eliminated_4 = BoardNeighbors()
        self.player_1_eliminated_4.coords = {'x': 50, 'y': 100}
        self.player_1_eliminated_5 = BoardNeighbors()
        self.player_1_eliminated_5.coords = {'x': 124, 'y': 140}
        self.player_1_eliminated_6 = BoardNeighbors()
        self.player_1_eliminated_6.coords = {'x': 50, 'y': 55}
        
        self.player_2_eliminated_1 = BoardNeighbors()
        self.player_2_eliminated_1.coords = {'x': 900, 'y': 752}
        self.player_2_eliminated_2 = BoardNeighbors()
        self.player_2_eliminated_2.coords = {'x': 975, 'y': 794}
        self.player_2_eliminated_3 = BoardNeighbors()
        self.player_2_eliminated_3.coords = {'x': 900, 'y': 843}
        self.player_2_eliminated_4 = BoardNeighbors()
        self.player_2_eliminated_4.coords = {'x': 975, 'y': 886}
        self.player_2_eliminated_5 = BoardNeighbors()
        self.player_2_eliminated_5.coords = {'x': 900, 'y': 940}
        self.player_2_eliminated_6 = BoardNeighbors()
        self.player_2_eliminated_6.coords = {'x': 975, 'y': 975}
        
        self.player_1_PC_1 = BoardNeighbors()
        self.player_1_PC_1.coords = {'x': 645, 'y': 185}
        self.player_1_PC_2 = BoardNeighbors()
        self.player_1_PC_2.coords = {'x': 727, 'y': 185}
        
        self.player_2_PC_1 = BoardNeighbors()
        self.player_2_PC_1.coords = {'x': 380, 'y': 840}
        self.player_2_PC_2 = BoardNeighbors()
        self.player_2_PC_2.coords = {'x': 297, 'y': 840}

class TvTBoardGenerator():
    ## 3v3 Board
    ## Update coordinates, neighbors and add mode selection WITH VALID TEAM FILES
    """Create board object with space labels and adjusted bools for special spaces"""
    def __init__(self):
        self.A1 = BoardNeighbors({"B1":1, "B2":2, "A2":3})
        self.A1.player_1_entry = True
        self.A1.coords = {'x': 290, 'y': 294}
        self.A2 = BoardNeighbors({"A1":7, "A3":3})
        self.A2.coords = {'x': 365, 'y': 293}
        self.A3 = BoardNeighbors({"A2":7, "A4":3})
        self.A3.coords = {'x': 436, 'y': 293}
        self.A4 = BoardNeighbors({"A3":7, "A5":3})
        self.A4.player_1_goal = True
        self.A4.coords = {'x': 512, 'y': 293}
        self.A5 = BoardNeighbors({"A4":7, "A6":3})
        self.A5.coords = {'x': 586, 'y': 293}
        self.A6 = BoardNeighbors({"A5":7, "A7":3})
        self.A6.coords = {'x': 658, 'y': 293}
        self.A6.player_1_entry = True
        self.A7 = BoardNeighbors({"A6":7, "B6":8, "B7":1})
        self.A7.coords = {'x': 732, 'y': 293}
        
        self.B1 = BoardNeighbors({"A1":5, "C1":1})
        self.B1.coords = {'x': 290, 'y': 414}
        self.B2 = BoardNeighbors({"A1":6, "C2":1})
        self.B2.coords = {'x': 400, 'y': 414}
        self.B6 = BoardNeighbors({"A7":5, "C6":1})
        self.B6.coords = {'x': 625, 'y': 414}
        self.B7 = BoardNeighbors({"A7":5, "C7":1})
        self.B7.coords = {'x': 732, 'y': 414}
        
        self.C1 = BoardNeighbors({"B1":5, "D1":1})
        self.C1.coords = {'x': 290, 'y': 514}
        self.C2 = BoardNeighbors({"B2":5, "D2":1, "C4":3})
        self.C2.coords = {'x': 400, 'y': 514}
        self.C4 = BoardNeighbors({"C2":7, "C6":3})
        self.C4.coords = {'x': 512, 'y': 512}
        self.C6 = BoardNeighbors({"B6":5, "D6":1, "C4":7})
        self.C6.coords = {'x': 625, 'y': 514}
        self.C7 = BoardNeighbors({"B7":5, "D7":1})
        self.C7.coords = {'x': 732, 'y': 514}
        
        self.D1 = BoardNeighbors({"E1":1, "C1":5})
        self.D1.coords = {'x': 290, 'y': 614}
        self.D2 = BoardNeighbors({"E1":8, "C2":5})
        self.D2.coords = {'x': 400, 'y': 614}
        self.D6 = BoardNeighbors({"E7":2, "C6":5})
        self.D6.coords = {'x': 625, 'y': 614}
        self.D7 = BoardNeighbors({"C7":5, "E7":1})
        self.D7.coords = {'x': 732, 'y': 614}
        
        self.E1 = BoardNeighbors({"D1":5, "E2":3, "D2":4})
        self.E1.coords = {'x': 290, 'y': 731}
        self.E2 = BoardNeighbors({"E1":7, "E3":3})
        self.E2.player_2_entry = True
        self.E2.coords = {'x': 365, 'y': 731}
        self.E3 = BoardNeighbors({"E2":7, "E4":3})
        self.E3.coords = {'x': 436, 'y': 731}
        self.E4 = BoardNeighbors({"E3":7, "E5":3})
        self.E4.player_2_goal = True
        self.E4.coords = {'x': 512, 'y': 731}
        self.E5 = BoardNeighbors({"E4":7, "E6":3})
        self.E5.coords = {'x': 586, 'y': 731}
        self.E6 = BoardNeighbors({"E5":7, "E7":3})
        self.E6.coords = {'x': 658, 'y': 731}
        self.E7 = BoardNeighbors({"E6":7, "D6":6, "D7":5})
        self.E7.player_2_entry = True
        self.E7.coords = {'x': 732, 'y': 731}
        
        self.player_1_bench_1 = BoardNeighbors({'A1':None, 'A6':None})
        self.player_1_bench_1.occupant = player_1_team.pkmn1
        self.player_1_bench_1.occupant_team = 1
        self.player_1_bench_1.occupied = True
        self.player_1_bench_1.coords = {'x': 311, 'y': 183}
        self.player_1_bench_2 = BoardNeighbors({'A1':None, 'A6':None})
        self.player_1_bench_2.occupant = player_1_team.pkmn2
        self.player_1_bench_2.occupant_team = 1
        self.player_1_bench_2.occupied = True
        self.player_1_bench_2.coords = {'x': 411, 'y': 183}
        self.player_1_bench_3 = BoardNeighbors({'A1':None, 'A6':None})
        self.player_1_bench_3.occupant = player_1_team.pkmn3
        self.player_1_bench_3.occupant_team = 1
        self.player_1_bench_3.occupied = True
        self.player_1_bench_3.coords = {'x': 511, 'y': 183}
        
        self.player_2_bench_1 = BoardNeighbors({'E2':None, 'E7':None})
        self.player_2_bench_1.occupant = player_1_team.pkmn1
        self.player_2_bench_1.occupant_team = 2
        self.player_2_bench_1.occupied = True
        self.player_2_bench_1.coords = {'x': 715, 'y': 845}
        self.player_2_bench_2 = BoardNeighbors({'E2':None, 'E7':None})
        self.player_2_bench_2.occupant = player_1_team.pkmn2
        self.player_2_bench_2.occupant_team = 2
        self.player_2_bench_2.occupied = True
        self.player_2_bench_2.coords = {'x': 615, 'y': 845}
        self.player_2_bench_3 = BoardNeighbors({'E2':None, 'E7':None})
        self.player_2_bench_3.occupant = player_1_team.pkmn3
        self.player_2_bench_3.occupant_team = 2
        self.player_2_bench_3.occupied = True
        self.player_2_bench_3.coords = {'x': 515, 'y': 845}
        
        self.player_1_ultra_space_1 = BoardNeighbors()
        self.player_1_ultra_space_1.coords = {'x': 900, 'y': 280}
        self.player_1_ultra_space_2 = BoardNeighbors()
        self.player_1_ultra_space_2.coords = {'x': 975, 'y': 240}
        self.player_1_ultra_space_3 = BoardNeighbors()
        self.player_1_ultra_space_3.coords = {'x': 900, 'y': 185}
        
        self.player_2_ultra_space_1 = BoardNeighbors()
        self.player_2_ultra_space_1.coords = {'x': 124, 'y': 752}
        self.player_2_ultra_space_2 = BoardNeighbors()
        self.player_2_ultra_space_2.coords = {'x': 50, 'y': 794}
        self.player_2_ultra_space_3 = BoardNeighbors()
        self.player_2_ultra_space_3.coords = {'x': 124, 'y': 843}
        
        self.player_1_eliminated_1 = BoardNeighbors()
        self.player_1_eliminated_1.coords = {'x': 124, 'y': 280}
        self.player_1_eliminated_2 = BoardNeighbors()
        self.player_1_eliminated_2.coords = {'x': 50, 'y': 240}
        self.player_1_eliminated_3 = BoardNeighbors()
        self.player_1_eliminated_3.coords = {'x': 124, 'y': 185}
        
        self.player_2_eliminated_1 = BoardNeighbors()
        self.player_2_eliminated_1.coords = {'x': 900, 'y': 752}
        self.player_2_eliminated_2 = BoardNeighbors()
        self.player_2_eliminated_2.coords = {'x': 975, 'y': 794}
        self.player_2_eliminated_3 = BoardNeighbors()
        self.player_2_eliminated_3.coords = {'x': 900, 'y': 843}
        
        self.player_1_PC_1 = BoardNeighbors()
        self.player_1_PC_1.coords = {'x': 681, 'y': 185}
        
        self.player_2_PC_1 = BoardNeighbors()
        self.player_2_PC_1.coords = {'x': 336, 'y': 840}

def knockback_pathing():
    """Check pathing for directional knockback effects"""
    ## PENDING IMPLEMENTATION, NEEDS WORK
    direction = board.B2.neighbors["C2"]
    valid_moves = []

    for x in board.C2.neighbors.keys():
        if board.C2.neighbors[x] == direction:
            valid_moves.append(x)
        else:
            continue
    return valid_moves
                    
    ## output -> ['D2']

def pc_rotate(ctrl_player):
    
    global game_mode

    if game_mode == "Classic":
        for pkmns in range(1,7):
            if eval(f"'PC' in player_{ctrl_player}_team.pkmn{pkmns}['loc']"):
                if eval(f"player_{ctrl_player}_team.pkmn{pkmns}['loc'][-1] == str(2)"):
                    exec(f"player_{ctrl_player}_team.pkmn{pkmns}['loc'] = 'player_{ctrl_player}_PC_1'")
                else:
                    exec(f"player_{ctrl_player}_team.pkmn{pkmns}['loc'] = player_{ctrl_player}_team.pkmn{pkmns}['orig_loc']")
                    if eval(f"player_{ctrl_player}_team.pkmn{pkmns}['wait']") < 2:
                        exec(f"player_{ctrl_player}_team.pkmn{pkmns}['wait'] += 2")
    elif game_mode == "3v3":
        for pkmns in range(1,4):
            if eval(f"'PC' in player_{ctrl_player}_team.pkmn{pkmns}['loc']"):
                exec(f"player_{ctrl_player}_team.pkmn{pkmns}['loc'] = player_{ctrl_player}_team.pkmn{pkmns}['orig_loc']")
                if eval(f"player_{ctrl_player}_team.pkmn{pkmns}['wait']") < 2:
                    exec(f"player_{ctrl_player}_team.pkmn{pkmns}['wait'] += 2")

def wait_tickdown():
    for x in range(1,3):
        for pkmns in range(1,7):
            if eval(f"player_{x}_team.pkmn{pkmns}['wait']") != 0:
                exec(f"player_{x}_team.pkmn{pkmns}['wait'] -= 1")

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
    # need to boil for loops down to a recursive function

    global valid_moves, first_turn, loop_counter

    loop_counter = 0

    del valid_moves[:]
    if first_turn == True:
        modifier = -1
        gamelog.append("First turn: Movement reduced by 1.")
    else:
        pass

    def path_iter(loc, move, modifier):
        global valid_moves, loop_counter
        next_moves = []
        for x in loc:
            if move + modifier == 0:
                break
            if eval(f"board.{x}.passable") == True:
                valid_moves.append(x)
                for y in eval(f"board.{x}.neighbors.keys()"):
                    next_moves.append(y)
            else:
                continue
        loop_counter += 1
        if loop_counter < move + modifier:
            path_iter(next_moves, modifier, move)

    path_iter(loc, move, modifier)
    checked_moves = set(valid_moves)
    to_remove = []
    for possible_moves in checked_moves:
        if eval(f"board.{possible_moves}.occupied") == True:
            to_remove.append(possible_moves)
        else:
            continue
    for invalid_move in to_remove:
        checked_moves.remove(invalid_move)
    valid_moves.clear()
    first_loop = 0
    return checked_moves
    
class PlayerTeam():
    """Instantiate class that contains player 1 team and base stats."""
    ## WORKAROUND IMPLEMENTED DUE TO TEAM INSTANTIATION ISSUES BETWEEN PLAYERS
    def __init__(self, ctrl_player):
        def create_team(self, top_range, bottom_range):
            for x in range(top_range, bottom_range):
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

        create_team(self, 1, 4)
        if game_mode == "Classic":
            create_team(self, 4, 7)

    def TeamUpdate(self, ctrl_player):
        ## Imports custom unit loadout from custom file
        
        ## Iterates over lines in custom unit loadout file, compares them to
        ## PKMN_STATS loaded above, and writes the correct stats to a created playerTeam() object
        global player_1_select, player_2_select, game_mode, team_list
        
        team_file = eval(f"player_{ctrl_player}_select")
        
        if game_mode == "Classic":
            selected_team_path = os.path.join(sys.path[0], f"saves\\classic_teams\\{team_file}")
            top_range = 1
            bottom_range = 7
        elif game_mode == "3v3":
            selected_team_path = os.path.join(sys.path[0], f"saves\\3v3_teams\\{team_file}")
            top_range = 1
            bottom_range = 4
        
        custom_team = open(selected_team_path)
        custom_team = custom_team.read().splitlines()
        line_counter = 1
        gamelog.append(f"Player {ctrl_player}'s team:")
        gamelog.append(str("-"*8 + team_file[:-4] + "-"*8))
        for line in custom_team:
            exec(f"self.pkmn{line_counter}.update(PKMN_STATS['{line}'])")
            gamelog.append(eval(f"PKMN_STATS['{line}']['name']"))
            line_counter += 1
            if game_mode == "Classic" and line_counter == 7:
                break
            elif game_mode == "3v3" and line_counter == 4:
                break
            else:
                continue
        for x in range(top_range, bottom_range):
            for y in range(1,10):
                if eval(f"self.pkmn{x}['attack{y}power']") != 'null':
                    exec(f"self.pkmn{x}['attack{y}origpower'] = self.pkmn{x}['attack{y}power']")
                else:
                    exec(f"self.pkmn{x}['attack{y}origpower'] = 'null'")

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
                ## Checks for Confusion status and returns next available attack segment
                if combatant['status'] == 'confused':
                    combatant_attack += 1
                    if eval(f"{combatant}['attack{wheel_numbers}name']") == "null":
                        combatant_attack = 1
                ## Returns segment number of SPIN result (wheel_numbers at correct iteration)
                return combatant_attack
                break
            else:
                continue
        else:
            break

def target_finder(combatant, attack_distance = 1):
    """Checks adjacent spaces for valid attack targets"""
    ##  TO ADD:
    ##  attack_distance variable accounts for extended
    ##  range attackers like Kartana or Aegislash
    ##  Need to rework function to be recursive for attack distance
    target_list = []
    combatant = eval(combatant)
    for x in eval(f"board.{combatant['loc']}.neighbors.keys()"):
        if len(combatant['loc']) == 2 and eval(f"board.{x}.occupied") == True:
                if eval(f"board.{x}.ctrl_player") != eval(
                    f"board.{combatant['loc']}.ctrl_player") or 0:
                    target_list.append(x)
    return target_list

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
    combatant_1 = eval(combatant_1)
    combatant_2 = eval(combatant_2)

    gamelog.append(f"Player {turn_player}'s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) attacked Player {combatant_2['ctrl']}'s {combatant_2['name']} ({combatant_2['orig_loc'][-1]})")
    combatant_1_attack = spin(combatant_1)
    gamelog.append(f"Player {turn_player}'s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) spun {combatant_1[f'attack{combatant_1_attack}name']}")
    gamelog.append("    " + f"Color: {combatant_1[f'attack{combatant_1_attack}color']} ----- Power: {combatant_1[f'attack{combatant_1_attack}power']}")
    combatant_2_attack = spin(combatant_2)
    gamelog.append(f"Player {combatant_2['ctrl']}'s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) spun {combatant_2[f'attack{combatant_2_attack}name']}")
    gamelog.append("    " + f"Color: {combatant_2[f'attack{combatant_2_attack}color']} ----- Power: {combatant_2[f'attack{combatant_2_attack}power']}")

    if combatant_1['status'] != 'frozen':
        combatant_1_color = eval(f"combatant_1['attack{combatant_1_attack}color']")
    else:
        combatant_1_color = "Red"
    if not combatant_1_color == "Red" and not combatant_1_color == "Blue":
        combatant_1_power = eval(f"combatant_1['attack{combatant_1_attack}power']")
        if combatant_1_color != "Purple":
            if combatant_1['status'] == "poison" or combatant_1['status'] == "burn":
                combatant_1_power -= 20
            elif combatant_1['status'] == "noxious":
                combatant_1_power -= 40
    else:
        pass
    if combatant_2['status'] != 'frozen':
        combatant_2_color = eval(f"combatant_2['attack{combatant_2_attack}color']")
    else:
        combatant_2_color = 'Red'
    if not combatant_2_color == "Red" and not combatant_2_color == "Blue":
        combatant_2_power = eval(f"combatant_2['attack{combatant_2_attack}power']")
        if combatant_2_color != "Purple":
            if combatant_2['status'] == "poison" or combatant_2['status'] == "burn":
                combatant_2_power -= 20
            elif combatant_2['status'] == "noxious":
                combatant_2_power -= 40
    else:
        pass

    if combatant_1_color == "White":
        if combatant_2_color == "White" or combatant_2_color == "Gold":
            if combatant_1_power > combatant_2_power:
                #Update other log entries here to this format
                gamelog.append(f"Player {turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
                return 1
            elif combatant_1_power < combatant_2_power:
                gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
                return 2
            elif combatant_1_power == combatant_2_power:
                gamelog.append("Tie!")
                return 0
        elif combatant_2_color == "Purple":
            gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 6
        elif combatant_2_color == "Red":
            gamelog.append(f"Player {turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
            return 1
        elif combatant_2_color == "Blue":
            gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 6
        
    elif combatant_1_color == "Gold":
        if combatant_2_color == "White" or combatant_2_color == "Gold":
            if combatant_1_power > combatant_2_power:
                gamelog.append(f"Player {turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
                return 1
            elif combatant_1_power < combatant_2_power:
                gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
                return 2
            elif combatant_1_power == combatant_2_power:
                gamelog.append("Tie!")
                return 0
        elif combatant_2_color == "Purple":
            gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 3
        elif combatant_2_color == "Red":
            gamelog.append(f"Player {turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
            return 1
        elif combatant_2_color == "Blue":
            gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 6
        
    elif combatant_1_color == "Purple":
        if combatant_2_color == "Purple":
            if combatant_1_power > combatant_2_power:
                gamelog.append(f"Player {turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
                return 5
            elif combatant_1_power < combatant_2_power:
                gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
                return 6
            elif combatant_1_power == combatant_2_power:
                gamelog.append("Tie!")
                return 7
        elif combatant_2_color == "White":
            gamelog.append(f"Player {turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
            return 5
        elif combatant_2_color == "Gold":
            gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 4
        elif combatant_2_color == "Red":
            gamelog.append(f"Player {turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
            return 5
        elif combatant_2_color == "Blue":
            gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 6

    elif combatant_1_color == "Blue":
        if combatant_2_color != "Blue":
            gamelog.append(f"Player {turn_player}s {combatant_1['name']} ({combatant_1['orig_loc'][-1]}) wins!")
            return 6
        else:
            gamelog.append("Tie!")
            return 7

    elif combatant_1_color == "Red":
        if combatant_2_color == "White" or combatant_2_color == "Gold":
            gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 2
        elif combatant_2_color == "Purple" or combatant_2_color == "Blue":
            gamelog.append(f"Player {combatant_2['ctrl']}s {combatant_2['name']} ({combatant_2['orig_loc'][-1]}) wins!")
            return 6
        elif combatant_2_color == "Red":
            gamelog.append("Tie!")
            return 0

class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        
        #arcade.set_background_color(arcade.color.BLACK)
        
        self.background = None
        self.ClassicBoard = None
        self.TvTBoard = None

        #Create initial state of sprites for both teams
        for x in range(1,3):
            for y in range(1,7):
                exec(f"self.player_{x}_pkmn_{y} = None")
        
        # If you have sprite lists, you should create them here,
        # and set them to None

        self.pkmn_list = None
        
    def on_show(self):
        # Create your sprites and sprite lists here
        self.pkmn_list = arcade.SpriteList()

        if game_mode == "Classic":
            range_top = 1
            range_bottom = 7
        elif game_mode == "3v3":
            range_top = 1
            range_bottom = 4
        
        for x in range(1,3):
            for y in range(range_top,range_bottom):
                pkmn_ref = f"player_{x}_team.pkmn{y}"
                pkmn_ref_loc = eval(f"{pkmn_ref}['loc']")
                pkmn_ref_x = eval(f"board.{pkmn_ref_loc}.coords['x']")
                pkmn_ref_y = eval(f"board.{pkmn_ref_loc}.coords['y']")
                sprite_file_name = eval(f"{pkmn_ref}['spritefile']")
                sprite_path = f"images/Sprites/{sprite_file_name}"
                exec(f"self.player_{x}_pkmn_{y} = arcade.Sprite('{sprite_path}', SPRITE_SCALING)")
                exec(f"self.player_{x}_pkmn_{y}.center_x = pkmn_ref_x")
                exec(f"self.player_{x}_pkmn_{y}.center_y = pkmn_ref_y")
                exec(f"self.pkmn_list.append(self.player_{x}_pkmn_{y})")

        self.background = arcade.load_texture(background_select)
        if game_mode == "Classic":
            self.ClassicBoard = arcade.load_texture("images/board/overlays/classic_duel_overlay.png")
        elif game_mode == "3v3":
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
        arcade.draw_texture_rectangle(SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_HEIGHT, SCREEN_HEIGHT, self.background)
        if game_mode == "Classic":
            arcade.draw_texture_rectangle(SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2,
                                          SCREEN_HEIGHT, SCREEN_HEIGHT, self.ClassicBoard)
            center_text_x = 450
            center_text_y = 500
            top_range = 1
            bottom_range = 7
            
        elif game_mode == "3v3":
            arcade.draw_texture_rectangle(SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2,
                                          SCREEN_HEIGHT, SCREEN_HEIGHT, self.TvTBoard)
            center_text_x = 450
            center_text_y = 369
            top_range = 1
            bottom_range = 4

        #draw unit bases
        for x in range(1,3):
            if x == 1:
                cir_color = arcade.color.AZURE
            elif x == 2:
                cir_color = arcade.color.RASPBERRY
            for y in range(top_range, bottom_range):
                pkmn_ref = f"player_{x}_team.pkmn{y}"
                pkmn_ref_loc = eval(f"{pkmn_ref}['loc']")
                pkmn_ref_x = eval(f"board.{pkmn_ref_loc}.coords['x']")
                pkmn_ref_y = eval(f"board.{pkmn_ref_loc}.coords['y']")
                exec(f"self.player_{x}_pkmn_{y}.center_x = pkmn_ref_x")
                exec(f"self.player_{x}_pkmn_{y}.center_y = pkmn_ref_y")
                exec(f"arcade.draw_circle_filled(self.player_{x}_pkmn_{y}.center_x, self.player_{x}_pkmn_{y}.center_y, 40, cir_color)")
                exec(f"arcade.draw_circle_filled(self.player_{x}_pkmn_{y}.center_x - circle_offset_x, self.player_{x}_pkmn_{y}.center_y - circle_offset_y, 12, arcade.color.BLUE_SAPPHIRE)")
                exec(f"arcade.draw_text(str(player_{x}_team.pkmn{y}['move']), self.player_{x}_pkmn_{y}.center_x - text_offset_x, self.player_{x}_pkmn_{y}.center_y - text_offset_y, arcade.color.WHITE, 16)")

                #Wait circle and text draw
                if eval(f"{pkmn_ref}['wait']") > 0:
                    exec(f"arcade.draw_circle_filled(self.player_{x}_pkmn_{y}.center_x + circle_offset_x, self.player_{x}_pkmn_{y}.center_y - circle_offset_y, 12, arcade.color.PURPLE)")
                    exec(f"arcade.draw_text(str(player_{x}_team.pkmn{y}['wait']), self.player_{x}_pkmn_{y}.center_x + text_offset_x - 10, self.player_{x}_pkmn_{y}.center_y - text_offset_y, arcade.color.WHITE, 16)")

        line_counter = 0
        for lines in gamelog[::-1]:
            arcade.draw_text(lines, 1030, 40 + line_counter*16, arcade.color.WHITE, font_name = "Arial")
            line_counter += 1
            if line_counter == 70:
                break

        if player_1_win == True:
            center_text = "Player 1 Wins!"
        elif player_2_win == True:
            center_text = "Player 2 Wins!"
        else:
            center_text = f"Player {turn_player} turn."

        arcade.draw_text(center_text, center_text_x, center_text_y, arcade.color.YELLOW, 18)
        if move_click == True:
            arcade.draw_text("Click this unit again\nto attack without moving,\nif able.", center_text_x - 15, center_text_y - 45, arcade.color.YELLOW, 12, align='center')
                
        if len(checked_moves) > 0:
            for moves in checked_moves:
                arcade.draw_circle_outline(eval(f"board.{moves}.coords['x']"), eval(f"board.{moves}.coords['y']"), 40, arcade.color.AMAZON, 5)
        if len(potential_targets) > 0:
            for targets in potential_targets:
                arcade.draw_circle_outline(eval(f"board.{targets}.coords['x']"), eval(f"board.{targets}.coords['y']"), 40, arcade.color.YELLOW , 5)
        # Call draw() on all your sprite lists below
        self.pkmn_list.update()
        self.pkmn_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.pkmn_list.update()
        self.pkmn_list.draw()
            
    def evolution_check(self, winner):
        global evo_complete
        
        def evolution_popup(winner_name, evo_list):

            root = tk.Tk()
            root.title(f"Select Evolution for {winner_name}")

            def close_window():
                root.destroy()
            
            def evolution_submit(selection):
                global evo_complete
                evo_complete = selection
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
        evo_complete = False
        
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
                        if evo_complete != False:
                            gamelog.append(f"{winner_name} evolving to {evo_complete}")
    
    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        global move_click, attack_click, in_transit, in_transit_loc, in_transit_combatant, checked_moves, potential_targets, turn_player, first_turn, gamelog, player_1_win, player_2_win

        if button == arcade.MOUSE_BUTTON_LEFT:
            #gamelog.append(f"Player {turn_player} turn.")
            if not move_click and not attack_click:
                if turn_player == 1:
                    
                    for units in dir(player_1_team):
                        if units.startswith("pkmn"):
                            units_loc_str = "player_1_team." + units + "['loc']"
                            units_loc_str = eval(units_loc_str)
                            if x in range(eval(f"board.{units_loc_str}.coords['x']") - 40,
                                          eval(f"board.{units_loc_str}.coords['x']") + 40
                                          ) and y in range(
                                              eval(f"board.{units_loc_str}.coords['y']") - 40,
                                              eval(f"board.{units_loc_str}.coords['y']") + 40):
                                move_click = True
                                in_transit = f"player_1_team.{units}"
                                in_transit_combatant = f'{in_transit}'
                                in_transit_loc = eval(f"{in_transit}['loc']")
                                checked_moves = path_check(eval(f"board.{units_loc_str}.neighbors.keys()"), eval(f"player_1_team.{units}['move']"))
                                break
                elif turn_player == 2:
                    for units in dir(player_2_team):
                        if units.startswith("pkmn"):
                            units_loc_str = "player_2_team." + units + "['loc']"
                            units_loc_str = eval(units_loc_str)
                            if x in range(eval(f"board.{units_loc_str}.coords['x']") - 40,
                                          eval(f"board.{units_loc_str}.coords['x']") + 40
                                          ) and y in range(
                                              eval(f"board.{units_loc_str}.coords['y']") - 40,
                                              eval(f"board.{units_loc_str}.coords['y']") + 40):
                                move_click = True
                                in_transit = f"player_2_team.{units}"
                                in_transit_combatant = f'{in_transit}'
                                in_transit_loc = eval(f"{in_transit}['loc']")
                                checked_moves = path_check(eval(f"board.{units_loc_str}.neighbors.keys()"), eval(f"player_2_team.{units}['move']"))
                                break

                        
            elif move_click:
                global unit_attacked, unit_moved
                for moves in checked_moves:
                    #Make space clearing its own function?
                    if x in range(eval(f"board.{moves}.coords['x']") - 40, eval(f"board.{moves}.coords['x']") + 40) and y in range(
                                        eval(f"board.{moves}.coords['y']") - 40, eval(f"board.{moves}.coords['y']") + 40) and eval(
                                        f"board.{moves}.occupied") == False:
                        unit_moved = True
                        gamelog.append(f"Player {turn_player}'s " +  eval(f"{in_transit}['name']") +  " (" + str(eval(f"{in_transit}['orig_loc'][-1]")) + ") "+ f"moved to {moves}.")
                        exec(f"board.{in_transit_loc}.occupied = False")
                        exec(f"board.{in_transit_loc}.occupant = ''")
                        exec(f"board.{in_transit_loc}.occupant_team = 0")
                        exec(f"board.{in_transit_loc}.ctrl_player = 0")
                        exec(f"board.{in_transit_loc}.passable = True")
                        exec(f"board.{moves}.occupied = True")
                        exec(f"board.{moves}.occupant = '{in_transit}'")
                        exec(f"board.{moves}.occupant_team = {in_transit}['ctrl']")
                        exec(f"board.{moves}.ctrl_player = {in_transit}['ctrl']")
                        exec(f"board.{moves}.passable = False")
                        exec(f"{in_transit}['loc'] = '{moves}'")
                        in_transit_loc = eval(f"{in_transit}['loc']")
                        for surround_neighbors in dir(board):
                            if len(surround_neighbors) == 2:
                                surround_target = eval(f"board.{surround_neighbors}.occupant")
                                if surround_target:
                                    exec(f"{surround_target}['is_surrounded'] = surround_check({surround_target})")
                        for team in range(1,3):
                            for surround_resolve in eval(f"dir(player_{team}_team)"):
                                if surround_resolve.startswith('pkmn'):
                                    winner_ctrl = eval(f"player_{team}_team.{surround_resolve}['loc']")
                                    if eval(f"player_{team}_team.{surround_resolve}['is_surrounded']") == True:
                                        gamelog.append(str(f"SURROUNDED:    Player {team}'s " +
                                              eval(f"player_{team}_team.{surround_resolve}['name']") + " (" +
                                                f"{surround_resolve}"[-1] +
                                                ") " +
                                              f" was sent to Player {team}'s PC."))
                                        exec(f"board.{winner_ctrl}.occupied = False")
                                        exec(f"board.{winner_ctrl}.occupant = ''")
                                        exec(f"board.{winner_ctrl}.occupant_team = 0")
                                        exec(f"board.{winner_ctrl}.ctrl_player = 0")
                                        exec(f"board.{winner_ctrl}.passable = True")
                                        pc_rotate(team)
                                        if game_mode == "Classic":
                                            exec(f"player_{team}_team.{surround_resolve}['loc'] = 'player_{team}_PC_2'")
                                        elif game_mode == "3v3":
                                            exec(f"player_{team}_team.{surround_resolve}['loc'] = 'player_{team}_PC_1'")
                                        exec(f"player_{team}_team.{surround_resolve}['is_surrounded'] = False")
                        potential_targets = target_finder(f'{in_transit}')
                        if len(potential_targets) > 0:
                            attack_click = True
                        else:
                            if turn_player == 1:
                                turn_player = 2
                                wait_tickdown()
                                if first_turn:
                                    if len(in_transit_loc) == 2:
                                        first_turn = False
                            elif turn_player == 2:
                                turn_player = 1
                                wait_tickdown()
                                if first_turn:
                                    if len(in_transit_loc) == 2:
                                        first_turn = False
                            in_transit = ''
                            in_transit_loc = ''
                            unit_moved = False
                            unit_attacked = False

                    elif len(in_transit_loc) == 2 and x in range(eval(f"board.{in_transit_loc}.coords['x']") - 40,
                                                                      eval(f"board.{in_transit_loc}.coords['x']") + 40) and y in range(
                                                                        eval(f"board.{in_transit_loc}.coords['y']") - 40,
                                                                        eval(f"board.{in_transit_loc}.coords['y']") + 40):
                        potential_targets = target_finder(f'{in_transit}')
                        if len(potential_targets) > 0:
                            attack_click = True
                        else:
                            in_transit = ''
                            in_transit_loc = ''
                            move_click = False
                        

                move_click = False
                checked_moves = []
                
                self.pkmn_list.update()

            elif attack_click:
                for targets in potential_targets:
                    global evo_complete
                    if x in range(eval(f"board.{targets}.coords['x']") - 40, eval(f"board.{targets}.coords['x']") + 40) and y in range(
                                        eval(f"board.{targets}.coords['y']") - 40, eval(f"board.{targets}.coords['y']") + 40):
                        unit_attacked = True
                        winner_check = battle_spin_compare(f'{in_transit_combatant}', eval(f'board.{targets}.occupant'))

                        #Add effects checks
                        if winner_check == 0:
                            pass
                        
                        if winner_check == 1:
                            winner_ctrl = eval(f"{in_transit}['ctrl']")
                            loser_ctrl_temp = eval(f"board.{targets}.occupant")
                            loser_ctrl = eval(f"{loser_ctrl_temp}['ctrl']")
                            gamelog.append(f"Player {loser_ctrl}s Pokemon was sent to the PC.")
                            exec(f"board.{targets}.occupied = False")
                            exec(f"board.{targets}.occupant = ''")
                            exec(f"board.{targets}.occupant_team = 0")
                            exec(f"board.{targets}.ctrl_player = 0")
                            exec(f"board.{targets}.passable = True")
                            pc_rotate(loser_ctrl)
                            if game_mode == "Classic":
                                exec(f"{loser_ctrl_temp}['loc'] = 'player_{loser_ctrl}_PC_2'")
                            elif game_mode == "3v3":
                                exec(f"{loser_ctrl}['loc'] = 'player_{loser_ctrl}_PC_1'")
                            self.evolution_check(eval(f"{in_transit}"))
                            if evo_complete:
                                print(evo_complete)
                                exec(f"{in_transit}.update(PKMN_STATS['{evo_complete}'])")
                                new_evo_path = eval(f"{in_transit}")['spritefile']
                                exec(f"{in_transit}['stage'] += 1")

                                for x in range(1,10):
                                    if type(eval(f"{in_transit}['attack{x}power']")) == int:
                                        if eval(f"{in_transit}['attack{x}color']") == 'White' or eval(f"{in_transit}['attack{x}color']") == 'Gold':
                                            exec(f"{in_transit}['attack{x}power'] += 10*{in_transit}['stage']")
                                        elif eval(f"{in_transit}['attack{x}color']") == 'Purple':
                                            exec(f"{in_transit}['attack{x}power'] += 1*{in_transit}['stage']")
                                    else:
                                        continue
                                    
                                exec(f"self.pkmn_list.remove(self.player_{winner_ctrl}_pkmn_{in_transit[-1]})")
                                exec(f"self.player_{winner_ctrl}_pkmn_{in_transit[-1]} = arcade.Sprite('images/sprites/{new_evo_path}', SPRITE_SCALING)")
                                exec(f"self.pkmn_list.append(self.player_{winner_ctrl}_pkmn_{in_transit[-1]})")
                                self.pkmn_list.update()
                        elif winner_check == 2:
                            winner_ctrl_temp = eval(f"board.{targets}.occupant")
                            winner_ctrl = eval(f"{winner_ctrl_temp}['ctrl']")
                            loser_ctrl = eval(f"{in_transit}['ctrl']")
                            gamelog.append(f"Player {loser_ctrl}s Pokemon was sent to the PC.")
                            exec(f"board.{in_transit_loc}.occupied = False")
                            exec(f"board.{in_transit_loc}.occupant = ''")
                            exec(f"board.{in_transit_loc}.occupant_team = 0")
                            exec(f"board.{in_transit_loc}.ctrl_player = 0")
                            exec(f"board.{in_transit_loc}.passable = True")
                            pc_rotate(loser_ctrl)
                            if game_mode == "Classic":
                                exec(f"{in_transit}['loc'] = 'player_{loser_ctrl}_PC_2'")
                            elif game_mode == "3v3":
                                exec(f"{in_transit}['loc'] = 'player_{loser_ctrl}_PC_1'")
                            self.evolution_check(winner_ctrl_temp)
                            if evo_complete:
                                exec(f"{winner_ctrl_temp}.update(PKMN_STATS['{evo_complete}'])")
                                new_evo_path = eval(f"{winner_ctrl_temp}")['spritefile']
                                exec(f"{winner_ctrl_temp}['stage'] += 1")

                                for x in range(1,10):
                                    if type(eval(f"{winner_ctrl_temp}['attack{x}power']")) == int:
                                        if eval(f"{winner_ctrl_temp}['attack{x}color']") == 'White' or eval(f"{winner_ctrl_temp}['attack{x}color']") == 'Gold':
                                            exec(f"{winner_ctrl_temp}['attack{x}power'] += 10*{winner_ctrl_temp}['stage']")
                                        elif eval(f"{winner_ctrl_temp}['attack{x}color']") == 'Purple':
                                            exec(f"{winner_ctrl_temp}['attack{x}power'] += 1*{winner_ctrl_temp}['stage']")
                                    else:
                                        continue
                                    
                                exec(f"self.pkmn_list.remove(self.player_{winner_ctrl}_pkmn_{winner_ctrl_temp[-1]})")
                                exec(f"self.player_{winner_ctrl}_pkmn_{winner_ctrl_temp[-1]} = arcade.Sprite('images/sprites/{new_evo_path}', SPRITE_SCALING)")
                                exec(f"self.pkmn_list.append(self.player_{winner_ctrl}_pkmn_{winner_ctrl_temp[-1]})")
                                self.pkmn_list.update()
                        elif winner_check == 3:
                            pass
                        elif winner_check == 4:
                            pass
                        elif winner_check == 5:
                            pass
                        elif winner_check == 6:
                            pass
                        elif winner_check == 7:
                            pass

                if unit_moved or unit_attacked:
                    if turn_player == 1:
                        turn_player = 2
                        wait_tickdown()
                    elif turn_player == 2:
                        turn_player = 1
                        wait_tickdown()
                attack_click = False
                in_transit = ''
                in_transit_loc = ''
                potential_targets = []
                unit_moved = False
                unit_attacked = False
                attack_click = False
                
                self.pkmn_list.update()
                self.pkmn_list.draw()

            if player_1_win == True or player_2_win == True:
                arcade.close_window()
                exit()
            
            if board.A4.ctrl_player == 2:
                player_2_win = True
                gamelog.append("Player 2 wins! Click anywhere to exit.")
                write_log()
                self.pkmn_list.update()
                self.pkmn_list.draw()
                
            elif board.E4.ctrl_player == 1:
                player_1_win = True
                gamelog.append("Player 1 wins! Click anywhere to exit.")
                write_log()
                self.pkmn_list.update()
                self.pkmn_list.draw()

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            global stats_x, stats_y
            
            stats_x = x
            stats_y = y
            stats_window = StatsWindow(self)
            self.window.show_view(stats_window)

class StatsWindow(arcade.View):

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
    
    global stats_x, stats_y
    
    def on_draw(self):
        arcade.start_render()
        for units in dir(player_1_team):
            if units.startswith("pkmn"):
                units_loc_str = "player_1_team." + units + "['loc']"
                units_loc_str = eval(units_loc_str)
                selected_stats = "player_1_team." + units
                if stats_x in range(eval(f"board.{units_loc_str}.coords['x']") - 40,
                              eval(f"board.{units_loc_str}.coords['x']") + 40
                              ) and stats_y in range(
                                  eval(f"board.{units_loc_str}.coords['y']") - 40,
                                  eval(f"board.{units_loc_str}.coords['y']") + 40):
                    line_counter = 0
                    selected_stats = eval(selected_stats)
                    for stats in selected_stats:
                        arcade.draw_text(stats + ":    " + str(selected_stats[stats]), 10, 1000 - 12*line_counter, arcade.color.WHITE)
                        line_counter += 1
                    line_counter = 0
        for units in dir(player_2_team):
            if units.startswith("pkmn"):
                units_loc_str = "player_2_team." + units + "['loc']"
                units_loc_str = eval(units_loc_str)
                selected_stats = "player_2_team." + units
                if stats_x in range(eval(f"board.{units_loc_str}.coords['x']") - 40,
                              eval(f"board.{units_loc_str}.coords['x']") + 40
                              ) and stats_y in range(
                                  eval(f"board.{units_loc_str}.coords['y']") - 40,
                                  eval(f"board.{units_loc_str}.coords['y']") + 40):
                    line_counter = 0
                    selected_stats = eval(selected_stats)
                    for stats in selected_stats:
                        arcade.draw_text(stats + ":    " + str(selected_stats[stats]), 10, 1000 - 12*line_counter, arcade.color.WHITE)
                        line_counter += 1
                    line_counter = 0

    def on_mouse_press(self, x, y, button, modifiers):
        self.window.show_view(self.game_view)

"""
class SetupView(arcade.View):

    def on_show(self):
        pass

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_filled(SCREEN_WIDTH//4, SCREEN_HEIGHT//4, 100, 75, arcade.color.WHITE)
           
    def on_mouse_press(self, x, y, button, modifiers):
        game = GameView()
        self.window.show_view(game)
"""

def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Game Start")
    game = GameView()
    window.show_view(game)  
    arcade.run()

def on_select_team(player_num, event = None):

    if event:
        if player_num == 1:
            player_1_select = event.widget.get()
        elif player_num == 2:
            player_2_select = event.widget.get()

def mode_select():

    global game_mode
    
    def button_click():
        global game_mode, background_select
        
        if var.get() == '3v3':
            game_mode = '3v3'

        elif var.get() == 'Classic':
            game_mode = 'Classic'

        background_select = f"images/board/backgrounds/{bg_cb.get()}.png"
        root.destroy()
    
    root = tk.Tk()
    root.title("PoDuReDux: Game Mode Select")

    var = tk.StringVar()
    var.set('1')

    try:
        fn = lambda x: x.split('/')[-1][:-4]
        background_textures = {fn(k) : k for k in iglob(BG_PATH + "/**/*.png", recursive=True)}
        
    except:
        pass

    background_list = []
    
    for items in background_textures.values():
        background_list.append(items[len(BG_PATH)+1:-4])

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

    global game_mode, player_1_select, player_2_select

    def button_click():

        global player_1_select, player_2_select
        
        player_1_select = p1team_cb.get()
        player_2_select = p2team_cb.get()
        root.destroy()
    
    root = tk.Tk()
    root.title(f"PoDuReDux: Team Select ({game_mode})")

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

if __name__ == "__main__":

    mode_select()
    
    team_list = []
    if game_mode == "Classic":
        for x in os.listdir(os.path.join(sys.path[0] + "\\saves\\classic_teams\\")):
            team_list.append(x)
    elif game_mode == "3v3":
        for x in os.listdir(os.path.join(sys.path[0] + "\\saves\\3v3_teams\\")):
            team_list.append(x)

    startup_window()
    
    player_1_team = PlayerTeam(1)
    player_2_team = PlayerTeam(2)

    player_1_team.TeamUpdate(1)
    player_2_team.TeamUpdate(2)

    if game_mode == "Classic":
        board = ClassicBoardGenerator()
    elif game_mode == "3v3":
        board = TvTBoardGenerator()

    main()
