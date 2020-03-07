# -*- coding: utf-8 -*-

"""
TODO NOW...:
-Create new stats viewer
-Add tagging logic for removal of ally markers and freeze / sleep

TODO LATER...:
-Properly display modified movement values on screen (KINDA DONE)
-Create functional ability button
-Fix GlobalVars.gamelog on-screen text overflow

-START ADDING ATTACK EFFECTS

    Priorities:
    -REWORK to replace exec(effects) to getattr()
    -Fly / Fly Away / Telekinesis effects
    -Psychic Shove
    -Markers
    -Knockout effects
    -Respin .Forced, tactical, Swords Dance, Fire Spin, etc)
    -Swap (Abra, Gardevoir)
    -Draco Meteor effects

    -Add check when attack_click == True so that tagging frozen,
    sleeping or marked units is allowed

    DONE:
    -Add tagging logic for removal of ally markers and freeze / sleep
    -MOVED TO OBJECT-ORIENTED SYSTEM
    -Simple, compulsory, linear knockback effects of varying
        distances (no optional or traced paths, i.e. 'opponent
        chooses the point' or around-the-corner pathing)
    -Updated evolution functions so that they occur outside
        of the game loop, allowing for use of evolution effects
    -Draw opaque rings or circles as indicators of status effects
    -Simple Wait effects (Purple / Blue; other colors' simple Wait
    effects in place but not implemented yet)
    -Simple Status Affliction

-ADD ABILITIES
    -Establish event ID checking system for accurate timing of
    abilities and attack effects (i.e. the difference between
    "White: When this unit is knocked out...", "White: Spin
    until you don't spin this attack. Gain X*Y", "White: if the
    opponent spins an attack >X, this unit can't be KO'd",
    "Ability: Water-types can't be paralyzed", etc)

-PACKAGING / HOSTING
    -UUUGGGHHHH

"""
from glob import iglob
import tkinter as tk
from tkinter import ttk
import arcade
import json
import sys
import os
import random
import time
from math import floor
from subprocess import call


class GlobalConst():
    def __init__(self):
        self.SCREEN_WIDTH = 0
        self.SCREEN_HEIGHT = 0
        self.ASPECT_RATIO = 0
        self.SPRITE_SCALING = 0
        self.SCREEN_TITLE = "PoDu ReDux v0.2.3"
        self.FILE_PATH = os.path.dirname(sys.argv[0])
        self.STATS_PATH = os.path.join(
            self.FILE_PATH,
            "pkmn-stats.json")
        self.PKMN_STATS = json.load(open(self.STATS_PATH, "r"))
        self.BG_PATH = os.path.join(
            self.FILE_PATH,
            "images",
            "board",
            "backgrounds")
        self.STATUS_COLORS = {'burned': (175, 0, 42),
                              'paralyzed': (255, 191, 0),
                              'frozen': (127, 255, 212),
                              'poisoned': (135, 50, 96),
                              'noxious': (255, 0, 127),
                              'sleep': (100, 149, 237)}


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
        self.turn_player = random.randint(1, 2)
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
        self.top_range = None
        self.bottom_range = None
        self.attacker_current_spin = None
        self.defender_current_spin = None
        self.p1_bench_targets = []
        self.p1_PC_targets = []
        self.p1_board_targets = []
        self.p1_Elim_targets = []
        self.p1_ultra_space_targets = []
        self.p2_bench_targets = []
        self.p2_PC_targets = []
        self.p2_board_targets = []
        self.p2_Elim_targets = []
        self.p2_ultra_space_targets = []
        self.combatant_1_power = 'None'
        self.combatant_2_power = 'None'
        self.tag_targets = []
        self.counter = 0
        self.hover_pkmn = None
        self.effect_targets = []
        self.checked_targets = []
        self.next_target = None
        self.turn_change = False

class BoardNeighbors():
    """
    Create generic board spaces and
    assign list of neighbor spaces
    """

    def __init__(self):
        self.Label = ''
        self.Neighbors = {}
        self.Coords = ()
        self.ForceStop = False
        self.ForceAttack = False
        self.Occupied = False
        self.Occupant = ''
        self.OccupantTeam = 0
        self.Passable = True
        self.Ctrl = 0
        self.Player1Entry = False
        self.Player1Goal = False
        self.Player2Entry = False
        self.Player2Goal = False

    def __str__(self):
        return self.Label

