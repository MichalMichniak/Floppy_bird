from turtle import width
import pygame  as pg


class Mario_Pipe:
    def __init__(self, x, y, l,fliped=False) -> None:
        self.x_ = x
        self.y_ = y
        self.l = l
        self.r_width = 14
        self.color = (0,255,0)
        self.color_end = (10,200,10)
        self.fliped_ = fliped
        pass
    
    def update_x(self, dx):
        self.x_ += dx

    def set_x(self,x):
        self.x_ = x
    
    def draw(self,win):
        if self.fliped_:
            pg.draw.rect(win,self.color,[self.x_-self.r_width,self.y_ - self.l,2*self.r_width,self.l])
            pg.draw.rect(win,self.color_end,[self.x_-self.r_width - 2,self.y_ - 5,2*(self.r_width+2),5])
        else:
            pg.draw.rect(win,self.color,[self.x_-self.r_width,self.y_,2*self.r_width,self.l])
            pg.draw.rect(win,self.color_end,[self.x_-self.r_width - 2,self.y_,2*(self.r_width+2),5])
        pass

class Row:
    def __init__(self, middlie_y, r_threshold,x,win_width = 600) -> None:
        """
        middle_y : float - point in the middle of a hole in OY
        r_threshold : float - radius around the middle_y
        x : float - middle of pipe in OX
        """
        self.x_ = x
        self.middle_y = middlie_y
        self.r_threshold = r_threshold
        self.upper = Mario_Pipe(x,middlie_y-r_threshold, middlie_y - r_threshold, True)
        self.bottom = Mario_Pipe(x,middlie_y+r_threshold, win_width - (middlie_y + r_threshold))
        pass

    def draw(self,win):
        self.upper.draw(win)
        self.bottom.draw(win)

    def update_x(self,dx):
        self.x_ += dx
        self.upper.update_x(dx)
        self.bottom.update_x(dx)
    
    def set_x(self, new_x):
        self.x_ = new_x
        self.upper.set_x(new_x)
        self.bottom.set_x(new_x)