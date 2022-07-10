from game.casting.actor import Actor
from game.shared.point import Point
from game.shared.color import Color
from random import randint
import constants

class Bonus(Actor):
    def __init__(self):
        super().__init__()
       
        self._points = 0
        self.set_text("*")
        self.set_color(Color(255,255,255))
        self.reset()

    def activate(self, actor):
        # activates the powers of the bonus on the other player in the game
        # Arguments:
        # accepts the actor taht needs to have their color changed
        
        # get the players current color
        current_color = actor.get_color()

        #set transparency lower than the current value
        alpha_value = randint(1, current_color.get_alpha())
        
        #assign new value to the alternate player
        actor.change_color(Color(current_color.get_red(), current_color.get_green(), current_color.get_blue(), alpha_value))

    def reset(self):
        """Selects a random position for the bonus item."""
        self._points = randint(1, 8)
        x = randint(1, constants.COLUMNS - 1)
        y = randint(1, constants.ROWS - 1)
        position = Point(x, y)
        position = position.scale(constants.CELL_SIZE)
        self.set_position(position)