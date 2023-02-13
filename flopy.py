import pygame as pg

class Flopy:
    gravity = 0.8
    def __init__(self,x,y_start,color = None):
        """
        x : float - x coord of flopy
        y_start : float - y_start of flopy
        color : Tuple[int] - color of bird
        """
        self.x_ = x
        self.y_ = y_start
        self.v_ = 0
        self.score = 0
        self.dead_or_alive = True
        if color == None:
            color = (255,255,0)
        self.color = color

    def update(self):
        self.v_ += self.gravity
        self.y_ += self.v_


    def fly(self):
        self.v_ = -5


    def draw(self,win):
        pg.draw.circle(win,self.color,(self.x_,self.y_), 10)
        if self.v_ >= 0:
            pg.draw.circle(win,(0,0,0),(self.x_+4,self.y_-4), 3)
            pg.draw.circle(win,(255,0,0),(self.x_+4,self.y_+4), 6)
            pg.draw.circle(win,(255,0,0),(self.x_+8,self.y_+8), 6)
        else:
            pg.draw.circle(win,(0,0,0),(self.x_-4,self.y_-4), 3)
            pg.draw.circle(win,(255,0,0),(self.x_+4,self.y_-4), 6)
            pg.draw.circle(win,(255,0,0),(self.x_+8,self.y_-8), 6)
    
    def update_score(self):
        self.score +=1

    def kill(self):
        self.dead_or_alive = False

    def revive(self):
        self.dead_or_alive = True