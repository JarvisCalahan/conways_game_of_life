from graphics import*
import time, sys, threading, math

class cell(Rectangle):
    def __init__(self, x, y, canvas, state = True):
        Rectangle.__init__(self, Point(x, y), Point(x+1, y+1))
        self.alive = state
        self.x = x
        self.y = y
        self.num = self.num = [[1,1],[-1,-1],[0,1],[1,0],[1,-1],[-1,1],[0,-1],[-1,0]]
        self.cv = canvas
        if self.alive: self.setFill('black')
        else: self.setFill('white')
        self.draw(self.cv)

    def clone(self, bool):
        other = cell(self.x, self.y, self.cv, state =  bool)
        other.config = self.config.copy()
        return other

    def switch(self):
        self.alive = not self.alive
        self.change(self.alive)

    def change(self, bool):
        if bool:
            self.setFill('black')
        else:
            self.setFill('white')

    def check(self, dict):
            n = 0
            for cmb in self.num:
                try:
                    state = dict['{},{}'.format(self.x + cmb[0],self.y + cmb[1])].alive
                    #print(self.x + cmb[0], self.y + cmb[1], state)
                except:
                    #print('fail')
                    state = None
                if state == True: n += 1
            #print(self.x, self.y, n)
            if self.alive:
                if(n > 3) or (n < 2):
                    return False
                else:
                    return True
            else:
                if n == 3:
                    return True
                else:
                    return False

class _board(GraphWin):
    def __init__(self, name, width, height, scale = 1, cur = None):
        GraphWin.__init__(self, title = name, width = width, height = height, autoflush = False)
        self.w = int(width * scale)
        self.h = int(height * scale)
        self.setCoords(0, 0, self.w, self.h)
        self.checked = 'n,n'
        self.scale = scale
        self.cur = dict()
        self.new = dict()
        self.click = False
        self.checkMotion = False
        self.unbind('<Button-1>')
        self.bind('<Button-1>', self._onClick)
        self.bind('<Motion>', self._motion)
        self.setup()

    def toggleMotion(self):
        self.checked = False
        if self.checkMotion:
            self.checkMotion = False
        else:
            self.checkMotion = True

    def _onClick(self, e):
        self.mouseX = e.x
        self.mouseY = e.y
        if self.setup:
            self.toggleMotion()
        """
        x = math.floor(e.x * self.scale)
        y = math.floor(self.h - (e.y * self.scale))
        cell = self.cur['{},{}'.format(x, y)]
        cell.switch()
        """

    def _motion(self, e):
        if self.checkMotion:
            x = math.floor(e.x * self.scale)
            y = math.floor(self.h - (e.y * self.scale))
            pos = '{},{}'.format(x,y)
            try:
                cell = self.cur[pos]
            except:
                pass
            if pos != self.checked:
                cell.switch()
                self.checked = pos

    def show(self):
        for col in self.cur:
            for cell in col:
                cell.undraw()
                cell.draw(self)

    def coordScale(self, x, y):
        if self.trans:
            return x/self.scale, y/self.scale
        return x, y

    def empty(self):
        return [['-' for i in range(self.h)] for j in range(self.w)]

    def setup(self):
        for i in range(self.w * self.h):
                x = i % self.w
                y = i // self.h
                if(12 < x < 13) and (12 < y < 13):
                    state = True
                else:
                    state = False
                self.cur.update({'{},{}'.format(x, y):cell(x, y, self, state = state)})
        self.setup = True
        input('fill in squares!')
        self.checkMotion = False
        self.setup = False
        self.mouseX, mouseY = None, None

    def generation(self):
        for key in self.cur.keys():
            cell = self.cur[key]
            state = cell.check(self.cur)
            cell.change(state)
            cellPos = '{},{}'.format(cell.x, cell.y)
            self.new.update({cellPos:cell.clone(state)})
        self.update()
        self.cur = self.new
        self.new = dict()
        return self.cur

cur = None
board = _board('gen 0', 700, 700, cur = cur, scale = 40/700)
i = 1
print('gen {}'.format(i-1))
user = ""
while board.mouseX == None:
    print('gen {}'.format(i))
    cur = board.generation()
    i += 1
