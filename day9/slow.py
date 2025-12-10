import sys
import time
from itertools import combinations
from shapely.geometry import Point, Polygon
from shapely.prepared import prep
from concurrent.futures import ProcessPoolExecutor, as_completed
import math
import os

def check_combo_batch(batch_data):
    """Process a batch of combinations in a single process"""
    combos, red_tiles_list = batch_data
    
    # Reconstruct polygon and prepared polygon in this process
    valid_tiles = Polygon(red_tiles_list)
    prepared_polygon = prep(valid_tiles)
    red_set = set(red_tiles_list)
    
    local_max_area = 0
    best_combo = None
    
    for combo in combos:
        x1, y1 = combo[0]
        x2, y2 = combo[1]

        min_x, max_x_rect = min(x1, x2), max(x1, x2)
        min_y, max_y_rect = min(y1, y2), max(y1, y2)
        
        # Early area check
        width = max_x_rect - min_x + 1
        height = max_y_rect - min_y + 1
        area = width * height
        
        if area <= local_max_area:
            continue

        # Check validity
        valid = True
        for x in range(min_x, max_x_rect + 1):
            for y in range(min_y, max_y_rect + 1):
                if (x, y) not in red_set:
                    pt = Point(x, y)
                    if not (prepared_polygon.contains(pt) or prepared_polygon.touches(pt)):
                        valid = False
                        break
            if not valid:
                break

        if valid and area > local_max_area:
            local_max_area = area
            best_combo = (min_x, min_y, max_x_rect, max_y_rect)
    
    return local_max_area, len(combos), best_combo

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = "input.txt"

    with open(file_name, 'r') as file:
        red_tiles = []
        
        for line in file:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                red_tiles.append((x, y))

        print(f"Red tiles: {len(red_tiles)} tiles")

        # Calculate total combinations
        total_combos = len(red_tiles) * (len(red_tiles) - 1) // 2
        print(f"Total combinations to check: {total_combos:,}")

        start_time = time.time()

        # Determine number of processes
        num_processes = os.cpu_count() or 4
        print(f"Using {num_processes} processes")
        
        # Split combinations into batches
        all_combos = list(combinations(red_tiles, 2))
        batch_size = math.ceil(len(all_combos) / num_processes)
        
        batches = []
        for i in range(0, len(all_combos), batch_size):
            batch = all_combos[i:i + batch_size]
            batches.append((batch, red_tiles))
        
        print(f"Split into {len(batches)} batches of ~{batch_size:,} combinations each")

        # Process batches in parallel
        max_area = 0
        best_rect = None
        checked = 0
        
        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            futures = {executor.submit(check_combo_batch, batch): i for i, batch in enumerate(batches)}
            
            for future in as_completed(futures):
                batch_max, batch_count, batch_rect = future.result()
                checked += batch_count
                
                if batch_max > max_area:
                    max_area = batch_max
                    best_rect = batch_rect
                    print(f"  -> New max area: {max_area:,} at {best_rect}")
                
                # Progress reporting
                elapsed = time.time() - start_time
                rate = checked / elapsed if elapsed > 0 else 0
                remaining = total_combos - checked
                eta_seconds = remaining / rate if rate > 0 else 0
                eta_minutes = eta_seconds / 60
                
                print(f"Progress: {checked:,}/{total_combos:,} ({100*checked//total_combos}%) - Max area: {max_area:,} - ETA: {eta_minutes:.1f} min ({rate:.0f} combos/sec)")

        elapsed_total = time.time() - start_time
        print(f"\nMaximum rectangle area is {max_area:,}")
        if best_rect:
            print(f"Best rectangle: ({best_rect[0]},{best_rect[1]}) to ({best_rect[2]},{best_rect[3]})")
        print(f"Total time: {elapsed_total:.2f} seconds ({elapsed_total/60:.2f} minutes)")