import asyncio
import pygame
import random

pygame.init()
score_font = pygame.font.Font(None, 36)

WIDTH = 800
HEIGHT = 600

PLAYER_SIZE = 50
RADIUS = 30
BOOM_RADIUS = 25
SPEED = 5
RESET_BUTTON = pygame.Rect(10, HEIGHT - 50, 120, 40)
GAME_DURATION = 20

score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Game")

#ריבוע מיקום על הלוח
x_re = WIDTH - PLAYER_SIZE
y_re = 0

#עיגול מיקום על הלוח
x_cir = RADIUS
y_cir = RADIUS

#עיגול boom מיקום על הלוח
x_boom = WIDTH // 2
y_boom = HEIGHT // 2

was_touching = False #אם הריבוע והעיגול נוגעים


def random_free_position(radius, other_x, other_y, other_radius):
    while True:
        candidate_x = random.randint(radius, WIDTH - radius)
        candidate_y = random.randint(radius, HEIGHT - radius)

        closest_x = max(x_re, min(candidate_x, x_re + PLAYER_SIZE))
        closest_y = max(y_re, min(candidate_y, y_re + PLAYER_SIZE))
        square_distance = (
            (candidate_x - closest_x) ** 2
            + (candidate_y - closest_y) ** 2
        )
        circles_distance = (
            (candidate_x - other_x) ** 2
            + (candidate_y - other_y) ** 2
        )

        # > מוודא שהעיגול לא נוגע בריבוע, אפילו לא בקצה
        if (
            square_distance > radius ** 2
            and circles_distance > (radius + other_radius) ** 2):
            return candidate_x, candidate_y


x_boom, y_boom = random_free_position(
    BOOM_RADIUS, x_cir, y_cir, RADIUS
)


def reset_game():
    global x_re, y_re, x_cir, y_cir, x_boom, y_boom
    global score, was_touching, RADIUS

    RADIUS = 30
    x_re = WIDTH - PLAYER_SIZE
    y_re = 0
    x_cir = RADIUS
    y_cir = RADIUS
    score = 0
    was_touching = False
    x_boom, y_boom = random_free_position(
        BOOM_RADIUS, x_cir, y_cir, RADIUS
    )

