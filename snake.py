import pygame
from pygame import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN

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
        self.head_x, self.head_y = x, y

    def get_directions(self, event):
        if len(self.pixels) == 0:
            if event.key in (K_LEFT, K_RIGHT):
                x = -10 if event.key == K_LEFT else 10
                y = 0
            elif event.key in (K_UP, K_DOWN):
                x = 0
                y = -10 if event.key == K_UP else 10
            return (x, y)
        
        pass