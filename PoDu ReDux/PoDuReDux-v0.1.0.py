##  -*- coding: utf-8 -*-

"""
CURRENT TO DO:

-Stitch surround logic to GUI
-Draw GUI elements for path and potential attack target previews

"""
import arcade, sys, os, game_logic, random

SPRITE_SCALING = 2.5

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
SCREEN_TITLE = "PoDu ReDux v0.1.0"

checked_moves = []
click_counter = 0
in_transit = ''
in_transit_location = ''
potential_targets = []
move_click = False
attack_click = False
turn_player = random.randint(1,2)

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        
        #arcade.set_background_color(arcade.color.BLACK)
        
        self.background = None
        self.ClassicBoard = None
        self.TvTBoard = None
        self.coords = {
            'A1':{'x': 290, 'y': 294},
            'A2':{'x': 365, 'y': 293},
            'A3':{'x': 436, 'y': 293},
            'A4':{'x': 512, 'y': 293},
            'A5':{'x': 586, 'y': 293},
            'A6':{'x': 658, 'y': 293},
            'A7':{'x': 732, 'y': 293},
            'B1':{'x': 290, 'y': 414},
            'B2':{'x': 400, 'y': 414},
            'B4':{'x': 512, 'y': 414},
            'B6':{'x': 625, 'y': 414},
            'B7':{'x': 732, 'y': 414},
            'C1':{'x': 290, 'y': 514},
            'C2':{'x': 400, 'y': 514},
            'C6':{'x': 625, 'y': 514},
            'C7':{'x': 732, 'y': 514},
            'D1':{'x': 290, 'y': 614},
            'D2':{'x': 400, 'y': 614},
            'D4':{'x': 512, 'y': 614},
            'D6':{'x': 625, 'y': 614},
            'D7':{'x': 732, 'y': 614},
            'E1':{'x': 290, 'y': 731},
            'E2':{'x': 365, 'y': 731},
            'E3':{'x': 436, 'y': 731},
            'E4':{'x': 512, 'y': 731},
            'E5':{'x': 586, 'y': 731},
            'E6':{'x': 658, 'y': 731},
            'E7':{'x': 732, 'y': 731},
            'player_1_bench_1':{'x': 311, 'y': 183},
            'player_1_bench_2':{'x': 411, 'y': 183},
            'player_1_bench_3':{'x': 511, 'y': 183},
            'player_1_bench_4':{'x': 360, 'y': 110},
            'player_1_bench_5':{'x': 460, 'y': 110},
            'player_1_bench_6':{'x': 560, 'y': 110},
            'player_2_bench_1':{'x': 715, 'y': 845},
            'player_2_bench_2':{'x': 615, 'y': 845},
            'player_2_bench_3':{'x': 515, 'y': 845},
            'player_2_bench_4':{'x': 661, 'y': 921},
            'player_2_bench_5':{'x': 561, 'y': 921},
            'player_2_bench_6':{'x': 461, 'y': 921},
            'player_1_eliminated_1':{'x': 124, 'y': 280},
            'player_1_eliminated_2':{'x': 50, 'y': 240},
            'player_1_eliminated_3':{'x': 124, 'y': 185},
            'player_1_eliminated_4':{'x': 50, 'y': 100},
            'player_1_eliminated_5':{'x': 124, 'y': 140},
            'player_1_eliminated_6':{'x': 50, 'y': 55},
            'player_2_eliminated_1':{'x': 900, 'y': 752},
            'player_2_eliminated_2':{'x': 975, 'y': 794},
            'player_2_eliminated_3':{'x': 900, 'y': 843},
            'player_2_eliminated_4':{'x': 975, 'y': 886},
            'player_2_eliminated_5':{'x': 900, 'y': 940},
            'player_2_eliminated_6':{'x': 975, 'y': 975},
            'player_1_ultra_space_1':{'x': 900, 'y': 280},
            'player_1_ultra_space_2':{'x': 975, 'y': 240},
            'player_1_ultra_space_3':{'x': 900, 'y': 185},
            'player_1_ultra_space_4':{'x': 975, 'y': 100},
            'player_1_ultra_space_5':{'x': 900, 'y': 140},
            'player_1_ultra_space_6':{'x': 975, 'y': 55},
            'player_2_ultra_space_1':{'x': 124, 'y': 752},
            'player_2_ultra_space_2':{'x': 50, 'y': 794},
            'player_2_ultra_space_3':{'x': 124, 'y': 843},
            'player_2_ultra_space_4':{'x': 50, 'y': 886},
            'player_2_ultra_space_5':{'x': 124, 'y': 940},
            'player_2_ultra_space_6':{'x': 50, 'y': 975},
            'player_1_PC_1':{'x': 645, 'y': 185},
            'player_1_PC_2':{'x': 727, 'y': 185},
            'player_2_PC_1':{'x': 380, 'y': 840},
            'player_2_PC_2':{'x': 297, 'y': 840},
            }
        
        self.player_1_pokemon_1 = None
        self.player_1_pokemon_2 = None
        self.player_1_pokemon_3 = None
        self.player_1_pokemon_4 = None
        self.player_1_pokemon_5 = None
        self.player_1_pokemon_6 = None
        self.player_2_pokemon_1 = None
        self.player_2_pokemon_2 = None
        self.player_2_pokemon_3 = None
        self.player_2_pokemon_4 = None
        self.player_2_pokemon_5 = None
        self.player_2_pokemon_6 = None
        
        # If you have sprite lists, you should create them here,
        # and set them to None

        self.pokemon_list = None
        
    def setup(self):
        # Create your sprites and sprite lists here
        self.pokemon_list = arcade.SpriteList()
        
        self.player_1_pokemon_1 = arcade.Sprite(
            f"images/Sprites/{game_logic.player_1_team.pokemon1['spritefile']}",
            SPRITE_SCALING)
        self.player_1_pokemon_2 = arcade.Sprite(
            f"images/Sprites/{game_logic.player_1_team.pokemon2['spritefile']}",
            SPRITE_SCALING)
        self.player_1_pokemon_3 = arcade.Sprite(
            f"images/Sprites/{game_logic.player_1_team.pokemon3['spritefile']}",
            SPRITE_SCALING)
        self.player_1_pokemon_4 = arcade.Sprite(
            f"images/Sprites/{game_logic.player_1_team.pokemon4['spritefile']}",
            SPRITE_SCALING)
        self.player_1_pokemon_5 = arcade.Sprite(
            f"images/Sprites/{game_logic.player_1_team.pokemon5['spritefile']}",
            SPRITE_SCALING)
        self.player_1_pokemon_6 = arcade.Sprite(
            f"images/Sprites/{game_logic.player_1_team.pokemon6['spritefile']}",
            SPRITE_SCALING)
        self.player_2_pokemon_1 = arcade.Sprite(
            f"images/Sprites/{game_logic.player_2_team.pokemon1['spritefile']}",
            SPRITE_SCALING)
        self.player_2_pokemon_2 = arcade.Sprite(
            f"images/Sprites/{game_logic.player_2_team.pokemon2['spritefile']}",
            SPRITE_SCALING)
        self.player_2_pokemon_3 = arcade.Sprite(
            f"images/Sprites/{game_logic.player_2_team.pokemon3['spritefile']}",
            SPRITE_SCALING)
        self.player_2_pokemon_4 = arcade.Sprite(
            f"images/Sprites/{game_logic.player_2_team.pokemon4['spritefile']}",
            SPRITE_SCALING)
        self.player_2_pokemon_5 = arcade.Sprite(
            f"images/Sprites/{game_logic.player_2_team.pokemon5['spritefile']}",
            SPRITE_SCALING)
        self.player_2_pokemon_6 = arcade.Sprite(
            f"images/Sprites/{game_logic.player_2_team.pokemon6['spritefile']}",
            SPRITE_SCALING)

        #Place Player 1 team on board        
        self.player_1_pokemon_1.center_x = eval(
            f"self.coords['{game_logic.player_1_team.pokemon1['location']}']['x']")
        self.player_1_pokemon_1.center_y = eval(
            f"self.coords['{game_logic.player_1_team.pokemon1['location']}']['y']")
        self.player_1_pokemon_2.center_x = eval(
            f"self.coords['{game_logic.player_1_team.pokemon2['location']}']['x']")
        self.player_1_pokemon_2.center_y = eval(
            f"self.coords['{game_logic.player_1_team.pokemon2['location']}']['y']")
        self.player_1_pokemon_3.center_x = eval(
            f"self.coords['{game_logic.player_1_team.pokemon3['location']}']['x']")
        self.player_1_pokemon_3.center_y = eval(
            f"self.coords['{game_logic.player_1_team.pokemon3['location']}']['y']")
        self.player_1_pokemon_4.center_x = eval(
            f"self.coords['{game_logic.player_1_team.pokemon4['location']}']['x']")
        self.player_1_pokemon_4.center_y = eval(
            f"self.coords['{game_logic.player_1_team.pokemon4['location']}']['y']")
        self.player_1_pokemon_5.center_x = eval(
            f"self.coords['{game_logic.player_1_team.pokemon5['location']}']['x']")
        self.player_1_pokemon_5.center_y = eval(
            f"self.coords['{game_logic.player_1_team.pokemon5['location']}']['y']")
        self.player_1_pokemon_6.center_x = eval(
            f"self.coords['{game_logic.player_1_team.pokemon6['location']}']['x']")
        self.player_1_pokemon_6.center_y = eval(
            f"self.coords['{game_logic.player_1_team.pokemon6['location']}']['y']")
        
        #Place Player 2 team 
        self.player_2_pokemon_1.center_x = eval(
            f"self.coords['{game_logic.player_2_team.pokemon1['location']}']['x']")
        self.player_2_pokemon_1.center_y = eval(
            f"self.coords['{game_logic.player_2_team.pokemon1['location']}']['y']")
        self.player_2_pokemon_2.center_x = eval(
            f"self.coords['{game_logic.player_2_team.pokemon2['location']}']['x']")
        self.player_2_pokemon_2.center_y = eval(
            f"self.coords['{game_logic.player_2_team.pokemon2['location']}']['y']")
        self.player_2_pokemon_3.center_x = eval(
            f"self.coords['{game_logic.player_2_team.pokemon3['location']}']['x']")
        self.player_2_pokemon_3.center_y = eval(
            f"self.coords['{game_logic.player_2_team.pokemon3['location']}']['y']")
        self.player_2_pokemon_4.center_x = eval(
            f"self.coords['{game_logic.player_2_team.pokemon4['location']}']['x']")
        self.player_2_pokemon_4.center_y = eval(
            f"self.coords['{game_logic.player_2_team.pokemon4['location']}']['y']")
        self.player_2_pokemon_5.center_x = eval(
            f"self.coords['{game_logic.player_2_team.pokemon5['location']}']['x']")
        self.player_2_pokemon_5.center_y = eval(
            f"self.coords['{game_logic.player_2_team.pokemon5['location']}']['y']")
        self.player_2_pokemon_6.center_x = eval(
            f"self.coords['{game_logic.player_2_team.pokemon6['location']}']['x']")
        self.player_2_pokemon_6.center_y = eval(
            f"self.coords['{game_logic.player_2_team.pokemon6['location']}']['y']")
        
        self.pokemon_list.append(self.player_1_pokemon_1)
        self.pokemon_list.append(self.player_1_pokemon_2)
        self.pokemon_list.append(self.player_1_pokemon_3)
        self.pokemon_list.append(self.player_1_pokemon_4)
        self.pokemon_list.append(self.player_1_pokemon_5)
        self.pokemon_list.append(self.player_1_pokemon_6)
        
        self.pokemon_list.append(self.player_2_pokemon_1)
        self.pokemon_list.append(self.player_2_pokemon_2)
        self.pokemon_list.append(self.player_2_pokemon_3)
        self.pokemon_list.append(self.player_2_pokemon_4)
        self.pokemon_list.append(self.player_2_pokemon_5)
        self.pokemon_list.append(self.player_2_pokemon_6)

        print("v^v^"*8, "\nAvailable Backgrounds:\n")
        try:
            for background_textures in os.listdir(os.path.join(sys.path[0] + "\\images\\board\\backgrounds\\")):
                print(background_textures[len(sys.path[0] + "\\images\\board\\backgrounds\\")*(-1):-4])
        except:
            pass
        print("v^v^"*8)
        background_select = input("Select background image.\n--->")
        self.background = arcade.load_texture(f"images/board/backgrounds/{background_select}.png")
        self.ClassicBoard = arcade.load_texture("images/board/overlays/dueloverlay.png")

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.ClassicBoard)
        arcade.draw_circle_filled(self.player_1_pokemon_1.center_x, self.player_1_pokemon_1.center_y,
                                  40, arcade.color.AZURE)
        arcade.draw_circle_filled(self.player_1_pokemon_2.center_x, self.player_1_pokemon_2.center_y,
                                  40, arcade.color.AZURE)
        arcade.draw_circle_filled(self.player_1_pokemon_3.center_x, self.player_1_pokemon_3.center_y,
                                  40, arcade.color.AZURE)
        arcade.draw_circle_filled(self.player_1_pokemon_4.center_x, self.player_1_pokemon_4.center_y,
                                  40, arcade.color.AZURE)
        arcade.draw_circle_filled(self.player_1_pokemon_5.center_x, self.player_1_pokemon_5.center_y,
                                  40, arcade.color.AZURE)
        arcade.draw_circle_filled(self.player_1_pokemon_6.center_x, self.player_1_pokemon_6.center_y,
                                  40, arcade.color.AZURE)
        arcade.draw_circle_filled(self.player_2_pokemon_1.center_x, self.player_2_pokemon_1.center_y,
                                  40, arcade.color.RASPBERRY)
        arcade.draw_circle_filled(self.player_2_pokemon_2.center_x, self.player_2_pokemon_2.center_y,
                                  40, arcade.color.RASPBERRY)
        arcade.draw_circle_filled(self.player_2_pokemon_3.center_x, self.player_2_pokemon_3.center_y,
                                  40, arcade.color.RASPBERRY)
        arcade.draw_circle_filled(self.player_2_pokemon_4.center_x, self.player_2_pokemon_4.center_y,
                                  40, arcade.color.RASPBERRY)
        arcade.draw_circle_filled(self.player_2_pokemon_5.center_x, self.player_2_pokemon_5.center_y,
                                  40, arcade.color.RASPBERRY)
        arcade.draw_circle_filled(self.player_2_pokemon_6.center_x, self.player_2_pokemon_6.center_y,
                                  40, arcade.color.RASPBERRY)

        # Call draw() on all your sprite lists below

        self.pokemon_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        
        #Place Player 1 team on board... again.
        
        self.player_1_pokemon_1.center_x = eval(
            f"self.coords['{game_logic.player_1_team.pokemon1['location']}']['x']")
        self.player_1_pokemon_1.center_y = eval(
            f"self.coords['{game_logic.player_1_team.pokemon1['location']}']['y']")
        self.player_1_pokemon_2.center_x = eval(
            f"self.coords['{game_logic.player_1_team.pokemon2['location']}']['x']")
        self.player_1_pokemon_2.center_y = eval(
            f"self.coords['{game_logic.player_1_team.pokemon2['location']}']['y']")
        self.player_1_pokemon_3.center_x = eval(
            f"self.coords['{game_logic.player_1_team.pokemon3['location']}']['x']")
        self.player_1_pokemon_3.center_y = eval(
            f"self.coords['{game_logic.player_1_team.pokemon3['location']}']['y']")
        self.player_1_pokemon_4.center_x = eval(
            f"self.coords['{game_logic.player_1_team.pokemon4['location']}']['x']")
        self.player_1_pokemon_4.center_y = eval(
            f"self.coords['{game_logic.player_1_team.pokemon4['location']}']['y']")
        self.player_1_pokemon_5.center_x = eval(
            f"self.coords['{game_logic.player_1_team.pokemon5['location']}']['x']")
        self.player_1_pokemon_5.center_y = eval(
            f"self.coords['{game_logic.player_1_team.pokemon5['location']}']['y']")
        self.player_1_pokemon_6.center_x = eval(
            f"self.coords['{game_logic.player_1_team.pokemon6['location']}']['x']")
        self.player_1_pokemon_6.center_y = eval(
            f"self.coords['{game_logic.player_1_team.pokemon6['location']}']['y']")
        
        #Place Player 2 team... again.
        
        self.player_2_pokemon_1.center_x = eval(
            f"self.coords['{game_logic.player_2_team.pokemon1['location']}']['x']")
        self.player_2_pokemon_1.center_y = eval(
            f"self.coords['{game_logic.player_2_team.pokemon1['location']}']['y']")
        self.player_2_pokemon_2.center_x = eval(
            f"self.coords['{game_logic.player_2_team.pokemon2['location']}']['x']")
        self.player_2_pokemon_2.center_y = eval(
            f"self.coords['{game_logic.player_2_team.pokemon2['location']}']['y']")
        self.player_2_pokemon_3.center_x = eval(
            f"self.coords['{game_logic.player_2_team.pokemon3['location']}']['x']")
        self.player_2_pokemon_3.center_y = eval(
            f"self.coords['{game_logic.player_2_team.pokemon3['location']}']['y']")
        self.player_2_pokemon_4.center_x = eval(
            f"self.coords['{game_logic.player_2_team.pokemon4['location']}']['x']")
        self.player_2_pokemon_4.center_y = eval(
            f"self.coords['{game_logic.player_2_team.pokemon4['location']}']['y']")
        self.player_2_pokemon_5.center_x = eval(
            f"self.coords['{game_logic.player_2_team.pokemon5['location']}']['x']")
        self.player_2_pokemon_5.center_y = eval(
            f"self.coords['{game_logic.player_2_team.pokemon5['location']}']['y']")
        self.player_2_pokemon_6.center_x = eval(
            f"self.coords['{game_logic.player_2_team.pokemon6['location']}']['x']")
        self.player_2_pokemon_6.center_y = eval(
            f"self.coords['{game_logic.player_2_team.pokemon6['location']}']['y']")

        #Trash old list and draw a new one.
        
        self.pokemon_list = None
        self.pokemon_list = arcade.SpriteList()
        
        self.pokemon_list.append(self.player_1_pokemon_1)
        self.pokemon_list.append(self.player_1_pokemon_2)
        self.pokemon_list.append(self.player_1_pokemon_3)
        self.pokemon_list.append(self.player_1_pokemon_4)
        self.pokemon_list.append(self.player_1_pokemon_5)
        self.pokemon_list.append(self.player_1_pokemon_6)
        
        self.pokemon_list.append(self.player_2_pokemon_1)
        self.pokemon_list.append(self.player_2_pokemon_2)
        self.pokemon_list.append(self.player_2_pokemon_3)
        self.pokemon_list.append(self.player_2_pokemon_4)
        self.pokemon_list.append(self.player_2_pokemon_5)
        self.pokemon_list.append(self.player_2_pokemon_6)
        
        self.pokemon_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        global move_click
        global attack_click
        global in_transit
        global in_transit_location
        global in_transit_combatant
        global checked_moves
        global potential_targets
        global turn_player

        if button == 1:
            print(f"Player {turn_player} turn.")

            if not move_click and not attack_click:
                if turn_player == 1:
                    for units in dir(game_logic.player_1_team):
                        if units.startswith("pokemon"):
                            if x in range(eval(f"self.coords[game_logic.player_1_team.{units}['location']]['x']") - 40,
                                          eval(f"self.coords[game_logic.player_1_team.{units}['location']]['x']") + 40
                                          ) and y in range(
                                              eval(f"self.coords[game_logic.player_1_team.{units}['location']]['y']") - 40,
                                              eval(f"self.coords[game_logic.player_1_team.{units}['location']]['y']") + 40):
                                move_click = True
                                in_transit = f"game_logic.player_1_team.{units}"
                                in_transit_combatant = f'{in_transit[11:]}'
                                in_transit_location = eval(f"{in_transit}['location']")
                                checked_moves = game_logic.path_check(eval(f"game_logic.player_1_team.{units}"))
                                print("Click this unit again to attack without moving, if able.")
                                break
                elif turn_player == 2:
                    for units in dir(game_logic.player_2_team):
                        if units.startswith("pokemon"):
                            if x in range(eval(f"self.coords[game_logic.player_2_team.{units}['location']]['x']") - 40,
                                          eval(f"self.coords[game_logic.player_2_team.{units}['location']]['x']") + 40
                                          ) and y in range(
                                              eval(f"self.coords[game_logic.player_2_team.{units}['location']]['y']") - 40,
                                              eval(f"self.coords[game_logic.player_2_team.{units}['location']]['y']") + 40):
                                move_click = True
                                in_transit = f"game_logic.player_2_team.{units}"
                                in_transit_combatant = f'{in_transit[11:]}'
                                in_transit_location = eval(f"{in_transit}['location']")
                                checked_moves = game_logic.path_check(eval(f"game_logic.player_2_team.{units}"))
                                print("Click this unit again to attack without moving, if able.")
                                break
                for units in dir(game_logic.player_1_team):
                        if units.startswith("pokemon"):
                            if x in range(eval(f"self.coords[game_logic.player_1_team.{units}['location']]['x']") - 40,
                                          eval(f"self.coords[game_logic.player_1_team.{units}['location']]['x']") + 40
                                          ) and y in range(
                                              eval(f"self.coords[game_logic.player_1_team.{units}['location']]['y']") - 40,
                                              eval(f"self.coords[game_logic.player_1_team.{units}['location']]['y']") + 40):
                                print("Player 1's ", eval(f"game_logic.player_1_team.{units}['name']"), "'s MP:\t", eval(f"game_logic.player_1_team.{units}['move']"))
                for units in dir(game_logic.player_2_team):
                        if units.startswith("pokemon"):
                            if x in range(eval(f"self.coords[game_logic.player_2_team.{units}['location']]['x']") - 40,
                                          eval(f"self.coords[game_logic.player_2_team.{units}['location']]['x']") + 40
                                          ) and y in range(
                                              eval(f"self.coords[game_logic.player_2_team.{units}['location']]['y']") - 40,
                                              eval(f"self.coords[game_logic.player_2_team.{units}['location']]['y']") + 40):
                                print("Player 2's ", eval(f"game_logic.player_2_team.{units}['name']"), "'s MP:\t", eval(f"game_logic.player_2_team.{units}['move']"))
                if len(checked_moves) > 0:
                    for moves in checked_moves:
                        arcade.draw_circle_filled(eval(f"self.coords['{moves}']['x']"), eval(f"self.coords['{moves}']['y']"), 40, arcade.color.AMAZON)
                        self.pokemon_list.draw()
                    
                        
            elif move_click:
                #Need to draw path previews to board
                for moves in checked_moves:
                    exec(f"first_turn_check = {in_transit}['location']")
                    #Make space clearing its own function?
                    if x in range(self.coords[moves]['x'] - 40, self.coords[moves]['x'] + 40) and y in range(
                                        self.coords[moves]['y'] - 40, self.coords[moves]['y'] + 40) and eval(
                                        f"game_logic.board.{moves}.occupied") == False:
                        temp1 = eval(f"{in_transit}['control']")
                        print(eval(f"{in_transit}['name']"), f" moved to {moves}.")
                        exec(f"game_logic.board.{in_transit_location}.occupied = False")
                        exec(f"game_logic.board.{in_transit_location}.occupant = ''")
                        exec(f"game_logic.board.{in_transit_location}.occupant_team = 0")
                        exec(f"game_logic.board.{in_transit_location}.controlling_player = 0")
                        exec(f"game_logic.board.{in_transit_location}.passable = True")
                        exec(f"game_logic.board.{moves}.occupied = True")
                        exec(f"game_logic.board.{moves}.occupant = '{in_transit}'[11:]")
                        exec(f"game_logic.board.{moves}.occupant_team = {in_transit}['control']")
                        exec(f"game_logic.board.{moves}.controlling_player = {in_transit}['control']")
                        exec(f"game_logic.board.{moves}.passable = False")
                        exec(f"{in_transit}['location'] = '{moves}'")
                        in_transit_location = eval(f"{in_transit}['location']")
                        for surround_neighbors in self.coords.keys():
                            if len(surround_neighbors) == 2:
                                surround_target = eval(f"game_logic.board.{surround_neighbors}.occupant")
                                if surround_target:
                                    exec(f"game_logic.{surround_target}['is_surrounded'] = game_logic.surround_check(game_logic.{surround_target})")
                        for team in range(1,3):
                            for surround_resolve in eval(f"dir(game_logic.player_{team}_team)"):
                                if surround_resolve.startswith('pokemon'):
                                    temp2 = eval(f"game_logic.player_{team}_team.{surround_resolve}['location']")
                                    if eval(f"game_logic.player_{team}_team.{surround_resolve}['is_surrounded']") == True:
                                        print(f"SURROUNDED\t Player {team}'s ", eval(f"game_logic.player_{team}_team.{surround_resolve}['name']"), f"was sent to Player {team}'s PC.")
                                        exec(f"game_logic.board.{temp2}.occupied = False")
                                        exec(f"game_logic.board.{temp2}.occupant = ''")
                                        exec(f"game_logic.board.{temp2}.occupant_team = 0")
                                        exec(f"game_logic.board.{temp2}.controlling_player = 0")
                                        exec(f"game_logic.board.{temp2}.passable = True")
                                        game_logic.pc_rotate(team)
                                        exec(f"game_logic.player_{team}_team.{surround_resolve}['location'] = 'player_{team}_PC_2'")
                                        exec(f"game_logic.player_{team}_team.{surround_resolve}['is_surrounded'] = False")
                        potential_targets = game_logic.target_finder(f'{in_transit[11:]}')
                        if len(potential_targets) > 0:
                            attack_click = True
                        else:
                            if turn_player == 1:
                                turn_player = 2
                                if game_logic.first_turn:
                                    if len(in_transit_location) == 2:
                                        game_logic.first_turn = False
                            elif turn_player == 2:
                                turn_player = 1
                                if game_logic.first_turn:
                                    if len(in_transit_location) == 2:
                                        game_logic.first_turn = False
                            in_transit = ''
                            in_transit_location = ''

                    elif len(in_transit_location) == 2 and x in range(eval(f"self.coords['{in_transit_location}']['x']") - 40, eval(f"self.coords['{in_transit_location}']['x']") + 40) and y in range(
                                    eval(f"self.coords['{in_transit_location}']['y']") - 40, eval(f"self.coords['{in_transit_location}']['y']") + 40):
                        potential_targets = game_logic.target_finder(f'{in_transit[11:]}')
                        if len(potential_targets) > 0:
                            attack_click = True
                        else:
                            in_transit = ''
                            in_transit_location = ''
                            move_click = False
                        

                move_click = False
                checked_moves = []
                
                self.pokemon_list.update()

            elif attack_click:
                #Need to add logic that manipulates board occuppancy and location properties like move logic above 
                for targets in potential_targets:
                    if x in range(self.coords[targets]['x'] - 40, self.coords[targets]['x'] + 40) and y in range(
                                        self.coords[targets]['y'] - 40, self.coords[targets]['y'] + 40):
                        winner_check = game_logic.battle_spin_compare(f'{in_transit_combatant}', eval(f'game_logic.board.{targets}.occupant'))
                        print(winner_check)
                        if winner_check == 1:
                            temp1 = eval(f"game_logic.board.{targets}.occupant")
                            temp2 = eval(f"game_logic.{temp1}['control']")
                            temp3 = eval(f"{in_transit}['control']")
                            exec(f"game_logic.board.{targets}.occupied = False")
                            exec(f"game_logic.board.{targets}.occupant = ''")
                            exec(f"game_logic.board.{targets}.occupant_team = 0")
                            exec(f"game_logic.board.{targets}.controlling_player = 0")
                            exec(f"game_logic.board.{targets}.passable = True")
                            game_logic.pc_rotate(temp2)
                            exec(f"game_logic.{temp1}['location'] = 'player_{temp2}_PC_2'")
                            print("KO GOOD")
                            evo_complete = game_logic.evolution_check(eval(f"{in_transit}"))
                            if evo_complete:
                                print("GOOD")
                                exec(f"{in_transit}.update(game_logic.pokemon_stats['{evo_complete}'])")
                                new_evo_path = eval(f"{in_transit}['spritefile']")
                                exec(f"self.player_{temp3}_pokemon_{in_transit[-1]} = arcade.Sprite(f'images/Sprites/{new_evo_path}', SPRITE_SCALING)")
                                self.pokemon_list.update()
                        elif winner_check == 2:
                            temp1 = eval(f"{in_transit}['control']")
                            temp2 = eval(f"game_logic.board.{targets}.occupant")
                            temp3 = eval(f"game_logic.{temp2}['control']")
                            exec(f"game_logic.board.{in_transit_location}.occupied = False")
                            exec(f"game_logic.board.{in_transit_location}.occupant = ''")
                            exec(f"game_logic.board.{in_transit_location}.occupant_team = 0")
                            exec(f"game_logic.board.{in_transit_location}.controlling_player = 0")
                            exec(f"game_logic.board.{in_transit_location}.passable = True")
                            game_logic.pc_rotate(temp1)
                            exec(f"{in_transit}['location'] = 'player_{temp1}_PC_2'")
                            evo_complete = game_logic.evolution_check(eval(f"game_logic.board.{targets}.occupant"))
                            if evo_complete:
                                exec(f"game_logic.{temp2}.update(game_logic.pokemon_stats['{evo_complete}'])")
                                new_evo_path = eval(f"game_logic.{temp2}['spritefile']")
                                exec(f"self.player_{temp3}_pokemon_{temp2[-1]} = arcade.Sprite(f'images/Sprites/{new_evo_path}', SPRITE_SCALING)")
                                self.pokemon_list.update()
                        elif winner_check == 3:
                            pass

                if turn_player == 1:
                    turn_player = 2
                elif turn_player == 2:
                    turn_player = 1
                attack_click = False
                in_transit = ''
                in_transit_location = ''
                
                self.pokemon_list.update()
                
            if game_logic.board.A4.controlling_player == 2:
                self.pokemon_list.update()
                self.pokemon_list.draw()
                print("Player 2 wins!")
                input("Press ENTER in this console to quit.")
            elif game_logic.board.E4.controlling_player == 1:
                self.pokemon_list.update()
                self.pokemon_list.draw()
                print("Player 1 wins!")
                input("Press ENTER in this console to quit.")
                arcade.close_window()
            

def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
