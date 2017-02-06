import time
import pygame
from pygame.locals import *

# Initialise Pygame
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
pygame.time.set_timer(USEREVENT, 250)

# Display some text
large_font = pygame.font.Font(None, LARGE_FONT_SIZE)
medium_font = pygame.font.Font(None, MEDIUM_FONT_SIZE)
small_font = pygame.font.Font(None, SMALL_FONT_SISE)



class Ball(pygame.Rect): pass
class Char(pygame.Rect): pass
class Block(pygame.Rect): pass
class LifeCursor(pygame.Rect): pass

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

game_text = lambda _font, _str, _color: _font.render( _str , 1, _color)

def new_pos(arg, dt, increase=True):
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

    cur_blocks = blocks.copy()

    # Game's text
    title_str = 'arkanoid'.capitalize()
    title = game_text(large_font, title_str, GRAY)
    title_pos = title.get_rect()
    title_pos.centerx = background.get_rect().centerx
    title_pos.centery = background.get_rect().centery

    rule_str = "Press q or d from right to left p for game and Esc for quit."

    rule = game_text(small_font, rule_str, RED)
    rule_pos = rule.get_rect()
    rule_pos.centerx = background.get_rect().centerx
    rule_pos.y = background.get_rect().centery + RULE_OFFSET_Y

    loser_str = 'game over'.upper()
    loser_text = game_text(large_font, loser_str, GRAY)
    loser_text_pos = loser_text.get_rect()
    loser_text_pos.centerx = background.get_rect().centerx + 2
    loser_text_pos.centery = background.get_rect().centery

    score = score
    cur_life = life

    score_str = "Score: {:05d}".format(score)
    score_text = game_text(medium_font, score_str, GRAY)
    score_text_pos = score_text.get_rect()
    score_text_pos.centerx = background.get_rect().centerx + 2
    score_text_pos.y = 3

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Training Mode Save System
    save_blocks = []
    save_game_pos = (ball.y, ball.x, ball_v, ball_h, char.x)

    # Event loop
    game_over = False
    death = False
    start = True

    while not game_over:

        dt = timer.tick(60)/1000

        # Exit events
        # -------------------------------------------------------------
        events = pygame.event.get()
        for event in events:

            if event.type == KEYDOWN and event.key in (K_q, K_d):
                char_right = event.key == K_d
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    game_over = True
                elif event.key in (K_q, K_d):
                    char_right = None
                elif event.key == K_p:
                    if not start:
                        save_game_pos = (ball.y, ball.x, ball_v, ball_h, char.x)
                        save_blocks = cur_blocks.copy()

                    else:
                        cur_blocks = save_blocks.copy()

                        ball.y, ball.x, ball_v, ball_h, char.x = save_game_pos 
                        save_blocks.clear()

                    if not death:
                        start = not start
                    else:
                        start = False
                        death = not death
                        cur_life = life
                        score = 0
                        ball_v = False
                        ball_h = None
                        ball.y = BALL_Y
                        ball.centerx = background.get_rect().centerx

            elif event.type == USEREVENT:
                score_str = "Score: {:05d}".format(score)
                score_text = game_text(medium_font, score_str, GRAY)

            elif event.type == pygame.QUIT:
                game_over = true

        # Update scene
        # --------------------------------------------------------------
        if not start and score == 0:
            cur_blocks = blocks.copy()

        if ball_v is not None:
            ball_y_motion = new_pos(ball.y, dt, increase=ball_v)

            if ball_y_motion > SURFACE_H:
                ball.centerx = SURFACE_W // 2
                ball.y = BALL_Y
                ball_h = None
                if not start:
                    cur_life -= 1

                if cur_life == 0:
                    death = not death


                if not death:
                    ball_v = False
                if start:
                    ball_v = True

            elif ball_y_motion < MARGIN_TOP:
                ball_v = not ball_v

            else:
                ball.y = ball_y_motion
        else:
            ball_v = False

        if ball_h is not None:
            ball_x_motion = new_pos(ball.x, dt, increase=ball_h)

            if ball_x_motion < 0:
                ball_h = not ball_h

            elif ball_x_motion > SURFACE_W - BALL_W:
                ball_h = not ball_h

            else:
                ball.x = ball_x_motion

        if char.colliderect(ball):
            if not death and not start:
                score += 10
            if ball_v:
                ball_v = not ball_v

            if ball_h is None:
                ball_h = True

        for _x, _y in (cur_blocks):
            block = Block(_x,_y , BLOCK_W, BLOCK_H)
            if ball.colliderect(block):
                cur_blocks.remove((block.x,block.y))
                if not death and not start:
                        score += 100

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
            char_x_motion = new_pos(char.x, dt, increase=char_right)

            if char_x_motion < MARGIN:
                char.x = MARGIN + 1

            elif char_x_motion > SURFACE_W - MARGIN - CHAR_W:
                char.x = SURFACE_W - MARGIN - CHAR_W - 1

            else:
                char.x = char_x_motion

        # Draw screen
        # --------------------------------------------------------------
        screen.blit(background, (0, 0))
        if not start:
            for n in range (cur_life):
                _x = score_text_pos.x - (n * (LIFE_CURSOR_W + 2)) - LIFE_CURSOR_W - 2
                life_cursor = LifeCursor(_x, LIFE_OFFSET_Y, LIFE_CURSOR_W, LIFE_CURSOR_H)
                pygame.draw.rect(screen, RED, life_cursor)

                #text
                screen.blit(score_text, score_text_pos)

        #ball
        pygame.draw.rect(screen, RED, ball)

        #char
        pygame.draw.rect(screen, BLACK, char)

        # blocs
        for xE, yE in cur_blocks:
            block = Block(xE, yE, BLOCK_W, BLOCK_H)
            pygame.draw.rect(screen, BLACK, block)

        if start:
            screen.blit(title, title_pos)
            screen.blit(rule, rule_pos)

        if death:
            screen.blit(loser_text, loser_text_pos)
            screen.blit(rule, rule_pos)


        # Blit everything to the screen
        # --------------------------------------------------------------

        pygame.display.update()


if __name__ == '__main__': main()
