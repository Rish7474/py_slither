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
BLUE = (0,100,200)
RED = (255,0,0)
GREEN = (0,255,0)
GRAY = (100,100,100)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        FONT = pygame.font.SysFont(None, 32)
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    #self.text = ''
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                FONT = pygame.font.SysFont(None, 32)
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def game_loop():
    global score
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
                score+=100*snake.len()
                time_cycle = 0
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
        score-=5
      
def draw_snake(snake):
    for block in snake.get_chain():
        pygame.draw.rect(window,WHITE,(block.xpos(),block.ypos(),block.length(),block.width()))

def draw_food(food):
    pygame.draw.rect(window,RED,(food.xpos(),food.ypos(),food.length(),food.width()))
   
def gen_food_block(grid_table):
    open_spots = grid_table.get_unmarked()
    rand_index = random.randint(0,len(open_spots)-1)
    coord = open_spots[rand_index]
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

def draw_end_screen(font):
    global score

    # input box operation to get name
    scoreBox = InputBox(230, 140, 140, 32)

    while True: 
        for event in pygame.event.get():
            name = scoreBox.handle_event(event)
            if event.type == pygame.KEYDOWN:
                #return if return key is pressed and user has inputed something
                if event.key == pygame.K_RETURN and name:
                    return name

        window.fill(BLACK)
        score_txt = 'Final score: ' + str(score)
        draw_text(score_txt,font,BLUE,200,270)
        draw_text('Press spacebar to return to the menu',font,WHITE,90,300)
        draw_text('Your name:',font,WHITE,90,150)
        scoreBox.update()
        scoreBox.draw(window)
        pygame.display.flip()

    pygame.display.flip()
    return name

def end_loop(font):
    name = draw_end_screen(font)
    print("receive:")
    print(name)
    if name:
        return True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False  
def main_menu(window):
    global score
    disp_font = pygame.font.SysFont(None,30,1)
    title_font = pygame.font.SysFont(None,60)
    button_start = pygame.Rect(200,200,200,50)
    button_score = pygame.Rect(200,260,200,50)
    draw_menu(disp_font,title_font,button_start,button_score)

    mouse_clicked = False
    while True:
        mx, my = pygame.mouse.get_pos()
        #if the mouse was clicked on start button
        if mouse_clicked and button_start.collidepoint((mx,my)):
            if not game_loop():
                return
            else:#end of a game
                if not end_loop(disp_font):
                    return
                #check if local score is beat highscore
                #  if so ask for name and replaced the data in db with new one
                #check if a global score was beat
                #  if so ask for name and place in the right spot
                score = 0
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
    main_menu(window)
    pygame.quit()

