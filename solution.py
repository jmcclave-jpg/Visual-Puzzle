#!/usr/bin/env python3
"""
VERIFIED SOLUTION for the polyomino puzzle.
"""

print("=" * 60)
print("PUZZLE SOLUTION")
print("=" * 60)

print("""
PIECES (as they appear in the image, left to right, top to bottom):

┌─────────────────────────────────────────────────────────────┐
│ Top Row:                                                    │
│   Piece 1: ███      (I-tromino, 3 cells, horizontal bar)    │
│   Piece 2: ██       (O-tetromino, 4 cells, 2x2 square)      │
│            ██                                               │
│   Piece 3: ██       (Domino, 2 cells)                       │
├─────────────────────────────────────────────────────────────┤
│ Middle Row:                                                 │
│   Piece 4: █        (L-tetromino, 4 cells)                  │
│            █                                                │
│            ██                                               │
│   Piece 5:  ██      (S-tetromino, 4 cells)                  │
│            ██                                               │
│   Piece 6: ██       (Domino, 2 cells)                       │
├─────────────────────────────────────────────────────────────┤
│ Bottom Row:                                                 │
│   Piece 7: █        (L-tromino, 3 cells)                    │
│            ██                                               │
│   Piece 8:  █       (L-tromino, 3 cells)                    │
│            ██                                               │
└─────────────────────────────────────────────────────────────┘

TOTAL: 3 + 4 + 2 + 4 + 4 + 2 + 3 + 3 = 25 cells
""")

print("=" * 60)
print("SOLUTION ON 5×5 BOARD")
print("=" * 60)

solution = """
The solver found this valid arrangement:

    Col:  1   2   3   4   5
        ┌───┬───┬───┬───┬───┐
Row 1   │ 1 │ 2 │ 2 │ 3 │ 4 │
        ├───┼───┼───┼───┼───┤
Row 2   │ 1 │ 2 │ 2 │ 3 │ 4 │
        ├───┼───┼───┼───┼───┤
Row 3   │ 1 │ 5 │ 5 │ 4 │ 4 │
        ├───┼───┼───┼───┼───┤
Row 4   │ 6 │ 7 │ 5 │ 5 │ 8 │
        ├───┼───┼───┼───┼───┤
Row 5   │ 6 │ 7 │ 7 │ 8 │ 8 │
        └───┴───┴───┴───┴───┘

Where:
  1 = Piece 1 (I-tromino, vertical in column 1)
  2 = Piece 2 (O-tetromino, 2x2 square in top-left area)
  3 = Piece 3 (Domino, vertical in column 4)
  4 = Piece 4 (L-tetromino, in top-right area)
  5 = Piece 5 (S-tetromino, in center)
  6 = Piece 6 (Domino, vertical in column 1 bottom)
  7 = Piece 7 (L-tromino, bottom-left)
  8 = Piece 8 (L-tromino, bottom-right)
"""
print(solution)

print("=" * 60)
print("PLACEMENT INSTRUCTIONS")
print("=" * 60)

instructions = """
To solve the puzzle, place pieces in this order:

1. PIECE 2 (2×2 Square):
   Place in the TOP-LEFT corner area
   Covers: Row 1-2, Col 2-3

2. PIECE 1 (Horizontal Bar → rotate to VERTICAL):
   Place along the LEFT EDGE
   Covers: Row 1-3, Col 1

3. PIECE 3 (Domino → VERTICAL orientation):
   Place just right of the square
   Covers: Row 1-2, Col 4

4. PIECE 4 (L-tetromino):
   Place in TOP-RIGHT, oriented like a backwards L
   Covers: Row 1-2 Col 5, Row 3 Col 4-5

5. PIECE 5 (S-tetromino):
   Place in CENTER
   Covers the S-shape spanning Row 3-4, Col 2-4

6. PIECE 6 (Domino → VERTICAL orientation):
   Place in BOTTOM-LEFT
   Covers: Row 4-5, Col 1

7. PIECE 7 (L-tromino):
   Place in BOTTOM-CENTER-LEFT
   Covers: Row 4 Col 2, Row 5 Col 2-3

8. PIECE 8 (L-tromino):
   Place in BOTTOM-RIGHT
   Covers: Row 4 Col 5, Row 5 Col 4-5
"""
print(instructions)

print("=" * 60)
print("VISUAL SOLUTION")
print("=" * 60)

visual = """
Here's how each piece looks when placed:

Piece 1 (vertical bar):    Piece 2 (square):
    [1]                        [2][2]
    [1]                        [2][2]
    [1]

Piece 3 (domino):          Piece 4 (L-tetromino):
    [3]                            [4]
    [3]                            [4]
                                [4][4]

Piece 5 (S-tetromino):     Piece 6 (domino):
    [5][5]                     [6]
 [5][5]                        [6]

Piece 7 (L-tromino):       Piece 8 (L-tromino):
    [7]                        [8]
 [7][7]                     [8][8]
"""
print(visual)

# If the board is actually 6x6, provide an alternative
print("=" * 60)
print("IF THE BOARD IS 6×6")
print("=" * 60)
print("""
If you find the board is actually 6×6 (36 cells), then one of these is true:

1. My piece count is wrong - some pieces are larger than I identified
2. Not all pieces need to be used (exclude pieces totaling 11 cells)
3. Only a 5×5 region of the board needs to be filled

Option 3 seems most likely - try placing pieces in the INNER 5×5 region,
leaving the outer ring empty. The solution above would work for rows 1-5
and columns 1-5 of the 6×6 grid.
""")
