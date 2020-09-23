# version 0.13dev 20 09 16


# works with testprog0.13
# filed as  dholden.snakesandladders.SnakesAndLadders0.13.py

import random
from random import randint


def one_game(n_players=3,
             SL_dict={},
             start=None,
             start_player=0,
             dicefunc=lambda: randint(1,6),
             MAX_ROUNDS=1000):
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

        if next_square == HOME:                     # if the move takes the player HOME
            return HOME                             # hand back control to the MAIN program,

        if next_square > HOME:
            next_square = 2 * HOME - next_square    # implements the 'bouncing back' rule

        if next_square in SL_dict:                  # check if new square is "active" (head of snake or foot of ladder)
            next_square = SL_dict[next_square]      # if it is a snake or ladder, move to its end

        return next_square                      # pass back the new position



# body of code for one_game()

                                        #create array to hold the positions of the players' counters on the board
    if start is None:
        start = [0] * n_players
    if not len(start) == n_players:
        n_players = len(start)
        print(f"warning: supplied start requires {len(start)} players")
    counter = list(start)
    current_player = start_player                 #player who has the first move in the start configuration
    round = 1
    scorecard = [list(counter)]                     # this list will store the history of the game

                           # one_game() just cycles through single_move() until someone wins
    for round in range(1, 3000):
        for current_player in range(n_players):
            try:
                counter[current_player] = move_from(counter[current_player]) # make player's move
            except Exception as e:
                print(f"Exception from player {current_player} in round {round}:\n{e}")
                raise
            if counter[current_player] == HOME:
                winner = current_player
                cc = list(counter)                # store the position data in scorecard
                scorecard.append(cc)
                return round, winner, scorecard
        cc = list(counter)                # store the position data for completed round (in scorecard)
        scorecard.append(cc)

    else:
        raise Exception(f"game terminated after {round} rounds")


