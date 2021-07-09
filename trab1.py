# trab1.py
import threading
import time
from datetime import timedelta
from contextlib import contextmanager
from multiprocessing import Manager, Pool
import numpy as np

def merge_sort(array):
    size = len(array)

    if size <= 1:
        return array

    midIndex = int(size / 2)
    left = array[:midIndex]
    right = array[midIndex:]
    
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)

###############################################################################
def merge(left, right):
    sorted_list = []
    left = left[:]
    right = right[:]
    
    while len(left) > 0 or len(right) > 0:
        if len(left) > 0 and len(right) > 0:
            if left[0] <= right[0]:
                sorted_list.append(left.pop(0))
            else:
                sorted_list.append(right.pop(0))
        elif len(left) > 0:
            sorted_list.append(left.pop(0))
        elif len(right) > 0:
            sorted_list.append(right.pop(0))
    return sorted_list

##############################################################################
@contextmanager
def process_pool(size):
    """Create a process pool and block until
    all processes have completed."""
    pool = Pool(size)
    yield pool
    pool.close()
    pool.join()


###############################################################################
def multiproc_merge_sort(array, procs):
    step = int(len(array)/procs)
    manager = Manager()
    results = manager.list()
    
    with process_pool(size = procs) as pool:
        for i in range(procs):
            if i < procs-1:
                chunk = array[i*step : i+1*step]
            else:
                chunk = array[i*step:]
            pool.apply_async(merge_sort_multiple, (results, chunk))
    
    while(len(results)) > 1:
        with process_pool(size=procs) as pool:
            pool.apply_async(merge_multiple,
                (results, results.pop(0), results.pop(0)))
            
    final_list = results[0]
    return final_list

###############################################################################    
def merge_sort_multiple(results, array):
  results.append(merge_sort(array))

###############################################################################
def merge_multiple(results, array_part_left, array_part_right):
  results.append(merge(array_part_left, array_part_right))
  
###############################################################################
def main():
    size = 1_000_000
    procs = 4
    
    vector = list(np.random.randint(0, 3*size, size))
    
    start = time.monotonic()
    sorted = multiproc_merge_sort(vector, procs)
    
    end = time.monotonic()
    elapsed = end-start
    
    print("Time elapsed: "  +str(timedelta(seconds = elapsed)))

if __name__ == "__main__":
    main()