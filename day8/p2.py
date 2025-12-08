import sys
from typing import Optional
import math
if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = "input.txt"
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
print(f"Loaded {len(boxes)} junction boxes")
# Pre-calculate all pairs and their distances, then sort
print("Calculating all pair distances...")
pairs = []
for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        distance = boxes[i].distance_to(boxes[j])
        pairs.append((distance, boxes[i], boxes[j]))
pairs.sort(key=lambda x: x[0])
print(f"Found {len(pairs)} pairs, sorted by distance")
print("\nConnecting junction boxes until all are in one circuit...\n")
connections_made = 0
last_connection = None
for distance, box1, box2 in pairs:
    circuit1 = box1.get_circuit()
    circuit2 = box2.get_circuit()
    # Skip if already in same circuit
    if circuit1 and circuit2 and circuit1 is circuit2:
        continue
    connections_made += 1
    # Merge or create circuits
    if circuit1 and circuit2:
        # Merging two different circuits
        for box in circuit2.junction_boxes:
            circuit1.add_junction_box(box)
            box.set_circuit(circuit1)
    elif circuit1:
        # Adding second box to existing circuit
        circuit1.add_junction_box(box2)
        box2.set_circuit(circuit1)
    elif circuit2:
        # Adding first box to existing circuit
        circuit2.add_junction_box(box1)
        box1.set_circuit(circuit2)
    else:
        # Creating new circuit for the two junction boxes
        new_circuit = Circuit()
        new_circuit.add_junction_box(box1)
        new_circuit.add_junction_box(box2)
        box1.set_circuit(new_circuit)
        box2.set_circuit(new_circuit)
    # Store this as the last connection
    last_connection = (box1, box2)
    # Check if all boxes are in the same circuit
    circuits = set()
    all_connected = True
    for box in boxes:
        circuit = box.get_circuit()
        if circuit is None:
            all_connected = False
            break
        circuits.add(id(circuit))
    if all_connected and len(circuits) == 1:
        print(f"All junction boxes are now in one circuit after {connections_made} connections!")
        print(f"\nLast connection made between:")
        print(f"  JunctionBox at ({last_connection[0].x}, {last_connection[0].y}, {last_connection[0].z})")
        print(f"  JunctionBox at ({last_connection[1].x}, {last_connection[1].y}, {last_connection[1].z})")
        print(f"  Distance: {distance:.2f}")
        product = last_connection[0].x * last_connection[1].x
        print(f"\nProduct of X coordinates: {last_connection[0].x} ├ù {last_connection[1].x} = {product}")
        break
# Count final circuits
circuits = {}
for box in boxes:
    circuit = box.get_circuit()
    if circuit:
        if id(circuit) not in circuits:
            circuits[id(circuit)] = circuit
    else:
        circuits[id(box)] = None
print(f"\nTotal circuits remaining: {len(circuits)}")
