import sys
from itertools import combinations

if len(sys.argv) > 1:
    file_name = sys.argv[1]

with open(file_name, 'r') as file:
    lines = [line.strip() for line in file]

    sum_presses = 0

    for line in lines:

        parts = line.split()
            
        # Extract indicator lights (in square brackets)
        lights_str = parts[0].strip('[]')
        target = [1 if c == '#' else 0 for c in lights_str]

        # Extract button configurations (in parentheses)
        buttons = []
        for part in parts[1:]:
            if part.startswith('(') and part.endswith(')'):
                button_indices = part.strip('()').split(',')
                buttons.append([int(x) for x in button_indices])
            elif part.startswith('{'):
                break  # Reached joltage requirements, ignore

        #print(parts)
        #print(lights_str)
        #print(target)
        #print(buttons)

        """Solve system over GF(2) and find solution with minimum weight."""

        n_lights = len(target)
        n_buttons = len(buttons)
        
        # Create coefficient matrix
        matrix = [[0] * n_buttons for _ in range(n_lights)]
        for button_idx, button in enumerate(buttons):
            for light_idx in button:
                matrix[light_idx][button_idx] = 1
        
        n_lights = len(target)
        n_buttons = len(matrix[0]) if matrix else 0
        

        if n_buttons == 0:
            break
        
        # Create augmented matrix [A|b]
        aug = [row[:] + [target[i]] for i, row in enumerate(matrix)]
        
        # Track pivot columns
        pivot_cols = []
        pivot_row = 0
        
        # Reduced row echelon form
        for col in range(n_buttons):
            # Find pivot
            found = False
            for row in range(pivot_row, n_lights):
                if aug[row][col] == 1:
                    aug[pivot_row], aug[row] = aug[row], aug[pivot_row]
                    found = True
                    break
            
            if not found:
                continue
            
            pivot_cols.append(col)
            
            # Eliminate
            for row in range(n_lights):
                if row != pivot_row and aug[row][col] == 1:
                    for j in range(n_buttons + 1):
                        aug[row][j] ^= aug[pivot_row][j]
            
            pivot_row += 1
        
        # Check consistency
        for i in range(pivot_row, n_lights):
            if aug[i][n_buttons] == 1:
                break
        
        # Identify free variables
        free_vars = [i for i in range(n_buttons) if i not in pivot_cols]
        
        # Try all combinations of free variables to minimize total
        min_presses = float('inf')
        
        for mask in range(1 << len(free_vars)):
            solution = [0] * n_buttons
            
            # Set free variables
            for i, var in enumerate(free_vars):
                solution[var] = (mask >> i) & 1
            
            # Set pivot variables
            for i, col in enumerate(pivot_cols):
                val = aug[i][n_buttons]
                for j in range(col + 1, n_buttons):
                    val ^= aug[i][j] * solution[j]
                solution[col] = val
            
            min_presses = min(min_presses, sum(solution))

        print("min presses:", min_presses)

        sum_presses = sum_presses + min_presses

    print("Sum presses: ", sum_presses)