class ClassicBoardGenerator():
    #6v6 Board
    """
    Create board object with space Labels
    and adjusted bools for special spaces
    """

    def __init__(self):

        """In-Play Spaces"""
        self.A1 = BoardNeighbors()
        self.A2 = BoardNeighbors()
        self.A3 = BoardNeighbors()
        self.A4 = BoardNeighbors()
        self.A5 = BoardNeighbors()
        self.A6 = BoardNeighbors()
        self.A7 = BoardNeighbors()
        self.B1 = BoardNeighbors()
        self.B2 = BoardNeighbors()
        self.B4 = BoardNeighbors()
        self.B6 = BoardNeighbors()
        self.B7 = BoardNeighbors()
        self.C1 = BoardNeighbors()
        self.C2 = BoardNeighbors()
        self.C6 = BoardNeighbors()
        self.C7 = BoardNeighbors()
        self.D1 = BoardNeighbors()
        self.D2 = BoardNeighbors()
        self.D4 = BoardNeighbors()
        self.D6 = BoardNeighbors()
        self.D7 = BoardNeighbors()
        self.E1 = BoardNeighbors()
        self.E2 = BoardNeighbors()
        self.E3 = BoardNeighbors()
        self.E4 = BoardNeighbors()
        self.E5 = BoardNeighbors()
        self.E6 = BoardNeighbors()
        self.E7 = BoardNeighbors()

        self.A1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.285),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A1.Label = "A1"
        self.A1.Neighbors = (self.B1, self.B2, self.A2)
        self.A1.Player1Entry = True
        
        self.A2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.356),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A2.Label = "A2"
        self.A2.Neighbors = (self.A1, self.A3)
        
        self.A3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.427),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A3.Label = "A3"
        self.A3.Neighbors = (self.A2, self.A4)
        
        self.A4.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.500),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A4.Label = "A4"
        self.A4.Neighbors = (self.A3, self.A5)
        self.A4.Player1Goal = True
        
        self.A5.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.572),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A5.Label = "A5"
        self.A5.Neighbors = (self.A4, self.B4, self.A6)
        
        self.A6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.643),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A6.Label = "A6"
        self.A6.Neighbors = (self.A5, self.A7)
        
        self.A7.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.713),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A7.Label = "A7"
        self.A7.Neighbors = (self.A6, self.B6, self.B7)
        self.A7.Player1Entry = True

        ####################################################

        self.B1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.285),
                          floor(GlobalConst.SCREEN_HEIGHT*0.405)]
        self.B1.Label = "B1"
        self.B1.Neighbors = (self.A1, self.C1)
        
        self.B2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.390),
                          floor(GlobalConst.SCREEN_HEIGHT*0.405)]
        self.B2.Label = "B2"
        self.B2.Neighbors = (self.A1, self.B4, self.C2)

        self.B4.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.500),
                          floor(GlobalConst.SCREEN_HEIGHT*0.405)]
        self.B4.Label = "B4"
        self.B4.Neighbors = (self.B2, self.A5, self.B6)
        
        self.B6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.609),
                          floor(GlobalConst.SCREEN_HEIGHT*0.405)]
        self.B6.Label = "B6"
        self.B6.Neighbors = (self.A7, self.C6, self.B4)
        
        self.B7.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.713),
                          floor(GlobalConst.SCREEN_HEIGHT*0.405)]
        self.B7.Label = "B7"
        self.B7.Neighbors = (self.A7, self.C7)

        ####################################################

        self.C1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.285),
                          floor(GlobalConst.SCREEN_HEIGHT*0.500)]
        self.C1.Label = "C1"
        self.C1.Neighbors = (self.B1, self.D1)
        
        self.C2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.390),
                          floor(GlobalConst.SCREEN_HEIGHT*0.500)]
        self.C2.Label = "C2"
        self.C2.Neighbors = (self.B2, self.D2)
        
        self.C6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.609),
                          floor(GlobalConst.SCREEN_HEIGHT*0.500)]
        self.C6.Label = "C6"
        self.C6.Neighbors = (self.B6, self.D6)
        
        self.C7.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.713),
                          floor(GlobalConst.SCREEN_HEIGHT*0.500)]
        self.C7.Label = "C7"
        self.C7.Neighbors = (self.B7, self.D7)

        ####################################################

        self.D1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.285),
                          floor(GlobalConst.SCREEN_HEIGHT*0.596)]
        self.D1.Label = "D1"
        self.D1.Neighbors = (self.E1, self.C1)
        
        self.D2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.390),
                          floor(GlobalConst.SCREEN_HEIGHT*0.596)]
        self.D2.Label = "D2"
        self.D2.Neighbors = (self.E1, self.D4, self.C2)

        self.D4.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.500),
                          floor(GlobalConst.SCREEN_HEIGHT*0.596)]
        self.D4.Label = "D4"
        self.D4.Neighbors = (self.D2, self.E3, self.D6)
        
        self.D6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.609),
                          floor(GlobalConst.SCREEN_HEIGHT*0.596)]
        self.D6.Label = "D6"
        self.D6.Neighbors = (self.E7, self.D4, self.C6)
        
        self.D7.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.713),
                          floor(GlobalConst.SCREEN_HEIGHT*0.596)]
        self.D7.Label = "D7"
        self.D7.Neighbors = (self.C7, self.E7)

        ####################################################

        self.E1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.285),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E1.Label = "E1"
        self.E1.Neighbors = (self.D1, self.E2, self.D2)
        self.E1.Player2Entry = True
        
        self.E2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.356),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E2.Label = "E2"
        self.E2.Neighbors = (self.E1, self.E3)
        
        self.E3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.427),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E3.Label = "E3"
        self.E3.Neighbors = (self.E2, self.D4, self.E4)
        
        self.E4.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.500),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E4.Label = "E4"
        self.E4.Neighbors = (self.E3, self.E5)
        self.E4.Player2Goal = True
        
        self.E5.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.572),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E5.Label = "E5"
        self.E5.Neighbors = (self.E4, self.E6)
        
        self.E6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.643),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E6.Label = "E6"
        self.E6.Neighbors = (self.E5, self.E7)
        
        self.E7.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.713),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E7.Label = "E7"
        self.E7.Neighbors = (self.E6, self.D6, self.D7)
        self.E7.Player2Entry = True

        ####################################################

        
        
        #Player 1 Bench

        self.Player1Bench1 = BoardNeighbors()
        self.Player1Bench1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.300),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.180)]
        self.Player1Bench1.Neighbors = (self.A1, self.A7)
        self.Player1Bench1.Occupant = PlayerTeams.Player1.Pkmn1
        self.Player1Bench1.OccupantTeam = 1
        self.Player1Bench1.Occupied = True

        self.Player1Bench2 = BoardNeighbors()
        self.Player1Bench2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.400),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.180)]
        self.Player1Bench2.Neighbors = (self.A1, self.A7)
        self.Player1Bench2.Occupant = PlayerTeams.Player1.Pkmn2
        self.Player1Bench2.OccupantTeam = 1
        self.Player1Bench2.Occupied = True

        self.Player1Bench3 = BoardNeighbors()
        self.Player1Bench3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.500),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.180)]
        self.Player1Bench3.Neighbors = (self.A1, self.A7)
        self.Player1Bench3.Occupant = PlayerTeams.Player1.Pkmn3
        self.Player1Bench3.OccupantTeam = 1
        self.Player1Bench3.Occupied = True

        self.Player1Bench4 = BoardNeighbors()
        self.Player1Bench4.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.350),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.110)]
        self.Player1Bench4.Neighbors = (self.A1, self.A7)
        self.Player1Bench4.Occupant = PlayerTeams.Player1.Pkmn4
        self.Player1Bench4.OccupantTeam = 1
        self.Player1Bench4.Occupied = True
        
        self.Player1Bench5 = BoardNeighbors()
        self.Player1Bench5.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.450),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.110)]
        self.Player1Bench5.Neighbors = (self.A1, self.A7)
        self.Player1Bench5.Occupant = PlayerTeams.Player1.Pkmn5
        self.Player1Bench5.OccupantTeam = 1
        self.Player1Bench5.Occupied = True

        self.Player1Bench6 = BoardNeighbors()
        self.Player1Bench6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.550),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.110)]
        self.Player1Bench6.Neighbors = (self.A1, self.A7)
        self.Player1Bench6.Occupant = PlayerTeams.Player1.Pkmn6
        self.Player1Bench6.OccupantTeam = 1
        self.Player1Bench6.Occupied = True

        ####################################################
        #Player 2 Bench

        self.Player2Bench1 = BoardNeighbors()
        self.Player2Bench1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.500),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.825)]
        self.Player2Bench1.Neighbors = (self.E1, self.E7)
        self.Player2Bench1.Occupant = PlayerTeams.Player2.Pkmn1
        self.Player2Bench1.OccupantTeam = 1
        self.Player2Bench1.Occupied = True

        self.Player2Bench2 = BoardNeighbors()
        self.Player2Bench2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.600),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.825)]
        self.Player2Bench2.Neighbors = (self.E1, self.E7)
        self.Player2Bench2.Occupant = PlayerTeams.Player2.Pkmn2
        self.Player2Bench2.OccupantTeam = 1
        self.Player2Bench2.Occupied = True

        self.Player2Bench3 = BoardNeighbors()
        self.Player2Bench3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.700),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.825)]
        self.Player2Bench3.Neighbors = (self.E1, self.E7)
        self.Player2Bench3.Occupant = PlayerTeams.Player2.Pkmn3
        self.Player2Bench3.OccupantTeam = 1
        self.Player2Bench3.Occupied = True

        self.Player2Bench4 = BoardNeighbors()
        self.Player2Bench4.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.450),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.900)]
        self.Player2Bench4.Neighbors = (self.E1, self.E7)
        self.Player2Bench4.Occupant = PlayerTeams.Player2.Pkmn4
        self.Player2Bench4.OccupantTeam = 1
        self.Player2Bench4.Occupied = True

        self.Player2Bench5 = BoardNeighbors()
        self.Player2Bench5.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.550),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.900)]
        self.Player2Bench5.Neighbors = (self.E1, self.E7)
        self.Player2Bench5.Occupant = PlayerTeams.Player2.Pkmn5
        self.Player2Bench5.OccupantTeam = 1
        self.Player2Bench5.Occupied = True

        self.Player2Bench6 = BoardNeighbors()
        self.Player2Bench6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.650),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.900)]
        self.Player2Bench6.Neighbors = (self.E1, self.E7)
        self.Player2Bench6.Occupant = PlayerTeams.Player2.Pkmn6
        self.Player2Bench6.OccupantTeam = 1
        self.Player2Bench6.Occupied = True

        self.Player1Bench1.Label = 'Player 1 Bench 1'
        self.Player1Bench2.Label = 'Player 1 Bench 2'
        self.Player1Bench3.Label = 'Player 1 Bench 3'
        self.Player1Bench4.Label = 'Player 1 Bench 4'
        self.Player1Bench5.Label = 'Player 1 Bench 5'
        self.Player1Bench6.Label = 'Player 1 Bench 6'
        self.Player2Bench1.Label = 'Player 2 Bench 1'
        self.Player2Bench2.Label = 'Player 2 Bench 2'
        self.Player2Bench3.Label = 'Player 2 Bench 3'
        self.Player2Bench4.Label = 'Player 2 Bench 4'
        self.Player2Bench5.Label = 'Player 2 Bench 5'
        self.Player2Bench6.Label = 'Player 2 Bench 6'
        

        ####################################################


        self.Player1USpace1 = BoardNeighbors()
        self.Player1USpace1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.878),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.270)]
        self.Player1USpace1.Label = "Player 1 Ultra Space 1"
        
        self.Player1USpace2 = BoardNeighbors()
        self.Player1USpace2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.878),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.180)]
        self.Player1USpace2.Label = "Player 1 Ultra Space 2"
        
        self.Player1USpace3 = BoardNeighbors()
        self.Player1USpace3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.878),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.100)]
        self.Player1USpace3.Label = "Player 1 Ultra Space 3"

        self.Player1USpace4 = BoardNeighbors()
        self.Player1USpace4.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.950),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.225)]
        self.Player1USpace4.Label = "Player 1 Ultra Space 4"

        self.Player1USpace5 = BoardNeighbors()
        self.Player1USpace5.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.950),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.140)]
        self.Player1USpace5.Label = "Player 1 Ultra Space 5"

        self.Player1USpace6 = BoardNeighbors()
        self.Player1USpace6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.950),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.50)]
        self.Player1USpace6.Label = "Player 1 Ultra Space 6"

        ####################################################


        self.Player2USpace1 = BoardNeighbors()
        self.Player2USpace1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.120),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.270)]
        self.Player2USpace1.Label = "Player 2 Ultra Space 1"
        
        self.Player2USpace2 = BoardNeighbors()
        self.Player2USpace2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.120),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.180)]
        self.Player2USpace2.Label = "Player 2 Ultra Space 2"
        
        self.Player2USpace3 = BoardNeighbors()
        self.Player2USpace3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.120),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.100)]
        self.Player2USpace3.Label = "Player 2 Ultra Space 3"

        self.Player2USpace4 = BoardNeighbors()
        self.Player2USpace4.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.50),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.775)]
        self.Player2USpace4.Label = "Player 2 Ultra Space 4"

        self.Player2USpace5 = BoardNeighbors()
        self.Player2USpace5.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.50),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.865)]
        self.Player2USpace5.Label = "Player 2 Ultra Space 5"

        self.Player2USpace6 = BoardNeighbors()
        self.Player2USpace6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.50),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.950)]
        self.Player2USpace6.Label = "Player 2 Ultra Space 6"

        ####################################################


        self.Player1Elim1 = BoardNeighbors()
        self.Player1Elim1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.120),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.735)]
        self.Player1Elim1.Label = "Player 1 Eliminated 1"
        
        self.Player1Elim2 = BoardNeighbors()
        self.Player1Elim2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.120),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.825)]
        self.Player1Elim2.Label = "Player 1 Eliminated 2"
        
        self.Player1Elim3 = BoardNeighbors()
        self.Player1Elim3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.120),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.905)]
        self.Player1Elim3.Label = "Player 1 Eliminated 3"

        self.Player1Elim4 = BoardNeighbors()
        self.Player1Elim4.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.50),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.225)]
        self.Player1Elim4.Label = "Player 1 Eliminated 4"

        self.Player1Elim5 = BoardNeighbors()
        self.Player1Elim5.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.50),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.140)]
        self.Player1Elim5.Label = "Player 1 Eliminated 5"

        self.Player1Elim6 = BoardNeighbors()
        self.Player1Elim6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.50),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.50)]
        self.Player1Elim6.Label = "Player 1 Eliminated 6"

        ####################################################


        self.Player2Elim1 = BoardNeighbors()
        self.Player2Elim1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.878),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.735)]
        self.Player2Elim1.Label = "Player 2 Eliminated 1"
        
        self.Player2Elim2 = BoardNeighbors()
        self.Player2Elim2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.878),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.825)]
        self.Player2Elim2.Label = "Player 2 Eliminated 2"
        
        self.Player2Elim3 = BoardNeighbors()
        self.Player2Elim3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.878),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.905)]
        self.Player2Elim3.Label = "Player 2 Eliminated 3"

        self.Player2Elim4 = BoardNeighbors()
        self.Player2Elim4.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.950),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.775)]
        self.Player2Elim4.Label = "Player 2 Eliminated 4"

        self.Player2Elim5 = BoardNeighbors()
        self.Player2Elim5.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.950),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.865)]
        self.Player2Elim5.Label = "Player 2 Eliminated 5"

        self.Player2Elim6 = BoardNeighbors()
        self.Player2Elim6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.950),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.950)]
        self.Player2Elim6.Label = "Player 2 Eliminated 6"

        ####################################################


        self.Player1PC1 = BoardNeighbors()
        self.Player1PC1.Label = "Player 1 PC 1"
        self.Player1PC1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.630),
                                  floor(GlobalConst.SCREEN_HEIGHT*0.180)]

        self.Player1PC2 = BoardNeighbors()
        self.Player1PC2.Label = "Player 1 PC 2"
        self.Player1PC2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.710),
                                  floor(GlobalConst.SCREEN_HEIGHT*0.180)]

        ####################################################


        self.Player2PC1 = BoardNeighbors()
        self.Player2PC1.Label = "Player 2 PC 1"
        self.Player2PC1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.370),
                                  floor(GlobalConst.SCREEN_HEIGHT*0.820)]

        self.Player2PC2 = BoardNeighbors()
        self.Player2PC2.Label = "Player 2 PC 2"
        self.Player2PC2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.290),
                                  floor(GlobalConst.SCREEN_HEIGHT*0.820)]

    def __iter__(self):
        GlobalVars.counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if GlobalVars.counter == len(self.__dict__.values()):
            GlobalVars.counter = 0
            raise StopIteration
        else:
            GlobalVars.counter += 1
            return __iterator
        
