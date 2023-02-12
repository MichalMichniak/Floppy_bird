import pygame as pg
from mario_pipe import Row
from flopy import Flopy
from floppy_with_control import Flopy_control
import random
from typing import List
from NEAT import NEAT
NR_OF_ROWS = 5
X_FLOPY = 50
NR_OF_INSTANCES = 100 
PIPE_RADIUS = 40
class MainWin:
    def __init__(self) -> None:
        pass

    def main_loop(self):
        pg.init()
        NR_OF_ROWS = 5
        X_FLOPY = 50
        win = pg.display.set_mode([500,500])
        run = True

        row_register = [Row(250+random.randint(-120,120),PIPE_RADIUS,250 + 200 * i) for i in range(NR_OF_ROWS)]
        fl = Flopy(X_FLOPY,250)
        next_row = 0
        begin = 0
        while run:
            win.fill((200,250,255))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        fl.fly()
            fl.update()
            for i in range(len(row_register)):
                row_register[i].update_x(-2)

            ## check if hit
            if X_FLOPY-14 < row_register[next_row].x_ < X_FLOPY+14:
                if (fl.y_< row_register[next_row].middle_y - row_register[next_row].r_threshold + 10) or (fl.y_> row_register[next_row].middle_y + row_register[next_row].r_threshold - 10):
                    fl.kill()
                pass
            if fl.y_ > 500:
                fl.kill()

            #pg.draw.circle(win,(0,0,0),(row_register[next_row].x_,250),10)
            if row_register[next_row].x_ < X_FLOPY-14:
                next_row= (next_row+1)%NR_OF_ROWS
                ## update score
                if fl.dead_or_alive:
                    fl.update_score()

            if row_register[begin].x_ < -10:
                row_register[begin].set_x(row_register[begin - 1].x_ + 200)
                row_register[begin].set_y(250+random.randint(-120,120))
                begin= (begin+1)%NR_OF_ROWS
            
            for i in range(len(row_register)):
                row_register[i].draw(win)
            if fl.dead_or_alive:
                fl.draw(win)
            else:
                run = False
            #pg.draw.circle(win,(255,0,0),[250,250],1)
            pg.display.update()
            pg.time.delay(30)
            pass
        pass

    def simulate(self,win,flopy_lst : List[Flopy_control],iteration_number = 0 ,delay = 0):
        run = True
        row_register = [Row(250+random.randint(-120,120),PIPE_RADIUS,250 + 200 * i) for i in range(NR_OF_ROWS)]
        alive_floppy_counter = len(flopy_lst)
        next_row = 0
        begin = 0
        count = 0
        while run:
            win.fill((200,250,255))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    return True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if delay == 0:
                            delay = 40
                        elif delay == 40:
                            delay = 5
                        else:
                            delay = 0
                        


            # control stage
            for i in range(len(flopy_lst)):
                if flopy_lst[i].dead_or_alive:
                    # 3 inputs x of obstacle, upper pipe limit, bottom pipe limit
                    flopy_lst[i].control(row_register[next_row].x_, row_register[next_row].middle_y - row_register[next_row].r_threshold + 10,row_register[next_row].middle_y + row_register[next_row].r_threshold - 10)


            # update stage
            for i in range(len(flopy_lst)):
                if flopy_lst[i].dead_or_alive:
                    flopy_lst[i].update()
            for i in range(len(row_register)):
                row_register[i].update_x(-2)

            ## for each alive floppy
            for i in range(len(flopy_lst)):
                if flopy_lst[i].dead_or_alive:
                    if X_FLOPY-14 < row_register[next_row].x_ < X_FLOPY+14:
                        if (flopy_lst[i].y_< row_register[next_row].middle_y - row_register[next_row].r_threshold + 10) or (flopy_lst[i].y_> row_register[next_row].middle_y + row_register[next_row].r_threshold - 10):
                            flopy_lst[i].kill()
                            alive_floppy_counter -=1
                    elif flopy_lst[i].y_ > 500 or flopy_lst[i].y_ < 0:
                        flopy_lst[i].kill()
                        flopy_lst[i].score = -1
                        alive_floppy_counter -=1

            if row_register[next_row].x_ < X_FLOPY-14:
                next_row= (next_row+1)%NR_OF_ROWS
                count +=1
                ## update score
                for i in range(len(flopy_lst)):
                    if flopy_lst[i].dead_or_alive:
                        if flopy_lst[i].dead_or_alive:
                            flopy_lst[i].update_score()

            if row_register[begin].x_ < -10:
                row_register[begin].set_x(row_register[begin - 1].x_ + 200)
                row_register[begin].set_y(250+random.randint(-120,120))
                begin= (begin+1)%NR_OF_ROWS
            
            for i in range(len(row_register)):
                row_register[i].draw(win)
            
            for i in range(len(flopy_lst)):
                if flopy_lst[i].dead_or_alive:
                    flopy_lst[i].draw(win)


            if alive_floppy_counter == 0:
                print(f"iter: {iteration_number}, best: {count}")
                run = False
            #pg.draw.circle(win,(255,0,0),[250,250],1)
            pg.display.update()
            pg.time.delay(delay)
        return delay
    
    def main_loop_multi_instances(self, iteration = 1000):
        pg.init()
        neat = NEAT()
        flag = 0
        win = pg.display.set_mode([500,500])
        flopy_lst = [Flopy_control(X_FLOPY,250+random.randint(-120,120)) for i in range(NR_OF_INSTANCES)]
        for i in range(iteration):
            # revive stage
            for j in range(len(flopy_lst)):
                flopy_lst[j].reset()
            #simulation stage
            flag = self.simulate(win,flopy_lst,i,flag)
            if type(flag) == bool:
                break
            # evolution stage
            flopy_lst = neat.evolve_population(flopy_lst,True)
        
        pass


if __name__ == "__main__":
    win = MainWin()
    win.main_loop()
    win.main_loop_multi_instances()