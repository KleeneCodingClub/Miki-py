import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Retro Game")

# Colors
BLUE = (0, 0, 255)
LIGHT BLUE = (134, 196, 248)
GREEN = (130, 248, 110)
WHITE = (255, 255, 255)

# Player properties
player_size = 40
player_x = width // 2 - player_size // 2
player_y = height - player_size - 10
player_velocity = 5
player_lives = 3

# Blue dot properties
dot_size = 20
dot_x = random.randint(0, width - dot_size)
dot_y = -dot_size
dot_velocity = 3

# Obstacle properties
obstacle_size = 40
obstacle_x = random.randint(0, width - obstacle_size)
obstacle_y = -obstacle_size
obstacle_velocity = 3

# Game states
game_started = False
game_over = False
score = 0

# Load heart image
heart_img = pygame.image.load("heart.png").convert()
heart_img.set_colorkey(WHITE)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_started and event.key == pygame.K_SPACE:
                game_started = True
            elif game_over and event.key == pygame.K_SPACE:
                game_started = False
                game_over = False
                score = 0
                player_lives = 3

    if game_started and not game_over:
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_velocity
        if keys[pygame.K_RIGHT] and player_x < width - player_size:
            player_x += player_velocity

        # Update blue dot position
        dot_y += dot_velocity

        # Check for collision with player
        if (
            player_x < dot_x + dot_size
            and player_x + player_size > dot_x
            and player_y < dot_y + dot_size
            and player_y + player_size > dot_y
        ):
            dot_x = random.randint(0, width - dot_size)
            dot_y = -dot_size
            score += 1

        # Update obstacle position
        obstacle_y += obstacle_velocity

        # Check for collision with player
        if (
            player_x < obstacle_x + obstacle_size
            and player_x + player_size > obstacle_x
            and player_y < obstacle_y + obstacle_size
            and player_y + player_size > obstacle_y
        ):
            player_lives -= 1
            obstacle_x = random.randint(0, width - obstacle_size)
            obstacle_y = -obstacle_size

        # Check for game over
        if player_lives <= 0 or score >= 10:
            game_over = True

    # Draw on the screen
    screen.fill(BLUE)  # Set the background color

    if not game_started:
        start_font = pygame.font.Font(None, 48)
        start_text = start_font.render("Press SPACEBAR to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(width // 2, height // 2))
        screen.blit(start_text, start_rect)
    else:
        pygame.draw.rect(screen, BLUE, pygame.Rect(0, 0, width, height))  # Draw the scrolling background

        # Draw the player
        pygame.draw.rect(screen, WHITE, pygame.Rect(player_x, player_y, player_size, player_size))

        # Draw the blue dot
        pygame.draw.rect(screen, LIGHT BLUE, pygame.Rect(dot_x, dot_y, dot_size, dot_size))

        # Draw the obstacle
        pygame.draw.rect(screen, GREEN, pygame.Rect(obstacle_x, obstacle_y, obstacle_size, obstacle_size))

        # Draw the hearts (player lives)
        for i in range(player_lives):
            heart_rect = heart_img.get_rect(topright=(width - (i + 1) * (heart_img.get_width() + 10), 10))
            screen.blit(heart_img, heart_rect)

        # Draw the score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

    if game_over:
        game_over_font = pygame.font.Font(None, 48)
        if player_lives <= 0:
            game_over_text = game_over_font.render("Game Over", True, WHITE)
        else:
            game_over_text = game_over_font.render("Level Complete", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))
        screen.blit(game_over_text, game_over_rect)

    pygame.display.flip()  # Update the contents of the entire display

    clock.tick(60)  # Limit the frame rate to 60 FPS

# Quit the game
pygame.quit()
