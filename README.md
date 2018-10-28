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

The evaluation function calculates how advantageous a state S is in respect to a player p.

To begin with, we associated the number of liberties of the player's strings as obviously proportional to its good situation
defensively (a string with more liberties has less ways of being captured), and the number of liberties of the opponent's
 strings as inversely proportional to an offensive advantage (if my opponent's strings have more less liberties, I have more
 ways to capture the string).

Computationally, our evaluation function does the following (to simplify notation, string-s_i has number of liberties - l_i ): 
1) Identifies player p's strings and calculates the respective number of liberties, and only saves l_i if it is lower than
the rest of 
2) If the 



The first thing that the function does is identify player p's strings and his opponent's and place them in separate lists.
In parallel and for each of these lists, the function calculates the number of liberties for each string, and only keeps the
string(s) with the least number of liberties. The PAYOFF will be calculated according to this number of liberties:
 - Positive if it is the opponent with the string with the least number of liberties;
 - Negative if it is the player p with the string with the least number of liberties;
 - In case of a tie in the least number of liberties, the PAYOFF will be an infinitesimal positive or negative according whose turn it is to play. If it is player's p turn to play, we consider
 this a slight advantage and so the player will "attack" and so the infinitesimal will be positive. If it is the opponents
 turn to play, we consider this a slight disadvantage, and so the infinitesimal will be negative. It is important to consider
 a specific case of this situation
 
 In case of ties on the least number of liberties, the tie breaker will be the number of liberties that the liberties have