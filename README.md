# shade_game
Proof of concept for a self teaching plant evolution art game thing

To see it in action, run:

`python3 demo.py`

## Wait, what is this?
The players in this game are plants, trying to develop better evolutionary strategies to outcompete their neighbours and collect the most sunlight.  That's a metaphor because games are more fun with colour.

Picture an array of 8x8 solar panels mounted on a wall.  These are real solar panels, these are not a metaphor. This is the game board. There is a window to the left of this array. Each solar panel is hinged on its left edge and paired with an motor that allows it to pivot to a 45 degree angle from the window (compared to the 90 degree angle that it would be at lying flat).  This allows it to capture more light, and cast shade on the panels to the right of it.  I'm still working on designing the hardware piece, so you'll need to use your imagination.  Here's some bad ASCII art:

    +-----------------------------------------------------+---------------------------------------------------------+
    |                             +------------+          |                                                         |
    |                   XXXXX     | Front view |          |                        +----------+                     |
    |                   X         +------------+          |                        |Top view  |                     |
    |                   X                                 |              XX        +----------+                     |
    |                  XXXXX     +--------+--------+      |              X    XX                                    |
    |                 XX         |        |        |      |      XXX    XXXXXXX                                     |
    |               XXX          |        |        |      |        XXXXXX  XXX                                      |
    |             XXXXXXX        |        |        |      |        XXX       X           XXX       +----------+     |
    |       XXXXXX      XX       +-----------------+      |        X          X            XX         Non-angled    |
    |           XX               |        |        |      |        X   Sun   XX             XX        panel         |
    |            XX              |        |        |      |      XXX        XX               XXXX     (in shade)    |
    |                            |        |        |      |        XX     XXX                   XX                  |
    |                            +--------+--------+      |         XXXXXX XXX           Angled                     |
    |                                                     |        XXX        X          panel                      |
    |                            ^        ^               |       XX                     (casting                   |
    |                            |        |               |                              shade)     x                |
    |                            +        |               |                                                         |
    |                            Hinge +--+               |                                                         |
    |                                                     |                                                         |
    |                                                     |                                                         |
    |                                                     |                                                         |
    |                                                     |                                                         |
    +-----------------------------------------------------+---------------------------------------------------------+

## That sounds like a boring game to play

That's because you're not supposed to play it smart ass, we've automated that part out.  Also, if you're just going to be negative, you can go home.

## So it's a game but I'm not supposed to play it?

Exactly. The idea is that you can watch evolution happening slower than it does in any kind of real ML training (allowing you to appreciate the nuance and beauty), but faster than it does in nature (because ain't nobody got time for that). Also, I want a cool electro-mechanical clanking thing doing machine learning in my living room. This will pit two rival algorithms against each other. Over the course of a day, the winner will be declared as the one who collects the most sunlight.  At then end of an elimination bracket (pairing many algorithms over many days), the highest scoring algorithms will live on, and also throw some slight variations on themselves in to the gene pool. I'll work up a dashboard eventually to monitor this.

## There are libraries that do most of this, why aren't you leveraging those

```
Tell me and I forget,
teach me and I remember,
involve me and I learn.
 ```

This is not built for efficiency or performance, it's built for the joy of building a thing.

## Currently implemented

Right now I'm just building out a rough framework to validate that the evolutionary algorithm can work in the way I'm picturing.  It could evolve into the actual code that will run the game, but right now it has a _lot_ of abstractions.

- Each player has x number of turns (this will happen in the real game, they will be evenly distributed throughout the day)
- The sun doesn't move (looking into the possibility of stopping the movement of the sun in real life, but I'm not hopeful)
- Points are awarded at the end of each turn for every non-shaded solar cell (final version will probably tally up time and/or intensity of light)
