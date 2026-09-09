import asyncio
import pygame
import random

# אתחול Pygame והגדרת גופן לשימוש בהצגת טקסט במשחק.
pygame.init()
score_font = pygame.font.Font(None, 36)

WIDTH = 800
HEIGHT = 600

PLAYER_SIZE = 50
RADIUS = 30
BOOM_RADIUS = 25
SPEED = 5
RESET_BUTTON = pygame.Rect(10, HEIGHT - 50, 120, 40)
TOTAL_TIME = 40

# המשתנה score שומר את הניקוד הנוכחי של השחקן.
score = 0
show_start_message = True

# יצירת חלון המשחק וקביעת הכותרת שלו.
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
    # מחפשים מיקום אקראי שבו העיגול החדש לא ייגע באובייקטים אחרים.
    while True:
        # בוחרים את מרכז העיגול כך שכל העיגול יישאר בתוך המסך.
        candidate_x = random.randint(radius, WIDTH - radius)
        candidate_y = random.randint(radius, HEIGHT - radius)

        # מוצאים את הנקודה בריבוע שהכי קרובה למרכז העיגול.
        closest_x = max(x_re, min(candidate_x, x_re + PLAYER_SIZE))
        closest_y = max(y_re, min(candidate_y, y_re + PLAYER_SIZE))
        # במקום לחשב את המרחק בעזרת שורש ריבועי, משווים את ריבועי המרחקים.
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
            # מחזירים את המיקום רק לאחר שעבר את שתי בדיקות המרחק.
            return candidate_x, candidate_y


x_boom, y_boom = random_free_position(
    BOOM_RADIUS, x_cir, y_cir, RADIUS
)


def reset_game():
    # החזרת כל האובייקטים והניקוד למצב ההתחלתי.
    global x_re, y_re, x_cir, y_cir, x_boom, y_boom
    global score, was_touching, RADIUS, show_start_message

    RADIUS = 30
    x_re = WIDTH - PLAYER_SIZE
    y_re = 0
    x_cir = RADIUS
    y_cir = RADIUS
    score = 0
    was_touching = False
    show_start_message = True

    x_boom, y_boom = random_free_position(
        BOOM_RADIUS, x_cir, y_cir, RADIUS
    )
    # החזרת זמן חדש כדי שכפתור Reset יתחיל ספירה חדשה.
    return pygame.time.get_ticks()

