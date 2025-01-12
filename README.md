# Lost In A Dungeon

A rougelike written in pygame.

<p align="center">
<img src="Screenshot_20250110_214304.png"
    alt="game screenshot"
    width="200"
    height="200"/>
</p>

## Usage

Clone the repo.

Run `pip install -r requirements.txt` to get pygame, if you don't have
it yet.

Then, run `$PYTHON3 src/main.py`, where `$PYTHON3` refers to your
Python 3 executable.

Currently, Python 3.13+ is supported.

### Command-Line Arguments

The application accepts an integer argument via the `-s` flag (long
form `--scale-factor`), used to scale the game display. For example,
the following invocation scales the game display by a factor of 2:

`python src/main.py -s 2`

Most users should be fine with the default, but in cases of a high
screen resolution, an argument of 2 may be needed.

## Background

You are lost in a maze, and need to find the way out.

Each time you enter the maze, it seems different each time.

Nevertheless, you are armed with a sword to fight anything that gets
in your way.

## Controls

Use w,a,s,d to move the player.

Use k to draw your sword, to kill the red crawlers.

## Rules and Objective

Avoid the crawlers. If you touch one, you lose the game.

Reach the stairs at the far corner of the maze, and you win.

## Sprite Attribution

[Legend of Zelda (Items and Weapons)](https://www.spriters-resource.com/nes/legendofzelda/sheet/54720/)

[Final Fantasy (Castle)](https://www.spriters-resource.com/nes/finalfantasy/sheet/115344/)

[Final Fantasy (Light Warriors)](https://www.spriters-resource.com/nes/finalfantasy/sheet/10555/)

## A Note on the Maze Generation Algorithm

The [Hunt and Kill](https://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm.html) algorithm is used to generate
a different maze on each run of the game.

It's similar to depth first search, except there's no need to keep a
stack for backtracking from dead ends.



