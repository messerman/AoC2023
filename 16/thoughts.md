# Part 1
* mirror-bouncing - fun!
* created a new utility class for 'Position', originally from Day 14
* classes: GridTile, Pairing(GridTile, GridTile), Grid
* main process - starting at `starting tile`, and heading in `direction`, add each next-to-be-visited tile to a queue (paired with the from tile)
* eliminated out-of-bounds tiles, and had a history/visited list to keep track of pairings already seen (to avoid infinite bouncing)
* biggest issue was that the starting tile in my input was not a . tile, and my code assumed it was
* sample ran fast, but input took 87 seconds to finish (unsure why - need to run through a profiler?)
# Part 2
* I'm on vacation, or I'd have tried to fix my 87 second issue, above.
* Instead I just ran through every possible starting tile/direction, and let all of this run overnight
* return max of above possibilities