import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 40)

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Constants
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3

def create_pipe():
    top_height = random.randint(50, 350)
    bottom_height = HEIGHT - top_height - PIPE_GAP
    return {'x': WIDTH, 'top': top_height, 'bottom': bottom_height, 'scored': False}

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe['x'], 0, PIPE_WIDTH, pipe['top']))
        pygame.draw.rect(screen, GREEN, (pipe['x'], HEIGHT - pipe['bottom'], PIPE_WIDTH, pipe['bottom']))

def check_collision(bird_rect, pipes, bird_y, bird_radius):
    if bird_y - bird_radius <= 0 or bird_y + bird_radius >= HEIGHT:
        return True
    for pipe in pipes:
        top_rect = pygame.Rect(pipe['x'], 0, PIPE_WIDTH, pipe['top'])
        bottom_rect = pygame.Rect(pipe['x'], HEIGHT - pipe['bottom'], PIPE_WIDTH, pipe['bottom'])
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True
    return False

def game_loop():
    bird_x = 50
    bird_y = 300
    bird_radius = 20
    bird_velocity = 0

    pipes = []
    spawn_timer = 0
    score = 0

    running = True
    game_over = False

    while running:
        clock.tick(60)
        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_velocity = JUMP_STRENGTH
                if event.key == pygame.K_r and game_over:
                    return  # Restart the game by re-calling game_loop

        if not game_over:
            # Bird physics
            bird_velocity += GRAVITY
            bird_y += bird_velocity

            # Pipe movement
            spawn_timer += 1
            if spawn_timer > 90:
                pipes.append(create_pipe())
                spawn_timer = 0

            for pipe in pipes:
                pipe['x'] -= PIPE_SPEED

            pipes = [pipe for pipe in pipes if pipe['x'] + PIPE_WIDTH > 0]

            # Scoring
            for pipe in pipes:
                if pipe['x'] + PIPE_WIDTH < bird_x and not pipe['scored']:
                    score += 1
                    pipe['scored'] = True

            # Collision check
            bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius*2, bird_radius*2)
            if check_collision(bird_rect, pipes, bird_y, bird_radius):
                game_over = True

        # Drawing
        pygame.draw.circle(screen, RED, (bird_x, int(bird_y)), bird_radius)
        draw_pipes(pipes)

        score_text = FONT.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = FONT.render("Game Over!", True, WHITE)
            restart_text = FONT.render("Press R to Restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - 130, HEIGHT // 2))

        pygame.display.flip()

# Start the game loop
while True:
    game_loop()
