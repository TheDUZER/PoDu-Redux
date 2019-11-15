# -*- coding: utf-8 -*-

"""
TO DO:

-Implement team file selection for GUI; limit iteration over team files to first 6 lines
-Set up team selection for two separate teams
-Add attributes to player pokemon for statuses and markers
"""

import json, sys, os, random, boardtest

class PlayerTeam:
    """Instantiate class that contains player teams."""
    def __init__(self, controlling_player, team_file):
        #Imports custom unit loadout from custom file
        selected_team_path = os.path.join(sys.path[0], f"saves\\teams\\{team_file}.txt")
        
        #Iterates over lines in custom unit loadout file, compares them to
        #pokemon_stats loaded above, and writes the correct stats to a created playerTeam() object
        with open(selected_team_path) as custom_team:
            custom_team = custom_team.read().splitlines()
            line_counter = 1
            for line in custom_team:
                exec(f"self.pokemon{line_counter} = pokemon_stats['{line}']")
                exec(f"self.pokemon{line_counter}['location'] = 'player_{controlling_player}_Bench[{line_counter-1}]'")
                exec(f"self.pokemon{line_counter}['Knocked_Out'] = False")
                exec(f"self.pokemon{line_counter}['To_PC'] = False")
                exec(f"self.pokemon{line_counter}['To_Eliminated'] = False")
                exec(f"self.pokemon{line_counter}['To_Ultra_Space'] = False")
                exec(f"self.pokemon{line_counter}['To_Bench'] = False")
                exec(f"self.pokemon{line_counter}['Wait'] = 0")
                exec(f"self.pokemon{line_counter}['status'] = 'Clear'")
                exec(f"self.pokemon{line_counter}['markers'] = 'Clear'")
                exec(f"self.pokemon{line_counter}['control'] = {controlling_player}")
                line_counter += 1

def spin(combatant):
    """Perform SPIN action for selected unit. Can be applied to effects and battles."""

    #Perform number randomization for spin
    combatant_spin = random.randint(1,24)

    #Iterate over wheel for maximum number of possible wheel segments for any unit (9)
    for wheel_numbers in range(1,10):
        #Check if wheel segment is valid
        if eval(f"combatant['attack{wheel_numbers}range']") != "null":
            #Pull wheel information from unit data and find segment
            #ranges to check against combatant_spin
            if combatant_spin <= eval(f"combatant['attack{wheel_numbers}range']"):
                combatant_attack = wheel_numbers
                #Returns segment number of SPIN result (wheel_numbers at correct iteration)
                return combatant_attack
                break
            else:
                continue
        else:
            break

def battle_spin_compare(combatant_1, combatant_2):
    """
    Compare the SPIN of two battling units.

    'If' blocks check for color matchups, then nest down to check power stats when
    relevant (i.e. White vs. Gold)
    """
    #To Do:
    #-Remove print statements and apply appropriate attribute / list item modifications to units and board
    combatant_1_attack = spin(combatant_1)
    combatant_2_attack = spin(combatant_2)
    combatant_1_color = eval(f"combatant_1['attack{combatant_1_attack}color']")
    if not combatant_1_color == "Red" or combatant_1_color == "Blue":
        combatant_1_power = eval(f"combatant_1['attack{combatant_1_attack}power']")
    else:
        pass
    combatant_2_color = eval(f"combatant_2['attack{combatant_2_attack}color']")
    if not combatant_2_color == "Red" or combatant_2_color == "Blue":
        combatant_2_power = eval(f"combatant_2['attack{combatant_2_attack}power']")
    else:
        pass
    if combatant_1_color == "White" and combatant_2_color == "White":
        if combatant_1_power > combatant_2_power:
            print("Combatant 1 Wins!")
        elif combatant_1_power < combatant_2_power:
            print("Combatant 2 Wins!")
        elif combatant_1_power == combatant_2_power:
            print("tie")
        else:
            pass
    elif combatant_1_color == "White" and combatant_2_color == "Gold":
        if combatant_1_power > combatant_2_power:
            print("Combatant 1 Wins!")
        elif combatant_1_power < combatant_2_power:
            print("Combatant 2 Wins!")
        elif combatant_1_power == combatant_2_power:
            print("tie")
        else:
            pass
    elif combatant_1_color == "Gold" and combatant_2_color == "White":
        if combatant_1_power > combatant_2_power:
            print("Combatant 1 Wins!")
        elif combatant_1_power < combatant_2_power:
            print("Combatant 2 Wins!")
        elif combatant_1_power == combatant_2_power:
            print("tie")
        else:
            pass
    elif combatant_1_color == "Gold" and combatant_2_color == "Gold":
        if combatant_1_power > combatant_2_power:
            print("Combatant 1 Wins!")
        elif combatant_1_power < combatant_2_power:
            print("Combatant 2 Wins!")
        elif combatant_1_power == combatant_2_power:
            print("tie")
        else:
            pass
    elif combatant_1_color == "Gold" and combatant_2_color == "Purple":
        print("Combatant 1 Wins!")
    elif combatant_1_color == "Purple" and combatant_2_color == "Gold":
        print("Combatant 2 Wins!")
    elif combatant_1_color == "Red" and combatant_2_color == "Red":
        print("tie")
    elif combatant_1_color == "Red" and combatant_2_color != "Red":
        print("Combatant 2 Wins!")
    elif combatant_1_color != "Red" and combatant_2_color == "Red":
        print("Combatant 1 Wins!")
    elif combatant_1_color == "Blue" and combatant_2_color != "Blue":
        print("Combatant 1 Wins!")
    elif combatant_1_color != "Blue" and combatant_2_color == "Blue":
        print("Combatant 2 Wins!")
    elif combatant_1_color == "Purple" and combatant_2_color == "White":
        print("Combatant 1 Wins!")
    elif combatant_1_color == "White" and combatant_2_color == "Purple":
        print("Combatant 2 Wins!")
    elif combatant_1_color == "Purple" and combatant_2_color == "Purple":
        if combatant_1_power > combatant_2_power:
            print("Combatant 1 Wins!")
        elif combatant_1_power < combatant_2_power:
            print("Combatant 2 Wins!")
        elif combatant_1_power == combatant_2_power:
            print("tie")
        else:
            pass
    else:
        pass

#Imports unit data from file location
stats_path = os.path.join(sys.path[0], "pokemon-stats.json")

#Loads unit data imported above
with open(stats_path, "r") as pokedata:
    pokemon_stats = json.load(pokedata)

player_1_team = PlayerTeam(1, "myteam")
player_2_team = PlayerTeam(2, "myteam")
