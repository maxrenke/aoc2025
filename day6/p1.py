import sys

if len(sys.argv) > 1:
    file_name = sys.argv[1]

with open(file_name, 'r') as file:
    lines = [line.strip() for line in file]

    matrix = []
    for line in lines:
        matrix.append(list(filter(None, line.split(" "))))

    problems = []

    transposed = list(zip(*matrix))
    for row in transposed:
        problems.append(" ".join(row))

    grand_total = 0

    for problem in problems:
        print(problem)
        elements = problem.split(" ")
        operand = elements[-1]
        result = 0
        print("Operand:", operand)
        if operand == "+":
            result = sum(int(x) for x in elements[:-1])
        elif operand == "*":
            result = 1
            for x in elements[:-1]:
                result *= int(x)
        else:
            result = "Unknown operand"

        print("Result:", result)
        grand_total += result
        print("-----")
    print("Grand Total:", grand_total)