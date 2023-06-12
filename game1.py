import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Retro Pixel Game")

# Player properties
player_size = 40
player_x = width // 2 - player_size // 2
player_y = height - player_size - 10
player_velocity = 5
player_lives = 3

# Obstacle properties
obstacle_size = 40
obstacle_x = random.randint(0, width - obstacle_size)
obstacle_y = -obstacle_size
obstacle_velocity = 3

# Timer properties
timer_font = pygame.font.Font(None, 36)
timer_value = 0  # in seconds
timer_text = timer_font.render(str(timer_value), True, (255, 255, 255))
timer_rect = timer_text.get_rect(center=(width // 2, 20))

# Game states
game_started = False
game_over = False

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
                player_lives = 3
                timer_value = 0

    if game_started and not game_over:
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_velocity
        if keys[pygame.K_RIGHT] and player_x < width - player_size:
            player_x += player_velocity

        # Update obstacle position
        obstacle_y += obstacle_velocity

        # Check for collision with obstacle
        if (
            player_x < obstacle_x + obstacle_size
            and player_x + player_size > obstacle_x
            and player_y < obstacle_y + obstacle_size
            and player_y + player_size > obstacle_y
        ):
            player_lives -= 1
            if player_lives <= 0:
                game_over = True
            else:
                obstacle_x = random.randint(0, width - obstacle_size)
                obstacle_y = -obstacle_size

        # Update timer
        if timer_value < 30:
            pygame.time.delay(1000)  # Delay for 1 second
            timer_value += 1
            timer_text = timer_font.render(str(timer_value), True, (255, 255, 255))

        # Check for level completion
        if timer_value == 30:
            game_over = True

    # Draw on the screen
    screen.fill((0, 0, 0))  # Clear the screen

    if not game_started:
        start_font = pygame.font.Font(None, 48)
        start_text = start_font.render("Press SPACEBAR to Start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(width // 2, height // 2))
        screen.blit(start_text, start_rect)
    else:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(player_x, player_y, player_size, player_size))  # Draw the player
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(obstacle_x, obstacle_y, obstacle_size, obstacle_size))  # Draw the obstacle
        screen.blit(timer_text, timer_rect)  # Draw the timer

    if game_over:
        game_over_font = pygame.font.Font(None, 48)
        if player_lives <= 0:
            game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        else:
            game_over_text = game_over_font.render("Level Complete", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))
        screen.blit(game_over_text, game_over_rect)

    pygame.display.flip()  # Update the contents of the entire display

    clock.tick(60)  # Limit the frame rate to 60 FPS

# Quit the game
pygame.quit()
