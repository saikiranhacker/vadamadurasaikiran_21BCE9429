import asyncio
import websockets
import json

class TurnBasedGame:
    def __init__(self):
        self.board = [['' for _ in range(5)] for _ in range(5)]
        self.current_player = 'A'
        self.setup_board()

    def setup_board(self):
        # Player A's pieces (P1, H1, H2)
        self.board[0] = ['A-P1', 'A-H1', 'A-P1', 'A-H2', 'A-P1']
        # Player B's pieces (P1, H2, P1, H1, P1)
        self.board[4] = ['B-P1', 'B-H2', 'B-P1', 'B-H1', 'B-P1']

    def is_valid_move(self, start_pos, end_pos, piece):
        x1, y1 = start_pos
        x2, y2 = end_pos

        # Ensure move is within the board boundaries
        if not (0 <= x2 < 5 and 0 <= y2 < 5):
            return False, "Move out of bounds"

        # Ensure the end position is not occupied by the same player's piece
        if self.board[x2][y2] and self.board[x2][y2][0] == piece[0]:
            return False, "Cannot move to a space occupied by your own piece"

        if piece.endswith('P1'):  # Pawn moves one block in any direction
            if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1:
                return True, None
        elif piece.endswith('H1'):  # Hero1 moves two blocks straight in any direction
            if (abs(x2 - x1) == 2 and y1 == y2) or (abs(y2 - y1) == 2 and x1 == x2):
                return True, None
        elif piece.endswith('H2'):  # Hero2 moves two blocks diagonally
            if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
                return True, None

        return False, "Invalid move for the selected piece"

    def get_path(self, start_pos, end_pos):
        path = []
        x1, y1 = start_pos
        x2, y2 = end_pos
        if x1 == x2:  # Horizontal move
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                path.append((x1, y))
        elif y1 == y2:  # Vertical move
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                path.append((x, y1))
        elif abs(x2 - x1) == abs(y2 - y1):  # Diagonal move
            if x2 > x1 and y2 > y1:  # Down-Right
                for i in range(1, x2 - x1):
                    path.append((x1 + i, y1 + i))
            elif x2 > x1 and y2 < y1:  # Down-Left
                for i in range(1, x2 - x1):
                    path.append((x1 + i, y1 - i))
            elif x2 < x1 and y2 > y1:  # Up-Right
                for i in range(1, x1 - x2):
                    path.append((x1 - i, y1 + i))
            elif x2 < x1 and y2 < y1:  # Up-Left
                for i in range(1, x1 - x2):
                    path.append((x1 - i, y1 - i))
        return path

    def move(self, start_pos, end_pos, piece):
        valid, error_message = self.is_valid_move(start_pos, end_pos, piece)
        if valid:
            # Clear the start position
            self.board[start_pos[0]][start_pos[1]] = ''
            # Remove any opponent's piece in the path for Hero1 and Hero2
            if piece.endswith('H1') or piece.endswith('H2'):
                path = self.get_path(start_pos, end_pos)
                for x, y in path:
                    if self.board[x][y] and self.board[x][y][0] != piece[0]:
                        self.board[x][y] = ''
            # Set the piece at the end position
            self.board[end_pos[0]][end_pos[1]] = piece

            # Switch to the other player
            self.current_player = 'B' if self.current_player == 'A' else 'A'
            return True, None
        else:
            return False, error_message

    def get_game_state(self):
        return {
            "board": self.board,
            "current_player": self.current_player
        }

async def handle_connection(websocket, path):
    game = TurnBasedGame()

    async def send_game_state():
        state = json.dumps(game.get_game_state())
        await websocket.send(state)

    await send_game_state()

    async for message in websocket:
        move = json.loads(message)
        start_pos = move['start']
        end_pos = move['end']
        piece = move['piece']

        success, error = game.move(start_pos, end_pos, piece)
        if success:
            await send_game_state()
        else:
            await websocket.send(json.dumps({'error': error}))

async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
