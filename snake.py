import pygame
import random

# ---------------------------
# 1. Initialize Pygame
# ---------------------------
pygame.init()

# ---------------------------
# 2. Screen setup
# ---------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # game window
pygame.display.set_caption("Snake Game")  # window title

# ---------------------------
# 3. Colors (R, G, B values)
# ---------------------------
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# ---------------------------
# 4. Snake properties
# ---------------------------
snake_block = 20   # size of each square in the snake
snake_speed = 5    # starting speed

# ---------------------------
# 5. Fonts for score & messages
# ---------------------------
score_font = pygame.font.SysFont("comicsansms", 35)
game_over_font = pygame.font.SysFont("comicsansms", 70)

# ---------------------------
# 6. Function to show score and level
# ---------------------------
def display_score(score, level):
    score_value = score_font.render("Score: " + str(score), True, WHITE)
    level_value = score_font.render("Level: " + str(level), True, WHITE)
    screen.blit(score_value, [0, 0])
    screen.blit(level_value, [0, 40])

# ---------------------------
# 7. Function to draw the snake
# ---------------------------
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

# ---------------------------
# 8. Function to spawn food
# ---------------------------
def spawn_food():
    """
    Returns a food object with color and effect.
    Normal food (red) appears most of the time.
    Bonus food (yellow) appears rarely.
    """
    if random.randint(1, 5) == 5:  # 1 in 5 chance → bonus food
        return {"color": YELLOW, "effect": 2}
    else:  # otherwise normal food
        return {"color": RED, "effect": 1}

# ---------------------------
# 9. Main Game Loop
# ---------------------------
def game_loop():
    game_over = False
    game_close = False

    # Snake starting position (center of the screen)
    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2
    x1_change = 0
    y1_change = 0
    snake_list = []         # stores the body of the snake
    length_of_snake = 1     # starting length

    # First random food
    food = spawn_food()
    food_x = round(random.randrange(0, SCREEN_WIDTH - snake_block) / 20.0) * 20.0
    food_y = round(random.randrange(0, SCREEN_HEIGHT - snake_block) / 20.0) * 20.0

    # Clock controls game speed
    clock = pygame.time.Clock()

    # Speed and level
    speed = snake_speed
    level = 1

    # ---------------------------
    # Game loop starts here
    # ---------------------------
    while not game_over:

        # ---------------------------
        # Game Over Screen
        # ---------------------------
        while game_close:
            screen.fill(BLACK)
            over_text = game_over_font.render("Game Over!", True, RED)
            screen.blit(over_text, [SCREEN_WIDTH / 4, SCREEN_HEIGHT / 3])
            final_score_text = score_font.render("Final Score: " + str(length_of_snake - 1), True, WHITE)
            screen.blit(final_score_text, [SCREEN_WIDTH / 4 + 50, SCREEN_HEIGHT / 2])
            pygame.display.update()

            # Waiting for player input after game over
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:   # press Q to quit
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:   # press C to play again
                        game_loop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        # ---------------------------
        # Player Input (controls)
        # ---------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # clicking X closes the game
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Move left (only if not moving right already)
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                # Move right
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                # Move up
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                # Move down
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # ---------------------------
        # Check collision with walls
        # ---------------------------
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        # ---------------------------
        # Move the snake
        # ---------------------------
        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)

        # Draw food
        pygame.draw.rect(screen, food["color"], [food_x, food_y, snake_block, snake_block])

        # Update snake body
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]   # remove last piece to keep snake length

        # ---------------------------
        # Check self-collision
        # ---------------------------
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        # Draw snake and score
        draw_snake(snake_list)
        display_score(length_of_snake - 1, level)
        pygame.display.update()

        # ---------------------------
        # Check if snake eats food
        # ---------------------------
        if x1 == food_x and y1 == food_y:
            length_of_snake += food["effect"]  # grow depending on food type

            # Spawn new random food
            food = spawn_food()
            food_x = round(random.randrange(0, SCREEN_WIDTH - snake_block) / 20.0) * 20.0
            food_y = round(random.randrange(0, SCREEN_HEIGHT - snake_block) / 20.0) * 20.0

            # Every 5 points → increase speed and level
            if (length_of_snake - 1) % 5 == 0 and length_of_snake > 1:
                speed += 2
                level += 1

        # Control game speed
        clock.tick(speed)

    # Quit pygame
    pygame.quit()
    quit()

# ---------------------------
# Start the game
# ---------------------------
game_loop()
