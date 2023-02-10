import pygame as pg
from mario_pipe import Row
from flopy import Flopy
class MainWin:
    def __init__(self) -> None:
        pass

    def main_loop(self):
        pg.init()
        NR_OF_ROWS = 5
        X_FLOPY = 50
        win = pg.display.set_mode([500,500])
        run = True

        row_register = [Row(250,60,250 + 200 * i) for i in range(NR_OF_ROWS)]
        fl = Flopy(X_FLOPY,250)
        next_row = 0
        begin = 0
        while run:
            win.fill((0,0,255))
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

            pg.draw.circle(win,(0,0,0),(row_register[next_row].x_,250),10)
            if row_register[next_row].x_ < X_FLOPY-14:
                next_row= (next_row+1)%NR_OF_ROWS
                ## update score
                if fl.dead_or_alive:
                    fl.update_score()
                    print(fl.score)

            if row_register[begin].x_ < -10:
                row_register[begin].set_x(row_register[begin - 1].x_ + 200)
                begin= (begin+1)%NR_OF_ROWS
            
            for i in range(len(row_register)):
                row_register[i].draw(win)
            if fl.dead_or_alive:
                fl.draw(win)
            else:
                run = False
            #pg.draw.circle(win,(255,0,0),[250,250],1)
            pg.display.update()
            pg.time.delay(40)
            pass
        pass

        


if __name__ == "__main__":
    win = MainWin()
    win.main_loop()