# mTree_cooperation_tournament


The goal of this project is to recreate Axelrod's iterated Prisoner's Dilemma tournaments (1980) in a microeconomic simulator. 

Completed agents:

RANDOM - randomly selects either cooperation or defection.

SIMPLE - always cooperates.

TIT FOR TAT - cooperates on the first round, then does whatever the opponent did on the previous round.

JOSS - similar to Tit for Tat, cooperates on the first round, then always defects after a defection, but only cooperates after a cooperation 90% of the time.

FRIEDMAN - begins the game by cooperating, but as soon as the other player defects it defects for the rest of the game.

EATHERLEY - Keeps track of how many times the other player has defected and after the other player defects it defects with a probability equal to the other players total defections to moves ratio up to that point.

FELD - Always defects after the other player defects, but its odds of cooperating after the other player cooperates starts at 100% at the beginning of the game, but by the end it is only 50%.

CHAMPION - Cooperates on the first 10 moves, then plays tit for tat for the next 15 moves. After these first 25 moves it cooperates unless all 3 of the following are true: 1. The other player defected on the previous move, 2. The other player has cooperated less than 60% of the time, 3. The random number between 0 and 1 is greater than the other player's cooperation rate.

NYDEGGER - Plays tit for tat for the first three moves, unless it is the only one to cooperate on the first move and the only one to defect on the second move, then it defects on the third move. After the third move, its choice is determined from the 3 preceding outcomes in the following manner. Let A be the sum formed by counting the other's defection as 2 points and one's own as 1 point, and giving weights of 16, 4, and 1 to the preceding three moves in chronological order. The choice can be described as defecting only when A equals 1, 6, 7, 17, 22, 23, 26, 29, 30, 31, 33, 38, 39, 45, 49, 54, 55, 58, or 61.

TESTER - Defects on the first move. If the other player ever defects it cooperates and plays tit for tat for the rest of the game. Otherwise, it defects as much as possible while keeping the ratio of defections to total moves under .5.

Still need to be added:

REVISED STATE TRANSITION - models the other player as a one step markov process and attempts to maximize its own long-term payoff with the assumption that the model is correct.

TRANQUILIZER - Will occasionally throw in a defection even if the other player is cooperating. Defections become more frequent if the other player cooperates, and as long as it is maintaining an average payoff of at least 2.25 points per move it will never defect twice in succession and it will not defect more than 1/4 of the time. 

DOWNING - This rule selects its choice to maximize its own long term expected payoff on the assumption that the other rule cooperates with a fixed probability which depends only on whether the other player cooperated or defected on the previous move. These two probabilities estimates are continuously updated as the game progresses. Initially, they are both assumed to be .5.

GRAASKAMP - Plays tit for tat for 50 moves, defects once, then plays tit for tat for another 5 moves. Checks to see if it is playing itself or tit for tat, if so it plays accordingly. If its score is bad it assumes it is playing random and defects for the rest of the game. Otherwise it plays tit for tat but throws in a defection every 5 to 15 moves.

 











