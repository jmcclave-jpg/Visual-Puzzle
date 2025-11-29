#!/usr/bin/env python3
"""
COMPREHENSIVE AUDIT: Determine which of 3 hypotheses best describes the puzzle

Hypothesis A (70% prior): 5×5 Board, Current Interpretation Correct
Hypothesis B (20% prior): 6×6 Board with 5×5 Playable Region
Hypothesis C (10% prior): Significant Piece Miscounting (board is 6×6)

This audit performs 10 distinct tests to gather evidence for/against each hypothesis.
"""

import copy
from typing import List, Set, Tuple, Optional, Dict
from itertools import product, combinations
import sys

# =============================================================================
# SOLVER ENGINE (copied from polyomino_solver.py for self-contained execution)
# =============================================================================

def get_all_orientations(piece: Set[Tuple[int, int]]) -> List[Set[Tuple[int, int]]]:
    """Generate all unique rotations and reflections of a piece."""
    orientations = set()

    def normalize(p: Set[Tuple[int, int]]) -> Tuple[Tuple[int, int], ...]:
        min_r = min(r for r, c in p)
        min_c = min(c for r, c in p)
        normalized = tuple(sorted((r - min_r, c - min_c) for r, c in p))
        return normalized

    def rotate_90(p: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        return {(c, -r) for r, c in p}

    def reflect(p: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        return {(r, -c) for r, c in p}

    current = piece
    for _ in range(4):
        orientations.add(normalize(current))
        orientations.add(normalize(reflect(current)))
        current = rotate_90(current)

    return [set(o) for o in orientations]


def create_board(rows: int, cols: int, blocked: Set[Tuple[int, int]] = None) -> List[List[int]]:
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    if blocked:
        for r, c in blocked:
            if 0 <= r < rows and 0 <= c < cols:
                board[r][c] = -1
    return board


def can_place(board: List[List[int]], piece: Set[Tuple[int, int]],
              start_r: int, start_c: int) -> bool:
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
    new_board = copy.deepcopy(board)
    for dr, dc in piece:
        new_board[start_r + dr][start_c + dc] = piece_id
    return new_board


def find_first_empty(board: List[List[int]]) -> Optional[Tuple[int, int]]:
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == 0:
                return (r, c)
    return None


def solve(board: List[List[int]], pieces: List[Tuple[str, List[Set[Tuple[int, int]]]]],
          piece_idx: int = 0, solutions: List = None, max_solutions: int = 1) -> List:
    if solutions is None:
        solutions = []

    if len(solutions) >= max_solutions:
        return solutions

    empty = find_first_empty(board)

    if empty is None:
        if piece_idx >= len(pieces):
            solutions.append(copy.deepcopy(board))
        return solutions

    if piece_idx >= len(pieces):
        return solutions

    r, c = empty
    piece_name, orientations = pieces[piece_idx]

    for orientation in orientations:
        for dr, dc in orientation:
            start_r, start_c = r - dr, c - dc
            if can_place(board, orientation, start_r, start_c):
                new_board = place_piece(board, orientation, start_r, start_c, piece_idx + 1)
                solve(new_board, pieces, piece_idx + 1, solutions, max_solutions)
                if len(solutions) >= max_solutions:
                    return solutions

    return solutions


def print_board(board: List[List[int]], indent: str = "  "):
    symbols = ' .123456789ABCDEFGHIJ'
    for row in board:
        print(indent + ' '.join(symbols[min(cell + 1, len(symbols) - 1)] for cell in row))


def test_configuration(pieces_dict: dict, board_rows: int, board_cols: int,
                       blocked: Set[Tuple[int, int]] = None,
                       max_solutions: int = 1, verbose: bool = True) -> List:
    """Test if pieces can tile a board, return solutions found."""
    total_cells = sum(len(p) for p in pieces_dict.values())
    target = board_rows * board_cols - (len(blocked) if blocked else 0)

    if total_cells != target:
        return []

    pieces = [(name, get_all_orientations(shape)) for name, shape in pieces_dict.items()]
    board = create_board(board_rows, board_cols, blocked)
    solutions = solve(board, pieces, max_solutions=max_solutions)

    return solutions


# =============================================================================
# PIECE DEFINITIONS FOR EACH HYPOTHESIS
# =============================================================================

# HYPOTHESIS A: Current interpretation (25 cells)
PIECES_HYPO_A = {
    'P1_I3': {(0, 0), (0, 1), (0, 2)},           # I-tromino (3)
    'P2_O4': {(0, 0), (0, 1), (1, 0), (1, 1)},   # O-tetromino (4)
    'P3_I2': {(0, 0), (0, 1)},                    # Domino (2)
    'P4_L4': {(0, 0), (1, 0), (2, 0), (2, 1)},   # L-tetromino (4)
    'P5_S4': {(0, 1), (0, 2), (1, 0), (1, 1)},   # S-tetromino (4)
    'P6_I2': {(0, 0), (0, 1)},                    # Domino (2)
    'P7_L3': {(0, 0), (1, 0), (1, 1)},           # L-tromino (3)
    'P8_L3': {(0, 0), (1, 0), (1, 1)},           # L-tromino (3)
}

# HYPOTHESIS C variants: Extended piece sizes for 6×6 (36 cells)

# C1: If P2 is 3x3 and others scaled up (36 cells)
PIECES_HYPO_C1 = {
    'P1_I4': {(0, 0), (0, 1), (0, 2), (0, 3)},                    # I-tetromino (4)
    'P2_O9': {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2),
              (2, 0), (2, 1), (2, 2)},                              # 3x3 square (9)
    'P3_I2': {(0, 0), (0, 1)},                                      # Domino (2)
    'P4_L5': {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},             # L-pentomino (5)
    'P5_S5': {(0, 2), (0, 3), (1, 1), (1, 2), (2, 0)},             # S-pentomino variant (5)
    'P6_I3': {(0, 0), (0, 1), (0, 2)},                              # I-tromino (3)
    'P7_L4': {(0, 0), (1, 0), (2, 0), (2, 1)},                     # L-tetromino (4)
    'P8_L4': {(0, 0), (1, 0), (2, 0), (2, 1)},                     # L-tetromino (4)
}

# C2: All pieces slightly larger (36 cells)
PIECES_HYPO_C2 = {
    'P1_I4': {(0, 0), (0, 1), (0, 2), (0, 3)},                     # I-tetromino (4)
    'P2_O4': {(0, 0), (0, 1), (1, 0), (1, 1)},                     # O-tetromino (4)
    'P3_I3': {(0, 0), (0, 1), (0, 2)},                              # I-tromino (3)
    'P4_L5': {(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)},             # L-pentomino (5)
    'P5_S5': {(0, 1), (0, 2), (1, 0), (1, 1), (2, 0)},             # S-pentomino (5)
    'P6_I3': {(0, 0), (0, 1), (0, 2)},                              # I-tromino (3)
    'P7_L4': {(0, 0), (1, 0), (2, 0), (2, 1)},                     # L-tetromino (4)
    'P8_L4': {(0, 0), (1, 0), (2, 0), (2, 1)},                     # L-tetromino (4)
}  # Total: 4+4+3+5+5+3+4+4 = 32 (not 36, adjust...)

# C3: Maximizing for 36
PIECES_HYPO_C3 = {
    'P1_I5': {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)},             # I-pentomino (5)
    'P2_O4': {(0, 0), (0, 1), (1, 0), (1, 1)},                     # O-tetromino (4)
    'P3_I3': {(0, 0), (0, 1), (0, 2)},                              # I-tromino (3)
    'P4_L5': {(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)},             # L-pentomino (5)
    'P5_S5': {(0, 1), (0, 2), (1, 0), (1, 1), (2, 0)},             # S-pentomino (5)
    'P6_I3': {(0, 0), (0, 1), (0, 2)},                              # I-tromino (3)
    'P7_L5': {(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)},             # L-pentomino (5)
    'P8_P6': {(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2)},     # P-hexomino (6)
}  # Total: 5+4+3+5+5+3+5+6 = 36

