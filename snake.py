# =========================
#  MEMBER 1 – PROJECT INTRODUCTION & SETUP-Samuel
# =========================

import pygame
import random
import math

#  Initialize Pygame
# Pygame is a library used to make games in Python.
# Before using it, we must initialize all its built-in modules (graphics, sound, input, etc.)
pygame.init()

# Screen setup
# Define the window size (width and height in pixels)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Creating the main window (called "screen") where the game will be displayed
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window 
pygame.display.set_caption("Snake Game")

#  Colors (R, G, B values)

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (150, 75, 0)
BLUE = (0, 0, 255)


# =========================
#  MEMBER 2 – SNAKE AND FOOD SYSTEM
# =========================
# Snake properties
# Each block of the snake is a  square.
snakeBlock = 20   # The size of each square in pixels
snakeSpeed = 5    # The starting  speed of the snake
#  Fonts for score and messages
# Text styles that will be used for displaying the score and "Game Over" message.
scoreFont = pygame.font.SysFont("comicsansms", 35)
Gover_font = pygame.font.SysFont("comicsansms", 70)
# Function to draw the snake
# This function draws all parts (blocks) of the snake.
def draw_snake(snake_list):
    for i, x in enumerate(snake_list):
        # The snake's body is green, but the head is drawn in a slightly darker color
        color = GREEN if i < len(snake_list) - 1 else (0, 200, 0)
        # Draw a rectangle (the block) for each part of the snake
        pygame.draw.rect(screen, color, [x[0], x[1], snakeBlock, snakeBlock])
# Function to spawn food
# This function creates either a normal or bonus food item.
def spawn_food():
    # Randomly decide if the food will be bonus or normal
    if random.randint(1, 5) == 5:  # 1 in 5 chance of spawning bonus food
        return {"color": YELLOW, "effect": 2}  # Bonus food gives +2 points and growth
    else:
        return {"color": RED, "effect": 1}     # Normal food gives +1 growth
# =========================
#  MEMBER 3 – SCORING, WALLS, & DISPLAY
# =========================

# Function to show score and level

# This function displays the player's score and level on the screen.
def display_score(score, level):
    # Render text as an image (white color)
    score_value = scoreFont.render("Score: " + str(score), True, WHITE)
    level_value = Gover_font.render("Level: " + str(level), True, WHITE)

    # Place the score and level at location on the screen
    screen.blit(score_value, [0, 0])
    screen.blit(level_value, [0, 40])


# Portal + Walls helpers

# The snake game will have walls that appear as obstacles when you go up .
def spawn_walls(num):
    # This function creates new walls at random positions.
    new_walls = []
    for _ in range(num):
        # Random positions that align with the grid (multiples of 20)
        x = round(random.randrange(0, SCREEN_WIDTH - snakeBlock) / 20.0) * 20.0
        y = round(random.randrange(0, SCREEN_HEIGHT - snakeBlock) / 20.0) * 20.0
        new_walls.append([x, y])
    return new_walls


# =========================
#  MEMBER 4 – GAME LOOP (CONTROLS, MOVEMENT, COLLISIONS)
# =========================

# 9. Main Game Loop

