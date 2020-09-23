###### simple snakes-and-ladders simulation                    aim here to make a one-game function for module
# version 0.13dev 20 09 16 
#
# this copy is testprog0.13 in dholden.snakesandladders
#
VERSION = 'Vn 0.13dev 19th September 2020'

MAX_ROUNDS = 3000 # cutout in case of infinite loop 



#request the required module and function for random number generation
import random
from random import randint
import numpy as np
import datetime
from datetime import date, datetime
import matplotlib.pyplot as plt

import SnakesAndLadders
from SnakesAndLadders import one_game

def dice12():
    '''simulates a throw of two normal dice'''
    d = randint(1,6) + randint(1,6)
    return d


def run_simulations(SL_dict):  

    
    #window dressing! info re version and time and date of run
    def print_title():
        print(f"Snakes and Ladders {VERSION}")
        TODAY = date.today()
        NOW = datetime.now().time() # time object
        print( TODAY.strftime("%B %d, %Y"), '  ',
                              NOW.strftime("%H:%M:%S"))
        print(f'simulation: {N_GAMES} games for {N_PLAYERS} players')
        print(f'dice option {DICE}')
#        print('board description', SL_dict)

    print_title()
    initial = np.zeros(N_PLAYERS) # this for present vn
    for _ in range(N_GAMES):
        rounds, winner, scorecard = one_game(N_PLAYERS, game_board, dicefunc = dice_func_dict[DICE])
        ss = list(scorecard)
        scorecard_history.append(ss)
        rounds_history.append(rounds)
        winner_history.append(winner) #append the results of this simulation

    mean_rounds = np.mean(np.array(rounds_history))
    sd    = np.std(np.array(rounds_history))
    se = sd / np.sqrt(N_GAMES)
    print(f'mean game duration:  {mean_rounds :8.2f}({se:5.1f}) moves. standard deviation ({sd:.2f})')
    return scorecard_history

game_board = {20:1, 22:1, 98:64, 96:64, 5:95,  66:2, 68:29, 5:40, 50:80, 63:17, 
             16:30, 17:31, 39:8, 4:71, 35:15, 99:56, 97:72, 74:30, 85:20} # the snakes and ladders dictionary

rounds_history = [] # create three empty lists to record simulation data
winner_history = []
scorecard_history = []

import sys

print( 'Number of arguments:', len(sys.argv), 'arguments.')
print( 'Argument List:', str(sys.argv))
#raise(Exception)

SHOW_N_MOVES = True # if true displays on each recored the length of that game in bold characters
dice_func_dict = {6: lambda : randint(1,6), 12: dice12}
N_PLAYERS = 5
DICE = 6
N_GAMES = 1000 # number of trials (games) per simulation


games = run_simulations(game_board) # runs N_GAMES simulations and stores the data

#OUTPUT TO FILE

file = open('testfile', 'w') # write the data to <testfile>
for j in range(0,len(games)):
    r = len(games[j])
    file.write(f'{r:5} {winner_history[j]: 5} \n')
    for k in range(r):
        for l in range(N_PLAYERS):
            file.write(f'{int(games[j][k][l]):6}')
        file.write('\n')        
file.close()


# GRAPHICS


def plot_games(m, n): # give plots of (six) randomly chosen games from the sample
    
    def draw_one_game(ax, nn):
        scorecard = games[nn]
        ax.axes.get_xaxis().set_visible(True)
        ax.axes.get_yaxis().set_visible(False)
        r = rounds_history[nn]
        x = np.arange(len(scorecard))
        y = np.zeros(len(x))
        for j in range(len(scorecard[1])):

            y = [scorecard[i][j] for i in range(len(scorecard))]
            ax.set_facecolor('xkcd:baby blue')
            if j == 0: ax.plot(x,y,'b',linewidth=0.8)
            if j == 1: ax.plot(x,y,'r',linewidth=0.8)
            if j == 2: ax.plot(x,y,'g',linewidth=0.8)
            if j == 3: ax.plot(x,y,linewidth=0.8)
            if j == 4: ax.plot(x,y,linewidth=0.8)
            if y[-1] == 100: # show winner
                     ax.scatter(x[-1],y[-1], 36, color=['k'])
                     ax.scatter(x[-1],y[-1], 12, color=['w'])

    fig, axs = plt.subplots(m, n, figsize = (12,6))
    for i in range(m):
        for j in range(n):
            nn = random.randint(0,len(games)-1)
            draw_one_game(axs[i,j], nn)
            if SHOW_N_MOVES and m==3 and n==2: 
                axs[i,j].text( 0.13 + 0.33*j,0.1 + 0.5 * i, str(rounds_history[nn]), 
                         fontsize=24, color='black')#transform = axs.transAxes)

    return fig  


fig = plot_games(3,2)
fig.tight_layout()
plt.show()
