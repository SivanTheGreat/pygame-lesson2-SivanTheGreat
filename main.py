import asyncio
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

PLAYER_SIZE = 50
SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Game")

#ריבוע
x_re = WIDTH - PLAYER_SIZE
y_re = 0

#עיגול
x_cir = 0
y_cir = 0

# איזה אובייקט בשליטה? True = ריבוע, False = עיגול
controlling_rect = True

async def main():
    global x_re, y_re, x_cir, y_cir ,controlling_rect

    running = True

    while running:

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    controlling_rect = not controlling_rect  # החלף
                if event.key == pygame.K_s:
                # החלף בין מיקומי העיגול והריבוע
                    x_re, x_cir = x_cir, x_re
                    y_re, y_cir = y_re, y_cir

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
            (x_cir, y_cir), PLAYER_SIZE //2 #רדיוס הוא חצי מכל האורך כלומר חצי מהקוטר
        )
        #ריבוע
        x_re = max(0, min(x_re, WIDTH - PLAYER_SIZE))
        y_re = max(0, min(y_re, HEIGHT - PLAYER_SIZE))

        #עיגול
        x_cir = max(PLAYER_SIZE // 2, min(x_cir, WIDTH - PLAYER_SIZE // 2))
        y_cir = max(PLAYER_SIZE // 2, min(y_cir, HEIGHT - PLAYER_SIZE // 2))
        
        pygame.display.flip()

        # Required for running Pygame in the browser
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
