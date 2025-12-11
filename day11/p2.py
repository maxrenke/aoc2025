import sys
from functools import lru_cache

if len(sys.argv) > 1:
    file_name = sys.argv[1]

with open(file_name, 'r') as file:
    lines = [line.strip() for line in file]

# Parse the input to build adjacency list
graph = {}
for line in lines:
    if ':' not in line:
        continue
    parts = line.split(':')
    source = parts[0].strip()
    destinations = parts[1].strip().split()
    graph[source] = tuple(destinations)  # tuple for hashability

def count_paths_memo(start, target, required_nodes):
    required_frozen = frozenset(required_nodes) if required_nodes else frozenset()
    
    @lru_cache(maxsize=None)
    def dfs(current, visited_required):
        if current == target:
            return 1 if required_frozen.issubset(visited_required) else 0
        
        if current not in graph:
            return 0
        
        # Update visited required nodes
        new_visited = visited_required | ({current} if current in required_frozen else set())
        new_visited_frozen = frozenset(new_visited)
        
        path_count = 0
        for neighbor in graph[current]:
            path_count += dfs(neighbor, new_visited_frozen)
        
        return path_count
    
    return dfs(start, frozenset())

# Part 1: you -> out (no requirements)
print("Part 1: ", count_paths_memo("you", "out", None))

# Part 2: svr -> out (must visit dac and fft)
print("Part 2: ", count_paths_memo("svr", "out", {'dac', 'fft'}))