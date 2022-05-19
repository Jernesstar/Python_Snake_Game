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

    def check_for_game_over(self):
        if (self.head_x, self.head_y) in self.pixels[:-1]:
            return True 
        return False

    def when_eat_food(self, food_coordinates):
        if isinstance(food_coordinates, list):
            for i, food_x_y in enumerate(food_coordinates):
                if (self.head_x, self.head_y) == food_x_y:
                    self.score += 1
                    self.length += 1
                    return i
            return -1
        elif isinstance(food_coordinates, tuple):
            if (self.head_x, self.head_y) == food_coordinates:
                self.score += 1
                self.length += 1
                return True
            return False
            
    def move(self, delta_x, delta_y, food_coordinates):
        self.head_x += delta_x
        self.head_y += delta_y
        game_over = self.check_for_game_over()
        food_eaten = self.when_eat_food(food_coordinates)
        self.pixels.append((self.head_x, self.head_y))

        if len(self.pixels) > self.length:
            self.pixels.pop(0)
        return (food_eaten, game_over)

    def directions(self, event, delta_x, delta_y):
        if self.controls == Control.KEYS:
            return self.get_directions_keys(event, delta_x, delta_y)
        elif self.controls == Control.WASD:
            return self.get_directions_wasd(event, delta_x, delta_y)
   
    def get_directions_keys(self, event, delta_x, delta_y):
        """
        Return directions to go depending on directional key presses. 
        
        Also makes sure the player can not go directly
        opposite of the direction they are currently going.

        The following if-statement checks that the snake is longer than one
        pixel:
        >>> if len(self.pixels) == 1

        so as this will prevent an `IndexError`

        The following line checks if the snake is currently going left
        >>> self.pixels[-2][0] - self.pixels[-1][0] < 0

        since the current snake head position always will correspond to:
        `self.pixels[-1]`

        as it will always be the last positions to be appended to
        `self.pixels`
        """
        if len(self.pixels) == 1:
            if event.key in (K_LEFT, K_RIGHT):
                delta_x = -self.size if event.key == K_LEFT else self.size
                delta_y = 0
            elif event.key in (K_UP, K_DOWN):
                delta_x = 0
                delta_y = -self.size if event.key == K_UP else self.size
            return (delta_x, delta_y)

        if event.key in (K_LEFT, K_RIGHT):
            """Snake is going left"""
            if (self.pixels[-1][0] - self.pixels[-2][0]) < 0:
                delta_x = -self.size
                delta_y = 0
                """
                Snake is currently moving up, so turning either 
                direction is fine 
                """
            elif (self.pixels[-1][0] - self.pixels[-2][0]) == 0:
                delta_x = -self.size if event.key == K_LEFT else self.size
                delta_y = 0
                """Snake is going right"""
            elif (self.pixels[-1][0] - self.pixels[-2][0]) > 0:
                delta_x = self.size
                delta_y = 0

        elif event.key in (K_UP, K_DOWN):
            if (self.pixels[-1][1] - self.pixels[-2][1]) < 0:
                delta_x = 0
                delta_y = -self.size
            elif (self.pixels[-1][1] - self.pixels[-2][1]) == 0:
                delta_x = 0
                delta_y = -self.size if event.key == K_UP else self.size
            elif (self.pixels[-1][1] - self.pixels[-2][1]) > 0:
                delta_x = 0
                delta_y = self.size
        return (delta_x, delta_y)
        
    def get_directions_wasd(self, event: pygame.event, delta_x, delta_y):
        
        if len(self.pixels) == 0:
            return
        if len(self.pixels) == 1:
            if event.key in (K_a, K_d):
                delta_x = -self.size if event.key == K_a else self.size
                delta_y = 0
            elif event.key in (K_w, K_s):
                delta_x = 0
                delta_y = -self.size if event.key == K_w else self.size
            return (delta_x, delta_y)

        if event.key in (K_a, K_d):
            """Snake is going left"""
            if (self.pixels[-1][0] - self.pixels[-2][0]) < 0:
                delta_x = -self.size
                delta_y = 0
            elif (self.pixels[-1][0] - self.pixels[-2][0]) == 0:
                delta_x = -self.size if event.key == K_a else self.size
                delta_y = 0
            elif (self.pixels[-1][0] - self.pixels[-2][0]) > 0:
                delta_x = self.size
                delta_y = 0

        elif event.key in (K_w, K_s):
            if (self.pixels[-1][1] - self.pixels[-2][1]) < 0:
                delta_x = 0
                delta_y = -self.size
            elif (self.pixels[-1][1] - self.pixels[-2][1]) == 0:
                delta_x = 0
                delta_y = -self.size if event.key == K_w else self.size
            elif (self.pixels[-1][1] - self.pixels[-2][1]) > 0:
                delta_x = 0
                delta_y = self.size
        return (delta_x, delta_y)