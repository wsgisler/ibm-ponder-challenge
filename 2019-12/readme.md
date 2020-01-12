https://www.research.ibm.com/haifa/ponderthis/challenges/December2019.html

Problem statement
=================

Approximating absolute value.
Find an expression with no more than 15 operations (+, -, *, /) that approximates the absolute value function on the interval [-1,1] with an MSE (mean squared error) of no more than 0.0001.

For example, (x+1)/2 can be computed with only two operations and has an MSE of 1/6.

Solution approach
=================

I used SciPy to fit a curve around some sample values that I generated for the absolute value function. It is a really simple approach but works efficiently. Most of the code is for output purposes.
