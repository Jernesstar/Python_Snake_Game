from enum import Enum

import pygame
from pygame import (
    K_LEFT, K_RIGHT, K_UP, K_DOWN, 
    K_a, K_d, K_w, K_s
)


class Apple(pygame.sprite.Sprite):

    def __init__(self, size) -> None:
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("resources\\apple.gif").convert()
        self.image = pygame.transform.scale(image, (size, size))


class Snake:

    class Controls(Enum):
        KEYS = 1
        WASD = 2

    score, size, length = 0, 10, 1
    head_x, head_y = 250, 250

    def __init__(self, game, name: str, controls=Controls.KEYS):
        self.name = name.strip()
        self.display_width = game.width
        self.display_height = game.height
        self.controls = controls
        self.size = game.square_size
        self.pixels = []

    def reset(self):
        self.pixels, self.score, self.length = [], 0, 1

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

    def check_for_food_eaten(self, food_coordinates):
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
            
    def move(self, delta_x, delta_y):
        self.head_x += delta_x
        self.head_y += delta_y
        self.pixels.append((self.head_x, self.head_y))
        if len(self.pixels) > self.length:
            self.pixels.pop(0)

    def directions(self, event, delta_x, delta_y):
        if self.controls == Snake.Controls.KEYS:
            return self.get_directions_keys(event, delta_x, delta_y)
        elif self.controls == Snake.Controls.WASD:
            return self.get_directions_wasd(event, delta_x, delta_y)
   
    def get_directions_keys(self, event, delta_x, delta_y):
        """
        Return directions for snake depending on directional key presses. 
        
        Also makes sure the player can not go directly
        opposite of the direction they are currently going.
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

        current_delta_x = self.pixels[-1][0] - self.pixels[-2][0]
        current_delta_y = self.pixels[-1][1] - self.pixels[-2][1]

        if event.key in (K_LEFT, K_RIGHT):
            """Snake is moving up or down"""
            if current_delta_x == 0:
                delta_x = -self.size if event.key == K_LEFT else self.size
                delta_y = 0
        elif event.key in (K_UP, K_DOWN):
            """Snake is going left or right"""
            if current_delta_y == 0:
                delta_x = 0
                delta_y = -self.size if event.key == K_UP else self.size
        return (delta_x, delta_y)
        
    def get_directions_wasd(self, event: pygame.event, delta_x, delta_y):
        """
        Return directions for snake depending on WASD key presses. 
        
        See docstring for `get_directions_keys`
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

        current_delta_x = self.pixels[-1][0] - self.pixels[-2][0]
        current_delta_y = self.pixels[-1][1] - self.pixels[-2][1]

        if event.key in (K_a, K_d):
            """Snake is going up or down"""
            if current_delta_x == 0:
                delta_x = -self.size if event.key == K_a else self.size
                delta_y = 0
        elif event.key in (K_w, K_s):
            """Snake is going left or right"""
            if current_delta_y == 0:
                delta_x = 0
                delta_y = -self.size if event.key == K_w else self.size
                """Snake is going down"""
        return (delta_x, delta_y)