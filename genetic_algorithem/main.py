from genetic_algorithem.grid import *
from genetic_algorithem.genetic_alg import *

from tkinter import *
import matplotlib.pyplot as plt
import random
import numpy as np

# set program parameters
MAX_GENERATIONS = 300
MAX_GENERATIONS_LARGE_BOARD = 500
BOLD = "Verdana 8 bold"

initialized = False
running = False

root = Tk()
root.title("Robot movement")

source_var = StringVar()
dest_var = StringVar()
generation_var = StringVar()
best_path_len_var = StringVar()
best_path_dist_var = StringVar()
worst_path_len_var = StringVar()
worst_path_dist_var = StringVar()
best_possible_length_var = StringVar()

# initializing the choice, i.e. the default size of the board is 10 * 10. size tested are 10 and 100
board_size = IntVar()
board_size.set(10)
size_radio_buttons = []

# initializing the population size, i.e. the default size of the board is 10 * 10. population size tested is 20,40,60
pop_size = IntVar()
pop_size.set(20)
population_radio_buttons = []

# set % of board squares that are obstacles. can be 0 for no obstacles grid
obstacles_percent = IntVar()
obstacles_percent.set(0)
obstacles_percent_radio_buttons = []

def init_genetic_alg():
    """
    initialize genetic algorithem object with defined board size, population size, obstacles and othe parameters.
    in this method, the first generation is created, starting point and target and obstacles are positioned on board.
    :return: GeneticAlg object
    """
    source = (random.randint(0, board_size.get() - 1), random.randint(0, board_size.get() - 1))
    dest = (random.randint(0, board_size.get() - 1), random.randint(0, board_size.get() - 1))
    return GeneticAlg(pop_size.get(), board_size.get(), source, dest, obstacles_percent.get() / 100)


def update_labels(genetic_alg):
    """
    update GUI informative labels referring to genetic algorithm execution progress
    :param genetic_alg:
    :return:
    """
    source_var.set("Source: " + str(genetic_alg.src))
    dest_var.set("Destination: " + str(genetic_alg.dst))
    generation_var.set("Generation: " + str(genetic_alg.cur_generation))
    best_path_len_var.set("Best length: " + str(genetic_alg.cur_best_length))
    best_path_dist_var.set("Best distance: " + str(genetic_alg.cur_best_distance))
    worst_path_len_var.set("Worst length: " + str(genetic_alg.cur_worst_length))
    worst_path_dist_var.set("Worst distance: " + str(genetic_alg.cur_worst_distance))
    best_possible_length_var.set("Best possible length: " + str(genetic_alg.best_possible_len))


def run_genetic_alg():
    """
    executing the genetic algorithem selection process. creating a new generation
    :return:
    """
    global running

    max_generations = MAX_GENERATIONS if board_size.get() == 10 else MAX_GENERATIONS_LARGE_BOARD
    genetic_alg.new_generation()
    update_labels(genetic_alg)
    robot_grid.update(genetic_alg)
    if not genetic_alg.is_optimal and genetic_alg.cur_generation <= max_generations and running:
        root.after(5, run_genetic_alg)
    else:
        running = False

# define optional commands in gui
def start_genetic_alg():
    """
    execute the genetic algorithem iterative process
    :return:
    """
    global running
    running = True
    run_genetic_alg()


def stop_genetic_alg():
    """
    interapt algorithem execution
    :return:
    """
    global running
    running = False


def update_size():
    global robot_grid
    global genetic_alg
    if initialized and not running:
        for widget in board_frm.winfo_children():
            widget.destroy()

        genetic_alg = init_genetic_alg()
        robot_grid = RobotGrid(board_frm, board_size.get(), genetic_alg.src, genetic_alg.dst, genetic_alg)
        robot_grid.draw()
        robot_grid.update(genetic_alg)
        update_labels(genetic_alg)


def reset_board():
    """

    :return:
    """
    update_size()


def plot_stats():
    """
    plot statistics about execution fitness: best fitness achieved among all generations, Average and worst.

    :return:
    """
    global genetic_alg
    plt.scatter(range(0, len(genetic_alg.worst_fitness)), genetic_alg.worst_fitness, s=5, label="Worst")
    plt.scatter(range(0, len(genetic_alg.average_fitness)), genetic_alg.average_fitness, s=5, label="Average")
    plt.scatter(range(0, len(genetic_alg.best_fitness)), genetic_alg.best_fitness, s=5, label="Best")
    plt.legend(['Worst', 'Average','Best'])
    plt.grid(True)

    # Set x limits
    plt.xlim(0, genetic_alg.cur_generation + 2)
    # Set x ticks
    l = len(genetic_alg.best_fitness) + 1
    s = 5 if l < 100 else int(l / 50)
    plt.xticks(np.arange(0, l, step=s), fontsize=8, rotation=90)

    plt.ylabel('Fitness')
    plt.xlabel('Generation')
    title = 'Fitness for chromosome length: ' + str(genetic_alg.chromosome_len) + ' [genes] population: ' + str(
        genetic_alg.population_size) + ' [chromosomes]'
    if obstacles_percent.get() > 0:
        title += '\nwith ' + str(obstacles_percent.get()) + '% obstacles'
    plt.title(title)
    plt.show()


def plot_last_generation_fitness():
    """
    plot distribution of fitness among current generation population
    :return:
    """
    global genetic_alg
    plt.scatter(range(1, len(genetic_alg.cur_gen_fitness) + 1), genetic_alg.cur_gen_fitness, s=5)
    plt.grid(True)

    # Set x limits
    plt.xlim(1, len(genetic_alg.cur_gen_fitness) + 2)
    # Set x ticks
    l = genetic_alg.population_size + 1
    plt.xticks(np.arange(1, l, step=3), rotation=20)

    plt.ylabel('Fitness')
    plt.xlabel('Chromosome #')
    title = 'Last generation fitness for ' + str(genetic_alg.population_size) + ' chromosomes of length ' + str(
        genetic_alg.chromosome_len)

    if obstacles_percent.get() > 0:
        title += '\nwith ' + str(obstacles_percent.get()) + '% obstacles'
    plt.title(title)
    plt.show()


