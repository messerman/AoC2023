# Part 1
* easier than I anticipated when first reading the problem
* past days led me to do OOP right off-the-bat
* class represents a hand of Camel Cards with methods to:
    - "score" (return hand-type) the hand
    - compare the hand vs another hand (for use with sorting)
* create the CamelHands, sort them by score, then loop through and multiply score by bid
# Part 2
* much easier than I anticipated when first reading this part of the problem
* created a second mapping from card-letter (e.g. K) to card-value (e.g. 13) for when jokers are in play
* added a `jokers` flag to the CamelHands constructor
* there aren't that many cases where jokers can even exist for each hand-type
    - determined (by hand) which hand-types would change to which other hand-types based on number of jokers
* modified class' compare method to use the new card-letter-to-value mapping when jokers are in play
* major cleanup allowed me to significantly reduce the amount of duplicate code (collapsed solution1() and 2() to solutions() plus a flag, score_hand() method, etc)