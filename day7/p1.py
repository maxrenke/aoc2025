import sys

if len(sys.argv) > 1:
    file_name = sys.argv[1]

with open(file_name, 'r') as file:
    lines = [list(line.strip()) for line in file]

    max_depth = len(lines)
    max_width = len(lines[0])

    start_line = lines[0]

    start_cell = start_line.index('S')

    def print_matrix(matrix):
        for row in matrix:
            print("".join(row))
        print()
    
    def send_beam(x, y, matrix):
        """Send a beam from (x,y) downwards and return number of unique paths
        that reach the bottom of the matrix. Each recursive branch gets its
        own copy of the matrix so paths are tracked separately.
        """
        print_matrix(matrix)

        # if next row is beyond the bottom, this path reached the exit
        if y+1 >= max_depth:
            return 1

        below = matrix[y+1][x]

        # splitter: branch left and right (if in bounds)
        if below == "^":
            if (x-1 < 0) or (x+1 >= max_width):
                return 0

            left_matrix = [row[:] for row in matrix]
            right_matrix = [row[:] for row in matrix]

            left_matrix[y+1][x-1] = "|"
            right_matrix[y+1][x+1] = "|"

            left_count = send_beam(x-1, y+1, left_matrix)
            right_count = send_beam(x+1, y+1, right_matrix)

            return left_count + right_count

        # normal cell: move straight down
        new_matrix = [row[:] for row in matrix]
        new_matrix[y+1][x] = "|"
        return send_beam(x, y+1, new_matrix)

    total_paths = send_beam(start_cell, 0, lines)

    print("Total paths: {}".format(total_paths))