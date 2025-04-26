# Magnus.exe - ChessBot in Python

## Overview
Magnus.exe is an AI-based ChessBot built in Python with a Tkinter GUI. It allows players to battle an AI opponent across multiple difficulty levels, with drag-and-drop piece movement and real-time snarky commentary from Magnus.exe.

## Features
- Play as White or Black
- Choose difficulty (Beginner to Advanced)
- Magnus.exe thinks ahead using Minimax search with dynamic depth scaling
- Smart evaluation based on material and positional bonuses
- GUI highlighting for legal moves
- Snarky comments generated dynamically
- End-game detection (Checkmate, Stalemate)

## Technologies Used
- Python
- tkinter (GUI)
- python-chess (game logic)
- Pillow (image handling)

## How to Run
1. Install the requirements:
    ```bash
    pip install python-chess pillow
    ```
2. Save your piece images into a folder (for example, `C:\Users\Lenovo\Pictures\Python\`).
3. Run the Python file:
    ```bash
    python chess_project_visual.py
    ```

## Future Scope
- Stockfish engine integration for Champion difficulty.
- Add timer and Blitz game modes.
- Multiplayer LAN support.
- Player statistics and achievements system.

---

*Created by Abhi Gupta, BTech CSE First Year (2025 Batch).*