class TvTBoardGenerator():
    # 3v3 Board
    """
    Create board object with space Labels
    and adjusted bools for special spaces
    """

    def __init__(self):

        """In-Play Spaces"""
        self.A1 = BoardNeighbors()
        self.A2 = BoardNeighbors()
        self.A3 = BoardNeighbors()
        self.A4 = BoardNeighbors()
        self.A5 = BoardNeighbors()
        self.A6 = BoardNeighbors()
        self.A7 = BoardNeighbors()
        self.B1 = BoardNeighbors()
        self.B2 = BoardNeighbors()
        self.B6 = BoardNeighbors()
        self.B7 = BoardNeighbors()
        self.C1 = BoardNeighbors()
        self.C2 = BoardNeighbors()
        self.C4 = BoardNeighbors()
        self.C6 = BoardNeighbors()
        self.C7 = BoardNeighbors()
        self.D1 = BoardNeighbors()
        self.D2 = BoardNeighbors()
        self.D6 = BoardNeighbors()
        self.D7 = BoardNeighbors()
        self.E1 = BoardNeighbors()
        self.E2 = BoardNeighbors()
        self.E3 = BoardNeighbors()
        self.E4 = BoardNeighbors()
        self.E5 = BoardNeighbors()
        self.E6 = BoardNeighbors()
        self.E7 = BoardNeighbors()
        
        self.A1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.285),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A1.Label = "A1"
        self.A1.Neighbors = (self.B1, self.B2, self.A2)
        self.A1.Player1Entry = True
        
        self.A2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.356),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A2.Label = "A2"
        self.A2.Neighbors = (self.A1, self.A3)
        
        self.A3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.427),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A3.Label = "A3"
        self.A3.Neighbors = (self.A2, self.A4)
        
        self.A4.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.500),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A4.Label = "A4"
        self.A4.Neighbors = (self.A3, self.A5)
        self.A4.Player1Goal = True
        
        self.A5.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.572),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A5.Label = "A5"
        self.A5.Neighbors = (self.A4, self.A6)
        
        self.A6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.643),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A6.Label = "A6"
        self.A6.Neighbors = (self.A5, self.A7)
        self.A6.Player1Entry = True
        
        self.A7.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.713),
                          floor(GlobalConst.SCREEN_HEIGHT*0.287)]
        self.A7.Label = "A7"
        self.A7.Neighbors = (self.A6, self.B6, self.B7)

        ####################################################

        self.B1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.285),
                          floor(GlobalConst.SCREEN_HEIGHT*0.405)]
        self.B1.Label = "B1"
        self.B1.Neighbors = (self.A1, self.C1)
        
        self.B2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.390),
                          floor(GlobalConst.SCREEN_HEIGHT*0.405)]
        self.B2.Label = "B2"
        self.B2.Neighbors = (self.A1, self.C2)
        
        self.B6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.609),
                          floor(GlobalConst.SCREEN_HEIGHT*0.405)]
        self.B6.Label = "B6"
        self.B6.Neighbors = (self.A7, self.C6)
        
        self.B7.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.713),
                          floor(GlobalConst.SCREEN_HEIGHT*0.405)]
        self.B7.Label = "B7"
        self.B7.Neighbors = (self.A7, self.C7)

        ####################################################

        self.C1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.285),
                          floor(GlobalConst.SCREEN_HEIGHT*0.500)]
        self.C1.Label = "C1"
        self.C1.Neighbors = (self.B1, self.D1)
        
        self.C2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.390),
                          floor(GlobalConst.SCREEN_HEIGHT*0.500)]
        self.C2.Label = "C2"
        self.C2.Neighbors = (self.B2, self.D2, self.C4)
        
        self.C4.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.500),
                          floor(GlobalConst.SCREEN_HEIGHT*0.500)]
        self.C4.Label = "C4"
        self.C4.Neighbors = (self.C2, self.C6)
        
        self.C6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.609),
                          floor(GlobalConst.SCREEN_HEIGHT*0.500)]
        self.C6.Label = "C6"
        self.C6.Neighbors = (self.B6, self.D6, self.C4)
        
        self.C7.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.713),
                          floor(GlobalConst.SCREEN_HEIGHT*0.500)]
        self.C7.Label = "C7"
        self.C7.Neighbors = (self.B7, self.D7)

        ####################################################

        self.D1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.285),
                          floor(GlobalConst.SCREEN_HEIGHT*0.596)]
        self.D1.Label = "D1"
        self.D1.Neighbors = (self.E1, self.C1)
        
        self.D2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.390),
                          floor(GlobalConst.SCREEN_HEIGHT*0.596)]
        self.D2.Label = "D2"
        self.D2.Neighbors = (self.E1, self.C2)
        
        self.D6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.609),
                          floor(GlobalConst.SCREEN_HEIGHT*0.596)]
        self.D6.Label = "D6"
        self.D6.Neighbors = (self.E7, self.C6)
        
        self.D7.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.713),
                          floor(GlobalConst.SCREEN_HEIGHT*0.596)]
        self.D7.Label = "D7"
        self.D7.Neighbors = (self.C7, self.E7)

        ####################################################

        self.E1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.285),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E1.Label = "E1"
        self.E1.Neighbors = (self.D1, self.E2, self.D2)
        
        self.E2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.356),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E2.Label = "E2"
        self.E2.Neighbors = (self.E1, self.E3)
        self.E2.Player2Entry = True
        
        self.E3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.427),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E3.Label = "E3"
        self.E3.Neighbors = (self.E2, self.E4)
        
        self.E4.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.500),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E4.Label = "E4"
        self.E4.Neighbors = (self.E3, self.E5)
        self.E4.Player2Goal = True
        
        self.E5.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.572),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E5.Label = "E5"
        self.E5.Neighbors = (self.E4, self.E6)
        
        self.E6.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.643),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E6.Label = "E6"
        self.E6.Neighbors = (self.E5, self.E7)
        
        self.E7.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.713),
                          floor(GlobalConst.SCREEN_HEIGHT*0.713)]
        self.E7.Label = "E7"
        self.E7.Neighbors = (self.E6, self.D6, self.D7)
        self.E7.Player2Entry = True

        ####################################################

        
        
        """Player 1 Bench"""

        self.Player1Bench1 = BoardNeighbors()
        self.Player1Bench1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.300),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.180)]
        self.Player1Bench1.Neighbors = (self.A1, self.A6)
        self.Player1Bench1.Occupant = PlayerTeams.Player1.Pkmn1
        self.Player1Bench1.OccupantTeam = 1
        self.Player1Bench1.Occupied = True

        self.Player1Bench2 = BoardNeighbors()
        self.Player1Bench2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.400),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.180)]
        self.Player1Bench2.Neighbors = (self.A1, self.A6)
        self.Player1Bench2.Occupant = PlayerTeams.Player1.Pkmn2
        self.Player1Bench2.OccupantTeam = 1
        self.Player1Bench2.Occupied = True

        self.Player1Bench3 = BoardNeighbors()
        self.Player1Bench3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.500),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.180)]
        self.Player1Bench3.Neighbors = (self.A1, self.A6)
        self.Player1Bench3.Occupant = PlayerTeams.Player1.Pkmn3
        self.Player1Bench3.OccupantTeam = 1
        self.Player1Bench3.Occupied = True

        ####################################################
        """Player 2 Bench"""

        self.Player2Bench1 = BoardNeighbors()
        self.Player2Bench1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.500),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.825)]
        self.Player2Bench1.Neighbors = (self.E2, self.E7)
        self.Player2Bench1.Occupant = PlayerTeams.Player2.Pkmn1
        self.Player2Bench1.OccupantTeam = 1
        self.Player2Bench1.Occupied = True

        self.Player2Bench2 = BoardNeighbors()
        self.Player2Bench2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.600),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.825)]
        self.Player2Bench2.Neighbors = (self.E2, self.E7)
        self.Player2Bench2.Occupant = PlayerTeams.Player2.Pkmn2
        self.Player2Bench2.OccupantTeam = 1
        self.Player2Bench2.Occupied = True

        self.Player2Bench3 = BoardNeighbors()
        self.Player2Bench3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.700),
                                     floor(GlobalConst.SCREEN_HEIGHT*0.825)]
        self.Player2Bench3.Neighbors = (self.E2, self.E7)
        self.Player2Bench3.Occupant = PlayerTeams.Player2.Pkmn3
        self.Player2Bench3.OccupantTeam = 1
        self.Player2Bench3.Occupied = True

        self.Player1Bench1.Label = 'Player 1 Bench 1'
        self.Player1Bench2.Label = 'Player 1 Bench 2'
        self.Player1Bench3.Label = 'Player 1 Bench 3'
        self.Player2Bench1.Label = 'Player 2 Bench 1'
        self.Player2Bench2.Label = 'Player 2 Bench 2'
        self.Player2Bench3.Label = 'Player 2 Bench 3'
        

        ####################################################


        self.Player1USpace1 = BoardNeighbors()
        self.Player1USpace1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.878),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.270)]
        self.Player1USpace1.Label = "Player 1 Ultra Space 1"
        
        self.Player1USpace2 = BoardNeighbors()
        self.Player1USpace2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.878),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.180)]
        self.Player1USpace2.Label = "Player 1 Ultra Space 2"
        
        self.Player1USpace3 = BoardNeighbors()
        self.Player1USpace3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.878),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.100)]
        self.Player1USpace3.Label = "Player 1 Ultra Space 3"

        ####################################################


        self.Player2USpace1 = BoardNeighbors()
        self.Player2USpace1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.120),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.270)]
        self.Player2USpace1.Label = "Player 2 Ultra Space 1"
        
        self.Player2USpace2 = BoardNeighbors()
        self.Player2USpace2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.120),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.180)]
        self.Player2USpace2.Label = "Player 2 Ultra Space 2"
        
        self.Player2USpace3 = BoardNeighbors()
        self.Player2USpace3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.120),
                                      floor(GlobalConst.SCREEN_HEIGHT*0.100)]
        self.Player2USpace3.Label = "Player 2 Ultra Space 3"

        ####################################################


        self.Player1Elim1 = BoardNeighbors()
        self.Player1Elim1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.120),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.735)]
        self.Player1Elim1.Label = "Player 1 Eliminated 1"
        
        self.Player1Elim2 = BoardNeighbors()
        self.Player1Elim2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.120),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.825)]
        self.Player1Elim2.Label = "Player 1 Eliminated 2"
        
        self.Player1Elim3 = BoardNeighbors()
        self.Player1Elim3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.120),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.905)]
        self.Player1Elim3.Label = "Player 1 Eliminated 3"

        ####################################################


        self.Player2Elim1 = BoardNeighbors()
        self.Player2Elim1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.878),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.735)]
        self.Player2Elim1.Label = "Player 2 Eliminated 1"
        
        self.Player2Elim2 = BoardNeighbors()
        self.Player2Elim2.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.878),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.825)]
        self.Player2Elim2.Label = "Player 2 Eliminated 2"
        
        self.Player2Elim3 = BoardNeighbors()
        self.Player2Elim3.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.878),
                                    floor(GlobalConst.SCREEN_HEIGHT*0.905)]
        self.Player2Elim3.Label = "Player 2 Eliminated 3"

        ####################################################


        self.Player1PC1 = BoardNeighbors()
        self.Player1PC1.Label = "Player 1 PC 1"
        self.Player1PC1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.675),
                                  floor(GlobalConst.SCREEN_HEIGHT*0.180)]

        ####################################################


        self.Player2PC1 = BoardNeighbors()
        self.Player2PC1.Label = "Player 2 PC 1"
        self.Player2PC1.Coords = [floor(GlobalConst.SCREEN_HEIGHT*0.330),
                                  floor(GlobalConst.SCREEN_HEIGHT*0.820)]

    def __iter__(self):
        GlobalVars.counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if GlobalVars.counter == len(self.__dict__.values()):
            GlobalVars.counter = 0
            raise StopIteration
        else:
            GlobalVars.counter += 1
            return __iterator

class AllTeams():
    def __init__(self):
        pass

    def __iter__(self):
        GlobalVars.counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if GlobalVars.counter == len(self.__dict__.values()):
            GlobalVars.counter = 0
            raise StopIteration
        else:
            GlobalVars.counter += 1
            return __iterator

    def __str__(self):
        return 'Player Teams'

class Pokemon():
    def __init__(self, line = None, Ctrl = None):
        self.Attacks = Attacks()
        self.Loc = None
        self.OrigLoc = None
        self.KnockedOut = False
        self.IsSurrounded = False
        self.ToPC = False
        self.ToElim = False
        self.ToUSpace = False
        self.ToBench = False
        self.Wait = 0
        self.InPlay = False
        self.Status = 'clear'
        self.Markers = 'clear'
        self.Ctrl = Ctrl
        self.Stage = 0
        self.FinalSongCount = None
        self.PreviousLoc = None
        self.OrigForm = None
        self.CombatRange = 1
        
        pkmn_stat_dict = GlobalConst.PKMN_STATS[line]
        for keys, values in pkmn_stat_dict.items():
            new_keys = keys[0].upper() + keys[1:]
            if keys.startswith('attack') == False:
                setattr(self, f"{new_keys}", values)
        for keys, values in pkmn_stat_dict.items():
            new_keys = keys[0].upper() + keys[1:]
            if keys.startswith('attack'):
                new_attack_keys = keys[7].upper() + keys[8:]
                if new_attack_keys == 'Color' and values == None:
                    break
                if hasattr(self, "Attacks") == False:
                    setattr(
                        self, "Attacks", AttackList())
                if hasattr(
                    self.Attacks, f"Attack{keys[6]}") == False:
                    setattr(
                        self.Attacks, f"Attack{keys[6]}", Attacks())
                current_attack = getattr(
                    self.Attacks, f"Attack{keys[6]}")
                setattr(current_attack, new_attack_keys, values)
                if hasattr(current_attack, "Effect") == False:
                    setattr(current_attack, "Effect", None)
                if hasattr(current_attack, "Power") == False:
                    setattr(current_attack, "Power", None)
                if current_attack.Power != None:
                    current_attack.OrigPower = current_attack.Power
                else:
                    current_attack.OrigPower = None


    def __iter__(self):
        GlobalVars.counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if GlobalVars.counter == len(self.__dict__.values()):
            GlobalVars.counter = 0
            raise StopIteration
        else:
            GlobalVars.counter += 1
            return __iterator

    def __str__(self):
        return self.Name

