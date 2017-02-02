import time
import pygame
from pygame.locals import *

pygame.init()

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
BLOCKS_MARGIN_TOP , BLOCKS_MARGIN_LEFT = 36, 29

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
class Block(pygame.Rect): pass

ball = Ball(0, BALL_Y, BALL_H, BALL_W)
char = Char(0, CHAR_POS_Y, CHAR_W, CHAR_H)

# __

blocks = []

# append blocks list
for n in range (BLOCKS_GRID):
    _x = n % BLOCKS_COLUMNS * (BLOCK_W + 5) + BLOCKS_MARGIN_LEFT
    _y = n // BLOCKS_COLUMNS * (BLOCK_H + 5) + BLOCKS_MARGIN_TOP
    block = Block(_x, _y, BLOCK_W, BLOCK_H)
    blocks.append((_x, _y))

# __

cur_blocks = blocks.copy()


game_text = lambda _font, _str, _color: _font.render( _str , 1, _color)

def ne_pos(arg, dt, increase=True):
    return arg + SPEED * dt * (1 if increase else -1)

def main(score=0, life=4, char_right=None,
         ball_v=None, ball_h=None):

    # Initialise screen
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

        dt = min(timer.tick(60)/1000, 0.010)

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
                fps_str = '{:.2f} ({})'.format(timer.get_fps(), dt)
                fps_text = game_text(medium_font, fps_str, GRAY)


        # Update scene
        # --------------------------------------------------------------

        if ball_v is not None:
            ball_y_motion = gen_pos(ball.y, dt, increase=ball_v)

            if ball_y_motion > SURFACE_H:
                ball.centerx = SURFACE_W // 2
                ball.y = BALL_Y
                ball_h = None
                ball_v = False

            elif ball_y_motion < MARGIN_TOP:
                ball_v = not ball_v

            else:
                ball.y = ball_y_motion
        else:
            ball_v = False

        if ball_h is not None:
            ball_x_motion = gen_pos(ball.x, dt, increase=ball_h)

            if ball_x_motion < 0:
                ball_h = not ball_h

            elif ball_x_motion > SURFACE_W - BALL_W:
                ball_h = not ball_h

            else:
                ball.x = ball_x_motion

        if char.colliderect(ball):
            if ball_v:
                ball_v = not ball_v

            if ball_h is None:
                ball_h = True

        for _x, _y in (cur_blocks):
            block = Block(_x,_y , BLOCK_W, BLOCK_H)
            if ball.colliderect(block):
                cur_blocks.remove((block.x,block.y))
                if ball.top < block.top or ball.bottom > block.bottom:
                    if ball.x < block.x:
                        ball_h = not ball_h
                        ball.right = block.left - 1

                    elif ball.x > block.x + BLOCK_W - BALL_W:
                        ball_h = not ball_h
                        ball.left = block.right + 1

                    elif ball.top < block.top:
                        ball_v = not ball_v
                        ball.bottom = block.top + 1

                    else:
                        ball_v = not ball_v
                        ball.top = block.bottom + 1
                    break

                else:
                    ball_h = not ball_v

        if char_right is not None:
            char_x_motion = gen_pos(char.x, dt, increase=char_right)

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

        # blocs
        for xE, yE in cur_blocks:
            block = Block(xE, yE, BLOCK_W, BLOCK_H)
            pygame.draw.rect(screen, BLACK, block)

        # Blit everything to the screen
        # --------------------------------------------------------------

        pygame.display.update()


if __name__ == '__main__': main()