def create_size_radio(frame):
    """
    create a button to configure board size
    :param frame:
    :return:
    """
    global board_size
    Label(frame, text="Board size:", font="Verdana 10 bold").pack(side=LEFT)
    b1 = Radiobutton(frame, text="10", variable=board_size, value=10, command=update_size).pack(side=LEFT)
    size_radio_buttons.append(b1)
    b2 = Radiobutton(frame, text="100", variable=board_size, value=100, command=update_size).pack(side=LEFT)
    size_radio_buttons.append(b2)


def create_population_radio(frame):
    """
    button to configure the size of population
    :param frame:
    :return:
    """
    global board_size
    Label(frame, text="Population size (requires reset):", font="Verdana 10 bold").pack(side=LEFT)
    b1 = Radiobutton(frame, text="20", variable=pop_size, value=20, command=update_population_size).pack(side=LEFT)
    population_radio_buttons.append(b1)
    b2 = Radiobutton(frame, text="40", variable=pop_size, value=40, command=update_population_size).pack(side=LEFT)
    population_radio_buttons.append(b2)
    b3 = Radiobutton(frame, text="60", variable=pop_size, value=60, command=update_population_size).pack(side=LEFT)
    population_radio_buttons.append(b3)


def update_population_size():
    """
    dummy function
    :return:
    """
    pass


def create_obstacle_radio(frame):
    """
    button to configure the percent of obstacles
    :param frame:
    :return:
    """
    global board_size
    Label(frame, text="Obstacles percent (requires reset):", font="Verdana 10 bold").pack(side=LEFT)
    b1 = Radiobutton(frame, text="0", variable=obstacles_percent, value=0, command=update_obstacles_percent).pack(side=LEFT)
    obstacles_percent_radio_buttons.append(b1)
    b2 = Radiobutton(frame, text="10", variable=obstacles_percent, value=10, command=update_obstacles_percent).pack(side=LEFT)
    obstacles_percent_radio_buttons.append(b2)
    b3 = Radiobutton(frame, text="20", variable=obstacles_percent, value=20, command=update_obstacles_percent).pack(side=LEFT)
    obstacles_percent_radio_buttons.append(b3)
    b4 = Radiobutton(frame, text="30", variable=obstacles_percent, value=30, command=update_obstacles_percent).pack(side=LEFT)
    obstacles_percent_radio_buttons.append(b4)


def update_obstacles_percent():
    """
    dummy function
    :return:
    """
    pass

def gui():
    global initialized
    global board_frm

    initialized = False
    board_frm = Frame(root, width=500, height=500)
    buttons = Frame(root)
    buttons.pack()

    start = Button(buttons, text="Start!", bg="green", font="Verdana 10 bold", command=start_genetic_alg)
    start.pack(side=LEFT, fill=X)
    stop = Button(buttons, text="Stop!", bg="red", font="Verdana 10 bold", command=stop_genetic_alg)
    stop.pack(side=LEFT, fill=X)
    reset = Button(buttons, text="Reset", bg="light blue", font="Verdana 10 bold", command=reset_board)
    reset.pack(side=LEFT, fill=X)
    plot_btn = Button(buttons, text="Plot Fitness", bg="white", font="Verdana 10", command=plot_stats)
    plot_btn.pack(side=LEFT, fill=X)
    plot_last_btn = Button(buttons, text="Plot Last Generation", bg="white", font="Verdana 10",
                           command=plot_last_generation_fitness)
    plot_last_btn.pack(side=LEFT, fill=X)

    config_frame = Frame(root)
    config_frame.pack()
    create_size_radio(config_frame)
    create_population_radio(config_frame)

    config_frame2 = Frame(root)
    config_frame2.pack()
    create_obstacle_radio(config_frame2)
    info_frame = Frame(root)
    info_frame.pack()
    info_frame2 = Frame(root)
    info_frame2.pack()

    source_var.set("Source: " + str(genetic_alg.src))
    dest_var.set("Destination: " + str(genetic_alg.dst))
    generation_var.set("Generation: 0")
    best_path_len_var.set("Best length: 0")
    worst_path_len_var.set("Worst length: 0")

    Label(info_frame, textvariable=source_var, fg="blue", font=BOLD).pack(side=LEFT)
    Label(info_frame, textvariable=dest_var, fg="green", font=BOLD).pack(side=LEFT)
    Label(info_frame, textvariable=generation_var, font=BOLD).pack(side=LEFT)
    Label(info_frame, textvariable=best_possible_length_var, font=BOLD).pack(side=LEFT)

    Label(info_frame2, textvariable=best_path_len_var, font=BOLD).pack(side=LEFT)
    Label(info_frame2, textvariable=best_path_dist_var, font=BOLD).pack(side=LEFT)
    Label(info_frame2, textvariable=worst_path_len_var, font=BOLD).pack(side=LEFT)
    Label(info_frame2, textvariable=worst_path_dist_var, font=BOLD).pack(side=LEFT)

    board_frm.pack()

    initialized = True

genetic_alg = init_genetic_alg()
gui()
robot_grid = RobotGrid(board_frm, board_size.get(), genetic_alg.src, genetic_alg.dst, genetic_alg)

update_labels(genetic_alg)
robot_grid.draw()
robot_grid.update(genetic_alg)

root.mainloop()

print("temp")
