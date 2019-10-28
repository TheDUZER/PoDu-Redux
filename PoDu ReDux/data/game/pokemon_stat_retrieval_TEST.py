# -*- coding: utf-8 -*-

import json, sys, os

class playerteam():
    pass

statspath = os.path.join(sys.path[0], 'pokemon-stats.json')
selectedteampath = os.path.join(sys.path[0], 'customteams\\myteam.txt')

with open(statspath, 'r') as pokedata:
    pokemonstats = json.load(pokedata)

for pokemon in pokemonstats.keys():
    if pokemon == 'Rampardos':
        print(pokemonstats[pokemon])

team1 = playerteam()
team2 = playerteam()

with open(selectedteampath) as customteam:
    customteam = customteam.read().splitlines()
    x = 1
    for line in customteam:
        exec(f'team1.pokemon{x} = line')
        x += 1
    print(team1.pokemon1)

print(pokemonstats[team1.pokemon1])

input()
