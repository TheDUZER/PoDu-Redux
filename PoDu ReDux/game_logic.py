##  -*- coding: utf-8 -*-

"""
TO DO:

-Implement team file selection for GUI; limit iteration over team files to first 6 lines
-Set up team selection for two separate teams
-MAKE PATH BUILDER RECURSIVE
-Refine knockback function and checks for straight lines (Mewtwo, Rhyperior, etc)
-Add attribute to player team objects for tracking evolution stages and previous evolutions
for reversion and evolution modifier effects
"""

import json, sys, os, random

class BoardNeighbors():
    """Create generic board spaces and assign list of neighbor spaces"""
    def __init__(self, neighbors):
        self.neighbors = neighbors
        self.coords = {}
        self.force_stop = False
        self.force_attack = False
        self.occupied = False
        self.occupant = ''
        self.occupant_team = 0
        self.passable = True
        self.controlling_player = 0
        self.player_1_entry = False
        self.player_1_goal = False
        self.player_2_entry = False
        self.player_2_goal = False
        
class ClassicBoardGenerator():
    """Create board object with space labels and adjusted bools for special spaces"""
    def __init__(self):
        ## Populate neutral spaces of board
        self.A1 = BoardNeighbors({"B1":1, "B2":2, "A2":3})
        self.A1.player_1_entry = True
        self.A2 = BoardNeighbors({"A1":7, "A3":3})
        self.A3 = BoardNeighbors({"A2":7, "A4":3})
        self.A4 = BoardNeighbors({"A3":7, "A5":3})
        self.A4.player_1_goal = True
        self.A5 = BoardNeighbors({"A4":7, "A6":3, "B4":1})
        self.A6 = BoardNeighbors({"A5":7, "A7":3})
        self.A7 = BoardNeighbors({"A6":7, "B6":8, "B7":1})
        self.A7.player_1_entry = True
        self.B1 = BoardNeighbors({"A1":5, "C1":1})
        self.B2 = BoardNeighbors({"A1":6, "B4":3, "C2":1})
        self.B4 = BoardNeighbors({"B2":7, "A5":5, "B6":3})
        self.B6 = BoardNeighbors({"B4":7, "A7":5, "C6":1})
        self.B7 = BoardNeighbors({"A7":5, "C7":1})
        self.C1 = BoardNeighbors({"B1":5, "D1":1})
        self.C2 = BoardNeighbors({"B2":5, "D2":1})
        self.C6 = BoardNeighbors({"B6":5, "D6":1})
        self.C7 = BoardNeighbors({"B7":5, "D7":1})
        self.D1 = BoardNeighbors({"E1":1, "C1":5})
        self.D2 = BoardNeighbors({"E1":8, "D4":3, "C2":5})
        self.D4 = BoardNeighbors({"D2":7, "E3":1, "D6":3})
        self.D6 = BoardNeighbors({"D4":7, "E7":2, "C6":5})
        self.D7 = BoardNeighbors({"C7":5, "E7":1})
        self.E1 = BoardNeighbors({"D1":5, "E2":3, "D2":4})
        self.E1.player_2_entry = True
        self.E2 = BoardNeighbors({"E1":7, "E3":3})
        self.E3 = BoardNeighbors({"E2":7, "E4":3, "D4":5})
        self.E4 = BoardNeighbors({"E3":7, "E5":3})
        self.E4.player_2_goal = True
        self.E5 = BoardNeighbors({"E4":7, "E6":3})
        self.E6 = BoardNeighbors({"E5":7, "E7":3})
        self.E7 = BoardNeighbors({"E6":7, "D6":6, "D7":5})
        self.E7.player_2_entry = True
        self.player_1_bench_1 = BoardNeighbors({'A1':None, 'A7':None})
        self.player_1_bench_1.occupant = player_1_team.pokemon1
        self.player_1_bench_1.occupant_team = 1
        self.player_1_bench_1.occupied = True
        self.player_1_bench_2 = BoardNeighbors({'A1':None, 'A7':None})
        self.player_1_bench_2.occupant = player_1_team.pokemon2
        self.player_1_bench_2.occupant_team = 1
        self.player_1_bench_2.occupied = True
        self.player_1_bench_3 = BoardNeighbors({'A1':None, 'A7':None})
        self.player_1_bench_3.occupant = player_1_team.pokemon3
        self.player_1_bench_3.occupant_team = 1
        self.player_1_bench_3.occupied = True
        self.player_1_bench_4 = BoardNeighbors({'A1':None, 'A7':None})
        self.player_1_bench_4.occupant = player_1_team.pokemon4
        self.player_1_bench_4.occupant_team = 1
        self.player_1_bench_4.occupied = True
        self.player_1_bench_5 = BoardNeighbors({'A1':None, 'A7':None})
        self.player_1_bench_5.occupant = player_1_team.pokemon5
        self.player_1_bench_5.occupant_team = 1
        self.player_1_bench_5.occupied = True
        self.player_1_bench_6 = BoardNeighbors({'A1':None, 'A7':None})
        self.player_1_bench_6.occupant = player_1_team.pokemon6
        self.player_1_bench_6.occupant_team = 1
        self.player_1_bench_6.occupied = True
        self.player_2_bench_1 = BoardNeighbors({'E1':None, 'E7':None})
        self.player_2_bench_1.occupant = player_1_team.pokemon1
        self.player_2_bench_1.occupant_team = 2
        self.player_2_bench_1.occupied = True
        self.player_2_bench_2 = BoardNeighbors({'E1':None, 'E7':None})
        self.player_2_bench_2.occupant = player_1_team.pokemon2
        self.player_2_bench_2.occupant_team = 2
        self.player_2_bench_2.occupied = True
        self.player_2_bench_3 = BoardNeighbors({'E1':None, 'E7':None})
        self.player_2_bench_3.occupant = player_1_team.pokemon3
        self.player_2_bench_3.occupant_team = 2
        self.player_2_bench_3.occupied = True
        self.player_2_bench_4 = BoardNeighbors({'E1':None, 'E7':None})
        self.player_2_bench_4.occupant = player_1_team.pokemon4
        self.player_2_bench_4.occupant_team = 2
        self.player_2_bench_4.occupied = True
        self.player_2_bench_5 = BoardNeighbors({'E1':None, 'E7':None})
        self.player_2_bench_5.occupant = player_1_team.pokemon5
        self.player_2_bench_5.occupant_team = 2
        self.player_2_bench_5.occupied = True
        self.player_2_bench_6 = BoardNeighbors({'E1':None, 'E7':None})
        self.player_2_bench_6.occupant = player_1_team.pokemon6
        self.player_2_bench_6.occupant_team = 2
        self.player_2_bench_6.occupied = True
        self.player_1_ultra_space_1 = BoardNeighbors({})
        self.player_1_ultra_space_2 = BoardNeighbors({})
        self.player_1_ultra_space_3 = BoardNeighbors({})
        self.player_1_ultra_space_4 = BoardNeighbors({})
        self.player_1_ultra_space_5 = BoardNeighbors({})
        self.player_1_ultra_space_6 = BoardNeighbors({})
        self.player_2_ultra_space_1 = BoardNeighbors({})
        self.player_2_ultra_space_2 = BoardNeighbors({})
        self.player_2_ultra_space_3 = BoardNeighbors({})
        self.player_2_ultra_space_4 = BoardNeighbors({})
        self.player_2_ultra_space_5 = BoardNeighbors({})
        self.player_2_ultra_space_6 = BoardNeighbors({})
        self.player_1_eliminated_1 = BoardNeighbors({})
        self.player_1_eliminated_2 = BoardNeighbors({})
        self.player_1_eliminated_3 = BoardNeighbors({})
        self.player_1_eliminated_4 = BoardNeighbors({})
        self.player_1_eliminated_5 = BoardNeighbors({})
        self.player_1_eliminated_6 = BoardNeighbors({})
        self.player_2_eliminated_1 = BoardNeighbors({})
        self.player_2_eliminated_2 = BoardNeighbors({})
        self.player_2_eliminated_3 = BoardNeighbors({})
        self.player_2_eliminated_4 = BoardNeighbors({})
        self.player_2_eliminated_5 = BoardNeighbors({})
        self.player_2_eliminated_6 = BoardNeighbors({})
        self.player_1_PC_1 = BoardNeighbors({})
        self.player_1_PC_2 = BoardNeighbors({})
        self.player_2_PC_1 = BoardNeighbors({})
        self.player_2_PC_2 = BoardNeighbors({})

        #board coordinates for each space

        
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

