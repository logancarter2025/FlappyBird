# Import the required libraries
import pygame
import sys
import random

# Initialize the pygame modules to get everything started.
pygame.init()

# The size of the screen is set here.
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# This is used to keep track of time within the game, such as the frame rate.
clock = pygame.time.Clock()

# Define some common color codes for use in the game.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Constants defining the physics of the game's world.
GRAVITY = 1
GAME_SPEED = 5

# Variables defining the player's properties.
player_size = 30
player_pos = [50, SCREEN_HEIGHT // 2]
player_vel = 0
player_jump_vel = -10

# Variables defining the properties of obstacles.
obstacle_width = 70
obstacle_gap = 110
obstacle_list = []
passed_pipes = []
SCORE = 0
GAME_ACTIVE = True

# Setting up the font for displaying the score.
font = pygame.font.Font(None, 36)

# Function to increment the score when the player passes an obstacle.
def check_score(obstacle_list, passed_pipes, score):
    # If there are obstacles on the list to check.
    if obstacle_list:
        for obstacle in obstacle_list:
            # When the player passes an obstacle, increment the score.
            if player_pos[0] > obstacle[0].x + obstacle_width and obstacle not in passed_pipes:
                score += 1
                passed_pipes.append(obstacle)
    return score

# Function to draw the floor on the game screen.
def draw_floor():
    pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT - 1), (SCREEN_WIDTH, SCREEN_HEIGHT - 1), 5)

# Function to draw obstacles (pipes) on the screen.
def draw_obstacles(obstacle_list):
    for obstacle in obstacle_list:
        pygame.draw.rect(screen, GREEN, obstacle[0])
        pygame.draw.rect(screen, GREEN, obstacle[1])

# Function to add a new pair of obstacles to the list.
def add_obstacle(obstacle_list):
    obstacle_height = random.randint(100, 300)
    bottom_obstacle = pygame.Rect(SCREEN_WIDTH, SCREEN_HEIGHT - obstacle_height, obstacle_width, obstacle_height)
    top_obstacle = pygame.Rect(SCREEN_WIDTH, 0, obstacle_width, SCREEN_HEIGHT - obstacle_height - obstacle_gap)
    obstacle_list.append((bottom_obstacle, top_obstacle))
    return obstacle_list

# Function to move the obstacles to the left as time progresses.
def move_obstacles(obstacle_list):
    for obstacle in obstacle_list:
        obstacle[0].x -= GAME_SPEED
        obstacle[1].x -= GAME_SPEED
    return [obstacle for obstacle in obstacle_list if obstacle[0].x > -obstacle_width]

# Function to check for collisions between the player and the obstacles.
def check_collision(player_pos, obstacle_list):
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for obstacle in obstacle_list:
        if player_rect.colliderect(obstacle[0]) or player_rect.colliderect(obstacle[1]):
            return True
    return False

# Function to draw the current score on the screen.
def draw_score(score):
    score_text = 'Score: ' + str(score)
    text_surface = font.render(score_text, True, WHITE)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH - 80, 30))
    screen.blit(text_surface, text_rect)

# Function to reset the game to the initial state when the player loses.
def reset_game():
    global player_pos, player_vel, obstacle_list, SCORE, GAME_ACTIVE
    player_pos = [50, SCREEN_HEIGHT // 2]
    player_vel = 0
    obstacle_list = []
    SCORE = 0
    GAME_ACTIVE = True

# The main game loop - this loop runs continuously while the game is running.
while True:
    # Event handling loop.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # If the space key is pressed and the game is active, make the player jump.
            if event.key == pygame.K_SPACE and GAME_ACTIVE:
                player_vel = player_jump_vel
            # If the space key is pressed and the game is not active, reset the game.
            if event.key == pygame.K_SPACE and not GAME_ACTIVE:
                reset_game()

    # Game logic for when the game is active.
    if GAME_ACTIVE:
        # Fill the screen with a blue sky color.
        screen.fill((135, 206, 235))
        # Draw the floor.
        draw_floor()
        # Apply gravity to the player's vertical velocity.
        player_vel += GRAVITY
        # Update the player's vertical position.
        player_pos[1] += player_vel

        # If the player hits the ground, end the game.
        if player_pos[1] > SCREEN_HEIGHT:
            GAME_ACTIVE = False

        # Draw the player on the screen.
        pygame.draw.rect(screen, YELLOW, (player_pos[0], player_pos[1], player_size, player_size))

        # Add a new obstacle when appropriate.
        if len(obstacle_list) == 0 or obstacle_list[-1][0].x < SCREEN_WIDTH - 300:
            obstacle_list = add_obstacle(obstacle_list)

        # Move existing obstacles.
        obstacle_list = move_obstacles(obstacle_list)
        # Draw the obstacles.
        draw_obstacles(obstacle_list)

        # Check for collisions and end the game if there is one.
        if check_collision(player_pos, obstacle_list):
            GAME_ACTIVE = False

        # Update the score as the player passes obstacles.
        SCORE = check_score(obstacle_list, passed_pipes, SCORE)
        # Draw the score on the screen.
        draw_score(SCORE)
    else:
        # If the game is not active, display the game over screen.
        screen.fill(RED)
        game_over_text = 'Game Over! Score: ' + str(SCORE)
        game_over_surface = font.render(game_over_text, True, WHITE)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20))
        replay_text = 'Press SPACE to Replay'
        replay_surface = font.render(replay_text, True, WHITE)
        replay_rect = replay_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
        screen.blit(game_over_surface, game_over_rect)
        screen.blit(replay_surface, replay_rect)

    # Refresh the screen to show the latest screen graphics.
    pygame.display.update()
    # Control the loop iteration speed to 50 times per second, which controls the frame rate.
    clock.tick(50)
