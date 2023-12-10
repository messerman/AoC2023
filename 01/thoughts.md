# Part 1
* pretty straightforward
* used a regex to find all the digits (`r'\d'`)
# Part 2
* hardest day 1.2 ever?
* first attempt (lookup dictionary with things like `one: 1`, and a new regex of `\d|one|two|three|four|five|six|seven|eight|nine` did not work due to words like `oneight` only picking up one, and not eight)
* second attempt involved a reverse lookup table (`eno: 1`, etc) and a reversal of the input string to find what I wanted
* post-success cleanup, generated my regexes, and collapsed my lookup dicts to a single line each
