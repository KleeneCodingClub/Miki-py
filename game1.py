import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 400, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Retro Game")

# Load background image
background_img = pygame.image.load("background.png").convert()
background_y = 0

# Player properties
player_size = 40
player_x = width // 2 - player_size // 2
player_y = height - player_size - 10
player_velocity = 5
player_lives = 3

# Blue dot properties
dot_radius = 10
dot_x = random.randint(dot_radius, width - dot_radius)
dot_y = -dot_radius
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
heart_img.set_colorkey((255, 255, 255))

# Game loop
running = True
clock = pygame.time.Clock()

def reset_objects():
    global dot_x, dot_y, obstacle_x, obstacle_y
    dot_x = random.randint(dot_radius, width - dot_radius)
    dot_y = -dot_radius
    obstacle_x = random.randint(0, width - obstacle_size)
    obstacle_y = -obstacle_size

def draw_objects():
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(player_x, player_y, player_size, player_size))
    pygame.draw.circle(screen, (134, 196, 248), (dot_x, dot_y), dot_radius)
    pygame.draw.rect(screen, (130, 248, 110), pygame.Rect(obstacle_x, obstacle_y, obstacle_size, obstacle_size))

def draw_hearts():
    for i in range(player_lives):
        heart_rect = heart_img.get_rect(topright=(width - (i + 1) * (heart_img.get_width() + 10), 10))
        screen.blit(heart_img, heart_rect)

def draw_score():
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

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
                reset_objects()

    if game_started and not game_over:
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_velocity
        if keys[pygame.K_RIGHT] and player_x < width - player_size:
            player_x += player_velocity

        # Update blue dot position
        if dot_y > height:
            dot_x = random.randint(dot_radius, width - dot_radius)
            dot_y = -dot_radius
        else:
            dot_y += dot_velocity

        # Check for collision with player
        if (
            player_x - dot_radius < dot_x < player_x + player_size + dot_radius
            and player_y - dot_radius < dot_y < player_y + player_size + dot_radius
        ):
            dot_x = random.randint(dot_radius, width - dot_radius)
            dot_y = -dot_radius
            score += 1

        # Update obstacle position
        if obstacle_y > height:
            obstacle_x = random.randint(0, width - obstacle_size)
            obstacle_y = -obstacle_size
        else:
            obstacle_y += obstacle_velocity

        # Check for collision with player
        if (
            player_x < obstacle_x + obstacle_size
            and player_x + player_size > obstacle_x
            and player_y < obstacle_y + obstacle_size
            and player_y + player_size > obstacle_y
        ):
            player_lives -= 1
            reset_objects()

        # Check for game over
        if player_lives <= 0 or score >= 10:
            game_over = True

    # Draw on the screen
    if game_started:
        screen.fill((0, 0, 0))
        screen.blit(background_img, (0, background_y))
        screen.blit(background_img, (0, background_y - background_img.get_height()))

        draw_objects()
        draw_hearts()
        draw_score()

        if game_over:
            game_over_font = pygame.font.Font(None, 48)
            if player_lives <= 0:
                game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
            else:
                game_over_text = game_over_font.render("Level Complete", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))
            screen.blit(game_over_text, game_over_rect)
    else:
        screen.fill((0, 0, 0))
        start_font = pygame.font.Font(None, 48)
        start_text = start_font.render("Press SPACEBAR to Start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(width // 2, height // 2))
        screen.blit(start_text, start_rect)

    pygame.display.flip()  # Update the contents of the entire display

    # Scroll the background
    background_y += 1
    if background_y >= background_img.get_height():
        background_y = 0

    clock.tick(60)  # Limit the frame rate to 60 FPS

# Quit the game
pygame.quit()