async def main():
    global x_re, y_re, x_cir, y_cir, x_boom, y_boom
    global score, was_touching, RADIUS

    running = True
    was_touching = False
    game_start_time = pygame.time.get_ticks()

    while running:

        seconds_passed = (pygame.time.get_ticks() - game_start_time) // 1000
        remaining_seconds = max(0, GAME_DURATION - seconds_passed)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False               
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and RESET_BUTTON.collidepoint(event.pos)
            ):
                reset_game()

        # INPUT
        keys = pygame.key.get_pressed()

        if remaining_seconds > 0:
            if keys[pygame.K_LEFT]:
                x_re -= SPEED
            if keys[pygame.K_RIGHT]:
                x_re += SPEED
            if keys[pygame.K_UP]:
                y_re -= SPEED
            if keys[pygame.K_DOWN]:
                y_re += SPEED

        # DRAW
        screen.fill((30, 30, 50)) #RGB

        pygame.draw.rect(
            screen,
            (255, 200, 50),
            (x_re, y_re, PLAYER_SIZE, PLAYER_SIZE)
        )

        pygame.draw.circle(
            screen,
            (100, 200, 255),
            (x_cir, y_cir), RADIUS #רדיוס הוא חצי מכל האורך כלומר חצי מהקוטר
        )

        # עיגול אדום, שמרכזו נמצא במיקום מסוים בצירי X ו-Y, וברדיוס של 25 פיקסלים
        pygame.draw.circle(
            screen,
            (220, 50, 50),
            (x_boom, y_boom), BOOM_RADIUS
        )
        #ריבוע
        x_re = max(0, min(x_re, WIDTH - PLAYER_SIZE))
        y_re = max(0, min(y_re, HEIGHT - PLAYER_SIZE))

        #עיגול
        x_cir = max(RADIUS, min(x_cir, WIDTH - RADIUS))
        y_cir = max(RADIUS, min(y_cir, HEIGHT - RADIUS))

        # בדיקה מדויקת אם הריבוע נוגע בכדור
        closest_x = max(x_re, min(x_cir, x_re + PLAYER_SIZE))
        closest_y = max(y_re, min(y_cir, y_re + PLAYER_SIZE))
        distance_x = x_cir - closest_x
        distance_y = y_cir - closest_y
        is_touching = (
            distance_x * distance_x + distance_y * distance_y
            <= RADIUS ** 2
        )

        boom_closest_x = max(x_re, min(x_boom, x_re + PLAYER_SIZE))
        boom_closest_y = max(y_re, min(y_boom, y_re + PLAYER_SIZE))
        boom_distance_x = x_boom - boom_closest_x
        boom_distance_y = y_boom - boom_closest_y
        is_touching_boom = (
            boom_distance_x * boom_distance_x
            + boom_distance_y * boom_distance_y
            <= BOOM_RADIUS ** 2
        )

        #אם הכדור נוגע בריבוע event
        if is_touching and not was_touching:
            score += 1
            RADIUS = random.randint(20, 50)
            print(f"Score: {score}")
            x_cir, y_cir = random_free_position(
                RADIUS, x_boom, y_boom, BOOM_RADIUS
            )
            x_boom, y_boom = random_free_position(
                BOOM_RADIUS, x_cir, y_cir, RADIUS
            )

        if is_touching_boom:
            score -= 1
            print(f"Score: {score}")
            x_boom, y_boom = random_free_position(
                BOOM_RADIUS, x_cir, y_cir, RADIUS
            )


        # f מאפשר לשלב את ערך score בתוך הטקסט שמוצג בפינה הימנית העליונה
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        score_position = score_text.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(score_text, score_position)

        timer_text = score_font.render(
            f"Time: {remaining_seconds}", True, (255, 255, 255)
        )
        screen.blit(timer_text, (10, 10))

        if remaining_seconds == 0:
            game_over_text = score_font.render(
                "Time's up!", True, (255, 255, 255)
            )
            game_over_position = game_over_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )
            screen.blit(game_over_text, game_over_position)

        pygame.draw.rect(screen, (70, 130, 220), RESET_BUTTON)
        reset_text = score_font.render("Reset", True, (255, 255, 255))
        reset_position = reset_text.get_rect(center=RESET_BUTTON.center)
        screen.blit(reset_text, reset_position)
        
        pygame.display.flip()

        # Required for running Pygame in the browser
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
import asyncio
import pygame
import random

pygame.init()
score_font = pygame.font.Font(None, 36)

WIDTH = 800
HEIGHT = 600

PLAYER_SIZE = 50
RADIUS = 30
BOOM_RADIUS = 25
SPEED = 5
RESET_BUTTON = pygame.Rect(10, HEIGHT - 50, 120, 40)

score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Game")

#ריבוע מיקום על הלוח
x_re = WIDTH - PLAYER_SIZE
y_re = 0

#עיגול מיקום על הלוח
x_cir = RADIUS
y_cir = RADIUS

#עיגול boom מיקום על הלוח
x_boom = WIDTH // 2
y_boom = HEIGHT // 2

# איזה אובייקט בשליטה? True = ריבוע, False = עיגול
controlling_rect = True

was_touching = False #אם הריבוע והעיגול נוגעים


def random_free_position(radius, other_x, other_y, other_radius):
    while True:
        candidate_x = random.randint(radius, WIDTH - radius)
        candidate_y = random.randint(radius, HEIGHT - radius)

        closest_x = max(x_re, min(candidate_x, x_re + PLAYER_SIZE))
        closest_y = max(y_re, min(candidate_y, y_re + PLAYER_SIZE))
        square_distance = (
            (candidate_x - closest_x) ** 2
            + (candidate_y - closest_y) ** 2
        )
        circles_distance = (
            (candidate_x - other_x) ** 2
            + (candidate_y - other_y) ** 2
        )

        # > מוודא שהעיגול לא נוגע בריבוע, אפילו לא בקצה
        if (
            square_distance > radius ** 2
            and circles_distance > (radius + other_radius) ** 2):
            return candidate_x, candidate_y


x_boom, y_boom = random_free_position(
    BOOM_RADIUS, x_cir, y_cir, RADIUS
)


def reset_game():
    global x_re, y_re, x_cir, y_cir, x_boom, y_boom
    global score, was_touching, RADIUS

    RADIUS = 30
    x_re = WIDTH - PLAYER_SIZE
    y_re = 0
    x_cir = RADIUS
    y_cir = RADIUS
    score = 0
    was_touching = False
    x_boom, y_boom = random_free_position(
        BOOM_RADIUS, x_cir, y_cir, RADIUS
    )