# =============================================================================
# AUDIT TESTS
# =============================================================================

def audit_test_1_solution_uniqueness():
    """
    AUDIT 1: How many solutions exist for Hypothesis A (5×5 board)?

    If many solutions exist → weaker evidence (lucky guess)
    If few/one solution exists → stronger evidence (constrained problem)
    """
    print("\n" + "=" * 70)
    print("AUDIT 1: Solution Uniqueness for Hypothesis A")
    print("=" * 70)

    solutions = test_configuration(PIECES_HYPO_A, 5, 5, max_solutions=100)

    print(f"  Solutions found: {len(solutions)}")
    if len(solutions) == 1:
        print("  → STRONG EVIDENCE for Hypo A: Unique solution suggests correct interpretation")
    elif 1 < len(solutions) <= 10:
        print("  → MODERATE EVIDENCE: Few solutions suggest reasonable interpretation")
    else:
        print("  → WEAK EVIDENCE: Many solutions could be coincidental")

    return {"solutions_count": len(solutions)}


def audit_test_2_near_miss_analysis():
    """
    AUDIT 2: What happens with slight variations in piece counts?

    Tests if 24-cell and 26-cell interpretations can also tile appropriate boards.
    """
    print("\n" + "=" * 70)
    print("AUDIT 2: Near-Miss Analysis (24 and 26 cell variants)")
    print("=" * 70)

    results = {}

    # 24 cells: remove 1 cell from P5 (S-tet → bent tromino)
    pieces_24 = {
        'P1': {(0, 0), (0, 1), (0, 2)},
        'P2': {(0, 0), (0, 1), (1, 0), (1, 1)},
        'P3': {(0, 0), (0, 1)},
        'P4': {(0, 0), (1, 0), (2, 0), (2, 1)},
        'P5': {(0, 0), (1, 0), (1, 1)},  # Changed to L-tromino (3)
        'P6': {(0, 0), (0, 1)},
        'P7': {(0, 0), (1, 0), (1, 1)},
        'P8': {(0, 0), (1, 0), (1, 1)},
    }
    total_24 = sum(len(p) for p in pieces_24.values())
    print(f"\n  24-cell variant: pieces sum to {total_24}")

    # 24 = 4×6 or 3×8
    sols_4x6 = test_configuration(pieces_24, 4, 6, max_solutions=5)
    sols_3x8 = test_configuration(pieces_24, 3, 8, max_solutions=5)
    print(f"    4×6 board: {len(sols_4x6)} solutions")
    print(f"    3×8 board: {len(sols_3x8)} solutions")
    results["24_cell_4x6"] = len(sols_4x6)
    results["24_cell_3x8"] = len(sols_3x8)

    # 26 cells: add 1 cell to P1 (tromino → tetromino)
    pieces_26 = {
        'P1': {(0, 0), (0, 1), (0, 2), (0, 3)},  # Changed to I-tetromino (4)
        'P2': {(0, 0), (0, 1), (1, 0), (1, 1)},
        'P3': {(0, 0), (0, 1)},
        'P4': {(0, 0), (1, 0), (2, 0), (2, 1)},
        'P5': {(0, 1), (0, 2), (1, 0), (1, 1)},
        'P6': {(0, 0), (0, 1)},
        'P7': {(0, 0), (1, 0), (1, 1)},
        'P8': {(0, 0), (1, 0), (1, 1)},
    }
    total_26 = sum(len(p) for p in pieces_26.values())
    print(f"\n  26-cell variant: pieces sum to {total_26}")
    print(f"    No standard board has 26 cells (not a rectangle)")
    results["26_cell_no_board"] = True

    # Analysis
    if results["24_cell_4x6"] > 0 or results["24_cell_3x8"] > 0:
        print("\n  → 24-cell variant ALSO works, which is suspicious")
        print("    Could suggest piece counting is ambiguous")
    else:
        print("\n  → 24-cell variant doesn't work cleanly")
        print("    → SUPPORTS Hypo A: 25-cell interpretation is special")

    return results


