# Turn-Based Chess-Like Game

## Overview
This is a turn-based chess-like game built with a server-client architecture using WebSockets for real-time communication. The game is played on a 5x5 grid with two players, each controlling a team of characters (Pawns, Hero1, and Hero2). The server manages the game logic and state, while the client provides the user interface.

## Game Rules

### Characters and Movement
1. **Pawn**:
   - Moves one block in any direction (Left, Right, Forward, or Backward).
   - Move commands: `L` (Left), `R` (Right), `F` (Forward), `B` (Backward).

2. **Hero1**:
   - Moves two blocks straight in any direction.
   - Kills any opponent's character in its path.
   - Move commands: `L` (Left), `R` (Right), `F` (Forward), `B` (Backward).

3. **Hero2**:
   - Moves two blocks diagonally in any direction.
   - Kills any opponent's character in its path.
   - Move commands: `FL` (Forward-Left), `FR` (Forward-Right), `BL` (Backward-Left), `BR` (Backward-Right).

## Setup and Run Instructions

### 1. Prerequisites
- **Python 3.7+** installed on your machine.
- **Node.js** and a modern web browser (e.g., Chrome, Firefox) for running the client-side.

### 2. Server Setup and Run Instructions

#### Step 1: Clone the Repository
```bash
git clone https://github.com/saikiranhacker/vadamadurasaikiarn_21BCE9429.git
cd vadamadurasaikiarn_21BCE9429
