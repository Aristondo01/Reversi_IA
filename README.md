# Othello AI

We built a Minmax algorithm to play the board game Othello. It was a challenging project, because we had to make some research
about the mechanics of the algorithm itself, and how it could adapt to exploit the game.

## Features
- Heuristics: It had different heuristics, which lead it to try win the game. These heuristics included
  how many black and white pieces were on the board. It tried to get more or less pieces depending of the
  stage of the game. It tried to always get the corners of the board.
- Depth: Because Python is no so fast, we used a depth of 3 for the search tree. Nevertheless, we implemented
  iterative search, so it could go further if it had time left to respond.
- Socket connection: The professor of the course provided a server which managed the games. Our application
  connects to the server and sends info with the movements chosen, as it receives the moves from the opponent.
