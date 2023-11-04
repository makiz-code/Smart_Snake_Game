import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN1 = (0, 200, 0)
GREEN2 = (100, 200, 100)

BLOCK_SIZE = 20
SPEED = 30

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.direction = pygame.K_RIGHT
        self.head = [self.w / 2, self.h / 2]
        self.snake = [self.head,
                      [self.head[0] - BLOCK_SIZE, self.head[1]],
                      [self.head[0] - (2 * BLOCK_SIZE), self.head[1]]]
        self.score = 0
        self.food = None
        self.place_food()

    def place_food(self):
        while True:
            x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            self.food = [x, y]
            if self.food not in self.snake:
                break

    def step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    self.direction = event.key

        self.move()
        self.snake.insert(0, self.head)

        game_over = False

        if self.is_collision():
            game_over = True
            return game_over, self.score

        if self.head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()

        self.render()

        return game_over, self.score

    def move(self):
        x = self.head[0]
        y = self.head[1]
        if self.direction == pygame.K_RIGHT:
            x += BLOCK_SIZE
        elif self.direction == pygame.K_LEFT:
            x -= BLOCK_SIZE
        elif self.direction == pygame.K_DOWN:
            y += BLOCK_SIZE
        elif self.direction == pygame.K_UP:
            y -= BLOCK_SIZE

        self.head = [x,y]

    def is_collision(self):
        if self.head in self.snake[1:]:
            return True

        if not (0 <= self.head[0] < self.w) or not (0 <= self.head[1] < self.h):
            return True

        return False

    def render(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt[0], pt[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt[0] + 4, pt[1] + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))

        font = pygame.font.SysFont('Garamond', 25)
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [8, 5])
        pygame.display.flip()

        self.clock.tick(SPEED)


if __name__ == '__main__':
    game = SnakeGame()

    while True:
        game_over, score = game.step()

        if game_over:
            break

    print('Final Score', score)

    pygame.quit()