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
            pygame.image.load(path / "block_left_up.png").convert_alpha(),
            pygame.image.load(path / "block_right_up.png").convert_alpha(),
            pygame.image.load(path / "block_straight.png").convert_alpha(),
            pygame.image.load(path / "block_up_left.png").convert_alpha(),
            pygame.image.load(path / "block_up_right.png").convert_alpha()
        ]
        self.images = [
            pygame.transform.scale(image, (size, size)) for image in images
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
    
        
class Snake(pygame.sprite.Sprite):

    class Controls(Enum):
        KEYS = 1
        WASD = 2

    score, size, length = 0, 10, 3
    head_x, head_y = 250, 250
    name = ""

    def __init__(self, game, controls=Controls.KEYS):
        pygame.sprite.Sprite.__init__(self)
        self.size = game.square_size
        size = self.size
        pos, width_height = (self.head_x, self.head_y), (size, size)
        self.rect = pygame.rect.Rect(pos, width_height)
        self.display_width = game.width
        self.display_height = game.height
        self.controls = controls
        self.pixels: list[Block] = []
        path = Path(os.path.split(__file__)[0]) / "resources"
        self._eye = pygame.image.load(path / "snake_eye_open.png").convert_alpha()
        self._eye = pygame.transform.scale(self._eye, (size / 2.5, size / 2.5))
        self.eye = self._eye
        self.eye_rect_1 = self.eye.get_rect()
        self.eye_rect_2 = self.eye.get_rect()
        self.eye_rect_1.topleft = self.rect.topleft
        self.eye_rect_2.topleft = self.rect.topleft

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

        vector_1 /= abs(vector_1) * -1
        vector_2 /= abs(vector_2) * -1
        vector_1 *= -1
        vector_2 *= -1

        vector_1 = np.nan_to_num(vector_1, nan=0)
        vector_2 = np.nan_to_num(vector_2, nan=0)

        x_y_1 = (int(vector_1[0]), int(vector_1[1]))
        x_y_2 = (int(vector_2[0]), int(vector_2[1]))

        # block = Block(1, (1, 1))
        # running_image = block.movement_to_image[(x_y_1, x_y_2)]
        # for i in reversed(range(len(self.pixels) - 1)): # Avoids head
        #     temp_image = self.pixels[i].image
        #     self.pixels[i].image = running_image
        #     running_image = temp_image
        # self.pixels[-1].image = block.movement_to_image[(x_y_1, x_y_1)]

        # Rotate snake eye according to the current velocity
        self.eye = pygame.transform.rotate(self._eye, -90 * x_y_2[0])
        self.eye = pygame.transform.rotate(self._eye, 90 * (x_y_2[1] + 1))

        if x_y_2 == LEFT:
            self.eye_rect_1.topleft = self.rect.topleft
            self.eye_rect_2.bottomleft = self.rect.bottomleft
        if x_y_2 == RIGHT:
            self.eye_rect_1.topright = self.rect.topright
            self.eye_rect_2.bottomright = self.rect.bottomright
        if x_y_2 == UP:
            self.eye_rect_1.topleft = self.rect.topleft
            self.eye_rect_2.topright = self.rect.topright
        if x_y_2 == DOWN:
            self.eye_rect_1.bottomleft = self.rect.bottomleft
            self.eye_rect_2.bottomright = self.rect.bottomright
        
    def check_for_game_over(self, game_over):
        if (self.rect.topleft) in (
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
            self.update()
            return
        self.head_x += delta_x
        self.head_y += delta_y
        self.rect.move_ip(delta_x, delta_y)
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