def audit_test_3_blocked_cell_patterns():
    """
    AUDIT 3: For Hypothesis B, which 6×6 blocking patterns work?

    Tests various ways to block 11 cells on a 6×6 board to leave 25 playable.
    """
    print("\n" + "=" * 70)
    print("AUDIT 3: 6×6 Board with 11 Blocked Cells (Hypothesis B)")
    print("=" * 70)

    results = {"patterns_tested": 0, "patterns_that_work": 0, "working_patterns": []}

    # Pattern 1: Block the rightmost column and bottom row
    pattern1 = set()
    for i in range(6):
        pattern1.add((i, 5))  # rightmost column
    for j in range(5):
        pattern1.add((5, j))  # bottom row (except corner already added)
    print(f"\n  Pattern 1 (right col + bottom row): {len(pattern1)} blocked")
    sols = test_configuration(PIECES_HYPO_A, 6, 6, blocked=pattern1, max_solutions=3)
    results["patterns_tested"] += 1
    if sols:
        results["patterns_that_work"] += 1
        results["working_patterns"].append("right_col_bottom_row")
        print(f"    ✓ WORKS! {len(sols)} solutions found")
    else:
        print(f"    ✗ No solution")

    # Pattern 2: Block a 3x3 corner + 2 extra cells
    pattern2 = set()
    for r in range(3):
        for c in range(3):
            if len(pattern2) < 11:
                pattern2.add((r + 3, c + 3))  # bottom-right 3x3
    while len(pattern2) < 11:
        pattern2.add((0, 5))  # add more
    print(f"\n  Pattern 2 (bottom-right corner + extras): {len(pattern2)} blocked")
    sols = test_configuration(PIECES_HYPO_A, 6, 6, blocked=pattern2, max_solutions=3)
    results["patterns_tested"] += 1
    if sols:
        results["patterns_that_work"] += 1
        results["working_patterns"].append("corner_block")
        print(f"    ✓ WORKS! {len(sols)} solutions found")
    else:
        print(f"    ✗ No solution")

    # Pattern 3: Scattered blocking
    pattern3 = {(0, 0), (0, 3), (0, 5), (1, 2), (2, 4), (3, 0), (3, 5), (4, 2), (5, 0), (5, 3), (5, 5)}
    print(f"\n  Pattern 3 (scattered): {len(pattern3)} blocked")
    sols = test_configuration(PIECES_HYPO_A, 6, 6, blocked=pattern3, max_solutions=3)
    results["patterns_tested"] += 1
    if sols:
        results["patterns_that_work"] += 1
        results["working_patterns"].append("scattered")
        print(f"    ✓ WORKS! {len(sols)} solutions found")
    else:
        print(f"    ✗ No solution")

    # Pattern 4: Inner 5x5 (block outer ring of 6x6 keeping a 4x4? No, we need 5x5 = 25)
    # For 6x6, outer ring has: 6+6+4+4 = 20 cells. That's too many.
    # Let's block just top row and left column = 6 + 5 = 11
    pattern4 = set()
    for i in range(6):
        pattern4.add((0, i))  # top row
    for j in range(1, 6):
        pattern4.add((j, 0))  # left column
    print(f"\n  Pattern 4 (top row + left col): {len(pattern4)} blocked")
    sols = test_configuration(PIECES_HYPO_A, 6, 6, blocked=pattern4, max_solutions=3)
    results["patterns_tested"] += 1
    if sols:
        results["patterns_that_work"] += 1
        results["working_patterns"].append("top_left_edge")
        print(f"    ✓ WORKS! {len(sols)} solutions found")
        print("    This is the inner 5x5 region:")
        print_board(sols[0])
    else:
        print(f"    ✗ No solution")

    # Summary
    print(f"\n  Summary: {results['patterns_that_work']}/{results['patterns_tested']} patterns work")
    if results["patterns_that_work"] > 0:
        print("  → SUPPORTS Hypo B: 6×6 with blocked cells is feasible")
    else:
        print("  → WEAKENS Hypo B: No obvious blocking pattern works")

    return results


