#!/usr/bin/env python3
"""
Rigorous analysis of the polyomino puzzle from the image.
This script helps verify interpretations and find valid configurations.
"""

from itertools import combinations, product
from typing import List, Tuple, Set
import copy

# =============================================================================
# BOARD ANALYSIS
# =============================================================================

def analyze_checkerboard(rows: int, cols: int) -> dict:
    """Analyze a checkerboard of given dimensions."""
    total = rows * cols
    # Standard checkerboard: top-left is one color
    # For even dimensions: equal split
    # For odd dimensions: one color has one more
    if (rows * cols) % 2 == 0:
        color1 = total // 2
        color2 = total // 2
    else:
        color1 = (total + 1) // 2
        color2 = total // 2

    return {
        'dimensions': f'{rows}x{cols}',
        'total_cells': total,
        'color1_cells': color1,  # e.g., black
        'color2_cells': color2,  # e.g., gray/white
    }

# Test different board sizes
print("=" * 60)
print("BOARD SIZE ANALYSIS")
print("=" * 60)
for size in [5, 6, 7]:
    info = analyze_checkerboard(size, size)
    print(f"{info['dimensions']}: total={info['total_cells']}, "
          f"per_color={info['color1_cells']}/{info['color2_cells']}")

# =============================================================================
# PIECE ANALYSIS - Multiple interpretations
# =============================================================================

print("\n" + "=" * 60)
print("PIECE INTERPRETATION ANALYSIS")
print("=" * 60)

# My original interpretation
original_interpretation = {
    'piece1_horizontal_bar': 3,
    'piece2_square': 4,
    'piece3_short_bar': 2,
    'piece4_L_shape': 4,
    'piece5_SZ_shape': 4,
    'piece6_short_bar': 2,
    'piece7_L_shape': 3,
    'piece8_L_shape': 3,
}

# Alternative interpretations with uncertainty ranges
piece_ranges = {
    'piece1_horizontal_bar': [2, 3, 4],      # domino, tromino, or tetromino?
    'piece2_square': [4],                      # definitely 2x2
    'piece3_short_bar': [2, 3],               # domino or tromino?
    'piece4_L_shape': [3, 4, 5],              # L-tromino, L-tetromino, or L-pentomino?
    'piece5_SZ_shape': [3, 4, 5],             # bent tromino, S-tetromino, or S-pentomino?
    'piece6_short_bar': [2, 3],               # domino or tromino?
    'piece7_L_shape': [2, 3, 4],              # domino, L-tromino, or L-tetromino?
    'piece8_L_shape': [2, 3, 4],              # domino, L-tromino, or L-tetromino?
}

print("\nOriginal interpretation:")
total_orig = sum(original_interpretation.values())
print(f"  Pieces: {list(original_interpretation.values())}")
print(f"  Total cells: {total_orig}")

# Find all possible totals
print("\nPossible cell totals across all interpretations:")
min_total = sum(min(v) for v in piece_ranges.values())
max_total = sum(max(v) for v in piece_ranges.values())
print(f"  Minimum possible: {min_total}")
print(f"  Maximum possible: {max_total}")

# =============================================================================
# TARGET ANALYSIS - What totals make sense?
# =============================================================================

print("\n" + "=" * 60)
print("TARGET ANALYSIS - Which totals make puzzle sense?")
print("=" * 60)

targets = {
    18: "Cover all gray squares on 6x6 board",
    36: "Cover entire 6x6 board",
    25: "Cover entire 5x5 board",
    13: "Cover one color on 5x5 board",
    12: "Cover one color on 5x5 board (other color)",
}

for target, description in targets.items():
    if min_total <= target <= max_total:
        status = "✓ ACHIEVABLE"
    else:
        status = "✗ NOT ACHIEVABLE"
    print(f"  {target} cells: {status} - {description}")

# =============================================================================
# FIND CONFIGURATIONS THAT MATCH SENSIBLE TARGETS
# =============================================================================

print("\n" + "=" * 60)
print("CONFIGURATIONS MATCHING KEY TARGETS")
print("=" * 60)

def find_configurations_for_target(target: int, piece_ranges: dict) -> List[dict]:
    """Find all piece configurations that sum to the target."""
    pieces = list(piece_ranges.keys())
    ranges = [piece_ranges[p] for p in pieces]

    valid_configs = []
    for combo in product(*ranges):
        if sum(combo) == target:
            config = dict(zip(pieces, combo))
            valid_configs.append(config)

    return valid_configs

# Check for 18 (cover one color on 6x6)
configs_18 = find_configurations_for_target(18, piece_ranges)
print(f"\nConfigurations totaling 18 (one color on 6x6): {len(configs_18)} found")
if configs_18:
    for i, cfg in enumerate(configs_18[:5]):  # Show first 5
        print(f"  Config {i+1}: {list(cfg.values())}")

# Check for 36 (entire 6x6 board)
configs_36 = find_configurations_for_target(36, piece_ranges)
print(f"\nConfigurations totaling 36 (entire 6x6): {len(configs_36)} found")
if configs_36:
    for i, cfg in enumerate(configs_36[:5]):
        print(f"  Config {i+1}: {list(cfg.values())}")

# Check for 25 (entire 5x5 board)
configs_25 = find_configurations_for_target(25, piece_ranges)
print(f"\nConfigurations totaling 25 (entire 5x5): {len(configs_25)} found")
if configs_25:
    for i, cfg in enumerate(configs_25[:5]):
        print(f"  Config {i+1}: {list(cfg.values())}")

