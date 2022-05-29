from enum import Enum
import os
from pathlib import Path

import numpy as np

import pygame
from pygame import (
    K_LEFT, K_RIGHT, K_UP, K_DOWN, 
    K_a, K_d, K_w, K_s
)


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Apple(pygame.sprite.Sprite):

    containers: pygame.sprite.Group

    def __init__(self, size, position: tuple[int, int]):
        pygame.sprite.Sprite.__init__(self, self.containers)
        image = pygame.image.load("resources\\apple.gif").convert()
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
    

class Block(pygame.sprite.Sprite):
    
    containers: pygame.sprite.RenderUpdates()
    images = []
    size = 50

    def __init__(self, size, pos: tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        path = Path(os.path.split(__file__)[0]) / "resources"
        self.images = [
            pygame.image.load(path / "block_left_up.png").convert(),
            pygame.image.load(path / "block_right_up.png").convert(),
            pygame.image.load(path / "block_straight.png").convert(),
            pygame.image.load(path / "block_up_left.png").convert(),
            pygame.image.load(path / "block_up_right.png").convert()
        ]
        self.images = [
            pygame.transform.scale(im, (size, size)) for im in self.images
        ]
        self.movement_to_image = {
            (LEFT, UP): self.images[3],
            (RIGHT, UP): self.images[4],
            (LEFT, DOWN): pygame.transform.rotate(self.images[3], -90),
            (RIGHT, DOWN): pygame.transform.rotate(self.images[4], 90),
            (UP, LEFT): self.images[0],
            (UP, RIGHT): self.images[1],
            (DOWN, LEFT): self.images[3],
            (DOWN, RIGHT): self.images[4],
            (UP, UP): self.images[2],
            (DOWN, DOWN): self.images[2],
            (LEFT, LEFT): pygame.transform.rotate(self.images[2], 90),
            (RIGHT, RIGHT): pygame.transform.rotate(self.images[2], 90)
        }
        self.image = self.images[2]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.update()
    
        
class Snake(pygame.sprite.Sprite):

    class Controls(Enum):
        KEYS = 1
        WASD = 2

    score, size, length = 0, 10, 1
    head_x, head_y = 250, 250

    def __init__(self, game, name: str, controls=Controls.KEYS):
        pygame.sprite.Sprite.__init__(self)
        pos, rect = (self.head_x, self.head_y), (self.size, self.size)
        self.rect = pygame.rect.Rect(pos, rect)
        self.name = name.strip()
        self.display_width = game.width
        self.display_height = game.height
        self.controls = controls
        self.size = game.square_size
        self.pixels = []
        self.block = Block(50, (44, 44))

    def reset(self):
        self.pixels = []
        self.score = 0
        self.length = 1

    def update(self):
        for i in range(len(self.pixels) - 1):
            current_vector = np.array(self.pixels[i].rect, dtype=int)
            vector_ahead = np.array(self.pixels[i + 1].rect, dtype=int)
            vector_behind = np.array(self.pixels[i - 1].rect, dtype=int)

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
            
    def move(self, delta_x, delta_y):
        self.head_x += delta_x
        self.head_y += delta_y
        self.rect.topleft = (self.head_x, self.head_y)
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