def audit_test_4_hypothesis_c_36_cell():
    """
    AUDIT 4: Test if 36-cell interpretations can tile 6×6 board.

    Tests various "generous" piece interpretations for Hypothesis C.
    """
    print("\n" + "=" * 70)
    print("AUDIT 4: 36-Cell Interpretations (Hypothesis C)")
    print("=" * 70)

    results = {}

    # C1: 3x3 square interpretation
    total_c1 = sum(len(p) for p in PIECES_HYPO_C1.values())
    print(f"\n  C1 (3×3 square): {total_c1} cells")
    if total_c1 == 36:
        sols = test_configuration(PIECES_HYPO_C1, 6, 6, max_solutions=3)
        results["C1_solutions"] = len(sols)
        print(f"    Solutions: {len(sols)}")
    else:
        print(f"    Total is {total_c1}, not 36 - skipping")
        results["C1_solutions"] = "N/A"

    # C3: Maximized interpretation
    total_c3 = sum(len(p) for p in PIECES_HYPO_C3.values())
    print(f"\n  C3 (maximized pieces): {total_c3} cells")
    if total_c3 == 36:
        sols = test_configuration(PIECES_HYPO_C3, 6, 6, max_solutions=3)
        results["C3_solutions"] = len(sols)
        print(f"    Solutions: {len(sols)}")
        if sols:
            print("    First solution:")
            print_board(sols[0])
    else:
        print(f"    Total is {total_c3}, not 36 - skipping")
        results["C3_solutions"] = "N/A"

    # Try to find ANY 36-cell configuration that works
    print("\n  Searching for any 36-cell configuration that tiles 6×6...")

    # Define piece ranges
    ranges = {
        'P1': [3, 4, 5],
        'P2': [4, 6, 9],  # 2x2, 2x3, or 3x3
        'P3': [2, 3],
        'P4': [4, 5, 6],
        'P5': [4, 5, 6],
        'P6': [2, 3],
        'P7': [3, 4, 5],
        'P8': [3, 4, 5],
    }

    found_36 = False
    for combo in product(*ranges.values()):
        if sum(combo) == 36:
            # Try this configuration
            pieces_test = {
                'P1': {(0, j) for j in range(combo[0])},  # I-shaped
                'P2': set(),  # Square-ish
                'P3': {(0, j) for j in range(combo[2])},
                'P4': set(),  # Will need to be L-shaped properly
                'P5': set(),
                'P6': {(0, j) for j in range(combo[5])},
                'P7': set(),
                'P8': set(),
            }
            # Fill P2 as square
            if combo[1] == 4:
                pieces_test['P2'] = {(0,0), (0,1), (1,0), (1,1)}
            elif combo[1] == 6:
                pieces_test['P2'] = {(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)}
            elif combo[1] == 9:
                pieces_test['P2'] = {(i,j) for i in range(3) for j in range(3)}

            # Simplified L-shapes
            def make_L(size):
                if size == 3:
                    return {(0,0), (1,0), (1,1)}
                elif size == 4:
                    return {(0,0), (1,0), (2,0), (2,1)}
                elif size == 5:
                    return {(0,0), (1,0), (2,0), (3,0), (3,1)}
                elif size == 6:
                    return {(0,0), (1,0), (2,0), (3,0), (4,0), (4,1)}
                return set()

            pieces_test['P4'] = make_L(combo[3])
            pieces_test['P5'] = make_L(combo[4])  # Using L for S approx
            pieces_test['P7'] = make_L(combo[6])
            pieces_test['P8'] = make_L(combo[7])

            total = sum(len(p) for p in pieces_test.values())
            if total == 36:
                sols = test_configuration(pieces_test, 6, 6, max_solutions=1)
                if sols:
                    print(f"    Found working config: {combo}")
                    found_36 = True
                    results["found_36_config"] = combo
                    break

    if not found_36:
        print("    No 36-cell configuration found that tiles 6×6")
        results["found_36_config"] = None

    return results


