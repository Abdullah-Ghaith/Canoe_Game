import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game screen dimensions
screen_width = 800
screen_height = 600

# Colors
background_color = (52, 235, 232)

# Create the game screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Canoe Dodge Game")

# Load and resize canoe image
original_canoe_img = pygame.image.load("canoe.png")
canoe_width = 80
canoe_height = 60
canoe_img = pygame.transform.scale(original_canoe_img, (canoe_width, canoe_height))
canoe_y = screen_height // 2 - canoe_height // 2

# Load and resize obstacle image
original_obstacle_img = pygame.image.load("obstacle.png")
obstacle_width = 50
obstacle_height = 50
obstacle_img = pygame.transform.scale(original_obstacle_img, (obstacle_width, obstacle_height))

# Load and resize smaller wave image for background
small_wave_img = pygame.image.load("small_wave.png")
small_wave_size = 205  # Size of the smaller wave image
small_wave_img = pygame.transform.scale(small_wave_img, (small_wave_size, small_wave_size))

# Initialize variables
obstacles = []
score = 0
clock = pygame.time.Clock()

# Game loop
start_time = time.time()
game_over = False  # Flag to track game over state

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                game_over = False
                obstacles = []
                score = 0
                canoe_y = screen_height // 2 - canoe_height // 2
                start_time = time.time()

    # Clear the screen
    screen.fill(background_color)

    # Draw repeating wave background
    for y in range(0, screen_height, small_wave_size):
        for x in range(0, screen_width, small_wave_size):
            screen.blit(small_wave_img, (x, y))

    if not game_over:
        # Add obstacles
        if random.randint(0, 100) < 3:
            obstacles.append([screen_width, random.randint(0, screen_height - obstacle_height)])

        # Update obstacles position and check for collisions
        for obstacle in obstacles:
            obstacle[0] -= 5
            screen.blit(obstacle_img, (obstacle[0], obstacle[1]))

            # Check for collision with canoe
            if canoe_y < obstacle[1] + obstacle_height and canoe_y + canoe_height > obstacle[1]:
                if 100 < obstacle[0] + obstacle_width < 100 + canoe_width:  # Adjust this condition based on your game layout
                    game_over = True

        # Remove off-screen obstacles
        obstacles = [obstacle for obstacle in obstacles if obstacle[0] > -obstacle_width]

        # Update canoe position
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and canoe_y > 0:
            canoe_y -= 5
        if keys[pygame.K_DOWN] and canoe_y < screen_height - canoe_height:
            canoe_y += 5
        screen.blit(canoe_img, (100, canoe_y))

        # Calculate and display score
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1:
            score += 2
            start_time = time.time()

    # Display game over text
    if game_over:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("I LOVE YOU SCHNIIBS!", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))

        # Add another line of text
        font = pygame.font.Font(None, 36)
        retry_text = font.render("Click to retry", True, (0, 0, 0))
        screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, screen_height // 2 + 50))

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

    pygame.display.update()
    clock.tick(60)
