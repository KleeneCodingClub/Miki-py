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

# Enemy properties
enemy_size = 30
enemy_x = random.randint(0, width - enemy_size)
enemy_y = 0
enemy_velocity = 3

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += player_velocity

    # Update enemy position
    enemy_y += enemy_velocity

    # Check for collision
    if player_x < enemy_x + enemy_size and player_x + player_size > enemy_x and player_y < enemy_y + enemy_size and player_y + player_size > enemy_y:
        # Collision occurred, game over
        running = False

    # Draw on the screen
    screen.fill((0, 0, 0))  # Clear the screen
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(player_x, player_y, player_size, player_size))  # Draw the player
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size))  # Draw the enemy

    pygame.display.flip()  # Update the contents of the entire display

    clock.tick(60)  # Limit the frame rate to 60 FPS

# Quit the game
pygame.quit()
