# Part 1
* so many off-by-1 errors
* mirrored rows/cols existed without, but reflections have to go *all the way to the edge* to count
    - this was not obvious from the problem statement
* basic strategy was to find *all* mirrored pairs that are adjacent (e.g. (3,4) would count if 3 == 4, but (2,5) would not, even if 2 == 5), and then for each of those pairs "growing" out to the nearest edge
# Part 2
* this looks obnoxious
* first idea: create a "matches" function that takes in two strings and returns if they match (and if not, how far off they are), and then use that, plus keeping the number of "off" areas (smudges) to a maximum of one, total