def surround_check(focal_unit):
    """Checks for surround conditions of a target space"""
    surround_counter = len(eval(f"board.{focal_unit['location']}.neighbors.keys()"))
    for x in eval(f"board.{focal_unit['location']}.neighbors.keys()"):
        if eval(f"board.{x}.occupied") == True and eval(f"board.{focal_unit['location']}.controlling_player") != eval(f"board.{x}.controlling_player"):
            surround_counter -= 1
        else:
            continue
    if surround_counter == 0:
        return True
    else:
        return False

def path_check(focal_unit):
    """Check all possible paths for various purposes, including movement and teleports"""
    ## need to boil for loops down to a recursive function

    global path_counter
    global valid_moves
    global first_loop

    if first_loop == 0:
        first_loop += 1
        del valid_moves[:]
    for x in eval(f"board.{focal_unit['location']}.neighbors.keys()"):
        if eval(f"board.{x}.passable") == True:
            valid_moves.append(x)
        else:
            continue
        if focal_unit['move'] > 1:
            for y in eval(f"board.{x}.neighbors.keys()"):
                if eval(f"board.{y}.passable") == True:
                    valid_moves.append(y)
                else:
                    continue
                if focal_unit['move'] > 2:
                    for z in eval(f"board.{y}.neighbors.keys()"):
                        if eval(f"board.{z}.passable") == True:
                            valid_moves.append(z)
                        else:
                            continue
                        if focal_unit['move'] > 3:
                            for a in eval(f"board.{z}.neighbors.keys()"):
                                if eval(f"board.{a}.passable") == True:
                                    valid_moves.append(a)
                                else:
                                    continue
                                if focal_unit['move'] > 4:
                                    for b in eval(f"board.{a}.neighbors.keys()"):
                                        if eval(f"board.{b}.passable") == True:
                                            valid_moves.append(b)
                                        else:
                                            continue
                                        if focal_unit['move'] > 5:        
                                            for c in eval(f"board.{b}.neighbors.keys()"):
                                                if eval(f"board.{c}.passable") == True:
                                                    valid_moves.append(c)
                                                else:
                                                    continue
                                                if focal_unit['move'] >6:
                                                    for d in eval(f"board.{c}.neighbors.keys()"):
                                                        if eval(f"board.{d}.passable") == True:
                                                            valid_moves.append(d)
                                                        else:
                                                            continue
                                                        if focal_unit['move'] >7:
                                                            for e in eval(f"board.{d}.neighbors.keys()"):
                                                                if eval(f"board.{e}.passable") == True:
                                                                    valid_moves.append(e)
                                                                else:
                                                                    continue
                                                                if focal_unit['move'] >8:
                                                                    for f in eval(f"board.{e}.neighbors.keys()"):
                                                                        if eval(f"board.{f}.passable") == True:
                                                                            valid_moves.append(f)
                                                                        else:
                                                                            continue

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
    return checked_moves
    
