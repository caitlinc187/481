# AI for Ultimate Tic Tac Toe Using Minimax and Heuristics
to run: python3 main.py

---

## Project Layout
```
481/
├── main.py                    # Application entry point
├── ultimate_tic_tac_toe.py    # Game rules, board logic, and AI
├── gui.py                     # GUI layout and interaction using pygames
```
---

## File Descriptions
**`main.py`**  
Initializes the game logic and GUI, sets up the Pygame window, and starts the main game loop. Runs the full GUI-based version of the game.

**`ultimate_tic_tac_toe.py`**  
Implements the core mechanics of the game:
- SmallBoard: Individual 3×3 boards with win detection.
- UltimateBoard: Manages 9 small boards and enforces Ultimate Tic Tac Toe rules.
- Minimax AI with Alpha-Beta pruning for optimal move selection.

**`gui.py`**  
Provides an interactive interface using Pygame:
- Renders the full Ultimate Tic Tac Toe grid.
- Highlights valid moves and next-board constraints.
- Handles player input and displays AI thinking status.
- Shows winners, draws, and board states.
