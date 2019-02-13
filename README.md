# Conway's Game of Life
An implementation of Conway's Game of Like in Python.

## Rules
The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, alive or dead, (or populated and unpopulated, respectively). Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:
* any live cell with fewer than two live neighbors dies, as if by underpopulation;
* any live cell with two or three live neighbors lives on to the next generation;
* any live cell with more than three live neighbors dies, as if by overpopulation;
* any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules simultaneously to every cell in the seed; births and deaths occur simultaneously, and the discrete moment at which this happens is sometimes called a tick. Each generation is a pure function of the preceding one. The rules continue to be applied repeatedly to create further generations.

<p align="center">
<img  src="https://i.imgur.com/P45WdoT.jpg" width="30%" height="30%"/>
</p>

## Functionalities
You can draw your starting configuration with mouse clicks and save the image to load it at any time later; you can also 
load some pre-built configurations.

<p align="center">
<img  src="https://media.giphy.com/media/kh71Gg2qOJangAGiuo/giphy.gif" width="50%" height="50%"/>
</p>

The app provides some extra features:

* you can zoom out/in from a 30x30 cells map to 200x200;
* you can speedup time increasing frame rate, starting from 1 fps to 60;
* you can see the cells lifetime pressing the ```heatmap``` toggle.

## License
Licensed under the term of [MIT License](https://github.com/SestoAle/Conway-s-Game-of-Life/blob/master/LICENSE).