class PlayerTeam():
    """Instantiate class that contains player 1 team and base stats."""
    ## WORKAROUND IMPLEMENTED DUE TO TEAM INSTANTIATION ISSUES BETWEEN PLAYERS
    def __init__(self, controlling_player):
        self.pokemon1 = {}
        self.pokemon2 = {}
        self.pokemon3 = {}
        self.pokemon4 = {}
        self.pokemon5 = {}
        self.pokemon6 = {}
        self.pokemon1['location'] = f'player_{controlling_player}_bench_1'
        self.pokemon1['knocked_out'] = False
        self.pokemon1['to_PC'] = False
        self.pokemon1['to_eliminated'] = False
        self.pokemon1['to_ultra_space'] = False
        self.pokemon1['to_bench'] = False
        self.pokemon1['wait'] = 0
        self.pokemon1['in-play'] = False
        self.pokemon1['status'] = 'clear'
        self.pokemon1['markers'] = 'clear'
        self.pokemon1['control'] = controlling_player
        self.pokemon2['location'] = f'player_{controlling_player}_bench_2'
        self.pokemon2['knocked_out'] = False
        self.pokemon2['to_PC'] = False
        self.pokemon2['to_eliminated'] = False
        self.pokemon2['to_ultra_space'] = False
        self.pokemon2['to_bench'] = False
        self.pokemon2['wait'] = 0
        self.pokemon2['in-play'] = False
        self.pokemon2['status'] = 'clear'
        self.pokemon2['markers'] = 'clear'
        self.pokemon2['control'] = controlling_player
        self.pokemon3['location'] = f'player_{controlling_player}_bench_3'
        self.pokemon3['knocked_out'] = False
        self.pokemon3['to_PC'] = False
        self.pokemon3['to_eliminated'] = False
        self.pokemon3['to_ultra_space'] = False
        self.pokemon3['to_bench'] = False
        self.pokemon3['wait'] = 0
        self.pokemon3['in-play'] = False
        self.pokemon3['status'] = 'clear'
        self.pokemon3['markers'] = 'clear'
        self.pokemon3['control'] = controlling_player
        self.pokemon4['location'] = f'player_{controlling_player}_bench_4'
        self.pokemon4['knocked_out'] = False
        self.pokemon4['to_PC'] = False
        self.pokemon4['to_eliminated'] = False
        self.pokemon4['to_ultra_space'] = False
        self.pokemon4['to_bench'] = False
        self.pokemon4['wait'] = 0
        self.pokemon4['in-play'] = False
        self.pokemon4['status'] = 'clear'
        self.pokemon4['markers'] = 'clear'
        self.pokemon4['control'] = controlling_player
        self.pokemon5['location'] = f'player_{controlling_player}_bench_5'
        self.pokemon5['knocked_out'] = False
        self.pokemon5['to_PC'] = False
        self.pokemon5['to_eliminated'] = False
        self.pokemon5['to_ultra_space'] = False
        self.pokemon5['to_bench'] = False
        self.pokemon5['wait'] = 0
        self.pokemon5['in-play'] = False
        self.pokemon5['status'] = 'clear'
        self.pokemon5['markers'] = 'clear'
        self.pokemon5['control'] = controlling_player
        self.pokemon6['location'] = f'player_{controlling_player}_bench_6'
        self.pokemon6['knocked_out'] = False
        self.pokemon6['to_PC'] = False
        self.pokemon6['to_eliminated'] = False
        self.pokemon6['to_ultra_space'] = False
        self.pokemon6['to_bench'] = False
        self.pokemon6['wait'] = 0
        self.pokemon6['in-play'] = False
        self.pokemon6['status'] = 'clear'
        self.pokemon6['markers'] = 'clear'
        self.pokemon6['control'] = controlling_player

    def TeamUpdate(self, controlling_player):
        ## Imports custom unit loadout from custom file
        
        ## Iterates over lines in custom unit loadout file, compares them to
        ## pokemon_stats loaded above, and writes the correct stats to a created playerTeam() object
        print("_-^-"*8, "\nAvailable Teams:\n")
        try:
            for teams in os.listdir(os.path.join(sys.path[0] + "\\saves\\teams\\")):
                print(teams[len(sys.path[0] + "\\save\\teams\\")*(-1):-4])
        except:
            pass
        print("_-^-"*8)
        #team_file = input(f"Select player {controlling_player} team.\n--->")
        selected_team_path = os.path.join(sys.path[0], f"saves\\teams\\TestCaseTeam.txt")
        custom_team = open(selected_team_path)
        custom_team = custom_team.read().splitlines()
        line_counter = 1
        for line in custom_team:
            exec(f"self.pokemon{line_counter}.update(pokemon_stats['{line}'])")
            line_counter += 1

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

