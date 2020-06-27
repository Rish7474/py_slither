#py_slither game

import pygame
import random
from GameObjects import Block, Snake
from Algos_DS import Hashtable

win_dim = [600,600] #window demension: 600px by 600px
window = None
score = 0

#color constants
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
GRAY = (100,100,100)

def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def game_loop():
    control = True
    snake = Snake(win_dim)
    grid_table = Hashtable(win_dim,20) #20px is the length of blocks
    grid_table.mark_arr(snake.get_chain())
    food = gen_food_block(grid_table)
    
    while True:
        pygame.time.wait(50)#ms
        if check_exit():
            return False #force quit game

        if control: #user mode
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                return False
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                snake.change_direction(0)
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                snake.change_direction(1)
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                snake.change_direction(2)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                snake.change_direction(3)

            if snake.eat_food(food):
                snake.grow(food)          
               # score+=1
                if score == 400: #max score
                    return True
                grid_table.mark(food.xpos(),food.ypos())
                food = gen_food_block(grid_table)

            grid_table.unmark(snake.end().xpos(),snake.end().ypos())
            snake.move()
            if snake.past_boundary():
                return True
            else:
                grid_table.mark(snake.head().xpos(),snake.head().ypos())

            if snake.bit_itself():
                return True
            
            window.fill(BLACK)
            draw_snake(snake)
            draw_food(food)
            pygame.display.update()
            
        else: #AI mode
            pass
        
def draw_snake(snake):
    for block in snake.get_chain():
        pygame.draw.rect(window,WHITE,(block.xpos(),block.ypos(),block.length(),block.width()))

def draw_food(food):
    pygame.draw.rect(window,RED,(food.xpos(),food.ypos(),food.length(),food.width()))
   
def gen_food_block(grid_table):
    openSpots = grid_table.get_unmarked()
    randIndex = random.randint(0,len(openSpots))
    coord = openSpots[randIndex]
    return Block(coord[0],coord[1])    

def draw_text(text, font, color, xpos, ypos):
    text_obj = font.render(text,1,color)
    text_box = text_obj.get_rect()
    text_box.topleft = (xpos,ypos)
    window.blit(text_obj,text_box)

def draw_menu(disp_font, title_font, button_start, button_score):
    window.fill(BLACK)
    pygame.draw.rect(window,GRAY,button_start)
    pygame.draw.rect(window,GRAY,button_score)
    
    draw_text('Start Game',disp_font,WHITE,240,215)
    draw_text('Global Scores',disp_font,WHITE,220,275)
    draw_text('py_slither',title_font,WHITE,200,100)
    pygame.display.flip()

def main_menu():
    disp_font = pygame.font.SysFont(None,30,1)
    title_font = pygame.font.SysFont(None,60)
    button_start = pygame.Rect(200,200,200,50)
    button_score = pygame.Rect(200,260,200,50)
    draw_menu(disp_font,title_font,button_start,button_score)

    mouse_clicked = False
    while True:
        mx, my = pygame.mouse.get_pos()
        if mouse_clicked and button_start.collidepoint((mx,my)):
            status = game_loop()
            if not status:
                return
            else:
                draw_menu(disp_font,title_font,button_start,button_score)
                
        elif mouse_clicked and button_score.collidepoint((mx,my)):
            pass #visit global highscore webpage

        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
        

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode(win_dim)
    pygame.display.set_caption('py_slither')
    main_menu()
    pygame.quit()