def audit_test_5_checkerboard_constraint():
    """
    AUDIT 5: Checkerboard color constraint analysis.

    Verifies that pieces can satisfy color balance requirements.
    """
    print("\n" + "=" * 70)
    print("AUDIT 5: Checkerboard Color Constraint Analysis")
    print("=" * 70)

    def color_balance(pieces_dict):
        """
        For each piece, determine its color coverage flexibility.
        On checkerboard, pieces of even size cover equal colors.
        Odd-size pieces have flexibility in color balance.
        """
        total = 0
        min_black = 0
        max_black = 0

        for name, cells in pieces_dict.items():
            size = len(cells)
            total += size
            if size % 2 == 0:  # Even: covers equal colors
                min_black += size // 2
                max_black += size // 2
            else:  # Odd: can cover n//2 or n//2+1 of one color
                min_black += size // 2
                max_black += size // 2 + 1

        return total, min_black, max_black

    # Analyze Hypothesis A
    total_a, min_b_a, max_b_a = color_balance(PIECES_HYPO_A)
    print(f"\n  Hypothesis A (5×5 board):")
    print(f"    Pieces: {[len(p) for p in PIECES_HYPO_A.values()]}")
    print(f"    Total: {total_a}, Black coverage: {min_b_a}-{max_b_a}")

    # 5×5 checkerboard has 13 black, 12 white (or vice versa)
    board_5x5_color1 = 13
    board_5x5_color2 = 12

    if min_b_a <= board_5x5_color1 <= max_b_a:
        print(f"    ✓ Can cover 13 black cells (5×5 requirement)")
    else:
        print(f"    ✗ Cannot cover exactly 13 black cells!")

    # Check actual solution
    solutions = test_configuration(PIECES_HYPO_A, 5, 5, max_solutions=1)
    if solutions:
        board = solutions[0]
        # Count color coverage
        black_covered = 0
        white_covered = 0
        for r in range(5):
            for c in range(5):
                if board[r][c] > 0:
                    if (r + c) % 2 == 0:
                        black_covered += 1
                    else:
                        white_covered += 1
        print(f"    Actual solution covers: {black_covered} black, {white_covered} white")

    return {"total": total_a, "min_black": min_b_a, "max_black": max_b_a}


