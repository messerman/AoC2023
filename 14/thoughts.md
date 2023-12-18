# Part 1
* classes: Rock, Platform
* pretty straightforward - just move all the rocks until they collide with something
# Part 2
* added a `run_cycle` method, that would run through the cycle n times
* kept a history of where I'd been, to detect cycles
    * history was the string representing the whole Platform, so not efficient, but it worked
* biggest mistake: not making sure to start from the tilting-to side, first (otherwise they'd collide too early)
* second-biggest: cycles didn't have to go back to the starting state, so my stop condition was wrong
