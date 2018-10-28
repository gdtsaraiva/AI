Artificial Intelligence and Decision Systems

Mini Project 1

Implementation of ATARI Go Engine and and Evaluation Function

1)Describe the state representation used and justify its choice.

The state representation that we have chosen is a 3-tuple S=(n,p,M), where n is the dimension of the board
, p is the player that is currently moving, and M is an n x n matrix that represents the board of the game.

In Python we chose to implement this state S as a list: s = [n,p,L1,...LN],
where each line L1,...,LN is also a list that stores the values of the Nth line of the board. We can
then easily extract the positioning of the stones by doing: board = s[2:].

In terms of choosing the 3-tuple S as the state, we see that there is a possible redundancy, as the
variable p, representing which player's turn it is to move, can be inferred by the state of the board
(assuming that black - 1, always plays first) as passes are not a valid move. However to diminish
unnecessary complexity, we chose to incorporate p in the state.

2)Describe the evaluation function used and justify its design.

The evaluation function that calculates the payoff of a state should 