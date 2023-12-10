# Part 1
* pretty straightforward
* I intentially captured more information than I needed, planning for part 2
* used a regex to do the entire splitting of each scratchcard line
* Scratchcard class uses sets to store both sets of numbers, and then has a method that returns the intersection of those two lists
# Part 2
* this is a twist I did not plan for
* I love it when I run with the real input, after debugging vs the sample input, and it passes on the first try
* main issues here had to do with keeping separate counts of how many cards to add to and how many there were of the cards
* other issue was needing to not just add 1 to the subsequent cards, but add the number of copies of my current card I have