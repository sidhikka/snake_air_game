import cv2
import mediapipe as mp
import pygame
import random
import numpy as np

# ===================== PYGAME =====================
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Gesture Snake 🐍")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

BLOCK = 20
SPEED = 6

font = pygame.font.SysFont(None, 26)

# ===================== CAMERA PREVIEW SIZE =====================
CAM_W, CAM_H = 160, 120
CAM_X = WIDTH - CAM_W - 10
CAM_Y = HEIGHT - CAM_H - 10   # 👈 bottom-right corner

# ===================== MEDIAPIPE =====================
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

MOVE_THRESHOLD = 30

# ===================== FUNCTIONS =====================
def draw_text(text, x, y):
    t = font.render(text, True, WHITE)
    screen.blit(t, (x, y))

def draw_snake(snake):
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x, y, BLOCK, BLOCK))

def move_snake(snake, direction):
    x, y = snake[0]
    if direction == "UP":
        y -= BLOCK
    elif direction == "DOWN":
        y += BLOCK
    elif direction == "LEFT":
        x -= BLOCK
    elif direction == "RIGHT":
        x += BLOCK
    snake.insert(0, (x, y))
    snake.pop()

def draw_camera_preview(frame, gesture):
    cam = cv2.resize(frame, (CAM_W, CAM_H))
    cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
    cam = np.rot90(cam)
    cam_surface = pygame.surfarray.make_surface(cam)

    screen.blit(cam_surface, (CAM_X, CAM_Y))
    pygame.draw.rect(screen, WHITE, (CAM_X, CAM_Y, CAM_W, CAM_H), 2)
    draw_text(f"Gesture: {gesture}", CAM_X, CAM_Y - 20)

# ===================== MAIN LOOP =====================
running = True

while running:
    # ---------- RESET GAME ----------
    snake = [(300, 200)]
    direction = "STOP"
    prev_x, prev_y = None, None
    score = 0

    # Food will NOT spawn under camera
    def new_food():
        while True:
            fx = random.randrange(0, WIDTH, BLOCK)
            fy = random.randrange(0, HEIGHT, BLOCK)
            if not (CAM_X <= fx <= CAM_X + CAM_W and CAM_Y <= fy <= CAM_Y + CAM_H):
                return (fx, fy)

    food = new_food()
    game_over = False

    # ---------- GAME LOOP ----------
    while not game_over:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True

        # ---------- HAND TRACKING ----------
        ret, frame = cap.read()
        gesture = "NONE"

        if ret:
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            if result.multi_hand_landmarks:
                hand = result.multi_hand_landmarks[0]
                finger = hand.landmark[8]
                x = int(finger.x * w)
                y = int(finger.y * h)

                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

                if prev_x is not None:
                    dx = x - prev_x
                    dy = y - prev_y

                    if abs(dx) > abs(dy) and abs(dx) > MOVE_THRESHOLD:
                        direction = "RIGHT" if dx > 0 else "LEFT"
                    elif abs(dy) > MOVE_THRESHOLD:
                        direction = "DOWN" if dy > 0 else "UP"

                prev_x, prev_y = x, y
                gesture = direction

        if direction != "STOP":
            move_snake(snake, direction)

        head_x, head_y = snake[0]

        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            game_over = True

        if (head_x, head_y) == food:
            snake.append(snake[-1])
            score += 1
            food = new_food()

        pygame.draw.rect(screen, RED, (*food, BLOCK, BLOCK))
        draw_snake(snake)

        draw_text(f"Score: {score}", 10, 10)
        draw_text("Watch camera bottom-right", 10, 35)

        if ret:
            draw_camera_preview(frame, gesture)

        pygame.display.update()
        clock.tick(SPEED)

    # ---------- GAME OVER ----------
    screen.fill(BLACK)
    draw_text("GAME OVER", 240, 160)
    draw_text("Press SPACE to restart", 200, 200)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

cap.release()
pygame.quit()            