#!/usr/bin/env python3
"""
RIGOROUS AUDIT PART 2: Other types of errors
"""

import copy
from typing import List, Set, Tuple, Optional

print("=" * 70)
print("RIGOROUS AUDIT PART 2: EXECUTION & PERCEPTION ERRORS")
print("=" * 70)

# =============================================================================
# AUDIT 6: Visual miscounting of board dimensions
# =============================================================================

print("\n" + "=" * 70)
print("AUDIT 6: BOARD DIMENSION VERIFICATION")
print("Re-examining whether board is 5x5, 6x6, or other")
print("=" * 70)

print("""
MULTIPLE VERIFICATION METHODS:

Method 1: Count squares in top row
- I see alternating BLACK-GRAY-BLACK-GRAY-BLACK-GRAY pattern
- That's 6 squares if counting each color: 3 black + 3 gray = 6
- For 5x5: would see BLACK-GRAY-BLACK-GRAY-BLACK (3 black + 2 gray = 5)
- VERDICT: Suggests 6 columns

Method 2: Count squares in left column
- I see alternating BLACK-GRAY-BLACK-GRAY-BLACK-GRAY pattern
- That's 6 squares
- VERDICT: Suggests 6 rows

Method 3: Count total black squares visible
- 6x6 board: 18 black squares
- 5x5 board: 13 black squares
- Looking at the image... I need to count carefully
- This is difficult to do precisely from visual inspection

Method 4: Aspect ratio check
- The board appears SQUARE (equal height and width)
- This is consistent with both 5x5 and 6x6

Method 5: Compare board size to piece sizes
- The 2x2 square piece should fit 3x3 times in a 6x6 board
- The 2x2 square piece should fit 2.5x2.5 times in a 5x5 board
- Looking at relative sizes... the board looks like it could fit about 3x3 squares
- VERDICT: Suggests 6x6

CRITICAL INSIGHT:
All my visual methods suggest 6x6, but my piece count (25) only works for 5x5.
This is a FUNDAMENTAL CONTRADICTION that I haven't resolved!

POSSIBLE RESOLUTIONS:
1. Board looks 6x6 but IS 5x5 (optical illusion or my counting is wrong)
2. Board IS 6x6 and my piece count is significantly wrong
3. Board IS 6x6 but only a 5x5 region is playable
4. The puzzle has non-standard rules I'm not aware of
""")

# =============================================================================
# AUDIT 7: Piece 4 cell count verification
# =============================================================================

print("\n" + "=" * 70)
print("AUDIT 7: PIECE 4 (L-SHAPE) CELL COUNT VERIFICATION")
print("=" * 70)

print("""
Piece 4 is in the middle-left of the piece palette.
It's clearly an L-shaped piece.

L-SHAPED POLYOMINOES:
- L-tromino: 3 cells (one corner + two extensions)
  Shape: █      or rotations/reflections
         ██

- L-tetromino: 4 cells (longer stem)
  Shape: █      or rotations/reflections
         █
         ██

- L-pentomino: 5 cells (even longer)
  Shape: █      or rotations/reflections
         █
         █
         ██

VISUAL ANALYSIS OF PIECE 4:
- Looking at the image, piece 4 has a vertical stem and horizontal extension
- Comparing to piece 2 (2x2 square = 4 cells):
  * Piece 4 appears to have SIMILAR total area to piece 2
  * This suggests piece 4 is ~4 cells

- Comparing to pieces 7 and 8 (which I identified as L-trominoes):
  * Piece 4 appears LARGER than pieces 7 and 8
  * This is consistent with piece 4 being 4 cells and pieces 7/8 being 3 cells

CONCLUSION: Piece 4 is most likely 4 cells (L-tetromino)
CONFIDENCE: Medium-High (visual comparison supports this)
UNCERTAINTY: Could be 3 or 5 cells, but 4 is most consistent with visual evidence
""")

# =============================================================================
# AUDIT 8: Piece 5 cell count verification
# =============================================================================

print("\n" + "=" * 70)
print("AUDIT 8: PIECE 5 (S/Z-SHAPE) CELL COUNT VERIFICATION")
print("=" * 70)

