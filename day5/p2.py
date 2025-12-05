import sys
import heapq
from itertools import chain

if len(sys.argv) > 1:
    file_name = sys.argv[1]

with open(file_name, 'r') as file:
    lines = [line.strip() for line in file]

    blank_index = lines.index('')

    fresh = lines[:blank_index] #inclusive and may overlap
    available = lines[blank_index + 1:]

    #print("Fresh:\n", fresh)
    heapq.heapify(fresh)
    #print("Heapified Fresh:\n", fresh)

    fresh_tuples = []
    for line in fresh:
        temp = line.split('-')
        start = int(temp[0])
        end = int(temp[1])
        fresh_tuples.append((start, end))

    print("Fresh Tuples:\n", fresh_tuples)

    fresh_ids = range(0)
    
    fresh_tuples.sort(key=lambda t: t[0])

    print("Sorted Fresh Tuples:\n", fresh_tuples)

    sweep_line = fresh_tuples[0][0]
    merged_fresh = []
    current_start, current_end = fresh_tuples[0]
    while fresh_tuples:
        top = heapq.heappop(fresh_tuples)
        if top[0] <= current_end:
            current_end = max(current_end, top[1])
        else:
            merged_fresh.append((current_start, current_end))
            current_start, current_end = top

    merged_fresh.append((current_start, current_end))
    print("Merged Fresh Ranges:\n", merged_fresh)

    total_fresh_ids = 0
    for start, end in merged_fresh:
        total_fresh_ids += (end - start + 1)

    print("Total number of unique fresh ingredient IDs:", total_fresh_ids)