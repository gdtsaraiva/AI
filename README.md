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

 - return  1 - WIN
 - return  0 - DRAW
 - return -1 - LOSE 

The evaluation function calculates how advantageous a state S is in respect to a player p, i.e. how close player p is to
a winning state.

To begin with, we associated the number of liberties of the player's strings as correlated to its good situation
defensively (a string with more liberties has less ways of being captured), and the number of liberties of the opponent's
 strings as inversely correlated to an offensive advantage (if the opponent's strings have less liberties, player p has more
 ways to capture the string).

Computationally, the evaluation function does the following:
1) Identifies player p's strings and the location/number of its liberties. Saves only the strings and location of liberties
that has the least number of liberties;
2) Does the same process for p's opponent;

The evaluation function can now assign an utility value to each state based on the number and location of the player's and
opponent's liberties.
From our previous intuition above, we can state that the utility value is:
 - Positive if it is the opponent with the string with the least number of liberties;
 - Negative if it is the player p with the string with the least number of liberties;

It is now important to state that 
 
