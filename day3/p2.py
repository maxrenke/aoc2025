import sys
from itertools import combinations

if len(sys.argv) > 1:
    file_name = sys.argv[1]

banks = []

with open(file_name, 'r') as file:
    for line in file:
        banks.append(line.strip())

#print(banks)

output = 0
total_batteries = 12

for bank in banks:

    # Greedy O(n) stack algorithm to get the largest subsequence of length m
    to_remove = len(bank) - total_batteries
    stack = []
    for battery in bank:
        while stack and to_remove > 0 and stack[-1] < battery:
            stack.pop()
            to_remove -= 1
        stack.append(battery)

    best_seq = ''.join(stack[:total_batteries])
    max_joltage = int(best_seq)

    print("Max joltage: ", max_joltage, " from batteries sequence ", best_seq)
    output += max_joltage

print("Output: ", output)
            