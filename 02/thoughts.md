# Part 1
* Parsing was definitely the pain point in this one.
* I really wanted to use regexps to parse this, but for the life of me I couldn't figure out how - wasted a lot of time on that
* I fell back on string manipulation using `split()`s and `strip()`s
* After that, it was just a matter of finding the max seen of each color in each round, and summing that up - easy
# Part 2
* First thing I did was split out my part 1 solution's parsing into its own function, and re-tested part 1 using that
* Once I had that, it was the same sort of max calculation, and then I just used a `functools.reduce()` to multiply all the max values per color per game, and then summed all the games