class AttackList():
    def __init__(self):
        pass

    def __iter__(self):
        GlobalVars.counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if GlobalVars.counter == len(self.__dict__.values()):
            GlobalVars.counter = 0
            raise StopIteration
        else:
            GlobalVars.counter += 1
            return __iterator

class Attacks():
    def __init__(self):
        pass

    def __iter__(self):
        GlobalVars.counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if GlobalVars.counter == len(self.__dict__.values()):
            GlobalVars.counter = 0
            raise StopIteration
        else:
            GlobalVars.counter += 1
            return __iterator

class PlayerTeam():
    def __init__(self, Ctrl):
        team_file = getattr(GlobalVars, f"player_{Ctrl}_select")
        if GlobalVars.game_mode == "Classic":
            selected_team_path = os.path.join(
                GlobalConst.FILE_PATH,
                "saves",
                "classic_teams",
                f"{team_file}")
            GlobalVars.top_range = 1
            GlobalVars.bottom_range = 7
        elif GlobalVars.game_mode == "3v3":
            selected_team_path = os.path.join(
                GlobalConst.FILE_PATH,
                "saves",
                "3v3_teams",
                f"{team_file}")
            GlobalVars.top_range = 1
            GlobalVars.bottom_range = 4

        custom_team = open(selected_team_path)
        custom_team = custom_team.read().splitlines()
        line_counter = 1
        GlobalVars.gamelog.append(f"Player {Ctrl}'s team:")
        GlobalVars.gamelog.append(str("-" * 8 + team_file[:-4] + "-" * 8))
        for line in custom_team:
            setattr(self, f"Pkmn{line_counter}", Pokemon(line, Ctrl))

            GlobalVars.gamelog.append(GlobalConst.PKMN_STATS[line]['name'])
            line_counter += 1
            if GlobalVars.game_mode == "Classic" and line_counter == 7:
                break
            elif GlobalVars.game_mode == "3v3" and line_counter == 4:
                break
            else:
                continue

            if current_poke.Name == 'Reshiram' or \
               current_poke.Name == 'Zekrom':
                current_poke.Wait = 9
            elif current_poke.Name == 'Nincada':
                current_poke.Wait = 10
        
    def __iter__(self):
        GlobalVars.counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if GlobalVars.counter == len(self.__dict__.values()):
            GlobalVars.counter = 0
            raise StopIteration
        else:
            GlobalVars.counter += 1
            return __iterator

    def __str__(self):
        return str(self)
##############################################################################


def write_log():
    log_stamp = time.ctime()
    log_stamp = log_stamp.replace(' ', '_')
    log_stamp = log_stamp.replace(':', '-')
    LOG_PATH = os.path.join(
        GlobalConst.FILE_PATH,
        "saves",
        "gamelogs",
        f"PoDuReDux_Log_{log_stamp}.txt")
    LOG_FILE = open(LOG_PATH, "a+")
    for lines in GlobalVars.gamelog:
        LOG_FILE.write(lines)
    LOG_FILE.close()


# DRAFT EFFECTS
"""
def turn_tickdown():
    #add when other tickdown effects are added
    mega_evolution_tickdown()
    wait_tickdown()
    final_song_tickdown()

def send_to_bench(target):
    # add when clear differentiation made between KOs, send-to-x,
    # etc and when Pokemon class attributes 
    target.Loc = target.OrigLoc
    target.Status = 'clear'
    target.Marker = 'clear'

def multitarget():
    # Run loops over teams and use this as a decorator for simpler effects.
    # EX:
    # multitarget(target_group, effect, *args)
    #     for pkmns in target_group:
    #         effect(*args) # Translates to apply_wait(target, 5)
    # multitarget(opposing_team, apply_wait, target, 5)
    # !!translation: apply wait 5 for entire opposing team

def attack_respin():
    #for optional respinning like Deoxy-A or Double Chance
    pass

def attack_spin_effect():
    #for Fire Spin, Swords Dance, etc
    pass

def fly():
    #for selectable flight pathing (i.e.
    #fly to space 1-2 spaces behind opponent)
    pass

def fly_away():
    #for pre-determined flight pathing (i.e. fly to space behind opponent)
    pass

def knockback():
    #for knockback resolution; implements knockback_pathing()
    pass

def final_song_tickdown():
    pass

def mega_evolution_tickdown():
    pass
"""

def knockback_pathing(effect_user,
                      target, distance = 1,
                      continuous = False,
                      multitarget = False):
    GlobalVars.effect_targets = []
    GlobalVars.loop_counter = 0
    GlobalVars.gamelog.append(f"{target.Name} was knocked back " \
                              f"{distance} step(s).")
    if target.Loc.Coords[0] == effect_user.Loc.Coords[0]:
        check_value = 0
    elif target.Loc.Coords[1] == effect_user.Loc.Coords[1]:
        check_value = 1
    else:
        check_value = None

    def single_target_iter(effect_user = effect_user,
                           target_loc = target.Loc,
                           distance = distance):
        for neighbors in target_loc.Neighbors:
            if neighbors:
                if neighbors == target_loc.Neighbors[-1]:
                    GlobalVars.loop_counter += 1
                if neighbors.Coords[
                    check_value] == effect_user.Loc.Coords[check_value]:
                    if neighbors not in GlobalVars.effect_targets \
                       and neighbors.Occupied == False:
                        GlobalVars.next_target = neighbors
                        GlobalVars.effect_targets.append(neighbors)
            else:
                GlobalVars.loop_counter += 1
        
        if GlobalVars.loop_counter == distance and GlobalVars.next_target:
            space_cleanup(target.Loc)
            move_to_space(target, GlobalVars.next_target)
            GlobalVars.effect_targets = []
            GlobalVars.loop_counter = 0
            GlobalVars.next_target = None
        elif GlobalVars.next_target == None:
            pass
        else:
            single_target_iter(effect_user,
                               GlobalVars.next_target,
                               distance = distance)
    if check_value != None:
        if multitarget == False:
            single_target_iter()
        elif multitarget == True and continuous == False:
            pass
            # add variables to establish specific target's
            # location as the focal point
        else:
            pass
    else:
        pass

        #for psychic shove
                
def turn_rotate():
    linebreak_text = '-' * 5
    if GlobalVars.turn_player == 1:
        GlobalVars.turn_player = 2
        GlobalVars.gamelog.append(linebreak_text*6)
        GlobalVars.gamelog.append(
            f"{linebreak_text}Player " \
            f"{GlobalVars.turn_player} " \
            f"Turn{linebreak_text}")
        GlobalVars.gamelog.append(linebreak_text*6)
        wait_tickdown()
        if GlobalVars.first_turn:
            GlobalVars.first_turn = False
    elif GlobalVars.turn_player == 2:
        GlobalVars.turn_player = 1
        GlobalVars.gamelog.append(linebreak_text*6)
        GlobalVars.gamelog.append(
            f"{linebreak_text}Player " \
            f"{GlobalVars.turn_player} " \
            f"Turn{linebreak_text}")
        GlobalVars.gamelog.append(linebreak_text*6)
        wait_tickdown()
        if GlobalVars.first_turn:
            GlobalVars.first_turn = False
    GlobalVars.in_transit = ''
    GlobalVars.unit_moved = False
    GlobalVars.unit_attacked = False
    GlobalVars.turn_change = False

def pc_rotate(target):
    target.Status = 'clear'
    target.Marker = 'clear'
    for teams in PlayerTeams:
        for pkmns in teams:
            if pkmns.Ctrl == target.Ctrl:
                if 'PC' in pkmns.Loc.Label:
                    if GlobalVars.game_mode == 'Classic':
                        if pkmns.Loc.Label.endswith('1'):
                            pkmns.Loc = pkmns.OrigLoc
                            if pkmns.Wait >= 1:
                                pkmns.Wait += 1
                            else:
                                pkmns.Wait += 2
                        else:
                            if pkmns.Ctrl == 1:
                                pkmns.Loc = board.Player1PC1
                            else:
                                pkmns.Loc = board.Player2PC1
                    elif GlobalVars.game_mode == '3v3':
                        pkmns.Loc = pkmns.OrigLoc
                        if pkmns.Wait >= 1:
                            pkmns.Wait += 1
                        else:
                            pkmns.Wait += 2
            pkmns.Sprite.set_position(*pkmns.Loc.Coords)
    if GlobalVars.game_mode == "Classic":
        target.Loc = getattr(board, f"Player{target.Ctrl}PC2")
    elif GlobalVars.game_mode == "3v3":
        target.Loc = getattr(board, f"Player{target.Ctrl}PC1")
    target.Sprite.set_position(*target.Loc.Coords)
        

def apply_wait(target, duration=2):
    if target.Wait > 0:
        target.Wait += duration - 1
        GlobalVars.gamelog.append(
            f"{target.Name} gained Wait {duration - 1}.")
    else:
        target.Wait += duration
        GlobalVars.gamelog.append(
            f"{target.Name} gained Wait {duration - 1}.")

def apply_marker(marker_type = 'clear'):
    #for MP-X, Curse, Disguise, etc
    target.Marker = marker_type

def wait_tickdown():
    for teams in PlayerTeams:
        for pkmns in teams:
            if pkmns.Wait != 0:
                pkmns.Wait -= 1


def apply_status(target, status_type='clear'):
    target.Status = status_type
    if status_type == 'frozen' or status_type == 'sleep':
        target.Loc.Passable = True
    elif status_type == 'clear':
        target.Loc.Passable = False


def apply_marker(target, marker_type='clear'):
    target.Marker = marker_type


def surround_check(target):
    """Checks for surround conditions of a target space"""
    surround_counter = len(target.Loc.Neighbors)
    for locs in target.Loc.Neighbors:
        if locs.Ctrl != target.Ctrl and locs.Occupied:
            if locs.Occupant.Status not in ['frozen', 'sleep']:
                surround_counter -= 1
        else:
            continue
    if surround_counter == 0:
        return True
    else:
        return False
"""
def targeting_check(effect_user,
                    targeting_range,
                    target_preference = effect_user.Ctrl):
    \"""
    Look for potential effect targets within a range.
    Target preference options:
    -Player 1 control = 1
    -Player 2 control = 2
    -Any target = 0 / False
    \"""

    del GlobalVars.effects_targets[:]
    
    def path_iter(target, targeting_range, target_preference):
        next_moves = []
        for neighbors in target:
            if move + modifier == 0:
                break
            if neighbors.Passable:
                GlobalVars.effect_targets.append(neighbors)
                for new_neighbors in GlobalVars.effect_targets:
                    for next_neighbors in new_neighbors.Neighbors:
                        next_moves.append(next_neighbors)
            else:
                continue
        GlobalVars.loop_counter += 1
        if GlobalVars.loop_counter < move + modifier:
            path_iter(next_moves, move, modifier)

    path_iter(target_unit.Loc.Neighbors, modifier, target_unit.Move)
    GlobalVars.checked_targets = set(GlobalVars.effect_targets)
    to_remove = []
    for possible_moves in GlobalVars.checked_targets:
        if possible_moves.Occupied:
            to_remove.append(possible_moves)
        else:
            continue
    for invalid_move in to_remove:
        GlobalVars.checked_targets.remove(invalid_move)
    GlobalVars.effect_targets.clear()
    GlobalVars.loop_counter = 0
"""

def path_check(target_unit, modifier = 0, move = 0):
    """
    Check all possible paths for various purposes,
    including movement and teleports
    """

    del GlobalVars.valid_moves[:]
    if GlobalVars.first_turn:
        modifier = -1
        GlobalVars.gamelog.append("First turn: Movement reduced by 1.")
    else:
        pass
    
    def path_iter(target, modifier, move):
        next_moves = []
        for neighbors in target:
            if move + modifier == 0:
                break
            if neighbors.Passable:
                GlobalVars.valid_moves.append(neighbors)
                for new_neighbors in GlobalVars.valid_moves:
                    for next_neighbors in new_neighbors.Neighbors:
                        next_moves.append(next_neighbors)
            else:
                continue
        GlobalVars.loop_counter += 1
        if GlobalVars.loop_counter < move + modifier:
            path_iter(next_moves, move, modifier)

    path_iter(target_unit.Loc.Neighbors, modifier, target_unit.Move)
    GlobalVars.checked_moves = set(GlobalVars.valid_moves)
    to_remove = []
    for possible_moves in GlobalVars.checked_moves:
        if possible_moves.Occupied:
            to_remove.append(possible_moves)
        else:
            continue
    for invalid_move in to_remove:
        GlobalVars.checked_moves.remove(invalid_move)
    GlobalVars.valid_moves.clear()
    GlobalVars.loop_counter = 0


