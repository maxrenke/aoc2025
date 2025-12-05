import sys

if len(sys.argv) > 1:
    file_name = sys.argv[1]

# Puzzle
# The forklifts can only access a roll of paper if there are fewer than four rolls of paper in the eight adjacent positions

with open(file_name, 'r') as file:
    lines = [line.strip() for line in file]
    matrix = [[1 if c == "@" else 0 for c in ln] for ln in lines]
    
    rows = len(matrix)
    cols = len(matrix[0])


    min_adjecent_count = 4 #from puzzle
    
    accessible = 1 #start at 1 for p2 modification

    removed = 0 #p2 modification

    while accessible > 0:
        accessible = 0 #reset for p2 modification
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c] == 1:
                    adjacent_count = 0
                    for dir_row in [-1, 0, 1]:
                        for dir_col in [-1, 0, 1]:
                            if dir_row == 0 and dir_col == 0:
                                continue
                            near_row = r + dir_row
                            near_col = c + dir_col
                            
                            if 0 <= near_row < rows and 0 <= near_col < cols:
                                adjacent_count += matrix[near_row][near_col]
                    
                    if adjacent_count < min_adjecent_count:
                        accessible += 1
                        matrix[r][c] = 0 #p2 modification
                        removed += 1
                        #print(f"Roll at ({r},{c}) is accessible and removed.")

    print("Total removed rolls of paper: ", removed)