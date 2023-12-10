# Part 1
* annoyingly complicated
* first major optimization problem
* solved by storing my map as tuples of (min_src, max_src) to delta(dest, src) and then checking that I was in between those numbers
* I did some clever things for building my maps, rather than having huge if-else statements for each mapping
# Part 2
* that's obnoxious - that's a tomorrow problem
* nearly 24 hours after I first saw the first part, I finished the second
* ended up building a class for Intervals and a class for Mappings, OOP saves my brain again