import pygame as pg
import random
import control as crl
class Flopy_control:
    gravity = 0.8
    def __init__(self,x,y_start,control = None,color = None):
        """
        x : float - x coord of flopy
        y_start : float - y_start of flopy
        color : Tuple[int] - color of bird
        """
        if control == None:
            control = crl.Control(3,1)
        self.control_ = control
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
        self.v_ = -10


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
    
    def control(self, x, u_l, b_l):
        x = x - self.x_
        u_l = self.y_ - u_l
        b_l = b_l - self.y_
        ctrl = self.control_.predict([x,u_l,b_l])
        if ctrl == 1:
            self.fly()