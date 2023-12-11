# Part 1
* As soon as I saw this day, I knew I had to do visualizations, so I spent some time cleaning up my codebase, and adding in some really basic utils (e.g. color-highlighting), cleaned up a lot of my template stuff, based on 9 days of using it, and added everything to a git project
* classes: MazeTile, Maze
* finding the "loop" was pretty straightforward - but I had to break my recursive approach out to a looped one when I hit the "real" input
# Part 2
* this was a beast - first one I didn't get done w/in 24 hours
* I got an almost-working solution done by finding "groups" and then if any of them were not "enclosed" (i.e. looped pipes in each direction) then I marked it as "outside" - but this left out the annoying edge case where the tile might be enclosed but on the wrong "side" of the loop
* eventually (w/ hints) got that edge case working by expanding the whole maze (doubling it in size), and then finding outsides, and then collapsing back to the original size
* final solution was so slow I thought something was broken, but it finished w/in a few minutes