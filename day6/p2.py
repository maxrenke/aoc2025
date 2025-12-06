import sys

if len(sys.argv) > 1:
    file_name = sys.argv[1]

with open(file_name, 'r') as file:
    lines = [line.rstrip('\n') for line in file]

    matrix = []
    for line in lines:
        matrix.append(list(line))
        
    max_cols = len(matrix[0])
    line_totals = []
    parts = []
    problems = []
    for col in range(max_cols).__reversed__():
        #print(f"Column {col}:")
        #print("".join(row[col] for row in matrix))

        column_elements = [row[col] for row in matrix]
        #print("Column elements:", column_elements)
        
        part = "".join(column_elements).strip()
        #print("Part:", part)
        if part != '': parts.append(part)
        else:
            problems.append(parts)
            parts = []

    #catch last problem
    problems.append(parts)
    
    #print("Problems:", problems)
    
    for problem in problems:
        # step 1 - strip operand
        #print("Problem:", problem)
        #print(problem[-1][-1:])
        operand = problem[-1][-1:]
        problem[-1] = problem[-1][:-1]
        #print(operand)
        # step 2 - combine all parts into single list of numbers
        elements = []
        for part in problem:
            elements.extend(part.strip().split())
        #print("Elements:", elements)
        # step 3 - calculate result based on operand
        result = 0              
        if operand == "+":
            result = sum(int(x) for x in elements if x != '')
        elif operand == "*":
            result = 1
            for x in elements:
                if x != '':
                    result *= int(x)
        else:
            result = "Unknown operand"

        #print("Result:", result)
        line_totals.append(result)
        #print("-----")

    grand_total = sum(line_totals)
    print("Grand Total:", grand_total)