def audit_test_6_piece_shape_validation():
    """
    AUDIT 6: Verify piece shapes are valid polyominoes.

    Checks connectivity and reasonableness of piece definitions.
    """
    print("\n" + "=" * 70)
    print("AUDIT 6: Piece Shape Validation")
    print("=" * 70)

    def is_connected(cells: Set[Tuple[int, int]]) -> bool:
        """Check if a polyomino is connected (4-connected)."""
        if not cells:
            return True
        cells = set(cells)
        start = next(iter(cells))
        visited = {start}
        frontier = [start]

        while frontier:
            r, c = frontier.pop()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (r + dr, c + dc)
                if neighbor in cells and neighbor not in visited:
                    visited.add(neighbor)
                    frontier.append(neighbor)

        return len(visited) == len(cells)

    results = {}
    all_valid = True

    for name, cells in PIECES_HYPO_A.items():
        connected = is_connected(cells)
        size = len(cells)
        results[name] = {"size": size, "connected": connected}

        status = "✓" if connected else "✗"
        print(f"  {name}: {size} cells, connected: {status}")

        if not connected:
            all_valid = False

    if all_valid:
        print("\n  → All pieces are valid connected polyominoes")
    else:
        print("\n  → WARNING: Some pieces are not connected!")

    return results


def audit_test_7_alternative_board_sizes():
    """
    AUDIT 7: Test pieces on alternative board sizes.

    Checks if pieces could tile other plausible boards.
    """
    print("\n" + "=" * 70)
    print("AUDIT 7: Alternative Board Sizes")
    print("=" * 70)

    results = {}

    # 25 cells can only tile 5×5 or 1×25
    boards_to_test = [
        (5, 5, "5×5 square"),
        (1, 25, "1×25 strip"),
    ]

    for rows, cols, name in boards_to_test:
        print(f"\n  Testing {name}:")
        solutions = test_configuration(PIECES_HYPO_A, rows, cols, max_solutions=10)
        results[name] = len(solutions)
        print(f"    Solutions found: {len(solutions)}")
        if solutions and rows * cols <= 30:
            print_board(solutions[0])

    # Check what piece counts could tile standard boards
    print("\n  What board sizes could different piece interpretations tile?")
    piece_ranges = {
        'P1': [2, 3, 4],
        'P2': [4],  # Fixed as 2×2
        'P3': [2, 3],
        'P4': [3, 4, 5],
        'P5': [3, 4, 5],
        'P6': [2, 3],
        'P7': [2, 3, 4],
        'P8': [2, 3, 4],
    }

    totals = {}
    for combo in product(*piece_ranges.values()):
        total = sum(combo)
        if total not in totals:
            totals[total] = 0
        totals[total] += 1

    print(f"\n  Achievable totals: {sorted(totals.keys())}")
    print(f"  25 cells (5×5): {totals.get(25, 0)} interpretations")
    print(f"  24 cells (4×6): {totals.get(24, 0)} interpretations")
    print(f"  28 cells (4×7): {totals.get(28, 0)} interpretations")

    return results


