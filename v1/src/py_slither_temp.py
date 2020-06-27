#py_game: classic snake game build on python

"""TODO (more to be added):
    2) generate random food (block)
    3) check for food and grow collision"""

import pygame
import random
from Objects import Snake, Block
from Hashtable import Hashtable

win_dim = [600, 600]

def start_game(window):
    running = True
    grid_table = Hashtable(win_dim, 20)
    user_snake = Snake(win_dim)
    grid_table.mark_arr(user_snake.get_chain())
    food_block = generate_food_block(grid_table)
    
    while running:
        pygame.time.wait(50)#ms
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            user_snake.change_direction(0)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            user_snake.change_direction(1)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            user_snake.change_direction(2)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            user_snake.change_direction(3)

        if eat_food(user_snake, food_block):
            user_snake.grow(food_block)
            grid_table.mark(food_block.xpos(),food_block.ypos())
            food_block = generate_food_block(grid_table)

        grid_table.unmark(user_snake.end().xpos(),user_snake.end().ypos())
        user_snake.move()
        if user_snake.past_boundary():
            running = False
        else:
            grid_table.mark(user_snake.head().xpos(),user_snake.head().ypos())

        if user_snake.bit_itself():
            running = False
        
        window.fill((0,0,0)) #reset the window
        draw_snake(window, user_snake.get_chain())
        draw_food(window, food_block)
        pygame.display.update()


def draw_snake(window, snake_chain):
    for block in snake_chain:
        pygame.draw.rect(window,(255,0,0),(block.xpos(),block.ypos(),block.length(),block.width()))
        
def draw_food(window, food_block):
    pygame.draw.rect(window,(0,0,255),(food_block.xpos(),food_block.ypos(),food_block.length(),food_block.width()))

def generate_food_block(grid_table):
    open_spots = grid_table.get_unmarked()
    rand_index = random.randint(0,len(open_spots))
    coord = open_spots[rand_index]
    return Block(coord[0],coord[1])

def eat_food(user_snake, food_block):
    return user_snake.head().ypos() == food_block.ypos() and user_snake.head().xpos() == food_block.xpos()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu(window):
    click = False

    

    while True:
        window.fill((0, 0, 0))

        font = pygame.font.SysFont(None, 30, 1)
        titleFont = pygame.font.SysFont(None, 60)

        mx, my = pygame.mouse.get_pos()

        button_start = pygame.Rect(200, 200, 200, 50)
        button_highScore = pygame.Rect(200, 300, 200, 50)

        pygame.draw.rect(window, (100, 100, 100), button_start)
        pygame.draw.rect(window, (100, 100, 100), button_highScore)
        
        draw_text('Start Game', font, (255, 255, 255), window, 240, 215)
        draw_text('High Score', font, (255, 255, 255), window, 240, 315)
        draw_text('py_slither', titleFont, (255, 255, 255), window, 200, 100)
        if button_start.collidepoint((mx, my)):
            if click:
                start_game(window)
        if button_highScore.collidepoint((mx, my)):
            pass

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()


def main():
    pygame.init()
    window = pygame.display.set_mode(win_dim)
    main_menu(window)
    pygame.quit()
if __name__ == '__main__':
    main()
