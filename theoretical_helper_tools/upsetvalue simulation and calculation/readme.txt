upsetcalculator is the program for simulating the game in the way:

Make up a couple of simple “toy” examples to illustrate different concepts.   For example, a couple of leagues with 4 or 5 teams (A,B,C,D, E) playing 5-10 games total, one in which each pair of teams plays exactly one game, another in which two teams may play each other twice or not at all, etc.   Try to come up with examples that illustrate very different scenarios, e.g., one with high predictability/low upset probability, and another with low predictability and an upset probability close to 1/2. List the results in the following forms:

List of games with results: Game 1:  A-B, A wins, Game 2: C-D, D wins, etc.  Use this representation to calculate the upset probability as described in the paper for each of the “toy” examples.

For each game predict a winner (favorite) based on win percentages (win rates) of the two teams involved  (if a team has not played any games yet, define the win percentage as 1/2), and define an upset as an outcome in which the predicted winner loses. The upset probability is the fraction of all games that are upsets.


(refering to Tuesday, Sept. 5, 5 pm: Theory Group Meeting)



[upset_calculator - 5 version.ipynb] is a stable version for simulating the single round-robin tournament, which means, it walks through all the situation when each pair of teams plays exactly one match with each other.

Functions:
1. create 1 matrix to record the detail and information of each simulated game season
2. create 1 array to store the upset value for each simulated game season
3. provide graph(box graph, line graph, etc.) to visualize the data

For example, if there are 3 teams A,B,C, there are 3 matchs, and the game season has 2^3 = 8 outcomes.


---
6： simulation - > winning rate -> upset

---
for version x.y, x means primary version, y means sub-version

essential modification: version 8 has changed the method of calculating upset value
---
output.txt is the output of information matrix from version 8.1

8.1 version is the best and stable and lastest one
