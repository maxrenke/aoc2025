import sys
from itertools import combinations

if len(sys.argv) > 1:
    file_name = sys.argv[1]

with open(file_name, 'r') as file:
    lines = [line.strip() for line in file]
    
    points = []

    for line in lines:
        x, y = map(int, line.split(','))
        points.append((x, y))

    print(points)

    max_area = 0
    for combo in combinations(points,2):
        #print(combo)
        x1 = combo[0][0]
        y1 = combo[0][1]
        x2 = combo[1][0]
        y2 = combo[1][1]

        width = abs(x2 - x1) + 1
        height = abs(y2 - y1) + 1
        area = width * height
        #print(area)

        max_area = area if area >= max_area else max_area


    print("Maximum rectangle area is ", max_area)