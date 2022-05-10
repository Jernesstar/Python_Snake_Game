import pygame
from pygame import (
    KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_a, K_d, K_s, K_w
)

class Snake:

    score = 0
    size = 10
    speed = 15
    length = 20
    head_x = 0
    head_y = 0
    name: str = ""
    pixels: list[tuple] = []

    def __init__(
        self, name: str, 
        display_width, 
        display_height, 
        controls="KEYS"
    ):
        self.name = name.strip()
        self.display_width = display_width
        self.display_height = display_height
        self.controls = controls

    def check_for_game_over(self):
        if (self.head_x, self.head_y) in self.pixels[:-1]:
            return True 
        return False

    def when_eat_food(self, target_x, target_y):
        if (self.head_x, self.head_y) == (target_x, target_y):
            self.score += 1
            self.length += 1

    def check_out_of_bounds(self, x, y):
        if x == self.display_width + 10:
            x = 10
        elif x == 0:
            x = self.display_width - 10   
        elif y == self.display_height:
            y = 10
        elif y == 0:
            y = self.display_height - 10
        return (x, y)

    def change_directions(self, delta_x, delta_y):
        self.head_x += delta_x
        self.head_y += delta_y

    def move_snake(self):
        pass

    def get_directions(self, event: pygame.event) -> tuple[int, int]:
        """
        Return directions to go depending on directional key presses. 
        
        Also makes sure the player can not go directly
        opposite of the direction they are currently going.

        The following if-statement checks that the snake is longer than one
        pixel:
        >>> if len(self.pixels) == 1

        so as this will prevent an IndexError

        The following line checks if the snake is currently going left
        >>> self.pixels[-2][0] - self.pixels[-1][0] < 0

        since the current snake head position always will correspond to:
        `self.pixels[-1]`

        as it will always be the last positions to be appended to
        `self.pixels`
        """
        delta_x, delta_y = 0, 0

        if len(self.pixels) == 1:
            if event.key in (K_LEFT, K_RIGHT):
                delta_x = -10 if event.key == K_LEFT else 10
                delta_y = 0
            elif event.key in (K_UP, K_DOWN):
                delta_x = 0
                delta_y = -10 if event.key == K_UP else 10
            return (delta_x, delta_y)

        if event.key in (K_LEFT, K_RIGHT, K_a, K_d):
            """Snake is going left"""
            if (self.pixels[-1][0] - self.pixels[-2][0]) < 0:
                delta_x = -10
                delta_y = 0
                """
                Snake is currently moving up, so turning either 
                direction is fine 
                """
            elif (self.pixels[-1][0] - self.pixels[-2][0]) == 0:
                delta_x = -10 if event.key in (K_LEFT, K_a) else 10
                delta_y = 0
            elif (self.pixels[-1][0] - self.pixels[-2][0]) > 0:
                delta_x = 10
                delta_y = 0

        elif event.key in (K_UP, K_DOWN, K_w, K_s):
            if (self.pixels[-1][1] - self.pixels[-2][1]) < 0:
                delta_x = 0
                delta_y = -10
            elif (self.pixels[-1][1] - self.pixels[-2][1]) == 0:
                delta_x = 0
                delta_y = -10 if event.key in (K_UP, K_s) else 10
            elif (self.pixels[-1][1] - self.pixels[-2][1]) > 0:
                delta_x = 0
                delta_y = 10
        else:
            delta_x = 0
            delta_y = 0
        return (delta_x, delta_y)
