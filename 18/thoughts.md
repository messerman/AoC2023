# Part 1
* First thing I did was update my visualization class to support RGB colors
* part 1 seems fairly straightforward, but doesn't use the colors - part 2 concerns me
* re-used a lot of code from day 16 - I should make my GridTile and Grid classes more generic and add them to tools
* ugh, same problem as day 10, where I have to determine if I'm inside or outside the enclosure
* did a decent job finding the 'inside vs outside' issue, but for some reason it's *really* slow when I'm cleaning up my list of tiles to look at
* cleaned up the above a bit by switching to a filter from a list comprehension
# Part 2
* 