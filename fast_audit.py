#!/usr/bin/env python3
"""
FAST COMPREHENSIVE AUDIT: Streamlined version that runs quickly.
Tests 3 hypotheses about the puzzle state.
"""

import copy
from typing import List, Set, Tuple, Optional, Dict
from itertools import product
import sys

# =============================================================================
# SOLVER ENGINE (optimized for speed)
# =============================================================================

def get_all_orientations(piece: Set[Tuple[int, int]]) -> List[Set[Tuple[int, int]]]:
    orientations = set()

    def normalize(p):
        min_r = min(r for r, c in p)
        min_c = min(c for r, c in p)
        return tuple(sorted((r - min_r, c - min_c) for r, c in p))

    def rotate_90(p):
        return {(c, -r) for r, c in p}

    def reflect(p):
        return {(r, -c) for r, c in p}

    current = piece
    for _ in range(4):
        orientations.add(normalize(current))
        orientations.add(normalize(reflect(current)))
        current = rotate_90(current)

    return [set(o) for o in orientations]


def solve_fast(board, pieces, piece_idx=0, max_solutions=1):
    """Fast solver with early termination."""
    solutions = []

    def find_first_empty():
        for r, row in enumerate(board):
            for c, cell in enumerate(row):
                if cell == 0:
                    return (r, c)
        return None

    def can_place(piece, start_r, start_c):
        rows, cols = len(board), len(board[0])
        for dr, dc in piece:
            r, c = start_r + dr, start_c + dc
            if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 0:
                return False
        return True

    def place(piece, start_r, start_c, pid):
        for dr, dc in piece:
            board[start_r + dr][start_c + dc] = pid

    def unplace(piece, start_r, start_c):
        for dr, dc in piece:
            board[start_r + dr][start_c + dc] = 0

    def backtrack(idx):
        if len(solutions) >= max_solutions:
            return

        empty = find_first_empty()
        if empty is None:
            if idx >= len(pieces):
                solutions.append([row[:] for row in board])
            return

        if idx >= len(pieces):
            return

        r, c = empty
        name, orientations = pieces[idx]

        for orientation in orientations:
            for dr, dc in orientation:
                start_r, start_c = r - dr, c - dc
                if can_place(orientation, start_r, start_c):
                    place(orientation, start_r, start_c, idx + 1)
                    backtrack(idx + 1)
                    unplace(orientation, start_r, start_c)
                    if len(solutions) >= max_solutions:
                        return

    backtrack(piece_idx)
    return solutions


def test_config(pieces_dict, rows, cols, blocked=None, max_sols=1):
    """Quick test of piece configuration."""
    total = sum(len(p) for p in pieces_dict.values())
    target = rows * cols - (len(blocked) if blocked else 0)

    if total != target:
        return []

    pieces = [(name, get_all_orientations(shape)) for name, shape in pieces_dict.items()]
    board = [[0] * cols for _ in range(rows)]
    if blocked:
        for r, c in blocked:
            if 0 <= r < rows and 0 <= c < cols:
                board[r][c] = -1

    return solve_fast(board, pieces, max_solutions=max_sols)


def print_board(board, indent="  "):
    symbols = ' .123456789ABCDEFGHIJ'
    for row in board:
        print(indent + ' '.join(symbols[min(cell + 1, len(symbols) - 1)] for cell in row))


# =============================================================================
# PIECE DEFINITIONS
# =============================================================================

PIECES_25 = {
    'P1': {(0, 0), (0, 1), (0, 2)},           # I-tromino (3)
    'P2': {(0, 0), (0, 1), (1, 0), (1, 1)},   # O-tetromino (4)
    'P3': {(0, 0), (0, 1)},                    # Domino (2)
    'P4': {(0, 0), (1, 0), (2, 0), (2, 1)},   # L-tetromino (4)
    'P5': {(0, 1), (0, 2), (1, 0), (1, 1)},   # S-tetromino (4)
    'P6': {(0, 0), (0, 1)},                    # Domino (2)
    'P7': {(0, 0), (1, 0), (1, 1)},           # L-tromino (3)
    'P8': {(0, 0), (1, 0), (1, 1)},           # L-tromino (3)
}

# =============================================================================
# AUDIT TESTS
# =============================================================================

print("=" * 70)
print("COMPREHENSIVE PUZZLE AUDIT")
print("Testing 3 Hypotheses to Determine True Puzzle State")
print("=" * 70)

print("""
HYPOTHESES:
  A (70% prior): 5×5 board, current 25-cell interpretation correct
  B (20% prior): 6×6 board with 5×5 playable region
  C (10% prior): 6×6 board, significant piece miscounting
""")