def spin(combatant):
    """
    Perform SPIN action for selected unit.
    Can be applied to effects and battles.
    """

    # Perfor  number randomization for spin
    combatant_spin = random.randint(1, 24)

    for attacks in combatant.Attacks:
        # Check if wheel segment is valid
        if combatant_spin <= attacks.Range:
            combatant_attack = attacks
            return combatant_attack
        else:
            continue

def move_to_space(target_pkmn, location):
    target_pkmn.Loc = location
    target_pkmn.Sprite.set_position(*location.Coords)
    location.Occupied = True
    location.Occupant = target_pkmn
    location.OccupantTeam = target_pkmn.Ctrl
    location.Ctrl = target_pkmn.Ctrl
    location.Passable = False

def space_cleanup(location):
    location.Occupied = False
    location.Occupant = None
    location.OccupantTeam = 0
    location.Ctrl = 0
    location.Passable = True

def target_finder(combatant):
    """
    Checks adjacent spaces for valid attack targets.
    Use effect_targeting for targets that don't involve
    normal attacks.
    """

    def target_iter(targets, attack_distance = combatant.CombatRange):
        next_targets = []
        for x in targets:
            GlobalVars.potential_targets.append(x)
            for y in GlobalVars.potential_targets:
                for new_neighbors in x.Neighbors:
                    next_targets.append(y)
        GlobalVars.loop_counter += 1
        if GlobalVars.loop_counter < attack_distance:
            target_iter(next_targets, attack_distance)

    if len(combatant.Loc.Label) == 2:
        GlobalVars.potential_targets = []
        GlobalVars.tag_targets = []
        target_iter(combatant.Loc.Neighbors)
        to_remove = []
        for x in GlobalVars.potential_targets:
            if x.Occupied == False:
                to_remove.append(x)
            elif x.Ctrl == combatant.Ctrl:
                to_remove.append(x)

                # add MP markers to this check when markers are implemented
                if x.Occupant.Status in ['frozen', 'sleep']:
                    GlobalVars.tag_targets.append(x)
            elif x.Ctrl == 0:
                to_remove.append(x)
        GlobalVars.potential_targets = set(
            GlobalVars.potential_targets).difference(to_remove)
        GlobalVars.tag_targets = set(GlobalVars.tag_targets)
    else:
        GlobalVars.potential_targets = []
        GlobalVars.tag_targets = []
    GlobalVars.loop_counter = 0

