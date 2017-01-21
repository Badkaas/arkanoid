import time
import pygame
from pygame.locals import *


# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (10, 10, 10)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SURFACE_W, SURFACE_H = 720, 480,
MARGIN, MARGIN_TOP = 13, 20,

CHAR_POS_Y = 425
CHAR_W, CHAR_H = 56, 9

BALL_W, BALL_H, BALL_Y = 13, 14, 384

BLOCK_W, BLOCK_H = 55, 25
BLOCKS_GRID, BLOCKS_COLUMNS = 44, 11
BLOCK_MARGIN_TOP , BLOCKS_MARGIN_LEFT = 36, 29

LARGE_FONT_SIZE = 100
MEDIUM_FONT_SIZE = 36
SMALL_FONT_SISE = 28

LIFE_CURSOR_W, LIFE_CURSOR_H = 14, 15
LIFE_OFFSET_Y = 7
SCORE_OFFSET_X, SCORE_OFFSET_Y = 2, 3
RULE_OFFSET_Y = 28

SPEED = 300

timer = pygame.time.Clock()
pygame.time.set_timer(USEREVENT, 1000)


class Ball(pygame.Rect): pass
class Char(pygame.Rect): pass

ball = Ball(0, BALL_Y,BALL_H,BALL_W)
char = Char(0,CHAR_POS_Y,CHAR_W,CHAR_H)

game_text = lambda _font, _str, _color: _font.render( _str , 1, _color)

def gen_pos(arg, dt, increase=True):
    if not increase:
        arg -=  SPEED * dt
    else:
        arg +=  SPEED * dt
    yield arg

def main(score=0, life=4, char_right=None,
         ball_v=False, ball_h=None):

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((SURFACE_W, SURFACE_H))
    pygame.display.set_caption('Arkanoid')


    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(WHITE)

    # __


    char.centerx = background.get_rect().centerx
    ball.centerx = background.get_rect().centerx

    # Display some text
    large_font = pygame.font.Font(None, LARGE_FONT_SIZE)
    medium_font = pygame.font.Font(None, MEDIUM_FONT_SIZE)
    small_font = pygame.font.Font(None, SMALL_FONT_SISE)

    fps_str = '{}'.format(timer.get_fps())
    fps_text = game_text(medium_font, fps_str, GRAY)
    fps_text_pos = fps_text.get_rect()
    fps_text_pos.centerx = background.get_rect().centerx + 2
    fps_text_pos.y = 3

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    game_over = False

    while not game_over:

        # Exit events
        # -------------------------------------------------------------
        events = pygame.event.get()
        for event in events:

            if event.type is KEYUP and event.key == K_ESCAPE \
               or event.type is pygame.QUIT:
                game_over = True

            # Detect events
            # ------------------------------------------------------

            elif event.type == KEYDOWN and event.key == K_q:
                char_right = False
            elif event.type == KEYUP and event.key == K_q:
                char_right = None
            elif event.type == KEYDOWN and event.key == K_d:
                char_right = True
            elif event.type == KEYUP and event.key == K_d:
                char_right = None
            elif event.type == KEYUP and event.key == K_p:
                pass
            elif event.type == USEREVENT:
                fps_str = '{:.2f}'.format(timer.get_fps())
                fps_text = game_text(medium_font, fps_str, GRAY)


        # Update scene
        # --------------------------------------------------------------
        dt = timer.tick(60)/1000

        if ball_h is not None:
            ball_pos_x = gen_pos(ball.x, dt, increase=ball_h)
            ball_x_motion = next(ball_pos_x)

            if ball_x_motion < 0:
                ball_h = not ball_h
            elif ball_x_motion > SURFACE_W - BALL_W:
                ball_h = not ball_h
            else:
                ball.x = ball_x_motion

        if ball_v is not None:
            ball_pos_y = gen_pos(ball.y, dt, increase=ball_v)
            ball_y_motion = next(ball_pos_y)

            if ball_y_motion > SURFACE_H:
                ball.centerx = SURFACE_W // 2
                ball.y = BALL_Y
                ball_h = None
                ball_v = True

            elif ball_y_motion < MARGIN_TOP:
                ball_v = not ball_v

            else:
                ball.y = ball_y_motion

        if ball.colliderect(char):
            ball_v = False

            if ball_h is None:
                ball_h = True


        if char_right is not None:
            char_pos_x = gen_pos(char.x, dt, increase=char_right)
            char_x_motion = next(char_pos_x)

            if char_x_motion < MARGIN:
                char.x = MARGIN + 1
            elif char_x_motion > SURFACE_W - MARGIN - CHAR_W:
                char.x = SURFACE_W - MARGIN - CHAR_W - 1
            else:
                char.x = char_x_motion

        # Draw screen
        # --------------------------------------------------------------
        screen.blit(background, (0, 0))

        #text
        screen.blit(fps_text, fps_text_pos)

        #ball
        pygame.draw.rect(screen, RED, ball)

        #char
        pygame.draw.rect(screen, BLACK, char)

        # Blit everything to the screen
        # --------------------------------------------------------------

        pygame.display.update()


if __name__ == '__main__': main()
