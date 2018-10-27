#######################################################################################################################
############################################# Atari Go game engine ####################################################
#######################################################################################################################
# goal: to interface an existing alpha-beta search with cutoff algorithm implementation
# note: no extra modules, besides the Python Standard Library
#######################################################################################################################
# To do:
# - blindar: not-square board; (are default values useful for this?)
#            play over stones
#######################################################################################################################
# Methods:
# [X]to_move(self, s): returns next player to move (1 or 2)
# [X]terminal_test(self, s): returns whether the current state of the game is terminal (1) or not (0)
# []utility(self, s, p):
# []actions(self, s):
# [X]result(self, s, a): returns the successor game state after playing move a (p, i, j) at state s
# [X]load_board(self, s): loads a board from an opened file stream s and returns the corresponding state
#######################################################################################################################
# state: board size, next player to play, board
# for checked and unchecked string points, I'm using lists for now, considering:
#   - sets are faster for checking existence
#   - lists are faster to iterate over
#   - lists have more functions
#######################################################################################################################

# to do (me):
# utility (evaluation regarding a player) (who wins, or if draw)
# actions ()
# check which deepcopy() are relevant (slowing down program)

#to do (Saraiva e Antonio):
#questionnaire
#testing (make code bulletproof)
#read the rules, make sure everything is correct

import auxf
import copy

class Game:
    ###################################################################################################################
    #   function:   given the state s, returns the next player to move
    #   input:      state
    #   output:     next player to move
    ###################################################################################################################
    def to_move(self, s):
        return s[1]

    ###################################################################################################################
    #   function:   checks whether the current state of the game is terminal (capture or unavoidable suicide)
    #   input:      state
    #   output:     boolean of whether state s is terminal (1 if terminal, 0 if not)
    ###################################################################################################################
    def terminal_test(self, s):
        state = copy.deepcopy(s)
        board = state[2:]
        can_avoid_suicide = 0

        # would it be better to id strings first and then check neighbours? (points as string of length 1)
        points_in_open_strings = []
        for i, line in enumerate(board):
            for j, point_val in enumerate(line):
                point = (i, j)
                if point_val == 0:
                    move = (state[1], i+1, j+1)
                    if self.is_suicide(state, move) == 0:
                        can_avoid_suicide = 1
                else:
                    if point in points_in_open_strings:
                        continue
                    string_state = auxf.is_string_surrounded(state, point, points_in_open_strings)
                    if string_state == 0:
                        continue
                    elif string_state == 1:
                        return 1
        if can_avoid_suicide == 1:
            return 0
        return 1

    ###################################################################################################################
    #   function:   returns the payoff of state s if it is terminal
    #   input:      state, and "score" with respect to player p
    #   output:     payoff of state if it is terminal (1 if p wins, -1 if p loses, 0 in case of draw)
    #               otherwise, its evaluation with respect to player p
    ###################################################################################################################
    def utility(self, s, p):
        board = list(s)
        n = board[0]
        board = board[2:]

        if self.terminal_test(s):
            pass
            # return calc_payoff(s, p)
                # payoff: (1 if p wins, -1 if p loses, 0 in case of draw) -> check who wins or if draw
        else:
            pass
            # eval_state(s, p)
                # are the hypothetically captured stones considered in the point counting?

    ###################################################################################################################
    #   function:   returns a list of valid moves at state s
    #   input:      state
    #   output:     list of valid moves
    ###################################################################################################################
    def actions(self, s):
        board = list(s)
        n = board[0]
        p = s[1]
        board = board[2:]

        actions = []
        empty_points = []
        for i, line in enumerate(board):
            for j, point_val in enumerate(line):
                if point_val == 0:
                    empty_points.extend([(i, j)])

                move = (p, i, j)
                self.is_suicide(s, move)
                # include all points (i,j) with value zero are allowed except for those corresponding to suicide

    ###############################################################################################
    #   function:   returns the successor game state after playing move a (p, i, j) at state s
    #   input:      .
    #   output:     .
    ###############################################################################################
    def result(self, s, a):
        new_state = copy.deepcopy(s)

        if a[0] == 1:
            new_state[1] = 2
        else:
            new_state[1] = 1

        # add stone to board
        i = 1 + a[1]
        j = a[2] - 1
        new_state[i][j] = a[0]

        return new_state

    ###############################################################################################
    #   function:   loads a board from an opened file stream s and returns the corresponding state
    #   input:      file stream
    #   output:     state corresponding to the file
    ###############################################################################################
    def load_board(self, s):

        lines = s.readlines()
        file.close()
        header = lines[0]

        header = header[:-1].replace(" ", "")
        n = int(header[0]) # board_size
        p = int(header[1]) # next player to move
        lines = lines[1:]
        board = []

        for line in lines:
            if line[-1] == '\n':
                line = line[:-1]
            int_line = []
            for digit in line:
                int_line.extend([int(digit)])
            board.append(int_line)

        state = [n, p]
        state.extend(board)
        return state

    ###############################################################################################
    #   function:   tests if move on a state is suicide
    #   input:      state, move
    #   output:     1 if suicide, 0 otherwise
    ###############################################################################################
    def is_suicide(self, s, move):
        point_coord = (move[1] - 1, move[2] - 1) # move is (p, i, j) with i and j starting at 1
        hip_state = self.result(s, move)

        if auxf.is_string_surrounded(hip_state, point_coord):
            neighbours = auxf.check_neighbourhood(hip_state, point_coord)
            foes_rel_coord = [index for index, value in enumerate(neighbours) if value == -1]
            for foe_rel_coord in foes_rel_coord:
                foe_coord = auxf.rel2abs_pos(point_coord, foe_rel_coord)
                if auxf.is_string_surrounded(hip_state, foe_coord):
                    return 0
            return 1
        return 0

jogo1 = Game()

# check the state data structure in order to increase performance
# need to take into account draws

file = open("C:\\Users\\HP\\Documents\\IST\\a5s1\\IASD\\Projects\\board.txt", "r")
state = jogo1.load_board(file)
print(jogo1.terminal_test(state))