def battle_spin_compare(combatant_1, combatant_2):
    """
    Compare the SPIN of two battling units.

    'if  .Locks check for color matchups,
    then nest down to check power stats when
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

    GlobalVars.combatant_1_power = 'None'
    GlobalVars.combatant_2_power = 'None'

    combatant_1_attack = spin(combatant_1)
    GlobalVars.attacker_current_spin = combatant_1_attack
    combatant_2_attack = spin(combatant_2)
    GlobalVars.defender_current_spin = combatant_2_attack
    GlobalVars.gamelog.append(
        f"Player {GlobalVars.turn_player}'s {combatant_1.Name} " \
        f"({combatant_1.OrigLoc.Label[-1]}) attacked " \
        f"Player {combatant_2.Ctrl}'s " \
        f"{combatant_2.Name} ({combatant_2.OrigLoc.Label[-1]})")
    #need to boil this down to one function rather than retyping per player
    if combatant_1.Status != 'frozen':
        combatant_1_color = combatant_1_attack.Color
    else:
        combatant_1_color = "Red"
        GlobalVars.gamelog.append(
            f"Player {combatant_1.Ctrl}s {combatant_1.Name} " \
            f"{combatant_1.OrigLoc.Label[-1]} is frozen. " \
            "Wheel has become Miss.")
    if not combatant_1_color in ['Red', 'Blue']:
        GlobalVars.combatant_1_power = combatant_1_attack.Power
        if combatant_1_color in ['White', 'Gold']:
            if combatant_1.Status in ['poisoned', 'burned']:
                GlobalVars.combatant_1_power -= 20
            elif combatant_1.Status == "noxious":
                GlobalVars.combatant_1_power -= 40

    # Need to rework code to prevent procs of burned/paralyzed
    # attack effects. Delphox miss effects need to be taken
    # into heavy consideration
    #
    # Need to add check for attacks with same name
    if combatant_1.Status in ['paralyzed', 'burned']:
        if combatant_1.Status == 'burned':
            GlobalVars.gamelog.append(
                    f"Player {combatant_1.Ctrl}s {combatant_1.Name} " \
                    f"({combatant_1.OrigLoc.Label[-1]}) is burned. " \
                    "Attack power reduced by -20.")
        elif combatant_1.Status == "paralyzed":
                GlobalVars.gamelog.append(
                    f"Player {combatant_1.Ctrl}s {combatant_1.Name} " \
                    f"({combatant_1.OrigLoc.Label[-1]}) is paralyzed.")
        baseline_size = 24
        miss_candidates = []
        for attacks in combatant_1.Attacks:
            if attacks.Color != "Red" and attacks.Size <= baseline_size:
                baseline_size = attacks.Size
                for candidates in miss_candidates:
                    if candidates.Size > baseline_size:
                        miss_candidates.remove(candidates)
                miss_candidates.append(attacks)
        miss_check = random.choice(miss_candidates)
        if miss_check == combatant_1_attack:
            combatant_1_color = "Red"
            combatant_1_miss_check = True
            if combatant_1.Status == "burned":
                GlobalVars.gamelog.append(
                    f"Player {combatant_1.Ctrl}s {combatant_1.Name} " \
                    f"({combatant_1.OrigLoc.Label[-1]}) is burned. " \
                    f"Segment ({miss_check.Name}) has become Miss.")
            elif combatant_1.Status == "paralyzed":
                GlobalVars.gamelog.append(
                    f"Player {combatant_1.Ctrl}s {combatant_1.Name} " \
                    f"({combatant_1.OrigLoc.Label[-1]}) is paralyzed. " \
                    f"Smallest segment ({miss_check.Name}) has become Miss.")
        else:
            combatant_1_miss_check = False
    # Checks for Confusion status and returns next available attack segment
    if combatant_1.Status == 'confused':
        GlobalVars.gamelog.append(
            f"Player {combatant_1.Ctrl}s {combatant_1.Name} " \
            f"{combatant_1.OrigLoc.Label[-1]} is confused. " \
            "Attack has shifted one segment from " \
            f"{combatant_1_attack.Name}.")
        try:
            attack_iter = iter(combatant_1.Attacks)
            for attack in attack_iter:
                if attack == combatant_1_attack:
                    combatant_1_attack = next(attack_iter)
        except:
            combatant_1_attack = combatant_1.Attacks.Attack1

    if combatant_2.Status != 'frozen':
        combatant_2_color = combatant_2_attack.Color
    else:
        combatant_2_color = "Red"
        GlobalVars.gamelog.append(
            f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
            f"{combatant_2.OrigLoc.Label[-1]} is frozen. " \
            "Wheel has become Miss.")
    if not combatant_2_color in ['Red', 'Blue']:
        GlobalVars.combatant_2_power = combatant_2_attack.Power
        if combatant_2_color in ['White', 'Gold']:
            if combatant_2.Status in ['poisoned', 'burned']:
                GlobalVars.combatant_2_power -= 20
            elif combatant_2.Status == "noxious":
                GlobalVars.combatant_2_power -= 40

    # Need to rework code to prevent procs of burned/paralyzed
    # attack effects. Delphox miss effects need to be taken
    # into heavy consideration
    #
    # Need to add check for attacks with same name
    if combatant_2.Status in ['paralyzed', 'burned']:
        if combatant_2.Status == 'burned':
            GlobalVars.gamelog.append(
                    f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                    f"({combatant_2.OrigLoc.Label[-1]}) is burned. " \
                    "Attack power reduced by -20.")
        elif combatant_2.Status == "paralyzed":
                GlobalVars.gamelog.append(
                    f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                    f"({combatant_2.OrigLoc.Label[-1]}) is paralyzed.")
        baseline_size = 24
        miss_candidates = []
        for attacks in combatant_2.Attacks:
            if attacks.Color != "Red" and attacks.Size <= baseline_size:
                baseline_size = attacks.Size
                for candidates in miss_candidates:
                    if candidates.Size > baseline_size:
                        miss_candidates.remove(candidates)
                miss_candidates.append(attacks)
        miss_check = random.choice(miss_candidates)
        if miss_check == combatant_2_attack:
            combatant_2_color = "Red"
            combatant_2_miss_check = True
            if combatant_2.Status == "burned":
                GlobalVars.gamelog.append(
                    f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                    f"({combatant_2.OrigLoc.Label[-1]}) is burned. " \
                    f"Segment ({miss_check.Name}) has become Miss.")
            elif combatant_2.Status == "paralyzed":
                GlobalVars.gamelog.append(
                    f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                    f"({combatant_2.OrigLoc.Label[-1]}) is paralyzed. " \
                    f"Segment ({miss_check.Name}) has become Miss.")
        else:
            combatant_2_miss_check = False
    # Checks for Confusion status and returns next available attack segment
    if combatant_2.Status == 'confused':
        GlobalVars.gamelog.append(
            f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
            f"{combatant_2.OrigLoc.Label[-1]} is confused. " \
            "Attack has shifted one segment from " \
            f"{combatant_2_attack.Name}.")
        try:
            attack_iter = iter(combatant_2.Attacks)
            for attack in attack_iter:
                if attack == combatant_2_attack:
                    combatant_2_attack = next(attack_iter)
        except StopIteration:
            combatant_2_attack = combatant_2.Attacks.Attack1

    if combatant_1.Status == 'frozen':
        GlobalVars.gamelog.append(
            f"Player {GlobalVars.turn_player}'s {combatant_1.Name} " \
            f"({combatant_1.OrigLoc.Label[-1]}) spun Miss")
        GlobalVars.gamelog.append("    " + "Color: Red ----- Power: None")
    elif combatant_1.Status in ['paralyzed', 'burned']:
        if combatant_1_miss_check:
            GlobalVars.gamelog.append(
                f"Player {GlobalVars.turn_player}'s " \
                f"{combatant_1.Name} ({combatant_1.OrigLoc.Label[-1]}) " \
                "spun Miss")
            GlobalVars.gamelog.append("    " + "Color: Red ----- Power: None")
        else:
            GlobalVars.gamelog.append(
                f"Player {GlobalVars.turn_player}'s {combatant_1.Name} " \
                f"({combatant_1.OrigLoc.Label[-1]}) spun " \
                f"{combatant_1_attack.Name}")
            GlobalVars.gamelog.append(
                "    " \
                f"Color: {combatant_1_attack.Color} ----- Power: " \
                f"{GlobalVars.combatant_1_power}")
    else:
        GlobalVars.gamelog.append(
            f"Player {GlobalVars.turn_player}'s {combatant_1.Name} " \
            f"({combatant_1.OrigLoc.Label[-1]}) spun " \
            f"{combatant_1_attack.Name}")
        GlobalVars.gamelog.append(
            "    " \
            f"Color: {combatant_1_attack.Color} ----- Power: "\
            f"{GlobalVars.combatant_1_power}")

    if combatant_2.Status == 'frozen':
        GlobalVars.gamelog.append(
            f"Player {combatant_2.Ctrl}'s {combatant_2.Name} " \
            f"({combatant_2.OrigLoc.Label[-1]}) spun Miss")
        GlobalVars.gamelog.append("    " + "Color: Red ----- Power: None")
    elif combatant_2.Status in ['paralyzed', 'burned']:
        if combatant_2_miss_check:
            GlobalVars.gamelog.append(
                f"Player {combatant_2.Ctrl}'s {combatant_2.Name} " \
                f"({combatant_2.OrigLoc.Label[-1]}) spun Miss")
            GlobalVars.gamelog.append("    " + "Color: Red ----- " \
                                      "Power: None")
        else:
            GlobalVars.gamelog.append(
                f"Player {combatant_2.Ctrl}'s {combatant_2.Name} " \
                f"({combatant_2.OrigLoc.Label[-1]}) spun " \
                f"{combatant_2_attack.Name}")
            GlobalVars.gamelog.append(
                "    " +
                f"Color: {combatant_2_attack.Color} ----- Power: " \
                f"{GlobalVars.combatant_2_power}")
    else:
        GlobalVars.gamelog.append(
            f"Player {combatant_2.Ctrl}'s {combatant_2.Name} " \
            f"({combatant_2.OrigLoc.Label[-1]}) spun " \
            f"{combatant_2_attack.Name}")
        GlobalVars.gamelog.append(
            "    " +
            f"Color: {combatant_2_attack.Color} ----- Power: "\
            f"{GlobalVars.combatant_2_power}")

    if combatant_1_color == "White":
        if combatant_2_color in ['White', 'Gold']:
            if GlobalVars.combatant_1_power > GlobalVars.combatant_2_power:
                GlobalVars.gamelog.append(
                    f"Player {GlobalVars.turn_player}s {combatant_1.Name} " \
                    f"({combatant_1.OrigLoc.Label[-1]}) wins!")
                return 1
            elif GlobalVars.combatant_1_power < GlobalVars.combatant_2_power:
                GlobalVars.gamelog.append(
                    f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                    f"({combatant_2.OrigLoc.Label[-1]}) wins!")
                return 2
            elif GlobalVars.combatant_1_power == GlobalVars.combatant_2_power:
                GlobalVars.gamelog.append("Tie!")
                return 0
        elif combatant_2_color == "Purple":
            GlobalVars.gamelog.append(
                f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                f"({combatant_2.OrigLoc.Label[-1]}) wins!")
            return 6
        elif combatant_2_color == "Red":
            GlobalVars.gamelog.append(
                f"Player {GlobalVars.turn_player}s {combatant_1.Name} " \
                f"({combatant_1.OrigLoc.Label[-1]}) wins!")
            return 1
        elif combatant_2_color == "Blue":
            GlobalVars.gamelog.append(
                f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                f"({combatant_2.OrigLoc.Label[-1]}) wins!")
            return 6

    elif combatant_1_color == "Gold":
        if combatant_2_color == "White" or combatant_2_color == "Gold":
            if GlobalVars.combatant_1_power > GlobalVars.combatant_2_power:
                GlobalVars.gamelog.append(
                    f"Player {GlobalVars.turn_player}s {combatant_1.Name} " \
                    f"({combatant_1.OrigLoc.Label[-1]}) wins!")
                return 1
            elif GlobalVars.combatant_1_power < GlobalVars.combatant_2_power:
                GlobalVars.gamelog.append(
                    f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                    f"({combatant_2.OrigLoc.Label[-1]}) wins!")
                return 2
            elif GlobalVars.combatant_1_power == GlobalVars.combatant_2_power:
                GlobalVars.gamelog.append("Tie!")
                return 0
        elif combatant_2_color == "Purple":
            GlobalVars.gamelog.append(
                f"Player {GlobalVars.turn_player}s {combatant_1.Name} " \
                f"({combatant_1.OrigLoc.Label[-1]}) wins!")
            return 3
        elif combatant_2_color == "Red":
            GlobalVars.gamelog.append(
                f"Player {GlobalVars.turn_player}s {combatant_1.Name} " \
                f"({combatant_1.OrigLoc.Label[-1]}) wins!")
            return 1
        elif combatant_2_color == "Blue":
            GlobalVars.gamelog.append(
                f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                f"({combatant_2.OrigLoc.Label[-1]}) wins!")
            return 6

    elif combatant_1_color == "Purple":
        if combatant_2_color == "Purple":
            if GlobalVars.combatant_1_power > GlobalVars.combatant_2_power:
                GlobalVars.gamelog.append(
                    f"Player {GlobalVars.turn_player}s {combatant_1.Name} " \
                    "({combatant_1.OrigLoc.Label[-1]}) wins!")
                return 5
            elif GlobalVars.combatant_1_power < GlobalVars.combatant_2_power:
                GlobalVars.gamelog.append(
                    f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                    f"({combatant_2.OrigLoc.Label[-1]}) wins!")
                return 6
            elif GlobalVars.combatant_1_power == GlobalVars.combatant_2_power:
                GlobalVars.gamelog.append("Tie!")
                return 7
        elif combatant_2_color == "White":
            GlobalVars.gamelog.append(
                f"Player {GlobalVars.turn_player}s {combatant_1.Name} " \
                f"({combatant_1.OrigLoc.Label[-1]}) wins!")
            return 5
        elif combatant_2_color == "Gold":
            GlobalVars.gamelog.append(
                f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                f"({combatant_2.OrigLoc.Label[-1]}) wins!")
            return 4
        elif combatant_2_color == "Red":
            GlobalVars.gamelog.append(
                f"Player {GlobalVars.turn_player}s {combatant_1.Name} " \
                f"({combatant_1.OrigLoc.Label[-1]}) wins!")
            return 5
        elif combatant_2_color == "Blue":
            GlobalVars.gamelog.append(
                f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                f"({combatant_2.OrigLoc.Label[-1]}) wins!")
            return 6

    elif combatant_1_color == "Blue":
        if combatant_2_color != "Blue":
            GlobalVars.gamelog.append(
                f"Player {GlobalVars.turn_player}s {combatant_1.Name} " \
                f"({combatant_1.OrigLoc.Label[-1]}) wins!")
            return 5
        else:
            GlobalVars.gamelog.append("Tie!")
            return 7

    elif combatant_1_color == "Red":
        if combatant_2_color in ['White', 'Gold']:
            GlobalVars.gamelog.append(
                f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                f"({combatant_2.OrigLoc.Label[-1]}) wins!")
            return 2
        elif combatant_2_color in ['Purple', 'Blue']:
            GlobalVars.gamelog.append(
                f"Player {combatant_2.Ctrl}s {combatant_2.Name} " \
                f"({combatant_2.OrigLoc.Label[-1]}) wins!")
            return 6
        elif combatant_2_color == "Red":
            GlobalVars.gamelog.append("Tie!")
            return 0

def evolve_target(target):
    target_evo = GlobalVars.evo_complete
    new_stage = target.Stage + 1
    new_loc = target.Loc
    old_sprite = target.Sprite
    current_spritelist = target.Sprite.sprite_lists[0]
    
    target.__dict__ = Pokemon(GlobalVars.evo_complete, target.Ctrl).__dict__
    
    target.Stage = new_stage
    target.Loc = new_loc
    target.OrigLoc = target.Loc
    new_sprite = arcade.Sprite(os.path.join(
                                        GlobalConst.FILE_PATH,
                                        "images",
                                        "sprites",
                                        target.Spritefile),
                                    GlobalConst.SPRITE_SCALING)
    current_spritelist.append(new_sprite)
    old_sprite.kill()
    target.Sprite = new_sprite
    target.Sprite.set_position(*target.Loc.Coords)
    
    for new_attacks in target.Attacks:
        if new_attacks.Power != None:
            if new_attacks.Color == 'White' or new_attacks.Color == 'Gold':
                new_attacks.Power += 10*target.Stage
            elif new_attacks.Color == 'Purple':
                new_attacks.Power += 1*target.Stage
            new_attacks.OrigPower = new_attacks.Power
        else:
            new_attacks.OrigPower = None
    GlobalVars.evo_complete = False

def evolution_check(target):

    def evolution_popup(target, evo_list):

        root = tk.Tk()
        root.title(f"Select Evolution for {target.Name}")

        def close_window():
            root.destroy()

        def evolution_submit(selection):
            GlobalVars.evo_complete = selection
            root.destroy()

        evo_cb = ttk.Combobox(root, values=evo_list)
        evo_cb.pack()
        evo_cb.set(evo_list[0])

        confirm_button = ttk.Button(
            root,
            text="Select",
            command=lambda: evolution_submit(evo_cb.get()))
        confirm_button.pack()

        done_button = ttk.Button(root, text="Cancel", command=close_window)
        done_button.pack()

        root.mainloop()

    evo_list = []
    if target.Evolutions:
        for evos in target.Evolutions:
            if ", Mega" in evos:
                continue
            else:
                evo_list.append(evos)
        if len(evo_list) > 0:
            evolution_popup(target, evo_list)
            if GlobalVars.evo_complete:
                GlobalVars.gamelog.append(f"{target.Name} evolving " \
                                          f"to {GlobalVars.evo_complete}")
                return True
            else:
                return False
        else:
            return False
    else:
        return False
                
def winner_resolve(winner, loser):
    GlobalVars.gamelog.append(f"Player {loser.Ctrl}s {loser.Name} " \
                              "was sent to the PC.")
    space_cleanup(loser.Loc)
    pc_rotate(loser)
    evolve_check = evolution_check(winner)
    if evolve_check:
        evolve_target(winner)
        
class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        self.background = None
        self.ClassicBoard = None
        self.TvTBoard = None

        # Create initial state of sprites for both teams
        for teams in PlayerTeams:
            for pkmns in teams:
                current_Ctrl = pkmns.Ctrl
                bench_spot = pkmns.OrigLoc.Label[-1]

        self.pkmn_list = None

    def on_show(self):
        # Create your sprites and sprite lists here
        self.pkmn_list = arcade.SpriteList()

        for teams in PlayerTeams:
            for pkmns in teams:
                bench_spot = pkmns.OrigLoc.Label[-1]
                sprite_path = os.path.join(
                                GlobalConst.FILE_PATH,
                                "images",
                                "sprites",
                                pkmns.Spritefile)
                setattr(self,
                        f"player_{pkmns.Ctrl}_pkmn_{bench_spot}",
                        arcade.Sprite(sprite_path, GlobalConst.SPRITE_SCALING))
                new_sprite = getattr(self,
                                     f"player_{pkmns.Ctrl}_pkmn_{bench_spot}")
                new_sprite.set_position(*pkmns.Loc.Coords)
                pkmns.Sprite = new_sprite
                self.pkmn_list.append(pkmns.Sprite)

        self.background = arcade.load_texture(GlobalVars.background_select)
        if GlobalVars.game_mode == "Classic":
            self.ClassicBoard = arcade.load_texture(
                os.path.join(
                    "images",
                    "board",
                    "overlays",
                    "classic_duel_overlay.png"))
        elif GlobalVars.game_mode == "3v3":
            self.TvTBoard = arcade.load_texture(
                os.path.join(
                    "images",
                    "board",
                    "overlays",
                    "3v3_duel_overlay.png"))

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen befor  we start drawing. It will clear
        # the screen to the background color, and erase what we drew last
        # frame.

        text_offset_x = floor(-20*GlobalConst.ASPECT_RATIO)
        text_offset_y = floor(35*GlobalConst.ASPECT_RATIO)
        circle_offset_x = floor(-25*GlobalConst.ASPECT_RATIO)
        circle_offset_y = floor(27*GlobalConst.ASPECT_RATIO)

        arcade.start_render()
        arcade.draw_texture_rectangle(
            GlobalConst.SCREEN_HEIGHT // 2,
            GlobalConst.SCREEN_HEIGHT // 2,
            GlobalConst.SCREEN_HEIGHT,
            GlobalConst.SCREEN_HEIGHT,
            self.background)
        if GlobalVars.game_mode == "Classic":
            arcade.draw_texture_rectangle(
                GlobalConst.SCREEN_HEIGHT // 2,
                GlobalConst.SCREEN_HEIGHT // 2,
                GlobalConst.SCREEN_HEIGHT,
                GlobalConst.SCREEN_HEIGHT,
                self.ClassicBoard)
            center_text_x = floor(500*GlobalConst.ASPECT_RATIO)

        elif GlobalVars.game_mode == "3v3":
            arcade.draw_texture_rectangle(
                GlobalConst.SCREEN_HEIGHT // 2,
                GlobalConst.SCREEN_HEIGHT // 2,
                GlobalConst.SCREEN_HEIGHT,
                GlobalConst.SCREEN_HEIGHT,
                self.TvTBoard)
            center_text_x = floor(550*GlobalConst.ASPECT_RATIO)

        # draw unit bases
        for teams, sprites in zip(PlayerTeams, self.pkmn_list):
            for pkmns in teams:
                if pkmns.Ctrl == 1:
                    cir_color = arcade.color.AZURE
                elif pkmns.Ctrl == 2:
                    cir_color = arcade.color.RASPBERRY
                cir_color = [_ for _ in cir_color]
                stage_cir_color = cir_color
                sprites.center = pkmns.Loc.Coords
                arcade.draw_circle_filled(
                    *pkmns.Loc.Coords,
                    floor(35*GlobalConst.ASPECT_RATIO),
                    cir_color)
                if pkmns.Stage > 0:
                    for stages in range(pkmns.Stage):
                        arcade.draw_circle_outline(
                            *pkmns.Loc.Coords,
                            floor((35+7*(stages+1))*GlobalConst.ASPECT_RATIO),
                            stage_cir_color, 3)
                for colors in GlobalConst.STATUS_COLORS.keys():
                    if pkmns.Status == colors:
                        arcade.draw_circle_filled(
                            *pkmns.Loc.Coords,
                            floor(30*GlobalConst.ASPECT_RATIO),
                            GlobalConst.STATUS_COLORS[colors])

        self.pkmn_list.draw()
        
        for teams in PlayerTeams:
            for pkmns in teams:
                # Wait circle and text draw
                arcade.draw_circle_filled(
                    pkmns.Loc.Coords[0] - circle_offset_x,
                    pkmns.Loc.Coords[1] - circle_offset_y,
                    12*GlobalConst.ASPECT_RATIO,
                    arcade.color.BLUE_SAPPHIRE)
                arcade.draw_text(
                    str(pkmns.Move - GlobalVars.first_turn),
                    pkmns.Loc.Coords[0] - text_offset_x,
                    pkmns.Loc.Coords[1] - text_offset_y,
                    arcade.color.WHITE,
                    floor(16*GlobalConst.ASPECT_RATIO))
                if pkmns.Wait > 0:
                    arcade.draw_circle_filled(
                        pkmns.Loc.Coords[0] + circle_offset_x,
                        pkmns.Loc.Coords[1] - circle_offset_y,
                        floor(12*GlobalConst.ASPECT_RATIO),
                        arcade.color.PURPLE)
                    arcade.draw_text(
                        str(pkmns.Wait),
                        pkmns.Loc.Coords[0] + text_offset_x - floor(10*GlobalConst.ASPECT_RATIO),
                        pkmns.Loc.Coords[1] - text_offset_y,
                        arcade.color.WHITE,
                        floor(16*GlobalConst.ASPECT_RATIO))

        line_counter = 0
        for lines in GlobalVars.gamelog[::-1]:
            lines_text = [lines[i:i + floor(85*GlobalConst.ASPECT_RATIO)] \
                          for i in range(
                              0,
                              len(lines),
                              floor(85*GlobalConst.ASPECT_RATIO))]
            for split_lines in lines_text[::-1]:
                arcade.draw_text(
                    split_lines,
                    GlobalConst.SCREEN_HEIGHT + 20*GlobalConst.ASPECT_RATIO,
                    floor(24*GlobalConst.ASPECT_RATIO + line_counter* \
                          floor(24*GlobalConst.ASPECT_RATIO)),
                    arcade.color.WHITE,
                    floor(18*GlobalConst.ASPECT_RATIO),
                    font_name="Arial")
                line_counter += 1
                if line_counter == floor(60*GlobalConst.ASPECT_RATIO):
                    break
            if line_counter == floor(60*GlobalConst.ASPECT_RATIO):
                break

        if GlobalVars.player_1_win:
            center_text = "Player 1 Wins!"
        elif GlobalVars.player_2_win:
            center_text = "Player 2 Wins!"
        else:
            center_text = f"Player {GlobalVars.turn_player} turn."

        arcade.draw_text(
            center_text,
            GlobalConst.SCREEN_HEIGHT // 2,
            GlobalConst.SCREEN_HEIGHT // 2 if GlobalVars.game_mode == "Classic" \
            else GlobalConst.SCREEN_HEIGHT // 2 + \
                 floor(50*GlobalConst.ASPECT_RATIO),
            arcade.color.YELLOW,
            floor(18*GlobalConst.ASPECT_RATIO),
            anchor_x="center",
            anchor_y="center",
            align="center",
            font_name="Arial")
        if GlobalVars.move_click:
            arcade.draw_text(
                "Click this unit again\nto attack without moving,\nif able.",
                floor(500*GlobalConst.ASPECT_RATIO),
                floor(500*GlobalConst.ASPECT_RATIO - 45 * \
                      GlobalConst.ASPECT_RATIO),
                arcade.color.YELLOW,
                floor(12*GlobalConst.ASPECT_RATIO),
                anchor_x="center",
                anchor_y="center",
                align='center',
                font_name="Arial")

        if len(GlobalVars.checked_moves) > 0:
            for moves in GlobalVars.checked_moves:
                arcade.draw_circle_filled(
                    *moves.Coords,
                    floor(35*GlobalConst.ASPECT_RATIO),
                    (59, 122, 87, 200))
        if len(GlobalVars.potential_targets) > 0:
            for targets in GlobalVars.potential_targets:
                arcade.draw_circle_filled(
                    *targets.Coords,
                    floor(35*GlobalConst.ASPECT_RATIO),
                    (255, 240, 0, 150))
        if len(GlobalVars.tag_targets) > 0:
            for targets in GlobalVars.tag_targets:
                arcade.draw_circle_filled(
                    *targets.Coords,
                    floor(35*GlobalConst.ASPECT_RATIO),
                    (255, 24, 180, 125))
        """
        # ON HOVER STATS VIEW, NEED LOTS OF WORK
        arcade.draw_rectangle_filled(
            1200,715,360,550,arcade.color.AIR_FORCE_BLUE)
        stats_counter = 0

        if GlobalVars.hover_pkmn:
            hover_dict = GlobalVars.hover_pkmn.__dict__
            for keys, stats in hover_dict.items():
                if keys != 'Loc' and keys != 'OrigLoc':
                    if keys != 'Attacks':
                        stats_text = [
                            str(stats)[i:i + 45] for i in range(
                                0, len(str(stats)), 45)]
                        for lines in stats_text[::-1]:
                            arcade.draw_text(
                                lines,
                                1030,
                                400 + stats_counter * 10,
                                arcade.color.BLACK,
                                10)
                            stats_counter += 1
                    elif keys == 'Attacks':
                        for new_atks in hover_dict['Attacks']:
                            new_atk_dict = new_atks.__dict__
                            for atk_keys, atk_stats in new_atk_dict.items():
                                atk_stats = str(atk_stats)
                                if atk_stats != None:
                                    atk_stats_text = [
                                        atk_stats[i:i + 45] for i in range(
                                            0, len(str(atk_stats)), 45)]
                                    for lines in atk_stats_text[::-1]:
                                        atk_str = str(
                                                atk_keys + ":  " + str(lines))
                                        arcade.draw_text(
                                            atk_str,
                                            1030,
                                            400 + stats_counter * 10,
                                            arcade.color.BLACK,
                                            10)
                                        stats_counter += 1
            """
                    
    def on_close(self):
        restart = True

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            if not GlobalVars.move_click and not GlobalVars.attack_click:
                if GlobalVars.turn_player == 1:
                    current_team = PlayerTeams.Player1
                elif GlobalVars.turn_player == 2:
                    current_team = PlayerTeams.Player2
                for pkmns in current_team:
                    if pkmns.Wait > 0:
                        continue
                    elif pkmns.Status in ['sleep', 'frozen']:
                        continue
                    else:
                        if x in range(pkmns.Loc.Coords[0] - floor(
                            35*GlobalConst.ASPECT_RATIO),
                                      pkmns.Loc.Coords[0] + floor(
                                          35*GlobalConst.ASPECT_RATIO)
                                      ) and y in range(
                                          pkmns.Loc.Coords[1] - floor(
                                              35*GlobalConst.ASPECT_RATIO),
                                          pkmns.Loc.Coords[1] + floor(
                                              35*GlobalConst.ASPECT_RATIO)):
                            GlobalVars.move_click = True
                            GlobalVars.in_transit = pkmns
                            path_check(pkmns)
                            occupancy_counter = len(pkmns.Loc.Neighbors)
                            for locs in pkmns.Loc.Neighbors:
                                if locs.Occupied:
                                    occupancy_counter -= 1
                            if occupancy_counter == 0:
                                target_finder(pkmns)
                                if len(GlobalVars.potential_targets) > 0 or \
                                   len(GlobalVars.tag_targets) > 0:
                                    GlobalVars.move_click = False
                                    GlobalVars.attack_click = True

            elif GlobalVars.move_click:
                for moves in GlobalVars.checked_moves:
                    if x in range(moves.Coords[0] - floor(
                        35*GlobalConst.ASPECT_RATIO),
                                  moves.Coords[0] + floor(
                                      35*GlobalConst.ASPECT_RATIO)
                                  ) and y in range(
                                      moves.Coords[1] - floor(
                                          35*GlobalConst.ASPECT_RATIO),
                                      moves.Coords[1] + floor(
                                          35*GlobalConst.ASPECT_RATIO)
                                      ) and moves.Occupied == False:
                        GlobalVars.unit_moved = True
                        GlobalVars.gamelog.append(
                            f"Player {GlobalVars.turn_player}'s " +
                            GlobalVars.in_transit.Name +
                            " (" +
                            GlobalVars.in_transit.OrigLoc.Label[-1] +
                            ") " +
                            f"moved to {moves}.")
                        space_cleanup(GlobalVars.in_transit.Loc)
                        move_to_space(GlobalVars.in_transit, moves)
                        for surround_neighbors in board:
                            if len(surround_neighbors.Label) == 2:
                                surround_target = surround_neighbors.Occupant
                                if surround_target:
                                    surround_target.IsSurrounded = \
                                        surround_check(surround_target)
                        for teams in PlayerTeams:
                            for pkmns in teams:
                                if pkmns.IsSurrounded:
                                    GlobalVars.gamelog.append(
                                        str(f"SURROUNDED:    Player " \
                                            f"{pkmns.Ctrl}'s {pkmns.Name} " \
                                            f"({pkmns.OrigLoc.Label[-1]}) " \
                                            f"was sent to Player " \
                                            f"{pkmns.Ctrl}'s PC."))
                                    space_cleanup(pkmns.Loc)
                                    pc_rotate(pkmns)
                                    pkmns.IsSurrounded = False
                        target_finder(GlobalVars.in_transit)
                        if len(GlobalVars.potential_targets) > 0 or \
                           len(GlobalVars.tag_targets) > 0:
                            GlobalVars.attack_click = True
                        else:
                            GlobalVars.turn_change = True
                    elif type(GlobalVars.in_transit) != str:
                        if len(
                            GlobalVars.in_transit.Loc.Label
                            ) == 2 and x in range(
                                GlobalVars.in_transit.Loc.Coords[0] - floor(
                                    35*GlobalConst.ASPECT_RATIO),
                                GlobalVars.in_transit.Loc.Coords[0] + floor(
                                    35*GlobalConst.ASPECT_RATIO)
                                ) and y in range(
                                    GlobalVars.in_transit.Loc.Coords[1] - \
                                    floor(35*GlobalConst.ASPECT_RATIO),
                                    GlobalVars.in_transit.Loc.Coords[1] + \
                                    floor(35*GlobalConst.ASPECT_RATIO)):
                            target_finder(GlobalVars.in_transit)
                            if len(GlobalVars.potential_targets) > 0 or \
                               len(GlobalVars.tag_targets) > 0:
                                GlobalVars.attack_click = True
                            else:
                                GlobalVars.in_transit = ''
                                GlobalVars.move_click = False
                                GlobalVars.potential_targets = []
                                GlobalVars.tag_targets = []

                GlobalVars.move_click = False
                GlobalVars.checked_moves = []

                self.pkmn_list.update()

            elif GlobalVars.attack_click:
                for targets in GlobalVars.potential_targets:
                    if x in range(targets.Coords[0] - floor(
                        35*GlobalConst.ASPECT_RATIO),
                                  targets.Coords[0] + floor(
                                      35*GlobalConst.ASPECT_RATIO)
                                  ) and y in range(
                                      targets.Coords[1] - floor(
                                          35*GlobalConst.ASPECT_RATIO),
                                      targets.Coords[1] + floor(
                                          35*GlobalConst.ASPECT_RATIO)):
                        GlobalVars.unit_attacked = True
                        winner_check = battle_spin_compare(
                            GlobalVars.in_transit,
                            targets.Occupant)

                        if targets.Occupant.Status in ['frozen', 'sleep']:
                            apply_status(targets.Occupant)
                        if GlobalVars.in_transit.Status in ['frozen', 'sleep']:
                            apply_status(GlobalVars.in_transit)
                        # Add effects checks
                        if winner_check == 0:
                            pass
                        elif winner_check == 1:
                            winner_resolve(
                                GlobalVars.in_transit,
                                targets.Occupant)
                            self.pkmn_list.update()
                        elif winner_check == 2:
                            winner_resolve(
                                targets.Occupant,
                                GlobalVars.in_transit)
                        elif winner_check == 3:
                            pass
                        elif winner_check == 4:
                            pass
                        elif winner_check == 5:
                            effect_user = GlobalVars.in_transit
                            target_opponent = targets.Occupant
                            if len(
                                GlobalVars.attacker_current_spin.Funcs) > 0:
                               for effects in \
                                   GlobalVars.attacker_current_spin.Funcs:
                                    exec(effects)
                        elif winner_check == 6:
                            effect_user = targets.Occupant
                            target_opponent = GlobalVars.in_transit
                            if len(
                                GlobalVars.defender_current_spin.Funcs) > 0:
                               for effects in \
                                   GlobalVars.defender_current_spin.Funcs:
                                    exec(effects)
                        elif winner_check == 7:
                            pass
                for targets in GlobalVars.tag_targets:
                    if x in range(targets.Coords[0] - floor(
                        35*GlobalConst.ASPECT_RATIO),
                                  targets.Coords[0] + floor(
                                      35*GlobalConst.ASPECT_RATIO)
                                  ) and y in range(
                                      targets.Coords[1] - floor(
                                          35*GlobalConst.ASPECT_RATIO),
                                      targets.Coords[1] + floor(
                                          35*GlobalConst.ASPECT_RATIO)):
                        if targets.Occupant.Status in ['frozen', 'sleep']:
                            apply_status(targets.Occupant)
                            apply_marker(targets.Occupant)
                            GlobalVars.gamelog.append(
                                f"Player {GlobalVars.turn_player} tagged " \
                                f"their {targets.Occupant.Name} " \
                                f"({targets.Occupant.OrigLoc.Label[-1]}). " \
                                "Status and markers cleared.")
                        #add statement for different markers
                        GlobalVars.unit_attacked = True

                if GlobalVars.unit_moved or GlobalVars.unit_attacked:
                    GlobalVars.turn_change = True
                GlobalVars.attack_click = False
                GlobalVars.in_transit = ''
                GlobalVars.in_transit_loc = ''
                GlobalVars.potential_targets = []
                GlobalVars.unit_moved = False
                GlobalVars.unit_attacked = False
                GlobalVars.tag_targets = []

                self.pkmn_list.update()

            if GlobalVars.player_1_win or GlobalVars.player_2_win:
                arcade.close_window()

            if board.A4.Ctrl == 2:
                GlobalVars.player_2_win = True
                GlobalVars.gamelog.append(
                    "Player 2 wins! Click anywhere to exit.")
                write_log()
                self.pkmn_list.update()

            elif board.E4.Ctrl == 1:
                GlobalVars.player_1_win = True
                GlobalVars.gamelog.append(
                    "Player 1 wins! Click anywhere to exit.")
                write_log()
                self.pkmn_list.update()
        
        for teams in PlayerTeams:
            for pkmns in teams:
                if len(pkmns.Loc.Label) == 2:
                    pkmns.IsSurrounded = surround_check(pkmns)
                    if pkmns.IsSurrounded:
                        GlobalVars.gamelog.append(
                                            str(f"SURROUNDED:    Player " \
                                                f"{pkmns.Ctrl}'s {pkmns.Name} " \
                                                f"({pkmns.OrigLoc.Label[-1]}) " \
                                                f"was sent to Player " \
                                                f"{pkmns.Ctrl}'s PC."))
                        space_cleanup(pkmns.Loc)
                        pc_rotate(pkmns)
                        pkmns.IsSurrounded = False
        if GlobalVars.turn_change == True:
            turn_rotate()
    
    #1020, 430, 1380, 990
    def on_mouse_motion(self, x, y, dx, dy):
        """
        for teams in PlayerTeams:
            for pkmns in teams:
                coords_x = pkmns.Loc.Coords[0]
                coords_y = pkmns.Loc.Coords[1]
                if x in range(
                    coords_x - 40,
                    coords_x + 40
                    ) and y in range(
                        coords_y - 40,
                        coords_y + 40):
                    GlobalVars.hover_pkmn = pkmns
        """
"""
    def on_resize(self, width, height):
    #add this when circle, sprite and movement scaling is added
        print(width, height)
        GlobalConst.SCREEN_HEIGHT = height
        GlobalConst.SCREEN_WIDTH = width
