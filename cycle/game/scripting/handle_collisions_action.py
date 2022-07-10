import constants
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point
from game.shared.color import Color

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the snake collides
    with the food, or the snake collides with its segments, or the game is over.
    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False
        self._winner_is = 1

    def execute(self, cast, script):
        """Executes the handle collisions action.
        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            # self._handle_food_collision(cast)
            self._handle_bonus_collision(cast)
            self._handle_segment_collision(cast)
            self._handle_game_over(cast)

    def _handle_bonus_collision(self, cast):
        """Updates the score nd moves the food if a snake collides with the food.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        bonus = cast.get_first_actor("bonus")
        snakes = cast.get_actors("snakes")
        
        snake_no = 0
        for snake in snakes:
            snake_no += 1
            head = snake.get_head()

            if head.get_position().equals(bonus.get_position()):
                snake.change_color(Color(snake.get_color().get_red(), snake.get_color().get_green(), snake.get_color().get_blue(), snake.get_color().get_alpha()+50 if snake.get_color().get_alpha() < 246 else 255))
                bonus.activate(cast.get_nth_actor("snakes", 1 if snake_no == 2 else 2))
                bonus.reset()

        
    def _handle_segment_collision(self, cast):
        """Sets the game over flag if the snake collides with one of its segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        snakes = cast.get_actors("snakes")
        total_segments = []
        for snake in snakes:
            total_segments.extend(snake.get_segments()[1:])

        head_locations = []

        for snake in snakes:
            head = snake.get_segments()[0]
            head_location = snake.get_segments()[0]
            head_locations.append(head_location)

        snake_no = 0
        for snake in snakes:
            snake_no += 1
            head = snake.get_segments()[0]
            for segment in total_segments:
                # if a collision has occured
                if head.get_position().equals(segment.get_position()):
                    self.set_winner_is(1 if snake_no == 2 else 2)
                    self._is_game_over = True
  
        # if a head to head collision occurs    
        if head_locations[0].get_position().equals(head_locations[1].get_position()):
            self.set_winner_is(99)
            self._is_game_over = True
            return

    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the snake and food white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            snakes = cast.get_actors("snakes")

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            winner_is = f"Player {self.get_winner_is()} Wins!" if self.get_winner_is() < 3 else "The game is a DRAWER!" 
            message.set_text(f"Game Over! "+ winner_is)
            message.set_position(position)
            cast.add_actor("messages", message)

            for snake in snakes:
                segments = snake.get_segments()
                for segment in segments:
                    segment.set_color(constants.WHITE)

    def get_winner_is(self):
        return self._winner_is

    def set_winner_is(self, winner):
        self._winner_is = winner    