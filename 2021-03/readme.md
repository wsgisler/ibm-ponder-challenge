# March 2021 - Challenge

Original problem statement: https://www.research.ibm.com/haifa/ponderthis/challenges/March2021.html

# Solution approach:

This problem resembles an open pit mining problem and can be easily formulated as a MIP

# Solution approach for the bonus question:

1. generate all possible solutions of the problem independent of the values
2. use constraint programming (IBM Cpoptimizer) to make sure that the value of every single solution is distinct