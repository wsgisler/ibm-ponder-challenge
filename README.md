# ibm-ponder-challenge
I occasionally solve the IBM ponder challenges (https://www.research.ibm.com/haifa/ponderthis/challenges/March2018.html) and often try to find a solution using a MIP, other optimization techniques or simulations

The code is written in Python often requires PuLP (https://github.com/coin-or/pulp), Docplex or GurobiPy.

My goal with these challenges is usually not to write the nicest piece of code, but to come up with a solution that is implemented quickly and uses only few lines of code. I appologize for the lack of comments and to compensate for it I will gladly take the time to explain my thoughts, if it is needed.

## Automatic notifications

I like to get automatic notifications when a new puzzle is available. For this purpose I made a small PHP script (cronjob.php) that is executed in regular intervals (using cron-job.org, a great free service). Feel free to use it for your own purposes. I recommend lima-city.de as a free web hoster with PHP support.
