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
            break
        else:
            grid_table.mark(user_snake.head().xpos(),user_snake.head().ypos())

        if user_snake.bit_itself():
            break
        
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
    is_moving_y = user_snake.dir() < 2
    is_touching_y = (user_snake.head().ypos()-20 == food_block.ypos() or user_snake.head().ypos() == food_block.ypos()-20) and user_snake.head().xpos() == food_block.xpos()
    from_y = is_moving_y and is_touching_y

    is_moving_x = user_snake.dir() > 1
    is_touching_x = (user_snake.head().xpos()-20 == food_block.xpos() or user_snake.head().xpos() == food_block.xpos()-20) and user_snake.head().ypos() == food_block.ypos()
    from_x = is_moving_x and is_touching_x  

    return from_y or from_x

def main():
    pygame.init()
    window = pygame.display.set_mode(win_dim)
    #TODO: Add menu, for now assume play now is selected
    #start game loop
    start_game(window)
    pygame.quit()
if __name__ == '__main__':
    main()
