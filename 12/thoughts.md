# Part 1
* parsing was straightforward
* made a class (ConditionRecord) to operate on each row
* big recursion method (had to make it @classmethod?) to translate '?' into '.' and '#'
* then verified every possible string from above, then split by '.' again, against a list of '#' strings corresponding to the lengths of the damaged contiguous sections
* not exactly efficient
# Part 2
* make it bigger - this kills my solution to part 1, unsurprisingly
* tried memoizing my recursive method, above, but it didn't seem to help
* looks like most people used dynamic programming