def find_largest_rectangle(input_text):
    """
    Find the largest rectangle that can be formed using red tiles
    as opposite corners.
    """
    # Parse the input to get coordinates
    lines = input_text.strip().split('\n')
    red_tiles = []
    
    for line in lines:
        if line.strip():
            x, y = map(int, line.split(','))
            red_tiles.append((x, y))
    
    # Find the maximum area
    max_area = 0
    best_pair = None
    
    # Try every pair of red tiles
    n = len(red_tiles)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            
            # Calculate rectangle area
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            area = width * height
            
            if area > max_area:
                max_area = area
                best_pair = (red_tiles[i], red_tiles[j])
    
    return max_area, best_pair

# Test with the example
example_input = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

max_area, best_pair = find_largest_rectangle(example_input)
print(f"Example - Maximum area: {max_area}")
print(f"Best pair: {best_pair}")
print()

# Now paste your puzzle input here:
puzzle_input = """
# PASTE YOUR PUZZLE INPUT HERE
"""

if puzzle_input.strip() and "PASTE" not in puzzle_input:
    max_area, best_pair = find_largest_rectangle(puzzle_input)
    print(f"Puzzle - Maximum area: {max_area}")
    print(f"Best pair: {best_pair}")
else:
    print("Please paste your puzzle input in the puzzle_input variable above")