async def main():
    global x_re, y_re, x_cir, y_cir, x_boom, y_boom
    global score, was_touching, RADIUS, show_start_message

    running = True
    was_touching = False
    # שמירת הזמן שבו המשחק התחיל, לצורך חישוב הספירה לאחור.
    game_start_time = pygame.time.get_ticks()

    while running:

        # הזמן מתחיל להיספר רק אחרי לחיצה על מקש.
        if show_start_message:
            remaining_seconds = TOTAL_TIME
        else:
            seconds_passed = (pygame.time.get_ticks() - game_start_time) // 1000
            remaining_seconds = max(0, TOTAL_TIME - seconds_passed)

        # EVENTS: בדיקה אם המשתמש סגר את החלון או לחץ על Reset.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False               
            if event.type == pygame.KEYDOWN and show_start_message:
                show_start_message = False
                game_start_time = pygame.time.get_ticks()
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and RESET_BUTTON.collidepoint(event.pos)
            ):
                game_start_time = reset_game()

        # INPUT: , הזזת הריבוע בעזרת מקשי החצים כל עוד נשאר זמן., המקשים יכולים לפעול במקביל ויכולים לא לפעול בכלל
        keys = pygame.key.get_pressed()

        # מאפשרים תנועה רק אחרי שהכיתוב נעלם ועדיין נשאר זמן במשחק.
        if not show_start_message and remaining_seconds > 0:
            if keys[pygame.K_LEFT]:
                x_re -= SPEED
            if keys[pygame.K_RIGHT]:
                x_re += SPEED
            if keys[pygame.K_UP]:
                y_re -= SPEED
            if keys[pygame.K_DOWN]:
                y_re += SPEED

        # DRAW: ניקוי המסך וציור כל האובייקטים מחדש בכל סיבוב.
        screen.fill((30, 30, 50)) #RGB

        if show_start_message:
            game_start_text = score_font.render(
                "Start game", True, (255, 255, 255)
            )
            game_start_position = game_start_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )
            screen.blit(game_start_text, game_start_position)

        pygame.draw.rect(
            screen,
            (255, 200, 50),
            (x_re, y_re, PLAYER_SIZE, PLAYER_SIZE)
        )

        pygame.draw.circle(
            screen,
            (50, 200, 80),
            (x_cir, y_cir), RADIUS #רדיוס הוא חצי מכל האורך כלומר חצי מהקוטר
        )

        # עיגול אדום, שמרכזו נמצא במיקום מסוים בצירי X ו-Y, וברדיוס של 25 פיקסלים
        pygame.draw.circle(
            screen,
            (220, 50, 50),
            (x_boom, y_boom), BOOM_RADIUS
        )
        # מגבילים את הריבוע כדי שלא יוכל לצאת מגבולות החלון.
        x_re = max(0, min(x_re, WIDTH - PLAYER_SIZE))
        y_re = max(0, min(y_re, HEIGHT - PLAYER_SIZE))

        # מגבילים גם את העיגול, לפי הרדיוס שלו, כדי שלא ייחתך בקצה המסך.
        x_cir = max(RADIUS, min(x_cir, WIDTH - RADIUS))
        y_cir = max(RADIUS, min(y_cir, HEIGHT - RADIUS))

        # בודקים אם המרחק בין מרכז העיגול לנקודה הקרובה בריבוע קטן מהרדיוס.
        closest_x = max(x_re, min(x_cir, x_re + PLAYER_SIZE))
        closest_y = max(y_re, min(y_cir, y_re + PLAYER_SIZE))
        distance_x = x_cir - closest_x
        distance_y = y_cir - closest_y
        is_touching = (
            distance_x * distance_x + distance_y * distance_y
            <= RADIUS ** 2
        )

        # אותה בדיקה עבור העיגול האדום, שמעניש את השחקן במגע.
        boom_closest_x = max(x_re, min(x_boom, x_re + PLAYER_SIZE))
        boom_closest_y = max(y_re, min(y_boom, y_re + PLAYER_SIZE))
        boom_distance_x = x_boom - boom_closest_x
        boom_distance_y = y_boom - boom_closest_y
        is_touching_boom = (
            boom_distance_x * boom_distance_x
            + boom_distance_y * boom_distance_y
            <= BOOM_RADIUS ** 2
        )

        # אם העיגול נגע בריבוע, מוסיפים נקודה ומעבירים את העיגולים.
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

        # אם הריבוע נגע בעיגול האדום, מורידים נקודה ומעבירים אותו.
        if is_touching_boom:
            score -= 1
            print(f"Score: {score}")
            x_boom, y_boom = random_free_position(
                BOOM_RADIUS, x_cir, y_cir, RADIUS
            )


        # הצגת הניקוד בפינה הימנית העליונה.
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        score_position = score_text.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(score_text, score_position)

        # הצגת הזמן שנותר בפינה השמאלית העליונה.
        timer_text = score_font.render(
            f"Time left: {remaining_seconds}", True, (255, 255, 255)
        )
        screen.blit(timer_text, (10, 10))

        # כשהזמן נגמר, מציגים הודעה ומפסיקים את תנועת הריבוע.
        if remaining_seconds == 0:
            time_end_text = score_font.render(
                "Time's up!", True, (255, 255, 255))
            game_over_text = score_font.render(
                "Game Over", True, (255, 255, 255))
            final_score = score_font.render(
                            f"Final Score: {score}", True, (255, 255, 255))
            time_end_position = time_end_text.get_rect(
                center=(WIDTH // 2, (HEIGHT // 2)-45)
            )
            game_over_position = game_over_text.get_rect(
                center=(WIDTH // 2, (HEIGHT // 2)-15))
            final_score_position = final_score.get_rect(
                            center=(WIDTH // 2, (HEIGHT // 2)+15))
            screen.blit(game_over_text, game_over_position)
            screen.blit(time_end_text, time_end_position)
            screen.blit(final_score, final_score_position)
            

        # ציור כפתור Reset והטקסט שבתוכו.
        pygame.draw.rect(screen, (70, 130, 220), RESET_BUTTON)
        reset_text = score_font.render("Reset", True, (255, 255, 255))
        reset_position = reset_text.get_rect(center=RESET_BUTTON.center)
        screen.blit(reset_text, reset_position)
        
        pygame.display.flip()

        # Required for running Pygame in the browser
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
