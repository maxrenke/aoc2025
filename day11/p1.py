import sys

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
        graph[source] = destinations
    
    # DFS to count all paths from start to end
    def dfs(current, target, visited):
        if current == target:
            return 1
        
        if current not in graph:
            return 0
        
        # Mark current as visited to avoid cycles
        visited.add(current)
        
        path_count = 0
        for neighbor in graph[current]:
            if neighbor not in visited:
                path_count += dfs(neighbor, target, visited)
        
        # Backtrack: unmark current to allow it in other paths
        visited.remove(current)

        return path_count
    
    print("Answer: ", dfs("you","out",set()))