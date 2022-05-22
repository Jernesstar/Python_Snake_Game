import pygame
from pygame import (
    K_DOWN, K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT,
    K_LEFT, K_RETURN, K_RIGHT
) 

from snake import Snake, Control

from game_modes import (
    Game_Mode,
    OnePlayer_Classic_Snake,
    TwoPlayer_Snake
)

pygame.init()
pygame.display.set_caption("Snake Game 2.0")


class SnakeGame:

    snake_1: Snake
    snake_2: Snake

    width, height = 1000, 600
    
    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (160, 160, 160)

    message_font = pygame.font.Font("resources\\pixel_font.ttf", 40)
    option_font = pygame.font.Font("resources\\pixel_font.ttf", 30)

    def __init__(self, name_1, name_2 = ""):
        self.clock = pygame.time.Clock()
        
        self.snake_1 = Snake(game=self, name=name_1, controls=Control.KEYS)
        self.snake_1.size = 50
    
        if name_2 != "":
            self.snake_2 = Snake(game=self, name=name_2, controls=Control.WASD)
            self.snake_2.size = 50
            
        self.width += self.width % self.snake_1.size
        self.height += self.height % self.snake_1.size
        
        self.game_display = pygame.display.set_mode((self.width, self.height))

        self.background = pygame.image.load(
            "resources\\start_bg.png").convert()
        self.background = pygame.transform.scale(self.background, 
            (self.width, self.height))
        
        self.classic_snake = OnePlayer_Classic_Snake(game=self)
        if name_2 != "":
            self.two_player = TwoPlayer_Snake(game=self)

    def start_screen(self):
        message = "Snake 2.0"
        message_2 = "Press any key to continue"

        text_2 = self.message_font.render(message_2, True, self.white)
       
        colors = [self.black, self.white]
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.end()
                    else:
                        return
            text = self.message_font.render(message, True, colors[0])
        
            self.game_display.blit(self.background, [0, 0])
            self.game_display.blit(
                text, 
                [(self.width // 2) - 120, 
                (self.height // 2) - self.message_font.get_height()]
            )
            self.game_display.blit(
                text_2, 
                [(self.width // 2) - 250, 
                (self.height // 2)]
            )
            self.clock.tick(self.snake_1.speed)
            self.clock.tick(2)
            colors.reverse()
            pygame.display.update()

    def menu_screen(self, last_selected) -> tuple[Game_Mode, int]:
        x_1 = self.width // 2 - 220
        y = self.height // 2
        x_2 = self.width // 2 + 30

        message = "Choose a game mode to play" 
        text = self.message_font.render(message, True, self.white)

        square = pygame.rect.Rect(x_1, y, 170, 50)
        square_2 = pygame.rect.Rect(x_2, y, 170, 50)
        square_3 = pygame.rect.Rect(x_1, y + 60, 170, 50)
        square_4 = pygame.rect.Rect(x_2, y + 60, 170, 50)

        colors = [self.white, self.black]
        color_1, color_2, fruit_count = self.grey, self.black, 1

        if last_selected == self.two_player:
            colors.reverse()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.end()
                    if event.key in (K_LEFT, K_RIGHT):
                        colors.reverse()
                        if colors[0] == self.white:
                            color_1 = self.grey
                            color_2 = self.black
                        if colors[1] == self.white:
                            color_2 = self.grey
                            color_1 = self.black
                    if event.key == K_UP:
                        if colors[0] == self.white:
                            color_1 = self.grey
                        if colors[1] == self.white:
                            color_2 = self.grey
                    if event.key == K_DOWN:
                        if colors[0] == self.white:
                            color_1 = self.white
                        if colors[1] == self.white:
                            color_2 = self.white
                    if event.key == K_RETURN:
                        if color_1 == self.white:
                            fruit_count = self.option_screen()
                        if color_2 == self.white:
                            fruit_count = self.option_screen()
                        if colors[0] == self.white and color_1 == self.grey:
                            return (self.classic_snake, fruit_count)
                        if colors[1] == self.white and color_2 == self.grey:
                            return (self.two_player, fruit_count)
     
            self.game_display.blit(self.background, [0, 0])

            text_1 = self.option_font.render("One Player", True, colors[0])
            text_2 = self.option_font.render("Two Player", True, colors[1])
            
            option_text_1 = self.option_font.render("Options", True, color_1)
            option_text_2 = self.option_font.render("Options", True, color_2)

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

    def option_screen(self):
        x_1 = self.width // 2
        y = self.height // 2

        colors = [self.white]
        fruit_count = 1

        option_text = self.message_font.render("Options", True, self.white)
        fruits_text = self.option_font.render("Fruit Number", True, self.white)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.end()
                    if event.key == K_RETURN:
                        return fruit_count
                    if event.key == K_SPACE:
                        if colors[0] == self.white:
                            if fruit_count < 11:
                                fruit_count += 1
                            if fruit_count == 11:
                                fruit_count = 1
            fruit_num_text = self.option_font.render(
                str(fruit_count), True, self.white)
            
            self.game_display.blit(self.background, [0, 0])
            self.game_display.blit(option_text, [self.width // 2 - 80, 60])
            self.game_display.blit(
                fruits_text, 
                [x_1 - 170, y - 90]
            )
            self.game_display.blit(
                fruit_num_text, 
                [x_1 + 60, y - 90]
            )
            pygame.display.update()
                    
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def play(self):
        self.start_screen()

        see_menu, stop = True, False
        fruit_count: int = 1
        game_mode = self.classic_snake

        while stop == False:
            if see_menu:
                (game_mode, fruit_count) = self.menu_screen(game_mode)
            self.snake_1.reset()
            self.snake_2.reset()
            (stop, see_menu) = game_mode.run(fruit_count=fruit_count)

        self.end()