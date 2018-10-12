to_move(s) returns the player to move next given the state s
terminal_test(s) returns a boolean of whether state s is terminal
utility(s, p) returns the payoff of state s if it is terminal (1 if p wins, -1
if p loses, 0 in case of a draw), otherwise, its evaluation with respect to player p
actions(s) returns a list of valid moves at state s
result(s, a) returns the sucessor game state after playing move a at state s
load_board(s) loads a board from an opened file stream s (see below for
format specification) and returns the corresponding state