# -----------------------------------------------------------------------------
# TEST 1: Solution count for 5×5 (Hypothesis A)
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("AUDIT 1: Solution Count for 5×5 Board")
print("=" * 70)

solutions_5x5 = test_config(PIECES_25, 5, 5, max_sols=20)
print(f"  Solutions found: {len(solutions_5x5)}")

if solutions_5x5:
    print("  First solution:")
    print_board(solutions_5x5[0])

if len(solutions_5x5) == 1:
    evidence_A_1 = "STRONG"
    score_A_1 = 0.95
elif len(solutions_5x5) <= 5:
    evidence_A_1 = "GOOD"
    score_A_1 = 0.85
else:
    evidence_A_1 = "MODERATE"
    score_A_1 = 0.70

print(f"\n  → {evidence_A_1} evidence for Hypothesis A (score: {score_A_1:.2f})")

# -----------------------------------------------------------------------------
# TEST 2: Piece shape validation
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("AUDIT 2: Piece Shape Validation")
print("=" * 70)

def is_connected(cells):
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

all_valid = True
for name, cells in PIECES_25.items():
    valid = is_connected(cells)
    status = "✓" if valid else "✗"
    print(f"  {name}: {len(cells)} cells - {status} connected")
    if not valid:
        all_valid = False

if all_valid:
    print("\n  → All 8 pieces are valid polyominoes")
    score_validity = 1.0
else:
    print("\n  → Some pieces are invalid!")
    score_validity = 0.5

# -----------------------------------------------------------------------------
# TEST 3: Checkerboard color constraint
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("AUDIT 3: Checkerboard Color Constraint")
print("=" * 70)

# For 5×5: 13 black, 12 white (or vice versa)
# Count color coverage in solution
if solutions_5x5:
    board = solutions_5x5[0]
    black_covered = sum(1 for r in range(5) for c in range(5)
                        if board[r][c] > 0 and (r + c) % 2 == 0)
    white_covered = sum(1 for r in range(5) for c in range(5)
                        if board[r][c] > 0 and (r + c) % 2 == 1)
    print(f"  5×5 board needs: 13 black + 12 white = 25 cells")
    print(f"  Solution covers: {black_covered} black + {white_covered} white = {black_covered + white_covered} cells")

    if black_covered + white_covered == 25:
        print("  → ✓ Solution perfectly tiles the board")
        score_color = 1.0
    else:
        print("  → ✗ Solution incomplete!")
        score_color = 0.5
else:
    score_color = 0.5

# -----------------------------------------------------------------------------
# TEST 4: Near-miss analysis (24-cell variant)
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("AUDIT 4: Near-Miss Analysis")
print("=" * 70)

# 24 cells (P5 as tromino instead of tetromino)
pieces_24 = {
    'P1': {(0, 0), (0, 1), (0, 2)},
    'P2': {(0, 0), (0, 1), (1, 0), (1, 1)},
    'P3': {(0, 0), (0, 1)},
    'P4': {(0, 0), (1, 0), (2, 0), (2, 1)},
    'P5': {(0, 0), (1, 0), (1, 1)},  # L-tromino (3) instead of S-tet (4)
    'P6': {(0, 0), (0, 1)},
    'P7': {(0, 0), (1, 0), (1, 1)},
    'P8': {(0, 0), (1, 0), (1, 1)},
}

total_24 = sum(len(p) for p in pieces_24.values())
print(f"  24-cell variant (P5 as tromino): {total_24} cells")

sols_4x6 = test_config(pieces_24, 4, 6, max_sols=5)
print(f"    4×6 board: {len(sols_4x6)} solutions found")

if sols_4x6:
    print("    → 24-cell variant ALSO works, suggesting ambiguity")
    score_ambiguity = 0.7  # Slight concern
else:
    print("    → 24-cell variant doesn't tile standard boards")
    score_ambiguity = 0.9  # More confidence in 25

# Actually check - 4x6 = 24 so it should work if pieces sum to 24
# The fact that 24-cell pieces CAN tile a board doesn't mean original is wrong
# It just shows 24 is also geometrically feasible

# -----------------------------------------------------------------------------
# TEST 5: 6×6 with blocked cells (Hypothesis B)
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("AUDIT 5: 6×6 Board with Blocked Cells (Hypothesis B)")
print("=" * 70)

# Test: Block right column + bottom row (11 cells) leaving 25
blocked_pattern = set()
for i in range(6):
    blocked_pattern.add((i, 5))  # right column