# This is the heart of the game.
# It keeps running until the player quits or loses.
def game_loop():
    game_over = False  # When True, the game fully ends
    game_close = False  # When True, "Game Over" screen is displayed

    # Snake starting position middle of the screen
    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    # Variables to store movement direction
    x1_change = 0
    y1_change = 0

    # List to store all snake body coordinates
    snake_list = []
    length_of_snake = 1  # Initial snake length

    # Food setup
    food = spawn_food()  # Spawn first food
    # Randomly place food on the screen
    food_x = round(random.randrange(0, SCREEN_WIDTH - snakeBlock) / 20.0) * 20.0
    food_y = round(random.randrange(0, SCREEN_HEIGHT - snakeBlock) / 20.0) * 20.0

    # Start with no walls
    walls = []
    # Clock helps control how fast the game runs fps(freames per sec)
    clock = pygame.time.Clock()

    # Game progress variables
    speed = snakeSpeed  # Start at base speed
    level = 1            # Level counter
    score = 0            # Player score

    # Combo system variables
    last_eat_time = 0    # Records the last time the snake ate food
    combo_count = 0      # Tracks how many foods eaten quickly in a row

    # Mission system variables
    mission_active = False     # Whether a mission is currently running
    mission_start_time = 0     # Time when mission started
    mission_count = 0          # How many foods eaten during mission
    mission_message = ""       # Text like "Mission Complete!" or "Mission Failed!"
    mission_message_time = 0   # When the message started showing
    # Game loop 
 
    while not game_over:  # Keep looping until player quits the game
        # Game Over Screen
        # If the snake crashes into itself or a wall, we enter the "game over" screen.
        while game_close:
            # Fill screen with black color
            screen.fill(BLACK)
            # Display "Game Over!" message in red
            over_text = Gover_font.render("Game Over!", True, RED)
            screen.blit(over_text, [SCREEN_WIDTH / 4, SCREEN_HEIGHT / 3])
            # Display the final score
            final_score_text = scoreFont.render("Final Score: " + str(score), True, WHITE)
            screen.blit(final_score_text, [SCREEN_WIDTH / 4 + 50, SCREEN_HEIGHT / 2])
            pygame.display.update()
             # =========================
            #  MEMBER 1 – Samuel
             # =========================

            # Wait for user input: press Q to quit or C to play again
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()  # Restart the game
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
   
        # Player Input
        # Handle keyboard events for movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True  # Player closed the window
            if event.type == pygame.KEYDOWN:
                # Move left, right, up, or down depending on arrow key pressed
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snakeBlock
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snakeBlock
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snakeBlock
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snakeBlock
                    x1_change = 0
        # Check collision with borders (screen edges)
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True  # Snake hit the wall, game over
        # Move the snake
        # Update the snake's position by adding movement values
        x1 += x1_change
        y1 += y1_change
        # Fill background with black color each frame
        screen.fill(BLACK)
        # Draw all walls (brown rectangles)
        for w in walls:
            pygame.draw.rect(screen, BROWN, [w[0], w[1], snakeBlock, snakeBlock])
        # Draw the food (either red or yellow)
        pygame.draw.rect(screen, food["color"], [food_x, food_y, snakeBlock, snakeBlock])
# =========================
#  MEMBER 5 – MISSIONS, COMBO SYSTEM, & GAME OVER SCREEN
# =========================

        # Update snake body
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for w in walls:
            if x1 == w[0] and y1 == w[1]:
                game_close = True

        draw_snake(snake_list)
        display_score(score, level)

        if mission_active:
            elapsed = (pygame.time.get_ticks() - mission_start_time) / 1000
            mission_text = scoreFont.render(f"Mission: 3 foods in 10s ({mission_count})", True, YELLOW)
            screen.blit(mission_text, [SCREEN_WIDTH/2 - 150, 10])
            if elapsed > 10:
                mission_active = False
                mission_message = "Mission Failed!"
                mission_message_time = pygame.time.get_ticks()

        if mission_message != "":
            elapsed = (pygame.time.get_ticks() - mission_message_time) / 1000
            if elapsed < 3:
                color = GREEN if "Complete" in mission_message else RED
                msg = scoreFont.render(mission_message, True, color)
                screen.blit(msg, [SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 50])
            else:
                mission_message = ""

        pygame.display.update()


# =========================
#  MEMBER 6 – WALLS, DIFFICULTY & CONCLUSION
# =========================

        if x1 == food_x and y1 == food_y:
            current_time = pygame.time.get_ticks()
            if current_time - last_eat_time <= 3000:
                combo_count += 1
                score_bonus = combo_count * 2
            else:
                combo_count = 1
                score_bonus = 0
            last_eat_time = current_time

            score += food["effect"] + score_bonus
            length_of_snake += food["effect"]

            if mission_active:
                mission_count += 1
                if mission_count >= 3:
                    score += 10
                    mission_active = False
                    mission_message = "Mission Complete!"
                    mission_message_time = pygame.time.get_ticks()

            food = spawn_food()
            food_x = round(random.randrange(0, SCREEN_WIDTH - snakeBlock) / 20.0) * 20.0
            food_y = round(random.randrange(0, SCREEN_HEIGHT - snakeBlock) / 20.0) * 20.0

            if random.randint(1, 10) == 1 and not mission_active:
                mission_active = True
                mission_start_time = pygame.time.get_ticks()
                mission_count = 0

            if score % 5 == 0 and score > 0:
                speed += 2
                level += 1
                walls = spawn_walls(level)

        clock.tick(speed)

    pygame.quit()
    quit()
game_loop()

#Additionals
# run with (python3 Snake_game/snake.py)

#git add .
#git commit -m "made changes"
#git pull origin main or your branch name 
#git push origin main
#git pull origin main (Pulling changes)
#git remote -v


#press Q to quit or C to play again
#we use render instaed of print because we are using a library(pygame)..
