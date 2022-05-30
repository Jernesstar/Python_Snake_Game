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
    
    images = []
    size = 50

    def __init__(self, size, pos: tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        path = Path(os.path.split(__file__)[0]) / "resources"
        images = [
            pygame.image.load(path / "block_left_up.png").convert(),
            pygame.image.load(path / "block_right_up.png").convert(),
            pygame.image.load(path / "block_straight.png").convert(),
            pygame.image.load(path / "block_up_left.png").convert(),
            pygame.image.load(path / "block_up_right.png").convert()
        ]
        self.images = [
            pygame.transform.scale(im, (size, size)) for im in images
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
            (RIGHT, RIGHT): pygame.transform.rotate(self.images[2], 90),
        }
        self.image = self.images[2]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, new_image: pygame.Surface):
        self.image = new_image
    
        
class Snake(pygame.sprite.Sprite):

    class Controls(Enum):
        KEYS = 1
        WASD = 2

    score, size, length = 0, 10, 3
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
        self.pixels: list[Block] = []
        path = Path(os.path.split(__file__)[0]) / "resources"
        self._eye = pygame.image.load(path / "snake_eye_open.png").convert()
        self._eye = pygame.transform.scale(
            self._eye, (self.size / 4, self.size / 4)
        )
        self.eye = self._eye

    def reset(self):
        self.pixels = []
        self.score = 0
        self.length = 3

    def update(self):
        np.seterr(invalid='ignore')
        # Vector for x y position of block of the head of the snake
        head_vector = np.array(self.pixels[-1].rect.topleft, dtype=float)
        # Vector for x y position of block behind the head
        vector_behind_1 = np.array(self.pixels[-2].rect.topleft, dtype=float)
        # Vector for x y position of block two places behind the head
        vector_behind_2 = np.array(self.pixels[-3].rect.topleft, dtype=float)

        vector_1: np.ndarray = vector_behind_1 - vector_behind_2
        vector_2: np.ndarray = head_vector - vector_behind_1

        vector_1 /= vector_1
        vector_2 /= vector_2

        vector_1 = np.nan_to_num(vector_1, nan=0)
        vector_2 = np.nan_to_num(vector_2, nan=0)
        x_y_1 = (int(vector_1[0]), int(vector_1[1]))
        x_y_2 = (int(vector_2[0]), int(vector_2[1]))

        # block = Block(1, (1, 1))
        # running_image = block.movement_to_image[(x_y_1, x_y_2)]
        # for i in reversed(range(len(self.pixels) - 1)): # Avoids head
        #     pass#self.pixels[i].update(block.movement_to_image[(x_y_1, x_y_2)])
        #     # temp_image = self.pixels[i].image
        #     # self.pixels[i].image = running_image
        #     # running_image = temp_image
        # self.pixels[-1].update(block.movement_to_image[(x_y_1, x_y_2)])
        self.eye = pygame.transform.rotate(self._eye, -90 * x_y_2[0])
        if x_y_2 == DOWN:
            self.eye = pygame.transform.rotate(self.eye, 180)
            
    def check_for_game_over(self, game_over):
        if (self.head_x, self.head_y) in (
            block.rect.topleft for block in self.pixels[:-1]):
            return True
        if self.check_for_out_of_bounds(game_over):
            return True
        return False

    def check_for_out_of_bounds(self, game_over):
        if game_over:
            return True
        if self.head_x >= self.display_width or self.head_x <= -self.size:
            return True
        elif self.head_y >= self.display_height or self.head_y <= -self.size:
            return True
        return False
            
    def move(self, delta_x, delta_y):
        if (delta_x, delta_y) == (0, 0):
            return
        self.head_x += delta_x
        self.head_y += delta_y
        self.rect.topleft = (self.head_x, self.head_y)
        new_block = Block(self.size, self.rect.topleft)
        self.pixels.append(new_block)
        if len(self.pixels) > self.length:
            self.pixels.pop(0)
        self.update()

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

        current_delta_x = (
            self.pixels[-1].rect.left - self.pixels[-2].rect.left
        )
        current_delta_y = (
            self.pixels[-1].rect.top - self.pixels[-2].rect.top
        )
        if len(self.pixels) == self.length and (delta_x, delta_y) == (0, 0):
            if event.key in (K_LEFT, K_RIGHT):
                if current_delta_x == self.size:
                    delta_x = self.size if event.key == K_RIGHT else 0
                    delta_y = 0
                if current_delta_x == -self.size:
                    delta_x = self.size if event.key == K_LEFT else 0
                    delta_y = 0
            elif event.key in (K_UP, K_DOWN):
                if current_delta_y == 0:
                    delta_x = 0
                    delta_y = -self.size if event.key == K_UP else self.size
        elif event.key in (K_LEFT, K_RIGHT):
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
        current_delta_x = (
            self.pixels[-1].rect.left - self.pixels[-2].rect.left
        )
        current_delta_y = (
            self.pixels[-1].rect.top - self.pixels[-2].rect.top
        )
        if len(self.pixels) == self.length and (delta_x, delta_y) == (0, 0):
            if current_delta_x == self.size:
                delta_x = self.size if event.key == K_d else 0
            if current_delta_x == -self.size:
                delta_x = self.size if event.key == K_a else 0
            delta_y = -self.size if event.key == K_w else self.size
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