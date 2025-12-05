import sys

if len(sys.argv) > 1:
    file_name = sys.argv[1]

dial = 50 # starts at position 50
dial_size = 100 # 0-99
password = 0

with open(file_name, 'r') as file:
    for line in file:
        direction = line.strip()[0]
        distance = int(line.strip()[1:])
        print(f"Direction: {direction}, Distance: {distance}")

        if direction == "L":
            dial = (dial - distance) % dial_size
        elif direction == "R":
            dial = (dial + distance) % dial_size

        print(f"New dial position: {dial}")
        if dial == 0:
            print("Reached position 0!")
            password+=1

    print(f"Final dial position: {dial}")

    print(f"Password (number of times dial reached 0): {password}")