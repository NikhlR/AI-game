import pygame
import random

pygame.init()
pygame.mixer.init()

# -------------------------
# SCREEN SETTINGS
# -------------------------
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bike Racing Game")

clock = pygame.time.Clock()

# -------------------------
# FONT
# -------------------------
font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 70)

# -------------------------
# HIGH SCORE
# -------------------------
with open("scores/highscore.txt", "r") as file:
    high_score = int(file.read())

# -------------------------
# IMAGES
# -------------------------
bike_img = pygame.image.load("assets/bike.png").convert_alpha()
bike_img = pygame.transform.scale(bike_img, (50, 80))

car_img = pygame.image.load("assets/car.png").convert_alpha()
car_img = pygame.transform.scale(car_img, (50, 80))

# -------------------------
# SOUNDS
# -------------------------
pygame.mixer.music.load("sounds/bg_music.mp3")
crash_sound = pygame.mixer.Sound("sounds/crash.mp3")

# -------------------------
# GAME VARIABLES
# -------------------------
bike_x = 375
bike_y = 500
bike_speed = 5

enemy_speed = 6

enemies = [
    [250, -100],
    [350, -300],
    [450, -500]
]

line_y = 0
score = 0

running = True
game_over = False
menu = True

# -------------------------
# MAIN LOOP
# -------------------------
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # MENU CONTROLS
            if menu:

                if event.key == pygame.K_RETURN:
                    menu = False
                    pygame.mixer.music.play(-1)

                elif event.key == pygame.K_ESCAPE:
                    running = False

            # RESTART
            elif game_over and event.key == pygame.K_r:

                bike_x = 375
                bike_y = 500

                score = 0
                enemy_speed = 6

                enemies = [
                    [250, -100],
                    [350, -300],
                    [450, -500]
                ]

                game_over = False
                pygame.mixer.music.play(-1)

    # -------------------------
    # MENU SCREEN
    # -------------------------
    if menu:

        screen.fill((20, 20, 20))

        title = title_font.render(
            "BIKE RACING GAME",
            True,
            (255, 255, 0)
        )

        hs = font.render(
            f"High Score: {high_score}",
            True,
            (255, 255, 255)
        )

        start_text = font.render(
            "Press ENTER to Start",
            True,
            (0, 255, 0)
        )

        exit_text = font.render(
            "Press ESC to Exit",
            True,
            (255, 100, 100)
        )

        screen.blit(title, (140, 180))
        screen.blit(hs, (290, 270))
        screen.blit(start_text, (240, 340))
        screen.blit(exit_text, (255, 390))

    elif not game_over:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            bike_x -= bike_speed

        if keys[pygame.K_RIGHT]:
            bike_x += bike_speed

        if bike_x < 220:
            bike_x = 220

        if bike_x > 530:
            bike_x = 530

        line_y += 5

        if line_y > 60:
            line_y = 0

        for enemy in enemies:

            enemy[1] += enemy_speed

            if enemy[1] > HEIGHT:

                enemy[1] = -100
                enemy[0] = random.choice(
                    [250, 350, 450, 550]
                )

                score += 1

                if score % 10 == 0:
                    enemy_speed += 1

        bike_rect = pygame.Rect(
            bike_x,
            bike_y,
            50,
            80
        )

        for enemy in enemies:

            enemy_rect = pygame.Rect(
                enemy[0],
                enemy[1],
                50,
                80
            )

            if bike_rect.colliderect(enemy_rect):

                crash_sound.play()
                pygame.mixer.music.stop()

                if score > high_score:

                    high_score = score

                    with open(
                        "scores/highscore.txt",
                        "w"
                    ) as file:

                        file.write(str(high_score))

                game_over = True

        # DRAW GAME
        screen.fill((34, 139, 34))

        pygame.draw.rect(
            screen,
            (70, 70, 70),
            (200, 0, 400, HEIGHT)
        )

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (200, 0),
            (200, HEIGHT),
            5
        )

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (600, 0),
            (600, HEIGHT),
            5
        )

        for y in range(-60, HEIGHT, 60):

            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (395, y + line_y, 10, 40)
            )

        screen.blit(bike_img, (bike_x, bike_y))

        for enemy in enemies:
            screen.blit(car_img, (enemy[0], enemy[1]))

        score_text = font.render(
            f"Score: {score}",
            True,
            (255, 255, 255)
        )

        high_text = font.render(
            f"High Score: {high_score}",
            True,
            (255, 255, 0)
        )

        screen.blit(score_text, (20, 20))
        screen.blit(high_text, (20, 60))

    else:

        screen.fill((20, 20, 20))

        over_text = title_font.render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )

        score_text = font.render(
            f"Final Score: {score}",
            True,
            (255, 255, 255)
        )

        restart_text = font.render(
            "Press R to Restart",
            True,
            (255, 255, 255)
        )

        screen.blit(over_text, (210, 220))
        screen.blit(score_text, (300, 320))
        screen.blit(restart_text, (240, 380))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