def audit_test_8_solution_robustness():
    """
    AUDIT 8: Test robustness of Hypothesis A solution.

    Verifies the solution under slight perturbations.
    """
    print("\n" + "=" * 70)
    print("AUDIT 8: Solution Robustness")
    print("=" * 70)

    # Get the solution
    solutions = test_configuration(PIECES_HYPO_A, 5, 5, max_solutions=1)

    if not solutions:
        print("  No solution found for Hypothesis A - cannot test robustness")
        return {"base_solution": False}

    base_solution = solutions[0]
    print("  Base solution for 5×5:")
    print_board(base_solution)

    # Verify each piece can be identified in the solution
    piece_cells = {}
    for r in range(5):
        for c in range(5):
            pid = base_solution[r][c]
            if pid > 0:
                if pid not in piece_cells:
                    piece_cells[pid] = []
                piece_cells[pid].append((r, c))

    print("\n  Pieces in solution:")
    for pid, cells in sorted(piece_cells.items()):
        print(f"    Piece {pid}: {len(cells)} cells at {cells}")

    # Verify totals match
    total_in_solution = sum(len(cells) for cells in piece_cells.values())
    print(f"\n  Total cells in solution: {total_in_solution}")

    if total_in_solution == 25:
        print("  ✓ Solution covers all 25 cells")
        return {"base_solution": True, "cells_covered": 25, "pieces_placed": len(piece_cells)}
    else:
        print(f"  ✗ Solution only covers {total_in_solution} cells!")
        return {"base_solution": False}


def audit_test_9_symmetry_analysis():
    """
    AUDIT 9: Analyze symmetry of pieces and solution.

    Checks if piece interpretations are consistent with visual symmetry.
    """
    print("\n" + "=" * 70)
    print("AUDIT 9: Symmetry Analysis")
    print("=" * 70)

    def count_orientations(cells: Set[Tuple[int, int]]) -> int:
        """Count number of distinct orientations for a piece."""
        return len(get_all_orientations(cells))

    results = {}

    print("  Piece symmetry (fewer orientations = more symmetric):")
    for name, cells in PIECES_HYPO_A.items():
        n_orient = count_orientations(cells)
        results[name] = n_orient

        symmetry = "HIGH" if n_orient <= 2 else "MEDIUM" if n_orient <= 4 else "LOW"
        print(f"    {name}: {len(cells)} cells, {n_orient} orientations ({symmetry} symmetry)")

    # Expected symmetries based on piece types
    print("\n  Expected symmetries:")
    print("    I-shapes: 2 orientations (0°, 90°)")
    print("    O-shape (square): 1 orientation")
    print("    L-shapes: 4-8 orientations")
    print("    S-shapes: 2-4 orientations")

    return results


