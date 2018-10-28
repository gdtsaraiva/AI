Inteligência Artificial e Sistemas de Decisão

Mini - Projecto 1

Implementar ATARI GO;

1)Describe the state representation used and justify its choice.

The state representation that we have chosen is a 3-tuple S=(n,p,M), where n is the dimension of the board
, p is the player that is currently moving, and M is an n x n matrix that represents the board of the game.

In the implementation in Python we chose to implement this state S as a list: s = [n,p,L1,...LN],
where each line L1,...,LN is also a list that stores the values of the Nth line of the board. We can
then easily extract the positioning of the stones by doing board = s[2:].

In terms of choosing the 3-tuple S

2)Describe the evaluation function used and justify its design.