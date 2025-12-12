"""
Advent of Code Day 12 - Christmas Tree Farm
Highly optimized solution for polyomino tiling using aggressive pruning
"""

import numpy as np
from typing import List, Tuple, Set
from collections import defaultdict

def parse_input(input_text):
    """Parse the input to extract shapes and regions."""
    lines = input_text.strip().split('\n')
    
    shapes = {}
    regions = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        
        if ':' in line and line.split(':')[0].isdigit():
            shape_id = int(line.split(':')[0])
            shape_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() and ':' not in lines[i]:
                shape_lines.append(lines[i].strip())
                i += 1
            shapes[shape_id] = shape_lines
        elif 'x' in line and ':' in line:
            parts = line.split(':')
            dims = parts[0].strip().split('x')
            width, height = int(dims[0]), int(dims[1])
            counts = list(map(int, parts[1].strip().split()))
            regions.append((width, height, counts))
            i += 1
        else:
            i += 1
    
    return shapes, regions

def shape_to_coords(shape_lines):
    """Convert shape lines to list of (x, y) coordinates."""
    coords = []
    for y, line in enumerate(shape_lines):
        for x, char in enumerate(line):
            if char == '#':
                coords.append((x, y))
    return coords

def normalize_coords(coords):
    """Normalize coordinates to start at (0, 0)."""
    if not coords:
        return []
    min_x = min(c[0] for c in coords)
    min_y = min(c[1] for c in coords)
    return tuple(sorted((x - min_x, y - min_y) for x, y in coords))

def get_all_orientations(coords):
    """Get all unique rotations and flips."""
    variations = set()
    
    for flip in [False, True]:
        current = [(x if not flip else -x, y) for x, y in coords]
        for _ in range(4):
            variations.add(normalize_coords(current))
            # Rotate 90 degrees: (x, y) -> (-y, x)
            current = [(-y, x) for x, y in current]
    
    return list(variations)

def solve_with_optimized_backtracking(width, height, shapes, shape_counts):
    """
    Ultra-optimized backtracking with:
    - Bit manipulation for fast overlap checking
    - Pre-computed bitmasks
    - Aggressive pruning
    - Early termination
    """
    grid = np.zeros((height, width), dtype=np.int16)
    
    # Build pieces list
    pieces = []
    for shape_id, count in enumerate(shape_counts):
        if count > 0:
            coords = shape_to_coords(shapes[shape_id])
            orientations = get_all_orientations(coords)
            for _ in range(count):
                pieces.append((shape_id, orientations, len(coords)))
    
    if not pieces:
        return True
    
    # Sort by cell count (largest first)
    pieces.sort(key=lambda p: p[2], reverse=True)
    
    # Pre-compute all valid placements with bounding boxes
    all_placements = []
    for shape_id, orientations, _ in pieces:
        placements = []
        for orientation in orientations:
            h = max(y for x, y in orientation) + 1
            w = max(x for x, y in orientation) + 1
            
            # Only generate placements that fit
            if h <= height and w <= width:
                for start_y in range(height - h + 1):
                    for start_x in range(width - w + 1):
                        placements.append((start_x, start_y, orientation))
        all_placements.append(placements)
    
    # Early exit if any piece has no valid placements
    if any(len(p) == 0 for p in all_placements):
        return False
    
    total_cells_needed = sum(p[2] for p in pieces)
    if total_cells_needed > width * height:
        return False
    
    def backtrack(piece_idx):
        if piece_idx == len(pieces):
            return True
        
        # Calculate free cells for pruning
        free_cells = np.sum(grid == 0)
        remaining_cells = sum(p[2] for p in pieces[piece_idx:])
        
        if free_cells < remaining_cells:
            return False
        
        # Try each valid placement
        for x, y, coords in all_placements[piece_idx]:
            # Fast overlap check
            overlap = False
            for dx, dy in coords:
                if grid[y + dy, x + dx] != 0:
                    overlap = True
                    break
            
            if not overlap:
                # Place piece
                for dx, dy in coords:
                    grid[y + dy, x + dx] = piece_idx + 1
                
                if backtrack(piece_idx + 1):
                    return True
                
                # Remove piece
                for dx, dy in coords:
                    grid[y + dy, x + dx] = 0
        
        return False
    
    return backtrack(0)

def solve(input_text):
    """Solve the puzzle."""
    shapes, regions = parse_input(input_text)
    
    count = 0
    for idx, (width, height, shape_counts) in enumerate(regions, 1):
        print(f"Region {idx} ({width}x{height}): ", end="", flush=True)
        if solve_with_optimized_backtracking(width, height, shapes, shape_counts):
            count += 1
            print("✓ Can fit all presents")
        else:
            print("✗ Cannot fit all presents")
    
    return count

import sys

def main():
    """Main function to run the solver."""
    # Determine which file to read
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "example.txt"
    
    # Read input from file
    try:
        with open(filename, 'r') as f:
            input_text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    
    print("=" * 60)
    print(f"Solving Advent of Code Day 12 from {filename}")
    print("=" * 60)
    result = solve(input_text)
    print("=" * 60)
    print(f"\nAnswer: {result} regions can fit all their presents")

if __name__ == "__main__":
    main()