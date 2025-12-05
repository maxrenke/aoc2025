import sys
import heapq

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

    fresh_ids = []

    for item in available:
        val = int(item.strip())
        temp_heap = []

        while fresh:
            top = heapq.heappop(fresh)
            temp_heap.append(top)

            range_array = top.split('-')
            mapped_range = range(int(range_array[0]), int(range_array[1]) + 1)
            if val in mapped_range:
                fresh_ids.append(val)
                break
            
            #print(f"Comparing available item {val} with fresh item {top}")

        #put values back
        while temp_heap:
            heapq.heappush(fresh, temp_heap.pop())
        
    #print(fresh)

    print("Count of available items found in fresh:", len(fresh_ids))
    #print("Fresh IDs:", fresh_ids)