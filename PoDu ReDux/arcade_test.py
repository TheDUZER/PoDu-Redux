"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade, sys, os, game_logic

SPRITE_SCALING = 1.5

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
SCREEN_TITLE = "PoDu ReDux v0.0.4"


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        #arcade.set_background_color(arcade.color.BLACK)
        self.background = None
        self.ClassicBoard = None
        self.TvTBoard = None
        self.pokemon_list = None
        self.A1 = None
        self.A2 = None
        self.A3 = None
        self.A4 = None
        self.A5 = None
        self.A6 = None
        self.A7 = None
        self.B1 = None
        self.B2 = None
        self.B4 = None
        self.B6 = None
        self.B7 = None
        self.C1 = None
        self.C2 = None
        self.C6 = None
        self.C7 = None
        self.D1 = None
        self.D2 = None
        self.D4 = None
        self.D6 = None
        self.D7 = None
        self.E1 = None
        self.E2 = None
        self.E3 = None
        self.E4 = None
        self.E5 = None
        self.E6 = None
        self.E7 = None
        self.player_1_bench_1 = None
        self.player_1_bench_2 = None
        self.player_1_bench_3 = None
        self.player_1_bench_4 = None
        self.player_1_bench_5 = None
        self.player_1_bench_6 = None
        self.player_2_bench_1 = None
        self.player_2_bench_2 = None
        self.player_2_bench_3 = None
        self.player_2_bench_4 = None
        self.player_2_bench_5 = None
        self.player_2_bench_6 = None
        self.player_1_eliminated_1 = None
        self.player_1_eliminated_2 = None
        self.player_1_eliminated_3 = None
        self.player_1_eliminated_4 = None
        self.player_1_eliminated_5 = None
        self.player_1_eliminated_6 = None
        self.player_2_eliminated_1 = None
        self.player_2_eliminated_2 = None
        self.player_2_eliminated_3 = None
        self.player_2_eliminated_4 = None
        self.player_2_eliminated_5 = None
        self.player_2_eliminated_6 = None
        self.player_1_ultra_space_1 = None
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

    def setup(self):
        # Create your sprites and sprite lists here
        self.pokemon_list = arcade.SpriteList()
        self.player_1_pokemon_1 = arcade.Sprite(f"images/Sprites/{game_logic.player_1_team.pokemon1['spritefile']}", SPRITE_SCALING)
        self.player_1_pokemon_2 = arcade.Sprite(f"images/Sprites/{game_logic.player_1_team.pokemon2['spritefile']}", SPRITE_SCALING)
        self.player_1_pokemon_3 = arcade.Sprite(f"images/Sprites/{game_logic.player_1_team.pokemon3['spritefile']}", SPRITE_SCALING)
        self.player_1_pokemon_4 = arcade.Sprite(f"images/Sprites/{game_logic.player_1_team.pokemon4['spritefile']}", SPRITE_SCALING)
        self.player_1_pokemon_5 = arcade.Sprite(f"images/Sprites/{game_logic.player_1_team.pokemon5['spritefile']}", SPRITE_SCALING)
        self.player_1_pokemon_6 = arcade.Sprite(f"images/Sprites/{game_logic.player_1_team.pokemon6['spritefile']}", SPRITE_SCALING)
        self.player_2_pokemon_1 = arcade.Sprite(f"images/Sprites/{game_logic.player_2_team.pokemon1['spritefile']}", SPRITE_SCALING)
        self.player_2_pokemon_2 = arcade.Sprite(f"images/Sprites/{game_logic.player_2_team.pokemon2['spritefile']}", SPRITE_SCALING)
        self.player_2_pokemon_3 = arcade.Sprite(f"images/Sprites/{game_logic.player_2_team.pokemon3['spritefile']}", SPRITE_SCALING)
        self.player_2_pokemon_4 = arcade.Sprite(f"images/Sprites/{game_logic.player_2_team.pokemon4['spritefile']}", SPRITE_SCALING)
        self.player_2_pokemon_5 = arcade.Sprite(f"images/Sprites/{game_logic.player_2_team.pokemon5['spritefile']}", SPRITE_SCALING)
        self.player_2_pokemon_6 = arcade.Sprite(f"images/Sprites/{game_logic.player_2_team.pokemon6['spritefile']}", SPRITE_SCALING)
        
        try:
            for background_textures in os.listdir(os.path.join(sys.path[0] + "\\images\\board\\backgrounds\\")):
                print(background_textures[len(sys.path[0] + "\\images\\board\\backgrounds\\")*(-1):-4])
        except:
            pass
        background_select = input("Select background image.")
        self.background = arcade.load_texture(f"images/board/backgrounds/{background_select}.png")
        self.ClassicBoard = arcade.load_texture("images/board/overlays/dueloverlay.png")
        self.player_1_pokemon_1.center_x = 311
        self.player_1_pokemon_1.center_y = 183
        self.player_1_pokemon_2.center_x = 411
        self.player_1_pokemon_2.center_y = 183
        self.player_1_pokemon_3.center_x = 511
        self.player_1_pokemon_3.center_y = 183
        self.player_1_pokemon_4.center_x = 360
        self.player_1_pokemon_4.center_y = 110
        self.player_1_pokemon_5.center_x = 460
        self.player_1_pokemon_5.center_y = 110
        self.player_1_pokemon_6.center_x = 560
        self.player_1_pokemon_6.center_y = 110
        self.player_2_pokemon_1.center_x = 715
        self.player_2_pokemon_1.center_y = 845
        self.player_2_pokemon_2.center_x = 615
        self.player_2_pokemon_2.center_y = 845
        self.player_2_pokemon_3.center_x = 515
        self.player_2_pokemon_3.center_y = 845
        self.player_2_pokemon_4.center_x = 661
        self.player_2_pokemon_4.center_y = 921
        self.player_2_pokemon_5.center_x = 561
        self.player_2_pokemon_5.center_y = 921
        self.player_2_pokemon_6.center_x = 461
        self.player_2_pokemon_6.center_y = 921
        
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
                                  30, arcade.color.AZURE)
        arcade.draw_circle_filled(self.player_1_pokemon_2.center_x, self.player_1_pokemon_2.center_y,
                                  30, arcade.color.AZURE)
        arcade.draw_circle_filled(self.player_1_pokemon_3.center_x, self.player_1_pokemon_3.center_y,
                                  30, arcade.color.AZURE)
        arcade.draw_circle_filled(self.player_1_pokemon_4.center_x, self.player_1_pokemon_4.center_y,
                                  30, arcade.color.AZURE)
        arcade.draw_circle_filled(self.player_1_pokemon_5.center_x, self.player_1_pokemon_5.center_y,
                                  30, arcade.color.AZURE)
        arcade.draw_circle_filled(self.player_1_pokemon_6.center_x, self.player_1_pokemon_6.center_y,
                                  30, arcade.color.AZURE)
        arcade.draw_circle_filled(self.player_2_pokemon_1.center_x, self.player_2_pokemon_1.center_y,
                                  30, arcade.color.RASPBERRY)
        arcade.draw_circle_filled(self.player_2_pokemon_2.center_x, self.player_2_pokemon_2.center_y,
                                  30, arcade.color.RASPBERRY)
        arcade.draw_circle_filled(self.player_2_pokemon_3.center_x, self.player_2_pokemon_3.center_y,
                                  30, arcade.color.RASPBERRY)
        arcade.draw_circle_filled(self.player_2_pokemon_4.center_x, self.player_2_pokemon_4.center_y,
                                  30, arcade.color.RASPBERRY)
        arcade.draw_circle_filled(self.player_2_pokemon_5.center_x, self.player_2_pokemon_5.center_y,
                                  30, arcade.color.RASPBERRY)
        arcade.draw_circle_filled(self.player_2_pokemon_6.center_x, self.player_2_pokemon_6.center_y,
                                  30, arcade.color.RASPBERRY)
        
        self.pokemon_list.draw()

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.pokemon_list.draw()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        print(x,y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player_1_pokemon_1.center_x = 292
            self.player_1_pokemon_1.center_y = 295
            self.pokemon_list.update()
        pass
    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