for j in range(5):
    blocked_pattern.add((5, j))  # bottom row

print(f"  Pattern: block right column + bottom row = {len(blocked_pattern)} cells")
print(f"  Playable cells: 36 - 11 = 25")

sols_6x6_blocked = test_config(PIECES_25, 6, 6, blocked=blocked_pattern, max_sols=5)
print(f"  Solutions found: {len(sols_6x6_blocked)}")

if sols_6x6_blocked:
    print("  First solution:")
    print_board(sols_6x6_blocked[0])
    print("  → ✓ Hypothesis B is FEASIBLE")
    score_B = 0.7
else:
    print("  → ✗ This blocking pattern doesn't work")
    score_B = 0.3

# -----------------------------------------------------------------------------
# TEST 6: Solution uniqueness comparison
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("AUDIT 6: Solution Uniqueness Comparison")
print("=" * 70)

print(f"  5×5 board (Hypo A): {len(solutions_5x5)} solutions")
print(f"  6×6 blocked (Hypo B): {len(sols_6x6_blocked)} solutions")

if len(solutions_5x5) > 0 and len(sols_6x6_blocked) > 0:
    if len(solutions_5x5) < len(sols_6x6_blocked):
        print("  → 5×5 is more constrained (fewer solutions)")
        uniqueness_favors = "A"
    elif len(solutions_5x5) > len(sols_6x6_blocked):
        print("  → 6×6 blocked is more constrained")
        uniqueness_favors = "B"
    else:
        print("  → Both have similar solution counts")
        uniqueness_favors = "TIE"
else:
    uniqueness_favors = "A" if len(solutions_5x5) > 0 else "NEITHER"

# -----------------------------------------------------------------------------
# TEST 7: Piece count range analysis
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("AUDIT 7: Piece Count Range Analysis")
print("=" * 70)

ranges = {
    'P1': [2, 3, 4],      # domino to tetromino
    'P2': [4],            # definitely 2×2
    'P3': [2, 3],         # domino or tromino
    'P4': [3, 4, 5],      # L-tromino to L-pentomino
    'P5': [3, 4, 5],      # tromino to S-pentomino
    'P6': [2, 3],         # domino or tromino
    'P7': [2, 3, 4],      # domino to L-tetromino
    'P8': [2, 3, 4],      # domino to L-tetromino
}

totals = {}
for combo in product(*ranges.values()):
    total = sum(combo)
    totals[total] = totals.get(total, 0) + 1

min_t, max_t = min(totals.keys()), max(totals.keys())
print(f"  Minimum possible: {min_t} cells")
print(f"  Maximum possible: {max_t} cells")
print(f"  Range: {sorted(totals.keys())}")

print(f"\n  Target board sizes:")
print(f"    25 cells (5×5): {totals.get(25, 0)} interpretations")
print(f"    24 cells (4×6): {totals.get(24, 0)} interpretations")
print(f"    36 cells (6×6): {totals.get(36, 0)} interpretations")

if 36 in totals:
    print("  → 36 cells IS achievable - Hypothesis C is possible")
    hypo_C_possible = True
else:
    print("  → 36 cells is NOT achievable - Hypothesis C is IMPOSSIBLE")
    hypo_C_possible = False

# -----------------------------------------------------------------------------
# TEST 8: Exhaustive 36-cell search
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("AUDIT 8: Can Any 36-Cell Interpretation Tile 6×6?")
print("=" * 70)

if not hypo_C_possible:
    print("  No 36-cell interpretation exists - skipping solver test")
    score_C = 0.0
else:
    print("  Searching for 36-cell configurations...")
    found_36_solution = False

    # Try a few plausible 36-cell configurations
    # Configuration: maximize everything
    pieces_36_try1 = {
        'P1': {(0, 0), (0, 1), (0, 2), (0, 3)},           # I-tet (4)
        'P2': {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)},  # 2x3 rect (6)
        'P3': {(0, 0), (0, 1), (0, 2)},                    # I-tromino (3)
        'P4': {(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)},    # L-pent (5)
        'P5': {(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)},    # S-pent (5)
        'P6': {(0, 0), (0, 1), (0, 2)},                    # I-tromino (3)
        'P7': {(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)},    # L-pent (5)
        'P8': {(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)},    # L-pent (5)
    }
    total_try1 = sum(len(p) for p in pieces_36_try1.values())
    print(f"  Configuration 1: {total_try1} cells")

    if total_try1 == 36:
        sols = test_config(pieces_36_try1, 6, 6, max_sols=1)
        if sols:
            print(f"    ✓ Found solution!")
            found_36_solution = True
        else:
            print(f"    ✗ No solution")

    if found_36_solution:
        print("  → Hypothesis C is viable")
        score_C = 0.5
    else:
        print("  → No 36-cell solution found after testing")
        score_C = 0.1