async def main():
    global x_re, y_re, x_cir, y_cir, x_boom, y_boom
    global controlling_rect, score, was_touching, RADIUS

    running = True
    was_touching = False

    while running:

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False               
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and RESET_BUTTON.collidepoint(event.pos)
            ):
                reset_game()

        # INPUT
        keys = pygame.key.get_pressed()

        if controlling_rect: #אם זה על מצב אמת
            #ריבוע
            if keys[pygame.K_LEFT]:
                x_re -= SPEED
            if keys[pygame.K_RIGHT]:
                x_re += SPEED
            if keys[pygame.K_UP]:
                y_re -= SPEED
            if keys[pygame.K_DOWN]:
                y_re += SPEED

        else:
            #עיגול
            if keys[pygame.K_LEFT]:
                x_cir -= SPEED
            if keys[pygame.K_RIGHT]:
                x_cir += SPEED
            if keys[pygame.K_UP]:
                y_cir -= SPEED
            if keys[pygame.K_DOWN]:
                y_cir += SPEED

        # DRAW
        screen.fill((30, 30, 50)) #RGB

        pygame.draw.rect(
            screen,
            (255, 200, 50),
            (x_re, y_re, PLAYER_SIZE, PLAYER_SIZE)
        )

        pygame.draw.circle(
            screen,
            (100, 200, 255),
            (x_cir, y_cir), RADIUS #רדיוס הוא חצי מכל האורך כלומר חצי מהקוטר
        )

        # עיגול אדום, שמרכזו נמצא במיקום מסוים בצירי X ו-Y, וברדיוס של 25 פיקסלים
        pygame.draw.circle(
            screen,
            (220, 50, 50),
            (x_boom, y_boom), BOOM_RADIUS
        )
        #ריבוע
        x_re = max(0, min(x_re, WIDTH - PLAYER_SIZE))
        y_re = max(0, min(y_re, HEIGHT - PLAYER_SIZE))

        #עיגול
        x_cir = max(RADIUS, min(x_cir, WIDTH - RADIUS))
        y_cir = max(RADIUS, min(y_cir, HEIGHT - RADIUS))

        # בדיקה מדויקת אם הריבוע נוגע בכדור
        closest_x = max(x_re, min(x_cir, x_re + PLAYER_SIZE))
        closest_y = max(y_re, min(y_cir, y_re + PLAYER_SIZE))
        distance_x = x_cir - closest_x
        distance_y = y_cir - closest_y
        is_touching = (
            distance_x * distance_x + distance_y * distance_y
            <= RADIUS ** 2
        )

        boom_closest_x = max(x_re, min(x_boom, x_re + PLAYER_SIZE))
        boom_closest_y = max(y_re, min(y_boom, y_re + PLAYER_SIZE))
        boom_distance_x = x_boom - boom_closest_x
        boom_distance_y = y_boom - boom_closest_y
        is_touching_boom = (
            boom_distance_x * boom_distance_x
            + boom_distance_y * boom_distance_y
            <= BOOM_RADIUS ** 2
        )

        #אם הכדור נוגע בריבוע event
        if is_touching and not was_touching:
            score += 1
            RADIUS = random.randint(20, 50)
            print(f"Score: {score}")
            x_cir, y_cir = random_free_position(
                RADIUS, x_boom, y_boom, BOOM_RADIUS
            )
            x_boom, y_boom = random_free_position(
                BOOM_RADIUS, x_cir, y_cir, RADIUS
            )

        if is_touching_boom:
            score -= 1
            print(f"Score: {score}")
            x_boom, y_boom = random_free_position(
                BOOM_RADIUS, x_cir, y_cir, RADIUS
            )


        # f מאפשר לשלב את ערך score בתוך הטקסט שמוצג בפינה הימנית העליונה
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        score_position = score_text.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(score_text, score_position)

        pygame.draw.rect(screen, (70, 130, 220), RESET_BUTTON)
        reset_text = score_font.render("Reset", True, (255, 255, 255))
        reset_position = reset_text.get_rect(center=RESET_BUTTON.center)
        screen.blit(reset_text, reset_position)
        
        pygame.display.flip()

        # Required for running Pygame in the browser
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
