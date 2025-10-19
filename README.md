# Chess Engine

A complete and polished chess game built using **Python** and **Pygame**, featuring realistic animations, full rule enforcement, and tournament-style time controls.

---

##  Overview

This project implements a **fully functional chess engine** that follows all standard **FIDE rules** of chess. It supports check, checkmate, stalemate, pawn promotion, castling, en passant, and time-based gameplay.

Designed to resemble professional online chess platforms, this engine combines **strong rule logic**, **intuitive controls**, and **smooth visuals** — making it ideal for both learners and developers looking to explore game programming, algorithms, and UI design.

---

##  Features

###  Game Rules

* All standard moves: Pawn, Rook, Knight, Bishop, Queen, King
* Special moves: Castling, En Passant, Pawn Promotion
* Check, Checkmate, and Stalemate detection
* Move legality enforcement (prevents illegal king exposures)

###  Visual System

* High-quality graphics rendered using Pygame
* Highlighting for selected pieces and possible moves
* Smooth animations (60 FPS interpolation)
* Modern, minimal interface with clean colors

### ⏱ Time Control System

* Dual player clocks (10-minute format by default)
* Automatic switching between turns
* Visual indication of active player
* Time-out detection and result handling

###  Game Management

* Detects and displays results (1-0, 0-1, or ½-½)
* Contextual messages for checkmate, stalemate, or time forfeit
* Simple restart with the `R` key

---

##  Installation

### Prerequisites

* Python 3.7 or newer
* pip package manager
* Pygame 2.0 or newer

### Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/chess-engine.git
cd chess-engine

# Install dependencies
pip install pygame
```

### Assets

Ensure the following images exist in `pieces/bases/`:

```
bp.png, br.png, bn.png, bb.png, bq.png, bk.png
wp.png, wr.png, wn.png, wb.png, wq.png, wk.png
```

Update file paths in `main.py` if your directory differs.

---

##  Usage

### Run the Game

```bash
python main.py
```

### Controls

* **Click** on a piece to view possible moves
* **Click** on a destination square to move
* **R key** – restart game
* **Automatic** turn switching and clock handling

### Pawn Promotion

When a pawn reaches the final rank, a dialog appears letting you choose between: **Queen**, **Rook**, **Bishop**, or **Knight**.

### Game End Conditions

* **Checkmate**: One player’s king cannot escape check
* **Stalemate**: Player has no legal moves but isn’t in check
* **Time Forfeit**: Player runs out of time

---

##  Technical Breakdown

### `chess_engine.py`

Contains the core logic and rule enforcement.

**GameState class:**

* Tracks current board layout, player turns, and move history
* Generates and validates legal moves
* Detects check, checkmate, and stalemate
* Handles special moves (castling, en passant)

**Move class:**

* Represents individual moves with start and end positions
* Stores captured pieces and promotion data
* Converts moves into algebraic notation

### `main.py`

Handles all **visuals**, **animation**, and **event handling**.

**Core Components:**

* Renders the board and chess pieces
* Displays player clocks and turn highlights
* Interpolates movement animations at 60 FPS
* Manages keyboard/mouse events and resets

---

##  Project Structure

```
chess-engine/
│
├── chess_engine.py       # Core logic and rule validation
├── main.py               # GUI and game loop
├── pieces/               # Image assets
│   └── bases/
└── README.md             # Documentation
```

---

##  Configuration

Modify these constants in `main.py` to customize behavior:

| Setting                    | Description                    | Default      |
| -------------------------- | ------------------------------ | ------------ |
| `width`, `height`          | Board display size             | 480 × 480    |
| `white_time`, `black_time` | Player starting time (seconds) | 600          |
| `max_fps`                  | Refresh rate                   | 15           |
| `frames_per_square`        | Animation smoothness           | 5            |
| Board colors               | Square color scheme            | Customizable |

---

##  Contributing

### Steps

1. Fork this repo
2. Create a new branch
3. Implement your feature
4. Test and commit changes
5. Open a pull request

### Guidelines

* Follow PEP 8 standards
* Add docstrings and comments
* Keep the code modular and clean
* Test thoroughly before submitting

### Potential Additions

* AI opponent
* Move history and PGN export
* Online multiplayer
* Opening book and evaluation
* Sound effects and themes

---

##  License & Credits

**License:** MIT License
**Built with:** Python, Pygame
**Inspired by:** https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&index=2
---

