import os
from pathlib import Path
from random import choice, randrange
import time
import json

import pygame
from pygame import (
    QUIT, KEYDOWN, K_BACKSPACE, K_ESCAPE, 
    K_SPACE, K_RETURN, K_DELETE,
    K_UP, K_DOWN, K_LEFT, K_RIGHT
)

from sprites import Snake, Apple
from game_modes import (
    Game_Mode,
    OnePlayer_Classic_Snake,
    TwoPlayer_Snake
)

pygame.init()
pygame.display.set_caption("Snake Game 2.0")

resources_path = Path(
        os.path.split(os.path.split(__file__)[0])[0]
    ) / "resources"

class SnakeGame:

    snake_1: Snake
    snake_2: Snake

    width, height = 1000, 600
    dimensions = (width, height)
    
    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (160, 160, 160)

    message_font = pygame.font.Font(f"{resources_path}\\pixel_font.ttf", 40)
    option_font = pygame.font.Font(f"{resources_path}\\pixel_font.ttf", 30)
    
    snake_1 = None
    snake_2 = None
    classic_snake = None
    two_player = None

    apples = pygame.sprite.Group()
    Apple.containers = apples 
    
    def __init__(self, size):
        self.clock = pygame.time.Clock()
        self.square_size = size
        self.width += self.width % size
        self.height += self.height % size
        self.game_display = pygame.display.set_mode(self.dimensions)
        background = pygame.image.load(
            f"{resources_path}\\start_bg.png").convert()
        self.background = pygame.transform.scale(background, self.dimensions)
        self.snake_1 = Snake(self, Snake.Controls.KEYS)
        self.snake_2 = Snake(self, Snake.Controls.WASD)
        self.classic_snake = OnePlayer_Classic_Snake(game=self)
        self.two_player = TwoPlayer_Snake(game=self)

    def get_random_fact(self, random_facts) -> tuple[str, tuple[int, int]]:
        rand_x = (self.width / 2 - 250, self.width / 2 - 150)
        rand_y = (100, self.height - 100)
        rand_index = randrange(0, len(random_facts))
        return (random_facts[rand_index], (choice(rand_x), choice(rand_y)))

    def start_screen(self):
        random_facts: list
        with open(resources_path / "random_facts.json") as json_file:
            random_facts = json.loads(json_file.read())

        main_message = "Snake 2.0"
        message = "Press any key to continue"
        colors = [self.black, self.white]
        x = self.width / 2
        y = self.height / 2
        offset_1 = self.message_font.size(main_message)[0] / 2
        offset_2 = self.message_font.size(message)[0] / 2

        rand_fact, rand_fact_2, rand_text = None, None, None
        rand_text_2, x_y_1, x_y_2 = None, None, None
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.end()
                    else:
                        return
            if time.time() % 1 > 0.5:
                text = self.message_font.render(main_message, True, colors[0])
            else:
                text = self.message_font.render(main_message, True, colors[1])
            text_2 = self.message_font.render(message, True, self.white)
            if round(time.time() % 5, 2) == 4.99:
                rand_fact, x_y_1 = self.get_random_fact(random_facts)
                if "\n" in rand_fact:
                    i = rand_fact.index("\n")
                    rand_fact_2 = rand_fact[i + 1:]
                    rand_fact = rand_fact[:i]
                    rand_text_2 = self.option_font.render(
                        rand_fact_2, True, self.white
                    )
                    size = self.option_font.size(rand_fact_2)
                    x_y_2 = ((x_y_1[0] / 2) - size[0] / 2, x_y_1[1] + size[1])
                    rand_text = self.option_font.render(rand_fact, True, self.white)
                else:
                    rand_text = self.option_font.render(rand_fact, True, self.white)
                    rand_fact_2 = None

            self.game_display.blit(self.background, [0, 0])
            self.game_display.blit(text, [x - offset_1, y - 40])
            self.game_display.blit(text_2, [x - offset_2, y])
            if rand_fact:
                self.game_display.blit(rand_text, x_y_1)
                if rand_fact_2:
                    self.game_display.blit(rand_text_2, x_y_2)
            pygame.display.update()

    def prompt_name_screen(self, message):
        name = ""
        plead = "Please enter a valid name"
        x = self.width // 2
        y = self.height // 2
        show_warn_valid = False
        rect = pygame.rect.Rect((x - 250, y - 20), (500, 50))

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.end()
                    elif event.key == K_BACKSPACE and len(name) >= 0:
                        name = name[:-1]
                    elif event.key == K_DELETE:
                        name = ""
                    elif event.key == K_RETURN:
                        if str.isspace(name) or name == "":
                            show_warn_valid = True
                        else: 
                            return name
                    elif 30 > len(name) >= 0:
                        name += event.unicode
            text = self.message_font.render(message, True, self.white)
            name_text = self.option_font.render(name, True, self.white)
            name_text = self.option_font.render(name, True, self.white)
            offset_1 = self.option_font.size(name)[0] / 2
            offset_2 = self.message_font.size(message)[0] / 2

            self.game_display.blit(self.background, [0, 0])
            self.game_display.blit(
                name_text, 
                [(rect.center[0] - offset_1), rect.topleft[1] + 13] 
            )
            self.game_display.blit(text, [x - offset_2, y - 120])

            pygame.draw.rect(self.game_display, self.white, rect, 3)

            cursor = pygame.rect.Rect(
                (rect.center[0] + offset_1, rect.topleft[1] + 8), (3, 35)
            )
            if time.time() % 1 > 0.5:
                pygame.draw.rect(self.game_display, self.white, cursor)
            
            if show_warn_valid:
                warning = self.option_font.render(plead, True, self.white)
                offset = self.option_font.size(plead)[0] / 2
                self.game_display.blit(warning, [x - offset, rect.bottom + 50])

            pygame.display.update()


    def menu_screen(self, last_selected: Game_Mode, options_1, options_2):
        x_1 = self.width // 2 - 220
        y = self.height // 2
        x_2 = self.width // 2 + 30
        message = "Choose a game mode to play" 
        colors = [self.white, self.black]
        color_1, color_2 = self.grey, self.black
        text = self.message_font.render(message, True, self.white)

        square = pygame.rect.Rect(x_1, y, 170, 50)
        square_2 = pygame.rect.Rect(x_2, y, 170, 50)
        square_3 = pygame.rect.Rect(x_1, y + 60, 170, 50)
        square_4 = pygame.rect.Rect(x_2, y + 60, 170, 50)

        if last_selected == self.two_player:
            colors[0] = self.black
            colors[1] = self.white
            color_1 = self.black
            color_2 = self.grey

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.end()
                    if event.key in (K_LEFT, K_RIGHT):
                        if colors[0] in (self.grey, self.white):
                            colors[0] = self.black  
                            colors[1] = self.white
                            color_1 = self.black
                            color_2 = self.grey
                        elif colors[1] in (self.grey, self.white):
                            colors[0] = self.white 
                            colors[1] = self.black
                            color_1 = self.grey
                            color_2 = self.black
                    if event.key == K_UP:
                        if colors[0] == self.grey:
                            color_1 = self.grey
                            colors[0] = self.white
                        if colors[1] == self.grey:
                            color_2 = self.grey
                            colors[1] = self.white
                    if event.key == K_DOWN:
                        if colors[0] == self.white:
                            color_1 = self.white
                            colors[0] = self.grey
                        if colors[1] == self.white:
                            color_2 = self.white
                            colors[1] = self.grey
                    if event.key == K_RETURN:
                        if color_1 == self.white:
                            self.option_screen(options_1)
                        if color_2 == self.white:
                            self.option_screen(options_2)
                        if colors[0] == self.white and color_1 == self.grey:
                            return (self.classic_snake, options_1)
                        if colors[1] == self.white and color_2 == self.grey:
                            return (self.two_player, options_2)

            text_1 = self.option_font.render("One Player", True, colors[0])
            text_2 = self.option_font.render("Two Player", True, colors[1])
            option_text_1 = self.option_font.render("Options", True, color_1)
            option_text_2 = self.option_font.render("Options", True, color_2)

            self.game_display.blit(self.background, [0, 0])

            pygame.draw.rect(self.game_display, color_1, square_3, 3)
            pygame.draw.rect(self.game_display, color_2, square_4, 3)
            pygame.draw.rect(self.game_display, colors[0], square, 3)
            pygame.draw.rect(self.game_display, colors[1], square_2, 3)

            self.game_display.blit(
                text, [self.width // 2 - 250, self.height // 2 - 90]
            )
            self.game_display.blit(
                text_1, [square.center[0] - 72, square.center[1] - 12]
            )
            self.game_display.blit(
                text_2, [square_2.center[0] - 74, square_2.center[1] - 12]
            )
            self.game_display.blit(
                option_text_1, 
                [square_3.center[0] - 50, square.center[1] + 45]
            )
            self.game_display.blit(
                option_text_2, 
                [square_4.center[0] - 50, square.center[1] + 45]
            )
            pygame.display.update()

    def option_screen(self, options):
        x = self.width // 2
        y = self.height // 2
        colors = [self.white, self.black]

        fruit_count = options["fruit_count"]
        speed = options["speed"]

        message = "Use up and down arrows to change category"
        message_2 = "Press space to change the values"
        text = self.option_font.render(message, True, self.white)
        text_2 = self.option_font.render(message_2, True, self.white)
        option_text = self.message_font.render("Options", True, self.white)
            
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.end()
                    if event.key == K_RETURN:
                        options["fruit_count"] = fruit_count
                        options["speed"] = speed
                        return
                    if event.key in (K_UP, K_DOWN):
                        colors.reverse()
                    if event.key == K_SPACE:
                        if colors[0] == self.white:
                            if fruit_count < 11:
                                fruit_count += 1
                            if fruit_count == 11:
                                fruit_count = 1
                        if colors[1] == self.white:
                            if speed <= 20:
                                speed += 1
                            if speed == 21:
                                speed = 10
            fruits_text = self.option_font.render(
                "Number of Fruits", True, colors[0]
            )
            fruit_num = self.option_font.render(
                str(fruit_count), True, colors[0]
            )
            speed_text = self.option_font.render(
                "Snake Speed", True, colors[1]
            )
            speed_num = self.option_font.render(
                str(speed), True, colors[1]
            )

            self.game_display.blit(self.background, [0, 0])
            self.game_display.blit(option_text, [x - 80, 60])

            self.game_display.blit(text, [x - 310, 100])
            self.game_display.blit(text_2, [x - 220, 140])

            self.game_display.blit(fruits_text, [x - 210, y - 60])
            self.game_display.blit(fruit_num, [x + 70, y - 60])

            self.game_display.blit(speed_text, [x - 210, y - 20])
            self.game_display.blit(speed_num, [x + 70, y - 20])
            pygame.display.update()
                    
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def play(self):
        see_menu, stop = True, False
        name_1, name_2 = "", ""
        game_mode = self.classic_snake
        options_1 = {
            "fruit_count": 1,
            "speed": 10
        }
        options_2 = {
            "fruit_count": 1,
            "speed": 10
        }

        self.start_screen()

        while stop == False:
            if see_menu:
                (game_mode, options) = self.menu_screen(
                    game_mode, options_1, options_2)
                    
            if game_mode == self.two_player and self.snake_1.name == "" and \
            self.snake_2.name == "":
                while name_1 == name_2 or name_1 == "":
                    name_1 = self.prompt_name_screen("Enter player 1 name")
                    self.snake_1.name = name_1   
                while name_2 == name_1 or name_2 == "":
                    name_2 = self.prompt_name_screen("Enter player 2 name")
                self.snake_2.name = name_2

            if game_mode == self.classic_snake and self.snake_1.name == "":
                while name_2 == name_1 or name_1 == "":
                    name_1 = self.prompt_name_screen("Enter your player name")
                self.snake_1.name = name_1

            if game_mode == self.two_player and self.snake_2.name == "":
                while name_2 == name_1 or name_2 == "":
                    name_2 = self.prompt_name_screen("Enter player 2 name")
                self.snake_2.name = name_2

            self.snake_1.reset()
            self.snake_2.reset()
            (stop, see_menu) = game_mode.run(options=options)

        self.end()