import sys
from typing import Optional
import math

if len(sys.argv) > 1:
    file_name = sys.argv[1]

if len(sys.argv) > 2:
    iterations = int(sys.argv[2])
else:
    iterations = 10 #part 1

with open(file_name, 'r') as file:
    lines = [list(line.strip().split(",")) for line in file]

class JunctionBox:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def distance_to(self, other: 'JunctionBox') -> float:
        return math.dist((self.x, self.y, self.z), (other.x, other.y, other.z))

    def set_circuit(self, circuit: 'Circuit'):
        self.circuit = circuit

    def get_circuit(self) -> Optional['Circuit']:
        return getattr(self, 'circuit', None)

    def __repr__(self):
        return f"JunctionBox({self.x}, {self.y}, {self.z})"

class Circuit:
    def __init__(self):
        self.junction_boxes = []

    def add_junction_box(self, box: JunctionBox):
        self.junction_boxes.append(box)

boxes = []    

for line in lines:
    box = JunctionBox(int(line[0]), int(line[1]), int(line[2]))
    boxes.append(box)
    print(f"JunctionBox at coordinates: x={box.x}, y={box.y}, z={box.z}")

# Pre-calculate all pairs and their distances, then sort
print("\nCalculating all pair distances...")
pairs = []
for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        distance = boxes[i].distance_to(boxes[j])
        pairs.append((distance, boxes[i], boxes[j]))

pairs.sort(key=lambda x: x[0])

print(f"Found {len(pairs)} pairs, sorted by distance")
print("\nConnecting junction boxes...\n")

connections_made = 0
for distance, box1, box2 in pairs:
    if connections_made >= iterations:
        break
    
    connections_made += 1
    print(f"--- Connection {connections_made} ---")
    print(f"Closest unprocessed pair: JunctionBox at ({box1.x}, {box1.y}, {box1.z}) to ({box2.x}, {box2.y}, {box2.z}) with distance {distance:.2f}")
    
    circuit1 = box1.get_circuit()
    circuit2 = box2.get_circuit()
    
    if circuit1 and circuit2 and circuit1 is circuit2:
        print("Both junction boxes are already in the same circuit. No action taken.")
    elif circuit1 and circuit2:
        print("Merging two different circuits.")
        for box in circuit2.junction_boxes:
            circuit1.add_junction_box(box)
            box.set_circuit(circuit1)
    elif circuit1:
        print("Adding second box to existing circuit.")
        circuit1.add_junction_box(box2)
        box2.set_circuit(circuit1)
    elif circuit2:
        print("Adding first box to existing circuit.")
        circuit2.add_junction_box(box1)
        box1.set_circuit(circuit2)
    else:
        print("Creating new circuit for the two junction boxes.")
        new_circuit = Circuit()
        new_circuit.add_junction_box(box1)
        new_circuit.add_junction_box(box2)
        box1.set_circuit(new_circuit)
        box2.set_circuit(new_circuit)

# Print final circuit sizes
print("\n--- Final Circuit Summary ---")
circuits = {}
for box in boxes:
    circuit = box.get_circuit()
    if circuit:
        if id(circuit) not in circuits:
            circuits[id(circuit)] = circuit
    else:
        # Box not in any circuit, counts as circuit of size 1
        circuits[id(box)] = None

circuit_sizes = []
for circuit_id, circuit in circuits.items():
    if circuit:
        size = len(circuit.junction_boxes)
        circuit_sizes.append(size)
        print(f"Circuit with {size} junction boxes")
    else:
        circuit_sizes.append(1)
        print(f"Circuit with 1 junction box")

circuit_sizes.sort(reverse=True)
print(f"\nTotal circuits: {len(circuit_sizes)}")
if len(circuit_sizes) >= 3:
    product = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
    print(f"Product of three largest circuits: {circuit_sizes[0]} × {circuit_sizes[1]} × {circuit_sizes[2]} = {product}")