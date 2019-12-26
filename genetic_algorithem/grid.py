from tkinter import *

CELL_HEIGHT_REGULAR = 20
CELL_HEIGHT_COMPACT = 10
CELL_WIDTH_REGULAR = 20
CELL_WIDTH_COMPACT = 10


class RobotGrid:
    def __init__(self, board_frame, board_size=10, source=(0, 0), dest=(9, 9), genetic_alg=None):
        self.rows = board_size
        self.columns = board_size
        self.source = source
        self.destination = dest

        self.cell_height = CELL_HEIGHT_REGULAR if board_size <= 10 else CELL_HEIGHT_COMPACT
        self.cell_width = CELL_WIDTH_REGULAR if board_size <= 10 else CELL_WIDTH_COMPACT
        # init board gui
        self.canvas = Canvas(board_frame, bg='white', width=(board_size+2)*self.cell_width, height=(board_size+2)*self.cell_height,
                             scrollregion=(0, 0, board_size*self.cell_width+50, board_size*self.cell_height+50))
        self.scroll_vertical = Scrollbar(board_frame, orient=VERTICAL)
        self.scroll_vertical.pack(side=LEFT, fill=Y)
        self.scroll_vertical.config(command=self.canvas.yview)

        self.scroll_horizontal = Scrollbar(board_frame, orient=HORIZONTAL)
        self.scroll_horizontal.pack(side=TOP, fill=X)
        self.scroll_horizontal.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.scroll_vertical.set)
        self.canvas.config(xscrollcommand=self.scroll_horizontal.set)
        self.canvas.pack(side=TOP)

        self.rectangles = []
        self.prop_text = []

        self.best = genetic_alg.cur_best_location if genetic_alg is not None else source
        self.worst = genetic_alg.cur_worst_location if genetic_alg is not None else dest

    def update(self, genetic_alg):
        """

        :param genetic_alg:
        :return:
        """
        bold_ = ("Calibri", 8, "bold")
        self.canvas.itemconfig(self.prop_text[self.source[0]][self.source[1]], text="S", font=bold_, fill="black")
        self.canvas.itemconfig(self.prop_text[self.destination[0]][self.destination[1]], text="D", font=bold_, fill="black")
        # reset text for PREVIOUS best:
        if self.best != genetic_alg.cur_best_location:
            self.canvas.itemconfig(self.prop_text[self.best[0]][self.best[1]], text="")
        # reset text for PREVIOUS worst:
        if self.worst != genetic_alg.cur_worst_location:
            self.canvas.itemconfig(self.prop_text[self.worst[0]][self.worst[1]], text="")

        # set text for CURRENT best:
        self.best = genetic_alg.cur_best_location
        self.canvas.itemconfig(self.prop_text[self.best[0]][self.best[1]], text="Best", font=bold_, fill="green")
        # set text for CURRENT worst:
        self.worst = genetic_alg.cur_worst_location
        if self.worst == self.best:
            self.canvas.itemconfig(self.prop_text[self.worst[0]][self.worst[1]], text="B/W", font=bold_, fill="blue")
        else:
            self.canvas.itemconfig(self.prop_text[self.worst[0]][self.worst[1]], text="Worst",
                               font=bold_, fill="red")
        # colour obstacles in black
        self.draw_obstacles(genetic_alg)
        # reset previous path colours:
        self.reset_fill_colours(genetic_alg)
        # colour best path in gray
        self.draw_best_path(genetic_alg)

    def draw_obstacles(self, genetic_alg):
        if genetic_alg.obstacles_len > 0 and genetic_alg.cur_generation < 1:
            # print("Obstacles:")
            # print(genetic_alg.obstacles)
            for obstacle in genetic_alg.obstacles:
                self.canvas.itemconfig(self.rectangles[obstacle[0]][obstacle[1]], fill="black")

    def draw_best_path(self, genetic_alg):
        for step in genetic_alg.cur_best_path:
            if genetic_alg.src != step and genetic_alg.dst != step:
                self.canvas.itemconfig(self.rectangles[step[0]][step[1]], fill="light grey")

    def reset_fill_colours(self, genetic_alg):
        for cur in genetic_alg.prev_best_path:
            if genetic_alg.src != cur and genetic_alg.dst != cur:
                self.canvas.itemconfig(self.rectangles[cur[0]][cur[1]], fill="white")

    def draw(self):
        """
        creates the board on which the robot will move around
        :return:
        """
        x = self.cell_height
        y = self.cell_width
        prop_text = []
        rectangles = []

        bold_ = ("Calibri", 8, "bold")
        regular_ = ("Calibri", 7, "bold")
        for row in range(self.rows):
            rectangles.append([])
            prop_text.append([])
            text_height = y + self.cell_height / 2
            # add row numbers
            self.canvas.create_text(x - self.cell_width / 2, text_height, text=str(row), font=regular_)
            # add row cells
            for col in range(self.columns):
                # add column numbers
                if row == 0:
                    self.canvas.create_text(x + self.cell_width / 2, text_height - self.cell_height, text=str(col),
                                            font=bold_)
                rect = self.canvas.create_rectangle(x, y, x + self.cell_width, y + self.cell_height, fill="white")
                rectangles[row].append(rect)
                text = self.canvas.create_text(x + self.cell_width / 2, text_height, text="", font=("Calibri", 8))
                prop_text[row].append(text)
                x += self.cell_height
            x = self.cell_width
            y += self.cell_height

        self.canvas.itemconfig(rectangles[self.source[0]][self.source[1]], fill="cyan", outline='blue')
        self.canvas.itemconfig(rectangles[self.destination[0]][self.destination[1]], fill="light green", outline='green')
        self.canvas.itemconfig(prop_text[self.source[0]][self.source[1]], text="S", font=bold_)
        self.canvas.itemconfig(prop_text[self.destination[0]][self.destination[1]], text="D", font=bold_)
        self.rectangles = rectangles[:]
        self.prop_text = prop_text[:]