"""                     


def on_select_team(player_num, event=None):

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

        GlobalVars.background_select = os.path.join(
            GlobalConst.BG_PATH,
            bg_cb.get() + ".png")
        GlobalConst.SCREEN_WIDTH, GlobalConst.SCREEN_HEIGHT = \
                                  resolution_list[res_cb.get()]
        GlobalConst.ASPECT_RATIO = GlobalConst.SCREEN_HEIGHT / 1000
        GlobalConst.SPRITE_SCALING = 2.5*(GlobalConst.ASPECT_RATIO)
        root.destroy()

    root = tk.Tk()
    root.title("PoDuReDux: Game Mode Select")

    var = tk.StringVar()
    var.set('1')

    try:
        def fn(x): return x.split('/')[-1][:-4]
        background_textures = {
            fn(k): k for k in iglob(
                GlobalConst.BG_PATH +
                "/**/*.png",
                recursive=True)}

    except BaseException:
        pass

    resolution_list = {"640x360":(640, 360),
                       "720x400":(720, 400),
                       "800x600":(800, 600),
                       "960x540":(960, 540),
                       "1280x720":(1280, 720),
                       "1600x900":(1600, 900),
                       "1920x1080":(1920, 1080),
                       "2560x1080":(2560, 1440),
                       "3200x1800":(3200, 1800),
                       "3840x1600":(3840, 1600),
                       "4096x2160":(4096, 2160),
                       "5120x2880":(5120, 2880),
                       "7680x4320":(7680, 4320)}
    
    background_list = []
    res_keys = [_ for _ in resolution_list.keys()]

    for items in background_textures.values():
        background_list.append(items[len(GlobalConst.BG_PATH) + 1:-4])

    bg_Label = ttk.Label(root, text="Choose Background image from drop-down:")
    bg_Label.pack()

    bg_cb = ttk.Combobox(root, values=background_list)
    bg_cb.set(background_list[0])
    bg_cb.pack()

    mode_select_Label = ttk.Label(root, text="Choose Game Mode:")
    mode_select_Label.pack()

    mode_select_classic_radio = ttk.Radiobutton(
        root, text="Classic", variable=var, value="Classic")
    mode_select_classic_radio.pack()
    mode_select_classic_radio.invoke()

    mode_select_3v3_radio = ttk.Radiobutton(
        root, text="3v3", variable=var, value="3v3")
    mode_select_3v3_radio.pack()

    mode_select_Label = ttk.Label(root, text="Select Resolution:")
    mode_select_Label.pack()

    res_cb = ttk.Combobox(root, values=res_keys)
    res_cb.set(res_keys[4])
    res_cb.pack()

    mode_select_confirm = ttk.Button(
        root, text="Confirm", command=button_click)
    mode_select_confirm.pack()

    root.mainloop()


def startup_window():

    def button_click():

        GlobalVars.player_1_select = p1team_cb.get()
        GlobalVars.player_2_select = p2team_cb.get()
        root.destroy()

    root = tk.Tk()
    root.title(f"PoDuReDux: Team Select ({GlobalVars.game_mode})")

    p1team_Label = ttk.Label(root, text="Player 1 Team:")
    p1team_Label.grid(row=0, column=0, padx=30, pady=(30, 10))

    p2team_Label = ttk.Label(root, text="Player 2 Team:")
    p2team_Label.grid(row=0, column=2, padx=30, pady=(30, 10))

    p1team_cb = ttk.Combobox(root, values=team_list)
    p1team_cb.set(team_list[0])
    p1team_cb.grid(row=1, column=0, padx=30, pady=10)
    p1team_cb.bind('<<ComboboxSelected>>', on_select_team(1))

    p2team_cb = ttk.Combobox(root, values=team_list)
    p2team_cb.set(team_list[0])
    p2team_cb.grid(row=1, column=2, padx=30, pady=10)
    p2team_cb.bind('<<ComboboxSelected>>', on_select_team(2))

    gamestart_button = ttk.Button(
        root, text="Start Game", command=button_click)
    gamestart_button.grid(row=3, column=1, padx=30, pady=(10, 30))

    root.mainloop()


def main():
    
    window = arcade.Window(
        GlobalConst.SCREEN_WIDTH,
        GlobalConst.SCREEN_HEIGHT,
        "Game Start",
        False,
        True)
    game = GameView()
    window.show_view(game)
    arcade.run()
    call(["pythonw", "PoDuReDux.pyw"])

if __name__ == "__main__":
    GlobalConst = GlobalConst()
    GlobalVars = GlobalVars()
    mode_select()
    team_list = []
    if GlobalVars.game_mode == "Classic":
        for x in os.listdir(
            os.path.join(
                os.path.abspath(
                    os.path.expanduser(
                GlobalConst.FILE_PATH)),
                "saves",
                "classic_teams")):
            team_list.append(x)
    elif GlobalVars.game_mode == "3v3":
        for x in os.listdir(
            os.path.join(
                os.path.abspath(
                    os.path.expanduser(
                GlobalConst.FILE_PATH)),
                "saves",
                "3v3_teams")):
            team_list.append(x)

    startup_window()

    PlayerTeams = AllTeams()

    PlayerTeams.Player1 = PlayerTeam(1)
    PlayerTeams.Player2 = PlayerTeam(2)
                
    if GlobalVars.game_mode == "Classic":
        board = ClassicBoardGenerator()
    elif GlobalVars.game_mode == "3v3":
        board = TvTBoardGenerator()
    for teams in PlayerTeams:
        x = 1
        for pkmns in teams:
            pkmns.Loc = getattr(board, f"Player{pkmns.Ctrl}Bench{x}")
            pkmns.OrigLoc = pkmns.Loc
            x += 1
    main()
