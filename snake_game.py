import pygame
import random

pygame.init()

# Window
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# Snake
snake_block = 10
snake_speed = 15
snake = [(100, 100)]
direction = "RIGHT"

# Food
food = (
    random.randrange(0, width, snake_block),
    random.randrange(0, height, snake_block)
)

font = pygame.font.SysFont(None, 35)

def draw_snake(snake):
    for x, y in snake:
        pygame.draw.rect(screen, green, [x, y, snake_block, snake_block])

def show_score(score):
    value = font.render(f"Score: {score}", True, white)
    screen.blit(value, [0, 0])

def move_snake(direction):
    x, y = snake[0]
    if direction == "UP":
        y -= snake_block
    elif direction == "DOWN":
        y += snake_block
    elif direction == "LEFT":
        x -= snake_block
    elif direction == "RIGHT":
        x += snake_block
    snake.insert(0, (x, y))
    snake.pop()

running = True
score = 0

while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                direction = "RIGHT"
            elif event.key == pygame.K_UP:
                direction = "UP"
            elif event.key == pygame.K_DOWN:
                direction = "DOWN"

    move_snake(direction)

    # Wall collision
    x, y = snake[0]
    if x < 0 or x >= width or y < 0 or y >= height:
        running = False

    # Food collision
    if (x, y) == food:
        snake.append(snake[-1])
        score += 1
        food = (
            random.randrange(0, width, snake_block),
            random.randrange(0, height, snake_block)
        )

    pygame.draw.rect(screen, red, [food[0], food[1], snake_block, snake_block])
    draw_snake(snake)
    show_score(score)

    pygame.display.update()
    clock.tick(snake_speed)

pygame.quit()
