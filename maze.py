from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
        
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")
    
    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)
        
    def close(self):
        self.__running = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
        canvas.pack(fill=BOTH, expand=1)

class Cell:
    def __init__(self, _win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._win = _win
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self.visited = False
    def draw(self, x1, x2, y1, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)))
        else:
            self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "white")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)))
        else:
            self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "white")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)))
        else:
            self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "white")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)))
        else:
            self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "white")
    def draw_move(self, to_cell, undo=False):
        from_x = (self._x1 + self._x2) / 2
        to_x = (to_cell._x1 + to_cell._x2) / 2
        from_y = (self._y1 + self._y2) / 2
        to_y = (to_cell._y1 + to_cell._y2) / 2
        if undo:
            color = "gray"
        else:
            color = "red"
        self._win.draw_line(Line(Point(from_x, from_y), Point(to_x, to_y)), color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, _win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = _win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed)
    def _create_cells(self):
        for i in range(self.num_cols):
            col_cells = []
            for j in range(self.num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self.x1 + (i * self.cell_size_x)
        x2 = x1 + self.cell_size_x
        y1 = self.y1 + (j * self.cell_size_y)
        y2 = y1 + self.cell_size_y
        self._cells[i][j].draw(x1, x2, y1, y2)
        self._animate()
    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)
    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        entrance.has_top_wall = False
        self._draw_cell(0, 0)
        exit = self._cells[self.num_cols - 1][self.num_rows - 1]
        exit.has_bottom_wall = False
        self._draw_cell((self.num_cols - 1), (self.num_rows - 1))
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            if i > 0 and self._cells[i-1][j].visited == False:
                to_visit.append((i-1, j))
            if i < self.num_cols - 1 and self._cells[i+1][j].visited == False:
                to_visit.append((i+1, j))
            if j > 0 and self._cells[i][j-1].visited == False:
                to_visit.append((i, j-1))
            if j < self.num_rows - 1 and self._cells[i][j+1].visited == False:
                to_visit.append((i, j+1))
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            direction = random.randrange(len(to_visit))
            to_cell = to_visit[direction]
            if to_cell[0] == i-1:
                self._cells[i][j].has_left_wall = False 
                self._cells[i-1][j].has_right_wall = False   
            if to_cell[0] == i+1:
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False  
            if to_cell[1] == j-1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False
            if to_cell[1] == j+1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False
            self._break_walls_r(to_cell[0], to_cell[1])
    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False
    def solve(self):
        return self._solve_r(0, 0)
    def _solve_r(self, i, j):
        self._animate()
        current = self._cells[i][j]
        current.visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        if i-1 >= 0 and not current.has_left_wall and not self._cells[i-1][j].visited:
            current.draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            else:
                current.draw_move(self._cells[i-1][j], True)
        if i+1 < self.num_cols and not current.has_right_wall and not self._cells[i+1][j].visited:
            current.draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            else:
                current.draw_move(self._cells[i+1][j], True)
        if j-1 >= 0 and not current.has_top_wall and not self._cells[i][j-1].visited:
            current.draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                current.draw_move(self._cells[i][j-1], True)
        if j+1 < self.num_rows and not current.has_bottom_wall and not self._cells[i][j+1].visited:
            current.draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                current.draw_move(self._cells[i][j+1], True)
        else:
            return False
            
                                


        
   
def main():
    win = Window(800, 600)
    m = Maze(100, 100, 15, 15, 40, 40, win)
    m.solve()
    win.wait_for_close()

main()