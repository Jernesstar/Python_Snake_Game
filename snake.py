from enum import Enum

from pygame import (
    K_LEFT, K_RIGHT, K_UP, K_DOWN, K_a, K_d, K_w, K_s
)
import pygame

class Control(Enum):
    KEYS = 1
    WASD = 2

class Snake:

    score = 0
    size = 10
    speed = 10
    length = 1

    head_x = 250
    head_y = 250

    def __init__(self, game, name, controls=Control.KEYS):
        self.name = name.strip()
        self.display_width = game.width
        self.display_height = game.height
        self.controls = controls
        self.pixels = []

    def reset(self):
        self.pixels = []
        self.score = 0
        self.length = 1

    def check_for_game_over(self, game_over):
        if (self.head_x, self.head_y) in self.pixels[:-1]:
            return True
        if self.check_for_out_of_bounds(game_over):
            return True
        return False

    def check_for_out_of_bounds(self, game_over):
        if game_over:
            return True
        if self.head_x >= self.display_width:
            return True
        elif self.head_x <= -self.size:
            return True
        elif self.head_y >= self.display_height:
            return True
        elif self.head_y <= -self.size:
            return True
        return False

    def when_eat_food(self, food_coordinates):
        if isinstance(food_coordinates, tuple):
            if (self.head_x, self.head_y) == food_coordinates:
                self.score += 1
                self.length += 1
                return True
            return False
        elif isinstance(food_coordinates, list):
            for i, food_x_y in enumerate(food_coordinates):
                if (self.head_x, self.head_y) == food_x_y:
                    self.score += 1
                    self.length += 1
                    return i
            return -1
            
    def move(self, delta_x, delta_y, food_coordinates):
        self.head_x += delta_x
        self.head_y += delta_y
        self.pixels.append((self.head_x, self.head_y))
        if len(self.pixels) > self.length:
            self.pixels.pop(0)
        return self.when_eat_food(food_coordinates) 

    def directions(self, event, delta_x, delta_y):
        if self.controls == Control.KEYS:
            return self.get_directions_keys(event, delta_x, delta_y)
        elif self.controls == Control.WASD:
            return self.get_directions_wasd(event, delta_x, delta_y)
   
    def get_directions_keys(self, event, delta_x, delta_y):
        """
        Return directions for snake depending on directional key presses. 
        
        Also makes sure the player can not go directly
        opposite of the direction they are currently going.

        The following if-statement checks that the snake is longer than one
        pixel:
        >>> if len(self.pixels) == 1

        so as this will prevent an `IndexError`

        The following is the current velocity of the snake
        >>> current_delta_x = self.pixels[-2][0] - self.pixels[-1][0]
        
        This line checks if the snake is currently going left
        >>> current_delta_x < 0

        since the current snake head position always will correspond to:
        `self.pixels[-1]`

        as it will always be the last positions to be appended to
        `self.pixels`
        """
        if self.pixels == []:
            return (0, 0)
        if len(self.pixels) == 1:
            if event.key in (K_LEFT, K_RIGHT):
                delta_x = -self.size if event.key == K_LEFT else self.size
                delta_y = 0
            elif event.key in (K_UP, K_DOWN):
                delta_x = 0
                delta_y = -self.size if event.key == K_UP else self.size
            return (delta_x, delta_y)
        if event.key in (K_LEFT, K_RIGHT):
            current_delta_x = self.pixels[-1][0] - self.pixels[-2][0]
            """Snake is moving up or down"""
            if current_delta_x == 0:
                delta_x = -self.size if event.key == K_LEFT else self.size
                delta_y = 0
        elif event.key in (K_UP, K_DOWN):
            current_delta_y = self.pixels[-1][1] - self.pixels[-2][1]
            """Snake is going left or right"""
            if current_delta_y == 0:
                delta_x = 0
                delta_y = -self.size if event.key == K_UP else self.size
        return (delta_x, delta_y)
        
    def get_directions_wasd(self, event: pygame.event, delta_x, delta_y):
        """
        Return directions for snake depending on WASD key presses. 
        
        Also makes sure the player can not go directly
        opposite of the direction they are currently going.

        The following if-statement checks that the snake is longer than one
        pixel:
        >>> if len(self.pixels) == 1

        so as this will prevent an `IndexError`

        The following is the current velocity of the snake
        >>> current_delta_x = self.pixels[-2][0] - self.pixels[-1][0]

        This line checks if the snake is currently going left
        >>> current_delta_x < 0

        since the current snake head position always will correspond to:
        `self.pixels[-1]`

        as it will always be the last positions to be appended to
        `self.pixels`
        """
        if self.pixels == []:
            return (0, 0) 
        if len(self.pixels) == 1:
            if event.key in (K_a, K_d):
                delta_x = -self.size if event.key == K_a else self.size
                delta_y = 0
            elif event.key in (K_w, K_s):
                delta_x = 0
                delta_y = -self.size if event.key == K_w else self.size
            return (delta_x, delta_y)
        if event.key in (K_a, K_d):
            current_delta_x = self.pixels[-1][0] - self.pixels[-2][0]
            """Snake is going up or down"""
            if current_delta_x == 0:
                delta_x = -self.size if event.key == K_a else self.size
                delta_y = 0
        elif event.key in (K_w, K_s):
            current_delta_y = self.pixels[-1][1] - self.pixels[-2][1]
            """Snake is going left or right"""
            if current_delta_y == 0:
                delta_x = 0
                delta_y = -self.size if event.key == K_w else self.size
                """Snake is going down"""
        return (delta_x, delta_y)