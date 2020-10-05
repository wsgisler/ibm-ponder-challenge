# September 2020 - Challenge

https://www.research.ibm.com/haifa/ponderthis/challenges/September2020.html

In a Rock-Paper-Scissors (RPS) game, players can choose one of three "weapons": Rock, Paper, or Scissors. Each weapon defeats exactly one other weapon. By assigning numbers to the weapons, we can describe the game as

 0 -> 1
 1 -> 2
 2 -> 0
 
(Read "0 -> 1" as "0 beats 1", etc.)

An automorphism of an RPS game is some permutation of the weapon numbers that keeps the rules of the game the same. For example, the permutation (0 1 2) in which 0 is mapped to 1, 1 is mapped to 2 and 2 is mapped to 0 is a permutation, since applying it to the list of rules results in the same list of rules. However, the permutation (0 2), which switches 0 and 2 but keeps 1 intact, results in the rules

 2 -> 1
 1 -> 0
 0 -> 2

which are different ("Paper beats Rock"), so (0 2) is not an automorphism of RPS.
We now consider generalized versions of RPS: an RPS(n) game consists of exactly n weapons, and rules such that every weapon beats exactly (n-1) / 2 of the other weapons such that for every pair of weapons, exactly one weapon beats the other. A famous example is the RPS(5) game "Rock-Paper-Scissors-Lizard-Spock", which maintains the RPS rules but adds the weapons Lizard (beats Paper and Spock, beaten by Rock and Scissors) and Spock (beats Rock and Scissors, beaten by Paper and Lizard). Denoting Lizard by 3 and Spock by 4, this game can be described by the rules

 0 -> 1, 3
 1 -> 2, 4
 2 -> 0, 3
 3 -> 1, 4
 4 -> 0, 2

It can be shown that any RPS(5) game has exactly five automorphisms.

Your goal is to find an RPS(9) game with at least 10 automorphisms. Give your solution as a list of the form

 0 -> a0, b0, c0, d0
 ...

 8 -> a8, b8, c8, d8

where the right-hand side of each row consists of four numbers between 0 and 8.

A bonus '*' for finding an RPS(11) game with at least 50 automorphisms.

## Solution approach

It is relatively straightforward to model this as a MIP. The code can be found in solver.py and I am using Cplex to solve the problem. The code can be adjusted easily: at the top you can define the number of weapons you want to solve the problem with and the minimum number of automorphisms you want to get.
I added on objective function which is not needed, but it helps getting multiple solutions. I also added some code to break the symmetries, which is also not absolutely required. The RPS(9) sample solves well without objective and symmetry breaking constraints in less than half a minute.
For the RPS(11)-game (bonus question), the model gets to big if you require 50 automorphisms, but chances are big that you find a solution with 50 or more automorphisms, even if you require only a few automorphisms.
The part that makes the problem explode is the code that makes sure that every automorphism is unique. I think it would be possible to make this part a bit more efficient, for example by requiring that only 5 (instead of all 11) weapons are considered to determine if a solution is unique or not.

## tester.py

There is a separate file that can be used to test a solution. I included an additional check to check if every automorphism can be depicted in a connected graph as I am not 100% sure if solutions that require more than one component in a graph are considered valid or not (the problem description give a slightly strange way of defining the permutations).