# =============================================================================
# PUZZLE SENSE CHECK
# =============================================================================

print("\n" + "=" * 60)
print("PUZZLE SENSE CHECK")
print("=" * 60)

print("""
Common polyomino puzzle types:
1. Cover one color of checkerboard (requires cells = board_size/2)
2. Cover entire board (requires cells = board_size)
3. Form a specific shape (variable)

For a 6x6 checkerboard:
- One color = 18 cells
- Entire board = 36 cells

For my original count of 25 cells:
- Doesn't match 18 (off by 7)
- Doesn't match 36 (off by 11)
- DOES match 5x5 board (25 cells exactly)

Key question: Is the board 6x6 or 5x5?
Or is my piece count wrong?
""")

# =============================================================================
# RELATIVE SIZE ANALYSIS
# =============================================================================

print("=" * 60)
print("RELATIVE SIZE ANALYSIS")
print("=" * 60)

print("""
Using the 2x2 square (piece 2) as reference (definitely 4 cells):

Visual observations from image:
- Piece 1 (horizontal bar): ~1.5x width of square → likely 3 cells (1x3)
- Piece 3 (short bar): ~same width as square → likely 2 cells (1x2)
- Piece 4 (L-shape): ~same total area as square → likely 4 cells
- Piece 5 (S/Z shape): ~same total area as square → likely 4 cells
- Piece 6 (short bar): ~same as piece 3 → likely 2 cells
- Piece 7 (L-shape): smaller than piece 4 → likely 3 cells
- Piece 8 (L-shape): same as piece 7 → likely 3 cells

This gives: 3 + 4 + 2 + 4 + 4 + 2 + 3 + 3 = 25

But 25 doesn't match any standard 6x6 target!
""")

# =============================================================================
# CHECKERBOARD CONSTRAINT ANALYSIS
# =============================================================================

print("=" * 60)
print("CHECKERBOARD TILING CONSTRAINT")
print("=" * 60)

print("""
CRITICAL INSIGHT: Checkerboard coloring constraint!

On a checkerboard, each cell is either black or white.
Any polyomino piece, when placed, covers some black and some white cells.

For dominoes (2 cells): always covers 1 black + 1 white
For L-trominoes (3 cells): covers either 2 black + 1 white OR 1 black + 2 white
For tetrominoes (4 cells):
  - O (square): 2 black + 2 white
  - I (line): 2 black + 2 white
  - L, J, T: 2 black + 2 white
  - S, Z: 2 black + 2 white

For a puzzle to be solvable, the pieces must be able to cover exactly
the right number of each color!

If covering only GRAY squares (18 cells), we need pieces that together
can be placed to hit only gray squares. This is ONLY possible if all
pieces are dominoes (covering 1 of each color each) - which they're not!

This suggests: The puzzle likely covers the ENTIRE board, not just one color!
""")

# Let's verify the coloring constraint
print("\n" + "=" * 60)
print("COLOR BALANCE ANALYSIS")
print("=" * 60)

def analyze_color_balance(piece_sizes: list) -> dict:
    """
    Analyze potential color balance for a set of pieces.
    Returns min/max possible coverage of each color.
    """
    min_color1 = 0
    max_color1 = 0

    for size in piece_sizes:
        if size == 2:  # domino: exactly 1 of each
            min_color1 += 1
            max_color1 += 1
        elif size == 3:  # tromino: 1 or 2 of color1
            min_color1 += 1
            max_color1 += 2
        elif size == 4:  # tetromino: exactly 2 of each
            min_color1 += 2
            max_color1 += 2
        elif size == 5:  # pentomino: 2 or 3 of color1
            min_color1 += 2
            max_color1 += 3

    total = sum(piece_sizes)
    return {
        'total_cells': total,
        'min_color1': min_color1,
        'max_color1': max_color1,
        'min_color2': total - max_color1,
        'max_color2': total - min_color1,
    }

# Analyze my original interpretation
orig_sizes = list(original_interpretation.values())
balance = analyze_color_balance(orig_sizes)
print(f"\nOriginal interpretation {orig_sizes}:")
print(f"  Total: {balance['total_cells']} cells")
print(f"  Color 1 (black): {balance['min_color1']} to {balance['max_color1']} cells")
print(f"  Color 2 (gray): {balance['min_color2']} to {balance['max_color2']} cells")

print(f"\nFor 6x6 board (18 black, 18 gray):")
if balance['min_color1'] <= 18 <= balance['max_color1'] and balance['min_color2'] <= 18 <= balance['max_color2']:
    if balance['total_cells'] == 36:
        print("  ✓ Color balance POSSIBLE for full board coverage")
    else:
        print(f"  ✗ Total cells ({balance['total_cells']}) doesn't match board (36)")
else:
    print("  ✗ Color balance IMPOSSIBLE")

print("\n" + "=" * 60)
print("CONCLUSION")
print("=" * 60)
print("""
Based on mathematical analysis:
1. My piece count of 25 doesn't match 6x6 board targets (18 or 36)
2. 25 exactly matches a 5x5 board
3. Either the board is 5x5, or my piece count is wrong

Most likely issues to audit:
1. Board size might be 5x5, not 6x6
2. I may be overcounting cells in the L-shaped pieces
3. I may be overcounting cells in the S/Z piece
4. The horizontal bar (piece 1) might be 2 cells, not 3
5. Some pieces might overlap or have special rules
""")
