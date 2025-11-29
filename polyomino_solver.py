#!/usr/bin/env python3
"""
Polyomino puzzle solver to verify if piece configurations can tile boards.
"""

import copy
from typing import List, Set, Tuple, Optional

# Define piece shapes as sets of (row, col) offsets from origin (0,0)
# Each piece includes all rotations and reflections

def get_all_orientations(piece: Set[Tuple[int, int]]) -> List[Set[Tuple[int, int]]]:
    """Generate all unique rotations and reflections of a piece."""
    orientations = set()

    def normalize(p: Set[Tuple[int, int]]) -> Tuple[Tuple[int, int], ...]:
        """Normalize piece to start at (0,0)."""
        min_r = min(r for r, c in p)
        min_c = min(c for r, c in p)
        normalized = tuple(sorted((r - min_r, c - min_c) for r, c in p))
        return normalized

    def rotate_90(p: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """Rotate piece 90 degrees clockwise."""
        return {(c, -r) for r, c in p}

    def reflect(p: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """Reflect piece horizontally."""
        return {(r, -c) for r, c in p}

    current = piece
    for _ in range(4):  # 4 rotations
        orientations.add(normalize(current))
        orientations.add(normalize(reflect(current)))
        current = rotate_90(current)

    return [set(o) for o in orientations]


# Define the pieces based on my interpretation
PIECES = {
    # Piece 1: I-tromino (3 cells horizontal)
    'piece1_I3': {(0, 0), (0, 1), (0, 2)},

    # Piece 2: O-tetromino (2x2 square)
    'piece2_O4': {(0, 0), (0, 1), (1, 0), (1, 1)},

    # Piece 3: Domino (2 cells)
    'piece3_I2': {(0, 0), (0, 1)},

    # Piece 4: L-tetromino (4 cells)
    'piece4_L4': {(0, 0), (1, 0), (2, 0), (2, 1)},

    # Piece 5: S-tetromino (4 cells)
    'piece5_S4': {(0, 1), (0, 2), (1, 0), (1, 1)},

    # Piece 6: Domino (2 cells)
    'piece6_I2': {(0, 0), (0, 1)},

    # Piece 7: L-tromino (3 cells)
    'piece7_L3': {(0, 0), (1, 0), (1, 1)},

    # Piece 8: L-tromino (3 cells)
    'piece8_L3': {(0, 0), (1, 0), (1, 1)},
}

# Alternative interpretation where piece 4 is L-tromino (3 cells)
PIECES_ALT = {
    'piece1_I3': {(0, 0), (0, 1), (0, 2)},
    'piece2_O4': {(0, 0), (0, 1), (1, 0), (1, 1)},
    'piece3_I2': {(0, 0), (0, 1)},
    'piece4_L3': {(0, 0), (1, 0), (1, 1)},  # Changed to L-tromino
    'piece5_S4': {(0, 1), (0, 2), (1, 0), (1, 1)},
    'piece6_I2': {(0, 0), (0, 1)},
    'piece7_L3': {(0, 0), (1, 0), (1, 1)},
    'piece8_L3': {(0, 0), (1, 0), (1, 1)},
}


def create_board(rows: int, cols: int, blocked: Set[Tuple[int, int]] = None) -> List[List[int]]:
    """Create a board with 0 = empty, -1 = blocked."""
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    if blocked:
        for r, c in blocked:
            if 0 <= r < rows and 0 <= c < cols:
                board[r][c] = -1
    return board


def can_place(board: List[List[int]], piece: Set[Tuple[int, int]],
              start_r: int, start_c: int) -> bool:
    """Check if piece can be placed at given position."""
    rows, cols = len(board), len(board[0])
    for dr, dc in piece:
        r, c = start_r + dr, start_c + dc
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != 0:
            return False
    return True


def place_piece(board: List[List[int]], piece: Set[Tuple[int, int]],
                start_r: int, start_c: int, piece_id: int) -> List[List[int]]:
    """Place piece on board, return new board."""
    new_board = copy.deepcopy(board)
    for dr, dc in piece:
        new_board[start_r + dr][start_c + dc] = piece_id
    return new_board


def find_first_empty(board: List[List[int]]) -> Optional[Tuple[int, int]]:
    """Find first empty cell (scanning left-to-right, top-to-bottom)."""
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == 0:
                return (r, c)
    return None


def solve(board: List[List[int]], pieces: List[Tuple[str, List[Set[Tuple[int, int]]]]],
          piece_idx: int = 0, solutions: List = None, max_solutions: int = 1) -> List:
    """
    Solve the puzzle using backtracking.
    Returns list of solution boards.
    """
    if solutions is None:
        solutions = []

    if len(solutions) >= max_solutions:
        return solutions

    # Find first empty cell
    empty = find_first_empty(board)

    if empty is None:
        # No empty cells - check if all pieces used
        if piece_idx >= len(pieces):
            solutions.append(copy.deepcopy(board))
        return solutions

    if piece_idx >= len(pieces):
        # No more pieces but board not full
        return solutions

    r, c = empty
    piece_name, orientations = pieces[piece_idx]

    # Try each orientation of current piece
    for orientation in orientations:
        # Try to place piece covering the empty cell
        for dr, dc in orientation:
            start_r, start_c = r - dr, c - dc
            if can_place(board, orientation, start_r, start_c):
                new_board = place_piece(board, orientation, start_r, start_c, piece_idx + 1)
                solve(new_board, pieces, piece_idx + 1, solutions, max_solutions)
                if len(solutions) >= max_solutions:
                    return solutions

    return solutions


def print_board(board: List[List[int]]):
    """Print board in readable format."""
    symbols = ' .123456789ABCDEFGHIJ'
    for row in board:
        print(' '.join(symbols[min(cell + 1, len(symbols) - 1)] for cell in row))


def test_configuration(pieces_dict: dict, board_rows: int, board_cols: int,
                       blocked: Set[Tuple[int, int]] = None, name: str = ""):
    """Test if a piece configuration can tile a board."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Board: {board_rows}x{board_cols} = {board_rows * board_cols} cells")
    if blocked:
        print(f"Blocked cells: {len(blocked)}")
        print(f"Playable cells: {board_rows * board_cols - len(blocked)}")

    total_cells = sum(len(p) for p in pieces_dict.values())
    print(f"Piece cells: {[len(p) for p in pieces_dict.values()]} = {total_cells} total")

    target = board_rows * board_cols - (len(blocked) if blocked else 0)
    if total_cells != target:
        print(f"❌ IMPOSSIBLE: Pieces ({total_cells}) != Target ({target})")
        return False

    # Prepare pieces with all orientations
    pieces = [(name, get_all_orientations(shape)) for name, shape in pieces_dict.items()]

    # Create board
    board = create_board(board_rows, board_cols, blocked)

    print(f"Searching for solution...")
    solutions = solve(board, pieces, max_solutions=1)

    if solutions:
        print(f"✅ SOLUTION FOUND!")
        print_board(solutions[0])
        return True
    else:
        print(f"❌ NO SOLUTION EXISTS")
        return False


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    print("POLYOMINO PUZZLE SOLVER")
    print("Testing various interpretations...")

    # Test 1: Original interpretation on 5x5 board (25 cells = 25 pieces)
    test_configuration(
        PIECES, 5, 5, None,
        "Original interpretation (25 cells) on 5x5 board"
    )

    # Test 2: Alternative interpretation (24 cells) on various boards
    total_alt = sum(len(p) for p in PIECES_ALT.values())
    print(f"\n\nAlternative interpretation total: {total_alt} cells")

    # Test 3: Check if original can tile 6x6 with some blocked cells
    # Block 11 cells to make 36-11=25 playable
    blocked_outer = set()
    # Block the outer ring except corners
    for i in range(6):
        if i not in [0, 5]:
            blocked_outer.add((0, i))  # top edge
            blocked_outer.add((5, i))  # bottom edge
            blocked_outer.add((i, 0))  # left edge
            blocked_outer.add((i, 5))  # right edge

    print(f"\nOuter ring blocked cells: {len(blocked_outer)}")

    # Test 4: What if only one color needs to be covered?
    # Create a 6x6 board where only gray cells are playable
    gray_cells = set()
    for r in range(6):
        for c in range(6):
            if (r + c) % 2 == 1:  # Gray cells
                gray_cells.add((r, c))
    black_cells = set()
    for r in range(6):
        for c in range(6):
            if (r + c) % 2 == 0:  # Black cells
                black_cells.add((r, c))

    print(f"\nGray cells (18): {len(gray_cells)}")
    print(f"Black cells (18): {len(black_cells)}")

    # Test if pieces can cover gray cells only (need 18 cells of pieces)
    # Since original is 25, this won't work
    print(f"\nOriginal pieces (25) cannot cover exactly 18 gray cells")

    # Let's find what piece configuration gives us 18 cells
    print("\n" + "="*60)
    print("SEARCHING FOR 18-CELL CONFIGURATIONS")
    print("="*60)

    # Minimum configuration
    pieces_min = {
        'piece1': {(0, 0), (0, 1)},  # 2 cells (domino)
        'piece2': {(0, 0), (0, 1), (1, 0), (1, 1)},  # 4 cells (square) - can't reduce
        'piece3': {(0, 0), (0, 1)},  # 2 cells
        'piece4': {(0, 0), (1, 0), (1, 1)},  # 3 cells (L-tromino)
        'piece5': {(0, 0), (1, 0), (1, 1)},  # 3 cells (bent tromino - NOT S-shape)
        'piece6': {(0, 0), (0, 1)},  # 2 cells
        'piece7': {(0, 0), (0, 1)},  # 2 cells (domino, not L-tromino)
        'piece8': {(0, 0), (0, 1)},  # 2 cells (domino, not L-tromino)
    }
    total_min = sum(len(p) for p in pieces_min.values())
    print(f"Minimum plausible interpretation: {total_min} cells")
    print("(This requires pieces 7, 8 to be dominoes, which contradicts their L-shape)")

    # What about 36?
    print("\n" + "="*60)
    print("TESTING 36-CELL POSSIBILITY")
    print("="*60)

    # To reach 36 from 25, we need +11 cells
    # This would require significant undercounting
    pieces_max = {
        'piece1': {(0, 0), (0, 1), (0, 2), (0, 3)},  # 4 cells (I-tetromino)
        'piece2': {(0, 0), (0, 1), (1, 0), (1, 1)},  # 4 cells
        'piece3': {(0, 0), (0, 1), (0, 2)},  # 3 cells
        'piece4': {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},  # 5 cells (L-pentomino)
        'piece5': {(0, 1), (0, 2), (1, 0), (1, 1), (2, 0)},  # 5 cells (S-pentomino)
        'piece6': {(0, 0), (0, 1), (0, 2)},  # 3 cells
        'piece7': {(0, 0), (1, 0), (2, 0), (2, 1)},  # 4 cells (L-tetromino)
        'piece8': {(0, 0), (1, 0), (2, 0), (2, 1)},  # 4 cells (L-tetromino)
    }
    total_max = sum(len(p) for p in pieces_max.values())
    print(f"Maximum plausible interpretation: {total_max} cells")

    if total_max >= 36:
        test_configuration(pieces_max, 6, 6, None, "Maximum interpretation on 6x6")
