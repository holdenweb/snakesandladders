# version 0.13dev 20 09 16 


# works with testprog0.13
# filed as  dholden.snakesandladders.SnakesAndLadders0.13.py

import random
from random import randint


def one_game(n_players = 3, SL_dict = {}, start = [0,0,0], start_player = 0, dicefunc = lambda : randint(1,6), MAX_ROUNDS=1000):
    '''runs a single simulation of snakes and ladders
    n_players = number of players
    SL_dict   = description of the board as dictionary
    start     = array or list of initial positions
    start_player = player whose turn it is
    dicefunc  = user-supplied function to generate dice throws (defauts to normal dice)
    max_rounds= cutoff limiting max rounds per game'''


    HOME = 100

    def move_from(start_square):                     # this function is the engine
        next_square = start_square + dicefunc()      # randint(1,6)       # move the counter

        if next_square == HOME:                 # check if the move takes the player HOME

                                                # if so:
            return HOME                         # hand back control to the MAIN program, 
                                                #informing that game has ended
                                                # otherwise continue analyzing the throw
        if next_square > HOME:
            next_square = 2 * HOME - next_square    # implements the 'bouncing back' rule

        if next_square in SL_dict.keys():       # check if new square is "active" (head of snake or foot of ladder)

                                                # if it is a snake or ladder, take appropriate action
            next_square = SL_dict[next_square]  # move down snake or up ladder

        return next_square                      # pass back the new position



# body of code for one_game()

                                        #create array to hold the positions of the players' counters on the board
    if start == [0,0,0] and not n_players == 3:
        start = [0 for j in range(n_players)]
    else: 
        if not len(start) == n_players:
            n_players = len(start)
            print("warning: n_players adjusted")
    counter = list(start)
    current_player = start_player                 #player who has the first move in the start configuration
    round = 1
    scorecard = [list(counter)]                     # this list will store the history of the game

                           # one_game() just cycles through single_move() until someone wins
    finished = False
    while not finished:

        try:
            counter[current_player] = move_from(counter[current_player]) # adjust the counter after a move
        except:
            print(f"current_player ={current_player}")
        else:
            if not counter[current_player] == HOME:
                current_player += 1                   # next player's turn
                if current_player == n_players:       # or end of a round, each player has had a throw
                    round += 1                        # increment the round count
                    current_player = 0                # ready to start a new round with player 0
                    cc = list(counter)                # store the position data for completed round (in scorecard)
                    scorecard.append(cc)

                    if round > MAX_ROUNDS:             #maybe there is an infinite loop?
                        raise Exception(f"game terminated after {round} rounds")
            else: 
                winner = current_player
                cc = list(counter)                # store the position data in scorecard
                scorecard.append(cc)
                finished = True

    return round, winner, scorecard