def target_finder(combatant, attack_distance = 1):
    """Checks adjacent spaces for valid attack targets"""
    ##  TO ADD:
    ##  attack_distance variable accounts for extended
    ##  range attackers like Kartana or Aegislash
    ##  Need to rework function to be recursive for attack distance
    target_list = []
    combatant = eval(combatant)
    for x in eval(f"board.{combatant['location']}.neighbors.keys()"):
        if len(combatant['location']) == 2:
            if eval(f"board.{x}.occupied") == True:
                if eval(f"board.{x}.controlling_player") != eval(
                    f"board.{combatant['location']}.controlling_player") or 0:
                    target_list.append(x)
                else:
                    continue
            else:
                continue
        else:
            continue
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
    """
    combatant_1 = eval(combatant_1)
    combatant_2 = eval(combatant_2)

    combatant_1_attack = spin(combatant_1)
    combatant_2_attack = spin(combatant_2)
    combatant_1_color = eval(f"combatant_1['attack{combatant_1_attack}color']")
    if not combatant_1_color == "Red" or combatant_1_color == "Blue":
        combatant_1_power = eval(f"combatant_1['attack{combatant_1_attack}power']")
        if combatant_1_color != "Purple":
            if combatant_1['status'] == "poison" or combatant_1['status'] == "burn":
                combatant_1_power -= 20
            elif combatant_1['status'] == "noxious":
                combatant_1_power -= 40
    else:
        pass
    combatant_2_color = eval(f"combatant_2['attack{combatant_2_attack}color']")
    if not combatant_2_color == "Red" or combatant_2_color == "Blue":
        combatant_2_power = eval(f"combatant_2['attack{combatant_2_attack}power']")
        if combatant_2_color != "Purple":
            if combatant_2['status'] == "poison" or combatant_2['status'] == "burn":
                combatant_2_power -= 20
            elif combatant_2['status'] == "noxious":
                combatant_2_power -= 40
    else:
        pass
    if combatant_1_color == "White" and combatant_2_color == "White":
        if combatant_1_power > combatant_2_power:
            return 1
        elif combatant_1_power < combatant_2_power:
            return 2
        elif combatant_1_power == combatant_2_power:
            return 0
        else:
            pass
    elif combatant_1_color == "White" and combatant_2_color == "Gold":
        if combatant_1_power > combatant_2_power:
            return 1
        elif combatant_1_power < combatant_2_power:
            return 2
        elif combatant_1_power == combatant_2_power:
            return 0
        else:
            pass
    elif combatant_1_color == "Gold" and combatant_2_color == "White":
        if combatant_1_power > combatant_2_power:
            return 1
        elif combatant_1_power < combatant_2_power:
            return 2
        elif combatant_1_power == combatant_2_power:
            return 0
        else:
            pass
    elif combatant_1_color == "Gold" and combatant_2_color == "Gold":
        if combatant_1_power > combatant_2_power:
            return 1
        elif combatant_1_power < combatant_2_power:
            return 2
        elif combatant_1_power == combatant_2_power:
            return 0
        else:
            pass
    elif combatant_1_color == "Gold" and combatant_2_color == "Purple":
        return 1
    elif combatant_1_color == "Purple" and combatant_2_color == "Gold":
        return 2
    elif combatant_1_color == "Red" and combatant_2_color == "Red":
        return 0
    elif combatant_1_color == "Red" and combatant_2_color != "Red":
        return 2
    elif combatant_1_color != "Red" and combatant_2_color == "Red":
        return 1
    elif combatant_1_color == "Blue" and combatant_2_color != "Blue":
        return 1
    elif combatant_1_color != "Blue" and combatant_2_color == "Blue":
        return 2
    elif combatant_1_color == "Purple" and combatant_2_color == "White":
        return 1
    elif combatant_1_color == "White" and combatant_2_color == "Purple":
        return 2
    elif combatant_1_color == "Purple" and combatant_2_color == "Purple":
        if combatant_1_power > combatant_2_power:
            return 1
        elif combatant_1_power < combatant_2_power:
            return 2
        elif combatant_1_power == combatant_2_power:
            return 0
        else:
            pass
    else:
        pass


## Imports unit data from file location
stats_path = os.path.join(sys.path[0], "pokemon-stats.json")

## Loads unit data imported above
pokemon_stats = json.load(open(stats_path, "r"))

path_counter = 0
valid_moves = []
first_loop = 0

player_1_team = PlayerTeam(1)
player_2_team = PlayerTeam(2)

player_1_team.TeamUpdate(1)
player_2_team.TeamUpdate(2)

## Must be instantiated after teams due to variable dependency / inheritance
## /whatever the technical term is. These will likely be moved to a game_start() function
board = ClassicBoardGenerator()