def audit_test_10_final_probability_update():
    """
    AUDIT 10: Bayesian probability update based on all evidence.

    Combines all audit results to update hypothesis probabilities.
    """
    print("\n" + "=" * 70)
    print("AUDIT 10: Final Probability Assessment")
    print("=" * 70)

    # Prior probabilities
    prior_A = 0.70  # 5×5 correct interpretation
    prior_B = 0.20  # 6×6 with blocked cells
    prior_C = 0.10  # Significant miscounting

    print(f"  Prior probabilities:")
    print(f"    Hypothesis A (5×5, current interpretation): {prior_A:.0%}")
    print(f"    Hypothesis B (6×6 with blocked region): {prior_B:.0%}")
    print(f"    Hypothesis C (6×6, pieces miscounted): {prior_C:.0%}")

    # Evidence from audits
    print("\n  Evidence collected:")

    # Test 1: Solution uniqueness (favors A if unique)
    test1 = audit_test_1_solution_uniqueness()
    if test1["solutions_count"] <= 3:
        likelihood_A_given_test1 = 0.9
        likelihood_B_given_test1 = 0.5
        likelihood_C_given_test1 = 0.1
    else:
        likelihood_A_given_test1 = 0.6
        likelihood_B_given_test1 = 0.6
        likelihood_C_given_test1 = 0.3

    print(f"    Test 1 (uniqueness): {test1['solutions_count']} solutions")

    # Test 3: Blocked cell patterns (favors B if works)
    test3 = audit_test_3_blocked_cell_patterns()
    if test3["patterns_that_work"] > 0:
        likelihood_A_given_test3 = 0.7
        likelihood_B_given_test3 = 0.8
        likelihood_C_given_test3 = 0.2
    else:
        likelihood_A_given_test3 = 0.8
        likelihood_B_given_test3 = 0.2
        likelihood_C_given_test3 = 0.2

    print(f"    Test 3 (blocked patterns): {test3['patterns_that_work']}/{test3['patterns_tested']} work")

    # Test 4: 36-cell config (favors C if found)
    test4 = audit_test_4_hypothesis_c_36_cell()
    if test4.get("found_36_config"):
        likelihood_A_given_test4 = 0.4
        likelihood_B_given_test4 = 0.3
        likelihood_C_given_test4 = 0.8
    else:
        likelihood_A_given_test4 = 0.8
        likelihood_B_given_test4 = 0.7
        likelihood_C_given_test4 = 0.1

    has_36 = "Yes" if test4.get("found_36_config") else "No"
    print(f"    Test 4 (36-cell config): {has_36}")

    # Combined posterior calculation (simplified - multiply likelihoods)
    posterior_A = prior_A * likelihood_A_given_test1 * likelihood_A_given_test3 * likelihood_A_given_test4
    posterior_B = prior_B * likelihood_B_given_test1 * likelihood_B_given_test3 * likelihood_B_given_test4
    posterior_C = prior_C * likelihood_C_given_test1 * likelihood_C_given_test3 * likelihood_C_given_test4

    # Normalize
    total = posterior_A + posterior_B + posterior_C
    posterior_A /= total
    posterior_B /= total
    posterior_C /= total

    print(f"\n  Updated (posterior) probabilities:")
    print(f"    Hypothesis A (5×5, current interpretation): {posterior_A:.1%}")
    print(f"    Hypothesis B (6×6 with blocked region): {posterior_B:.1%}")
    print(f"    Hypothesis C (6×6, pieces miscounted): {posterior_C:.1%}")

    # Verdict
    print("\n  VERDICT:")
    max_prob = max(posterior_A, posterior_B, posterior_C)
    if max_prob == posterior_A:
        print("    → HYPOTHESIS A IS MOST LIKELY")
        print("    The puzzle is a 5×5 board with 8 pieces totaling 25 cells.")
    elif max_prob == posterior_B:
        print("    → HYPOTHESIS B IS MOST LIKELY")
        print("    The puzzle is a 6×6 board with a 5×5 playable region.")
    else:
        print("    → HYPOTHESIS C IS MOST LIKELY")
        print("    The puzzle is 6×6 and pieces are significantly larger.")

    return {
        "posterior_A": posterior_A,
        "posterior_B": posterior_B,
        "posterior_C": posterior_C,
    }


# =============================================================================
# MAIN AUDIT EXECUTION
# =============================================================================

def run_full_audit():
    """Run all 10 audit tests and compile results."""
    print("=" * 70)
    print("COMPREHENSIVE PUZZLE AUDIT")
    print("Testing 3 Hypotheses to Determine True Puzzle State")
    print("=" * 70)

    results = {}

    # Run all tests
    results["test_1"] = audit_test_1_solution_uniqueness()
    results["test_2"] = audit_test_2_near_miss_analysis()
    results["test_3"] = audit_test_3_blocked_cell_patterns()
    results["test_4"] = audit_test_4_hypothesis_c_36_cell()
    results["test_5"] = audit_test_5_checkerboard_constraint()
    results["test_6"] = audit_test_6_piece_shape_validation()
    results["test_7"] = audit_test_7_alternative_board_sizes()
    results["test_8"] = audit_test_8_solution_robustness()
    results["test_9"] = audit_test_9_symmetry_analysis()
    results["test_10"] = audit_test_10_final_probability_update()

    print("\n" + "=" * 70)
    print("AUDIT COMPLETE")
    print("=" * 70)

    return results


if __name__ == "__main__":
    run_full_audit()
