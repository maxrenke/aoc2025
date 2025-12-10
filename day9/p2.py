"""
Advent of Code 2025 - Day 9 Part 2
Uses Shapely library for polygon geometry
"""
from itertools import combinations
from shapely.geometry import Polygon, box
from shapely.prepared import prep

def solve_part2(input_text):
    lines = input_text.strip().split('\n')
    red_tiles = [(int(l.split(',')[0]), int(l.split(',')[1])) for l in lines]
    
    # Create polygon from the red tiles
    # The tiles form a closed loop when connected in order
    polygon = Polygon(red_tiles)
    
    # Prepare the polygon for faster 'within' checks
    prepared_polygon = prep(polygon)
    
    max_area = 0
    best_rect = None
    
    # Try all pairs of red tiles as opposite corners
    for i, (x1, y1) in enumerate(red_tiles):
        if i % 50 == 0:
            print(f"Progress: {i}/{len(red_tiles)}")
        
        for j in range(i + 1, len(red_tiles)):
            x2, y2 = red_tiles[j]
            
            # Create rectangle from these two corners
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            
            # Create a box (rectangle) geometry
            rectangle = box(min_x, min_y, max_x, max_y)
            
            # Check if rectangle is completely within the polygon
            if prepared_polygon.contains(rectangle):
                area = (max_x - min_x + 1) * (max_y - min_y + 1)
                if area > max_area:
                    max_area = area
                    best_rect = (x1, y1, x2, y2)
    
    print(f"\nMaximum area: {max_area}")
    if best_rect:
        print(f"Rectangle corners: ({best_rect[0]}, {best_rect[1]}) to ({best_rect[2]}, {best_rect[3]})")
    
    return max_area

if __name__ == "__main__":
    # Read input
    with open('input.txt', 'r') as f:
        input_data = f.read()
    
    answer = solve_part2(input_data)
    print(f"\nFinal Answer: {answer}")