print("""
Piece 5 is in the middle-center of the piece palette.
It has an S or Z shaped pattern.

S/Z SHAPED POLYOMINOES:
- "Bent" tromino: 3 cells (like a staircase with 3 steps)
  Shape:  █     This is actually the same as L-tromino
         ██     just viewed differently

- S-tetromino: 4 cells (classic Tetris S-piece)
  Shape:  ██
         ██

- Z-tetromino: 4 cells (classic Tetris Z-piece)
  Shape: ██
          ██

- S/Z pentomino: 5 cells (extended S or Z)
  Shape:   ██
          ██
         █

VISUAL ANALYSIS OF PIECE 5:
- Looking at the image, piece 5 has TWO horizontal segments OFFSET from each other
- This is the classic S or Z tetromino pattern
- A 3-cell "bent" tromino would look more like an angle, not an offset pattern

- Comparing to piece 2 (2x2 square = 4 cells):
  * Piece 5 appears to have SIMILAR total area to piece 2
  * This supports 4 cells

CONCLUSION: Piece 5 is most likely 4 cells (S-tetromino or Z-tetromino)
CONFIDENCE: High (the offset pattern is characteristic of 4-cell S/Z)
UNCERTAINTY: Very unlikely to be 3 cells; could possibly be 5
""")

# =============================================================================
# AUDIT 9: Code bug check in solver
# =============================================================================

print("\n" + "=" * 70)
print("AUDIT 9: SOLVER CODE VERIFICATION")
print("Testing solver correctness with known cases")
print("=" * 70)

def get_all_orientations(piece: Set[Tuple[int, int]]) -> List[Set[Tuple[int, int]]]:
    """Generate all unique rotations and reflections of a piece."""
    orientations = set()

    def normalize(p: Set[Tuple[int, int]]) -> Tuple[Tuple[int, int], ...]:
        min_r = min(r for r, c in p)
        min_c = min(c for r, c in p)
        return tuple(sorted((r - min_r, c - min_c) for r, c in p))

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

# Test 1: Domino orientations
domino = {(0, 0), (0, 1)}
domino_orientations = get_all_orientations(domino)
print(f"Test 1 - Domino orientations: {len(domino_orientations)}")
print(f"  Expected: 2 (horizontal and vertical)")
print(f"  Got: {len(domino_orientations)}")
print(f"  Orientations: {[sorted(o) for o in domino_orientations]}")
assert len(domino_orientations) == 2, "FAIL: Domino should have 2 orientations"
print("  ✓ PASS")

# Test 2: Square orientations
square = {(0, 0), (0, 1), (1, 0), (1, 1)}
square_orientations = get_all_orientations(square)
print(f"\nTest 2 - Square orientations: {len(square_orientations)}")
print(f"  Expected: 1 (square is symmetric)")
print(f"  Got: {len(square_orientations)}")
assert len(square_orientations) == 1, "FAIL: Square should have 1 orientation"
print("  ✓ PASS")

# Test 3: L-tromino orientations
l_tromino = {(0, 0), (1, 0), (1, 1)}
l_orientations = get_all_orientations(l_tromino)
print(f"\nTest 3 - L-tromino orientations: {len(l_orientations)}")
print(f"  Expected: 4 (4 rotations, reflections are same)")
print(f"  Got: {len(l_orientations)}")
assert len(l_orientations) == 4, "FAIL: L-tromino should have 4 orientations"
print("  ✓ PASS")

# Test 4: Simple tiling test - fill 2x2 with dominos
print(f"\nTest 4 - Can 2 dominoes fill a 2x2 board?")

def can_place(board, piece, start_r, start_c):
    rows, cols = len(board), len(board[0])
    for dr, dc in piece:
        r, c = start_r + dr, start_c + dc
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != 0:
            return False
    return True

def place_piece(board, piece, start_r, start_c, piece_id):
    new_board = copy.deepcopy(board)
    for dr, dc in piece:
        new_board[start_r + dr][start_c + dc] = piece_id
    return new_board

def find_first_empty(board):
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == 0:
                return (r, c)
    return None

def solve(board, pieces, piece_idx=0, solutions=None, max_solutions=1):
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

board_2x2 = [[0, 0], [0, 0]]
pieces_2dom = [
    ('dom1', get_all_orientations({(0, 0), (0, 1)})),
    ('dom2', get_all_orientations({(0, 0), (0, 1)}))
]
solutions = solve(board_2x2, pieces_2dom, max_solutions=10)
print(f"  Expected: 2 solutions (both horizontal, both vertical)")
print(f"  Got: {len(solutions)} solutions")
for i, sol in enumerate(solutions):
    print(f"    Solution {i+1}: {sol}")
