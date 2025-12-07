import sys


if len(sys.argv) > 1:
    file_name = sys.argv[1]

with open(file_name, 'r') as file:
    lines = [list(line.strip()) for line in file]

    max_depth = len(lines)
    max_width = len(lines[0])

    start_line = lines[0]
    start_cell = start_line.index('S')

    # dp_row[x] = number of ways to be at column x on current row
    dp_row = [0] * max_width
    dp_row[start_cell] = 1

    total_paths = 0

    # iterate rows from 0 .. max_depth-1; transitions go to y+1
    for y in range(0, max_depth):
        dp_next = [0] * max_width
        for x, cnt in enumerate(dp_row):
            if cnt == 0:
                continue

            # if next row is beyond bottom, these paths exit
            if y + 1 >= max_depth:
                total_paths += cnt
                continue

            below = lines[y+1][x]
            if below == '^':
                # splitter: branch left and right; out-of-bounds branches lost
                if x - 1 >= 0:
                    dp_next[x-1] += cnt
                if x + 1 < max_width:
                    dp_next[x+1] += cnt
            else:
                # normal: go straight down
                dp_next[x] += cnt

        dp_row = dp_next

    print(f"Total paths: {total_paths}")