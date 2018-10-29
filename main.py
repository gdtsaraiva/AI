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
    #   function:   returns the payoff of state s if it is terminal, otherwise evaluation with respect to player p
    #   input:      state s, player p
    #   output:     evaluation: 1 if p wins , -1 if p loses, 0 in case of draw
    #               better results closer to 1 worst closer to -1 (careful to avoid -1, 0, 1 when not terminal)
    ###################################################################################################################
    # loop 1 - through all board points:
    #       ID all strings
    #       Build 2 structures (one for each player) containing: coordinates of his string(s) with fewest liberties as well as their coordinates
    #           structure worst_strings_p1(/p2): ([(pi1,pj1),(pi2,pj2),...],[(li1,lj1),(li2,lj2),...])
    #       If there is any string with 0 liberties return -1 or 1 immediately
    #
    # loop?? 2 - through data structures: run through the 2 structures previously built
    #       if there is any +inf or -inf return it immediately (if 2 with only one liberty even if you're the next playing it's also inf)
    #       calculate weights of each string
    def utility(self, s, p):
        state = copy.deepcopy(s)
        board = state[2:]
        next_player = state[1]  # next_player != p
        can_avoid_suicide = 0
        open_strings = []
        worst_strings_p1 = []
        worst_strings_p2 = []
        for i, line in enumerate(board):
            for j, point_val in enumerate(line):
                point = (i, j)
                if point_val == 0:
                    move = (next_player, i + 1, j + 1)
                    if self.is_suicide(state, move) == 0:
                        can_avoid_suicide = 1
                    continue
                for open_string in open_strings:
                    if point in open_string:
                        continue

                ########## if here, it's not empty nor in a previously identified open string ##########
                string = [point]
                unchecked_buddies = [point]
                checked_buddies = []
                string_liberties = []
                while len(unchecked_buddies) != 0:
                    unchecked_buddy = unchecked_buddies[0]
                    del unchecked_buddies[0]
                    checked_buddies.extend([unchecked_buddy])
                    neighbours = auxf.check_neighbourhood(state, unchecked_buddy)
                    liberties_rel_coord = [index for index, value in enumerate(neighbours) if value == 2]
                    for liberty_rel_coord in liberties_rel_coord:
                        liberty_coord = auxf.rel2abs_pos(unchecked_buddy, liberty_rel_coord)
                        if liberty_coord not in string_liberties:
                            string_liberties.extend([liberty_coord])
                    buddies_rel_coord = [index for index, value in enumerate(neighbours) if value == 1]
                    for buddy_rel_coord in buddies_rel_coord:
                        buddy_coord = auxf.rel2abs_pos(unchecked_buddy, buddy_rel_coord)
                        if buddy_coord not in string:
                            string.extend([buddy_coord])
                        if buddy_coord not in unchecked_buddies and buddy_coord not in checked_buddies:
                            unchecked_buddies.extend([buddy_coord])

                ########## here, we have a list with the new string's coordinates and one with its libs ##########
                if len(string_liberties) > 0:
                    open_strings.append(string)
                    new_n_lib = len(string_liberties)
                    if point_val == 1:  # string belongs to player 1
                        old_n_lib = len(worst_strings_p1[0][1])
                        if new_n_lib > old_n_lib:
                            continue
                        elif new_n_lib == old_n_lib:
                            worst_strings_p1.extend([(string, string_liberties)])
                        else:
                            worst_strings_p1 = [(string, string_liberties)]
                    elif point_val == 2:  # string belongs to player 1
                        old_n_lib = len(worst_strings_p2[0][1])
                        if new_n_lib > old_n_lib:
                            continue
                        elif new_n_lib == old_n_lib:
                            worst_strings_p2.extend([(string, string_liberties)])
                        else:
                            worst_strings_p2 = [(string, string_liberties)]
                elif p == next_player:
                    return -1
                else:
                    return 1
        if can_avoid_suicide == 0:
            return 0

        ###############################################################################################################
        # here, we have payoff (lost, draw, win) and we have the data structures worst_strings_p1 and (p2)
        # now, calculate other evaluations, being careful not to return -1, 0, 1 in these


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