assert len(solutions) == 2, "FAIL: Should find 2 ways to tile 2x2 with 2 dominoes"
print("  ✓ PASS")

# Test 5: Impossible tiling
print(f"\nTest 5 - Can 3 dominoes fill a 2x2 board? (Should fail - 6 cells > 4)")
pieces_3dom = [
    ('dom1', get_all_orientations({(0, 0), (0, 1)})),
    ('dom2', get_all_orientations({(0, 0), (0, 1)})),
    ('dom3', get_all_orientations({(0, 0), (0, 1)}))
]
solutions = solve(board_2x2, pieces_3dom, max_solutions=10)
print(f"  Expected: 0 solutions")
print(f"  Got: {len(solutions)} solutions")
assert len(solutions) == 0, "FAIL: Should not be able to fit 3 dominoes in 2x2"
print("  ✓ PASS")

print("\n✓ All solver tests passed! Solver code appears correct.")

# =============================================================================
# AUDIT 10: Check if I missed any pieces
# =============================================================================

print("\n" + "=" * 70)
print("AUDIT 10: PIECE COUNT VERIFICATION")
print("Did I miss any pieces or double-count?")
print("=" * 70)

print("""
PIECE INVENTORY FROM IMAGE:

RIGHT PANEL - Piece Palette:
┌─────────────────────────────────────────┐
│  TOP ROW:                               │
│    Position 1: Horizontal bar           │
│    Position 2: Square                   │
│    Position 3: Short horizontal bar     │
├─────────────────────────────────────────┤
│  MIDDLE ROW:                            │
│    Position 4: L-shaped piece           │
│    Position 5: S/Z-shaped piece         │
│    Position 6: Short horizontal bar     │
├─────────────────────────────────────────┤
│  BOTTOM ROW:                            │
│    Position 7: L-shaped piece           │
│    Position 8: L-shaped piece           │
└─────────────────────────────────────────┘

COUNT: 3 + 3 + 2 = 8 pieces

VERIFICATION:
- Are there any pieces partially hidden?
  Looking at image: No, all pieces appear fully visible

- Could any pieces be overlapping?
  Looking at image: No, pieces are clearly separated

- Could pieces 7 and 8 be the SAME piece shown twice (UI artifact)?
  Looking at image: They appear to be two distinct pieces

- Could there be pieces outside the visible palette area?
  Looking at image: The palette appears complete

CONCLUSION: 8 pieces is most likely correct.
CONFIDENCE: High
UNCERTAINTY: Could be 7 if pieces 7 and 8 are one piece, or 9+ if I missed something
""")

print("\n" + "=" * 70)
print("AUDIT SUMMARY")
print("=" * 70)

print("""
FINDINGS FROM RIGOROUS AUDIT:

METHODOLOGICAL ERRORS:
1. CONFIRMATION BIAS: Possible - I found 25=5x5 and may have stopped looking
2. OVER-RELIANCE ON MATH: Yes - I dismissed visual 6x6 evidence due to math
3. REFERENCE PIECE: Verified - 2x2 square is reasonable
4. CIRCULAR REASONING: Possible - can't fully rule out
5. 6x6 TESTING: Verified impossible with my piece ranges

OTHER ERRORS:
6. BOARD COUNT: UNRESOLVED - Visual suggests 6x6, math suggests 5x5
7. PIECE 4 COUNT: Likely correct (4 cells) based on relative sizes
8. PIECE 5 COUNT: Likely correct (4 cells) based on shape
9. SOLVER CODE: Verified correct with test cases
10. PIECE COUNT: Likely correct (8 pieces)

CRITICAL UNRESOLVED ISSUE:
The fundamental contradiction between:
- Visual observation: Board appears to be 6x6
- Mathematical analysis: Pieces only work for 5x5

This suggests one of:
a) My visual board counting is wrong (it's actually 5x5)
b) My piece size estimates are significantly wrong
c) The puzzle has special rules (partial coverage, excluded pieces, etc.)
d) There's something about the puzzle I fundamentally misunderstand
""")
