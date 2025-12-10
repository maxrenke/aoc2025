def parse_machine(line):
    """Parse a machine specification line."""
    parts = line.strip().split()
    
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
    
    return target, buttons

def solve_machine_bruteforce(target, buttons):
    """Solve by trying all combinations (for small cases)."""
    n_buttons = len(buttons)
    n_lights = len(target)
    
    min_presses = float('inf')
    
    # Try all 2^n_buttons combinations
    for mask in range(1 << n_buttons):
        # Calculate resulting light configuration
        lights = [0] * n_lights
        presses = 0
        
        for button_idx in range(n_buttons):
            if mask & (1 << button_idx):
                presses += 1
                for light_idx in buttons[button_idx]:
                    lights[light_idx] ^= 1
        
        # Check if matches target
        if lights == target:
            min_presses = min(min_presses, presses)
    
    return min_presses if min_presses != float('inf') else None

def solve_gf2_minimal(matrix, target):
    """Solve system over GF(2) and find solution with minimum weight."""
    n_lights = len(target)
    n_buttons = len(matrix[0]) if matrix else 0
    
    if n_buttons == 0:
        return None
    
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
            return None
    
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
    
    return min_presses

def solve_machine(target, buttons):
    """Find minimum button presses for a machine."""
    n_lights = len(target)
    n_buttons = len(buttons)
    
    # For small cases, use brute force (more reliable)
    if n_buttons <= 15:
        return solve_machine_bruteforce(target, buttons)
    
    # Create coefficient matrix
    matrix = [[0] * n_buttons for _ in range(n_lights)]
    for button_idx, button in enumerate(buttons):
        for light_idx in button:
            matrix[light_idx][button_idx] = 1
    
    return solve_gf2_minimal(matrix, target)

# Test with the example
example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

total = 0
for line in example.strip().split('\n'):
    target, buttons = parse_machine(line)
    presses = solve_machine(target, buttons)
    print(f"Target: {''.join('#' if x else '.' for x in target)}")
    print(f"Minimum presses: {presses}")
    total += presses
    print()

print(f"Total minimum presses: {total}")