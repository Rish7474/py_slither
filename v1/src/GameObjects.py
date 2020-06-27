#custom objects used in py_grow

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wid = 20
        self.len = 20

    def xpos(self):
        return self.x

    def ypos(self):
        return self.y

    def width(self):
        return self.wid

    def length(self):
        return self.len

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        
class Snake:
    def __init__(self, win_size):
        self.blocks = [Block(0,0)] #head of snake is first element
        self.direction = 3 #moving right
        self.velocity = 20
        self.plane = win_size
        
    def move(self):
        for i in reversed(range(self.len())):
            cur_xpos = self.blocks[i].xpos()
            cur_ypos = self.blocks[i].ypos()

            if i == 0: #if head of snake, move in the current direction
                incr = self.get_delta()
                cur_xpos = cur_xpos+incr[0]
                cur_ypos = cur_ypos+incr[1]
            else: #else move block up by 1 up the snake chain
                cur_xpos = self.blocks[i-1].xpos()
                cur_ypos = self.blocks[i-1].ypos()

            self.blocks[i].set_pos(cur_xpos, cur_ypos) 

    def head(self):
        return self.blocks[0]

    def end(self):
        return self.blocks[self.len()-1]
    
    def get_delta(self):
        if self.direction == 0:
            return [0,self.velocity]
        
        elif self.direction == 1:
            return [0,self.velocity*-1]
        
        elif self.direction == 2:
            return [self.velocity*-1,0]
        
        else:
            return [self.velocity,0]
    
    def get_chain(self):
        return self.blocks
    
    def len(self):
        return len(self.blocks)
    
    def grow(self, block):
        self.blocks.insert(0,block)

    def change_direction(self, direction):
        self.direction = direction
        
    def dir(self):
        return self.direction
    
    def bit_itself(self):
        for i in range(1,self.len()):
            if self.blocks[0].xpos() == self.blocks[i].xpos() and self.blocks[0].ypos() == self.blocks[i].ypos():
                return True
        return False

    def past_boundary(self):
        if self.blocks[0].xpos() < 0 or self.blocks[0].xpos() > self.plane[0]-20:
            return True
        if self.blocks[0].ypos() < 0 or self.blocks[0].ypos() > self.plane[1]-20:
            return True
        return False

    def eat_food(self, food):
        return self.head().ypos() == food.ypos() and self.head().xpos() == food.xpos()
        
