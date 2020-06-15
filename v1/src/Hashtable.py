from Objects import Block

class Hashtable:
    def __init__(self, dim, block_size):
        self.row_size = dim[0]
        self.col_size = dim[1]
        self.block_size = block_size
        self.num_rows = int(dim[0] / block_size)
        self.num_cols = int(dim[1] / block_size)
        self.table = [False] * (self.num_cols * self.num_rows)
    
    def hash(self, xpos, ypos):
        row = int(xpos / self.block_size)
        col = int(ypos / self.block_size) * self.num_cols    
        return row + col

    def rev_hash(self, index):
        col = int(index / self.num_cols)
        row = index - col*self.num_cols
        return [row*self.block_size,col*self.block_size]

    def at(self, row, col):
        index = self.hash(row,col)
        return self.table[index] 
    
    def mark(self, row, col):
        index = self.hash(row,col)
        self.table[index] = True

    def mark_arr(self, blocks):
        for block in blocks:
            index = self.hash(block.xpos(),block.ypos())
            self.table[index] = True

    def unmark(self, row, col):
        index = self.hash(row,col)
        self.table[index] = False

    def unmark_arr(self, blocks):
        for block in blocks:
            index = self.hash(block.xpos(),block.ypos())
            self.table[index] = False

    def get_marked(self):
        marked = []
        for i in range(len(self.table)):
            if self.table[i]:
                coord = self.rev_hash(i)
                marked.append(coord)
        return marked
    
    def get_unmarked(self):
        marked = []
        for i in range(len(self.table)):
            if not self.table[i]:
                coord = self.rev_hash(i)
                marked.append(coord)
        return marked