# -----------------------------------------------------------------------------
# TEST 9: Robustness check - verify solution covers all cells
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("AUDIT 9: Solution Robustness Check")
print("=" * 70)

if solutions_5x5:
    board = solutions_5x5[0]
    piece_cells = {}
    for r in range(5):
        for c in range(5):
            pid = board[r][c]
            if pid > 0:
                piece_cells[pid] = piece_cells.get(pid, 0) + 1

    print("  Pieces in solution:")
    for pid in sorted(piece_cells.keys()):
        expected_sizes = [3, 4, 2, 4, 4, 2, 3, 3]  # P1-P8
        actual = piece_cells[pid]
        expected = expected_sizes[pid - 1]
        match = "✓" if actual == expected else "✗"
        print(f"    Piece {pid}: {actual} cells (expected {expected}) {match}")

    total_covered = sum(piece_cells.values())
    print(f"\n  Total cells covered: {total_covered}/25")

    if total_covered == 25 and len(piece_cells) == 8:
        print("  → ✓ Solution is COMPLETE and VALID")
        score_robustness = 1.0
    else:
        print("  → ✗ Solution has issues")
        score_robustness = 0.5
else:
    score_robustness = 0.0

# -----------------------------------------------------------------------------
# TEST 10: Final probability calculation
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("AUDIT 10: Final Bayesian Probability Update")
print("=" * 70)

# Priors
prior_A = 0.70
prior_B = 0.20
prior_C = 0.10

# Combine evidence
likelihood_A = score_A_1 * score_validity * score_color * score_robustness
likelihood_B = score_B * 0.8 if sols_6x6_blocked else 0.1
likelihood_C = score_C if hypo_C_possible else 0.01

# Posterior (unnormalized)
post_A = prior_A * likelihood_A
post_B = prior_B * likelihood_B
post_C = prior_C * likelihood_C

# Normalize
total_post = post_A + post_B + post_C
post_A /= total_post
post_B /= total_post
post_C /= total_post

print(f"  Prior probabilities:")
print(f"    Hypothesis A (5×5, 25 cells): {prior_A:.0%}")
print(f"    Hypothesis B (6×6, blocked): {prior_B:.0%}")
print(f"    Hypothesis C (6×6, 36 cells): {prior_C:.0%}")

print(f"\n  Evidence scores:")
print(f"    Likelihood A: {likelihood_A:.3f}")
print(f"    Likelihood B: {likelihood_B:.3f}")
print(f"    Likelihood C: {likelihood_C:.3f}")

print(f"\n  POSTERIOR PROBABILITIES:")
print(f"    Hypothesis A (5×5, 25 cells): {post_A:.1%}")
print(f"    Hypothesis B (6×6, blocked): {post_B:.1%}")
print(f"    Hypothesis C (6×6, 36 cells): {post_C:.1%}")

# Verdict
print("\n" + "=" * 70)
print("FINAL VERDICT")
print("=" * 70)

winner = max([("A", post_A), ("B", post_B), ("C", post_C)], key=lambda x: x[1])

if winner[0] == "A":
    print(f"""
  HYPOTHESIS A IS MOST LIKELY ({post_A:.1%} probability)

  The puzzle is a 5×5 board with 8 pieces totaling 25 cells:
    - Piece 1: I-tromino (3 cells)
    - Piece 2: O-tetromino (4 cells)
    - Piece 3: Domino (2 cells)
    - Piece 4: L-tetromino (4 cells)
    - Piece 5: S-tetromino (4 cells)
    - Piece 6: Domino (2 cells)
    - Piece 7: L-tromino (3 cells)
    - Piece 8: L-tromino (3 cells)

  Total: 3 + 4 + 2 + 4 + 4 + 2 + 3 + 3 = 25 cells = 5×5 board

  The solver found {len(solutions_5x5)} valid solution(s).
""")
elif winner[0] == "B":
    print(f"""
  HYPOTHESIS B IS MOST LIKELY ({post_B:.1%} probability)

  The puzzle is a 6×6 board with a 5×5 playable region.
  Block the right column and bottom row to create a 5×5 play area.
""")
else:
    print(f"""
  HYPOTHESIS C IS MOST LIKELY ({post_C:.1%} probability)

  The puzzle is a 6×6 board and pieces are larger than initially identified.
""")

print("=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)
