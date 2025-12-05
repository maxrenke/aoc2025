import sys

if len(sys.argv) > 1:
    file_name = sys.argv[1]

# validation function (returns bool)
def valid(n):
    
    mid = len(n) // 2
    left = n[:mid]
    right = n[mid:]

    if left == right:
        return False
    
    return True

with open(file_name, 'r') as file:
    for line in file:
        print(line.strip())
        ranges = line.strip().split(',')

sum = 0

for r in ranges:
    first, last = r.split('-')
    #print(f"First: {first}, Last: {last}")

    for i in range(int(first), int(last) + 1):
        if valid(str(i)):
            continue
        print(f"Invalid number found: {i}")
        sum += i #add invalid IDs together

print(f"Sum of invalid numbers: {sum}")
