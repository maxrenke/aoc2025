import sys
from itertools import product

try:
    from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpStatus
    HAS_PULP = True
except ImportError:
    HAS_PULP = False

if len(sys.argv) > 1:
    file_name = sys.argv[1]

with open(file_name, 'r') as file:
    lines = [line.strip() for line in file]

    sum_presses_part1 = 0
    sum_presses_part2 = 0

    for line_num, line in enumerate(lines, 1):

        parts = line.split()
            
        # Extract indicator lights (in square brackets)
        lights_str = parts[0].strip('[]')
        target_lights = [1 if c == '#' else 0 for c in lights_str]

        # Extract button configurations (in parentheses)
        buttons = []
        joltage_idx = -1
        for i, part in enumerate(parts[1:], 1):
            if part.startswith('(') and part.endswith(')'):
                button_indices = part.strip('()').split(',')
                buttons.append([int(x) for x in button_indices])
            elif part.startswith('{'):
                joltage_idx = i
                break
        
        # Extract joltage requirements (in curly braces) - for Part 2
        if joltage_idx >= 0:
            joltage_str = parts[joltage_idx].strip('{}')
            target_joltage = [int(x) for x in joltage_str.split(',')]
        else:
            target_joltage = []

        print(f"\nLine {line_num}:")

        # ============ PART 1: Lights (GF(2)) ============
        n_lights = len(target_lights)
        n_buttons = len(buttons)
        
        # Create coefficient matrix
        matrix = [[0] * n_buttons for _ in range(n_lights)]
        for button_idx, button in enumerate(buttons):
            for light_idx in button:
                if light_idx < n_lights:
                    matrix[light_idx][button_idx] = 1
        
        if n_buttons == 0:
            continue
        
        # Create augmented matrix [A|b]
        aug = [row[:] + [target_lights[i]] for i, row in enumerate(matrix)]
        
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
        inconsistent = False
        for i in range(pivot_row, n_lights):
            if aug[i][n_buttons] == 1:
                inconsistent = True
                break
        
        if inconsistent:
            min_presses_part1 = None
        else:
            # Identify free variables
            free_vars = [i for i in range(n_buttons) if i not in pivot_cols]
            
            # Try all combinations of free variables to minimize total
            min_presses_part1 = float('inf')
            
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
                
                min_presses_part1 = min(min_presses_part1, sum(solution))

        print(f"  Part 1 min presses: {min_presses_part1}")
        if min_presses_part1 != float('inf'):
            sum_presses_part1 += min_presses_part1

        # ============ PART 2: Joltage (Integer Linear) ============
        n_counters = len(target_joltage)
        
        # Build coefficient matrix for joltage
        joltage_matrix = [[0] * n_buttons for _ in range(n_counters)]
        for button_idx, button in enumerate(buttons):
            for counter_idx in button:
                if counter_idx < n_counters:
                    joltage_matrix[counter_idx][button_idx] = 1
        
        if HAS_PULP:
            # Create ILP problem
            prob = LpProblem(f"Joltage_{line_num}", LpMinimize)
            
            # Decision variables: number of times each button is pressed
            x = [LpVariable(f"button_{i}", lowBound=0, cat='Integer') for i in range(n_buttons)]
            
            # Objective: minimize total button presses
            prob += lpSum(x)
            
            # Constraints: each counter must equal its target
            for counter_idx in range(n_counters):
                prob += (
                    lpSum(joltage_matrix[counter_idx][button_idx] * x[button_idx] 
                          for button_idx in range(n_buttons)) == target_joltage[counter_idx],
                    f"counter_{counter_idx}"
                )
            
            # Solve
            prob.solve()
            
            if LpStatus[prob.status] == 'Optimal':
                min_presses_part2 = int(sum(var.varValue for var in x))
            else:
                min_presses_part2 = None
                print(f"  Part 2: No solution found (status: {LpStatus[prob.status]})")
        else:
            min_presses_part2 = None
            print("  (PuLP not available for Part 2 - install with: pip install pulp)")
        
        print(f"  Part 2 min presses: {min_presses_part2}")
        if min_presses_part2:
            sum_presses_part2 += min_presses_part2

    print(f"\n{'='*50}")
    print(f"Part 1 Sum presses: {sum_presses_part1}")
    print(f"Part 2 Sum presses: {sum_presses_part2}")