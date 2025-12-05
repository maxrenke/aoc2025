import sys

if len(sys.argv) > 1:
    file_name = sys.argv[1]

banks = []

with open(file_name, 'r') as file:
    for line in file:
        banks.append(line.strip())

#print(banks)

output = 0

for bank in banks:
    left_digit = bank[0]
    right_digit = bank[1]

    max_joltage = 0
    max_left = left_digit
    max_right = right_digit

    print("Bank: ", bank)
    for i in range(0, len(bank)):
        battery_left = int(bank[i])
        for j in range(0, len(bank)):
            battery_right = int(bank[j])
           
            if i >= j:
                continue

            #print( (str(battery_left) + str(battery_right)))
            #joltage = int((str(battery_left) + str(battery_right)))
            joltage = battery_left * 10 + battery_right
            #print("Joltage: ", joltage)
            if joltage > max_joltage:
                max_joltage = joltage
                max_left = battery_left
                max_right = battery_right

    print("Max joltage: ", max_joltage, " from batteries ", max_left, " and ", max_right)
    output += max_joltage

print("Output: ", output)
            