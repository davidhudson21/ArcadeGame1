# CONTROLS
# W - Up
# A - Left
# S - Down
# D - Right
# SPACE_BAR - Shoot

# RESOURCES
# Background - https://freesvg.org/seamless-pattern-with-space-objects
# Airplane - https://www.maxpixel.net/Aeroplane-Jet-Flying-Red-Airplane-Plane-Aircraft-304892
# Laser - https://www.maxpixel.net/The-Device-Light-Radius-The-Beam-Red-Laser-3774964
# Laser Sound - https://www.soundjay.com/gun-sound-effect.html

import arcade
import pathlib
from enum import auto, Enum

class MoveEnum(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class MovingBackgroundSprite(arcade.Sprite):
    def __init__(self, background_path: str, speed:int, game_window):
        super().__init__(background_path)
        self.speed = speed
        self.game = game_window

    def move(self):
        self.center_x += self.speed

        if self.center_x * 2 >= self.game.width + self.width/2:
            self.center_x = self.game.width - self.width/2

class BulletSprite(arcade.Sprite):
    def __init__(self, speed:int, game_window, pos_x, pos_y, background_path = str(pathlib.Path.cwd() / 'Assets' / "Bullet.png")):
        super().__init__(background_path)
        self.speed = speed
        self.game = game_window
        self.center_x = pos_x + self.width
        self.center_y = pos_y


    def move(self):
        self.center_x += self.speed



        if self.game.pict_list != None:
            if self.center_x - self.width/2 > self.game.width:
                if self in self.game.pict_list:
                    self.remove_from_sprite_lists()



class AirplaneSprite(arcade.Sprite):
    def __init__(self, ship_path: str, speed:int, game_window):
        super().__init__(ship_path)
        self.speed = speed
        self.game = game_window


    def move(self, direction:MoveEnum):

        if direction == MoveEnum.UP and not (self.center_y + self.height/2) > self.game.height:
            self.center_y += self.speed
        elif direction == MoveEnum.DOWN and not (self.center_y - self.height/2) < 0:
            self.center_y -= self.speed
        elif direction == MoveEnum.LEFT and not (self.center_x - self.width/2) < 0:
            self.center_x -=self.speed
        elif direction == MoveEnum.RIGHT and not (self.center_x + self.width/2) > self.game.width:
            self.center_x += self.speed
        else: #should be MoveEnum.NONE
            pass


class MimimalArcade(arcade.Window):

    def __init__(self, airplane_image_name:str, background_image_name:str, screen_w:int = 1024, screen_h:int =1024):
        super().__init__(screen_w, screen_h)
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.airplane_image_path = pathlib.Path.cwd() / 'Assets' / airplane_image_name
        self.background_image_path = pathlib.Path.cwd() / 'Assets' / background_image_name
        self.airplane_pict = None
        self.background_pict = None
        self.direction = MoveEnum.NONE
        self.pict_list = None
        self.bullet_list = None

        self.bullet_sound = arcade.Sound(pathlib.Path.cwd() / 'Assets' / "bullet_sound.wav")


    def setup(self):
        self.airplane_pict = AirplaneSprite(str(self.airplane_image_path), speed=3, game_window=self)
        self.airplane_pict.center_x = 300
        self.airplane_pict.center_y = 300

        self.background_pict = MovingBackgroundSprite(str(self.background_image_path), speed=2, game_window=self)
        self.background_pict.center_x = 300
        self.background_pict.center_y = 300


        self.pict_list = arcade.SpriteList()
        self.pict_list.append(self.background_pict)
        self.pict_list.append(self.airplane_pict)

        self.bullet_list = arcade.SpriteList()

    def on_update(self, delta_time: float):
        #to get really smooth movement we would use the delta time to
        #adjust the movement, but for this simple version I'll forgo that.
        self.airplane_pict.move(self.direction)
        self.background_pict.move()

        for bullet in self.bullet_list:
            bullet.move()

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Code to draw the screen goes here
        self.pict_list.draw()
        self.bullet_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.direction = MoveEnum.UP
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.direction = MoveEnum.DOWN
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.direction = MoveEnum.LEFT
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.direction = MoveEnum.RIGHT
        elif key == arcade.key.SPACE:
            self.bullet_sound.play()
            new_bullet = BulletSprite(speed=25, game_window=self, pos_x=self.pict_list[1].center_x, pos_y=self.pict_list[1].center_y)
            self.bullet_list.append(new_bullet)


    def on_key_release(self, key: int, modifiers: int):
        """called by arcade for keyup events"""
        if (key == arcade.key.UP or key == arcade.key.W) and \
                self.direction == MoveEnum.UP:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.DOWN or key == arcade.key.S) and\
                self.direction == MoveEnum.DOWN:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.LEFT or key == arcade.key.A) and \
                self.direction == MoveEnum.LEFT:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.RIGHT or key == arcade.key.D) and \
                self.direction == MoveEnum.RIGHT:
            self.direction = MoveEnum.NONE



def main():
    """ Main method """
    window = MimimalArcade(airplane_image_name="Airplane.png", background_image_name="RepeatingBackground.png", screen_w=600, screen_h=600)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()