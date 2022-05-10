from random import randint, randrange, choice as rand_choice
import pygame
from pygame import (
    KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT
)

from snake import Snake

pygame.init()
pygame.display.set_caption("Snake Game")

class SnakeGame:

    snakes: list[Snake] = []
    width, height = 700, 500
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    orange = (255, 165, 0)

    message_font = pygame.font.SysFont("arial", 30)
    score_font = pygame.font.SysFont("arial", 25)

    def __init__(self, names_and_controls: list[tuple[str, str]]):
        self.clock = pygame.time.Clock()
        self.game_display = pygame.display.set_mode((self.width, self.height))
        self.game_display.fill(self.white)
        pygame.display.update()

        for name, control in names_and_controls:
            snake = Snake(
                name, self.width, self.height, control
            )
            self.snakes.append(snake)

    def update(self):
        pygame.display.update()

    def print_score(self, score: int) -> None:
        for i, snake in enumerate(self.snakes):
            text = self.score_font.render(
                f"{snake.name}'s score: {snake.score}", 
                True, 
                self.orange
            )
            self.game_display.blit(text, [0, i + 4 if i > 0 else i])
        
    def print_time(self, time: int):
        text = self.score_font.render(f"Time: {time}", True, self.orange)
        self.game_display.blit(text, [30, 0])

    def draw_snakes(self):
        pass

    def draw_fruits(self, coordinates: list[tuple[int, int]]):
        for x, y in coordinates:
            pygame.draw.rect(
                self.game_display, 
                self.orange, 
                [x, y, 10, 10]
            )

    def rand_x_y(self):
        rand_x = randrange(10, (self.width - 10) / 10.0) * 10.0
        rand_y = randrange(10, (self.height - 10) / 10.0) * 10.0
        return (rand_x, rand_y)

    def game_over_screen(self):
        message = f"Game Over! Score: {self.score}"
        text = self.score_font.render(
            message, 
            True, 
            self.orange
        )

        while game_close == False:
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_close = True

        self.game_display.fill(self.black)
        self.game_display.blit(text, 
            [(self.width // 2) - 130, (self.height // 2) - 20]
        )
        self.update()

    def run(self):
        pass
        
    def end(self):
        pygame.display.quit()
        pygame.quit()
        quit()

    def play(self):
        game.run()
        game.end()

if __name__ == '__main__':
    game = SnakeGame()
    game.play()