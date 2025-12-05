import sys

if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    raise SystemExit("Usage: p2.py <input_file>")

dial = 50  # starts at position 50
dial_size = 100  # 0-99
password = 0

with open(file_name, 'r') as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        direction = line[0]
        distance = int(line[1:])
        print(f"Direction: {direction}, Distance: {distance}")

        start = dial

        if direction == "L":
            # Count k in 1..distance with (start - k) % dial_size == 0
            if start == 0:
                crossings = distance // dial_size
            else:
                crossings = ((distance - start) // dial_size + 1) if distance >= start else 0

            dial = (start - distance) % dial_size

        elif direction == "R":
            # Count k in 1..distance with (start + k) % dial_size == 0
            crossings = (start + distance) // dial_size
            dial = (start + distance) % dial_size

        else:
            print(f"Ignoring unknown direction: {direction}")
            continue

        password += crossings
        print(f"Crossings of 0 during move: {crossings}")
        print(f"New dial position: {dial}")

    print(f"Final dial position: {dial}")
    print(f"Password (total times dial was at 0 during moves): {password}")