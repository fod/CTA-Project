# main.py
# CTA-Project sorting algorithms
# Author: Fiachra O' Donoghue

from random import randint
from tabulate import tabulate
import json
import time
import os
import matplotlib.pyplot as plt


def insertion_sort(arr):
    """Insertion sort. 

    Args:
        list of comparables: A list of elements which are 
                             comparable using <, >, =; i.e.
                             implement __lt__, __gt__, and __eq__

    Returns:
        sorted list: The sorted list
    """

    # Iterate through list starting at second element
    # The value at arr[i] is the key
    for i in range(1, len(arr)):
        
        # Keep doing this until the key is at the leftmost position of
        # the list, or the value to the left of the key is less than the key
        while i > 0 and arr[i] < arr[i - 1]:

            # Swap the key value with the value to its left
            arr[i], arr[i - 1] = arr[i - 1], arr[i]

            # Decrement the index variable so that it tracks the position of the key
            i -= 1

    # return a reference to the sorted array
    return arr


def partition(arr, start_idx, pivot_idx):
    # Performs the list partitioning for quicksort and introsort

        # The pivot value
        pivot = arr[pivot_idx]

        # The partition end boundary - starts outside the partition
        end_idx = start_idx - 1

        # Iterate through list (or sub-list) from the start to the end 
        # of the current partition
        for i in range(start_idx, pivot_idx):

            # If the current value is less than or equal to the pivot value...
            if arr[i] <= pivot:
                
                # move the end index to the right
                end_idx += 1

                # the swap the value at the end index and the current value so that 
                # everything to the left of the end index is less than the pivot
                arr[end_idx], arr[i] = arr[i], arr[end_idx]

        # Finally, swap the value to the right of the end index with the
        # pivot so the pivot sits between the sub list of values less than it 
        # and the sublist of values greater than it
        arr[end_idx + 1], arr[pivot_idx] = arr[pivot_idx], arr[end_idx + 1]

        # The value to the right of the end index will be the pivot for that sublist
        return end_idx + 1


def quicksort(arr, start_idx=0, pivot_idx=0, first_run=True):
    """Quicksort. Based on pseudocode found in 
    Cormen et al., 2001, p. 146; Introduction to Algorithms, 2nd Ed.

    Args:
        list of comparables: A list of elements which are 
                             comparable using <, >, =; i.e.
                             implement __lt__, __gt__, and __eq__

        int: The index of the start of the first partition

        int: The index of the pivot value
    """

    # first_run flag allows the default pivot to be the last element in the list
    if first_run:
        pivot_idx = len(arr) - 1

    # The base condition - if start_idx = pivot_idx the sublist must
    # only be one element long
    if start_idx <= pivot_idx:

        # The partition function returns the pivot for the new sublist
        new_pivot_idx = partition(arr, start_idx, pivot_idx)

        # Recursively call quicksort on the two sublists produced from the last partition
        quicksort(arr, start_idx, new_pivot_idx - 1, first_run=False)
        quicksort(arr, new_pivot_idx + 1, pivot_idx, first_run=False)
        
    return arr


def heapsort(arr):

    def max_heapify(arr, heap_size, i):
    # Recursively construct max heaps from sub-arrays
    # Takes a list, a heap-size, which is the index of
    # the end of the current sub-list, and i the index of the current node

        # calculate the indices of the left and right children 
        # of the current node
        l = (2 * i) + 1
        r = (2 * i) + 2

        # If the left child is part of this sub array 
        # check if it is larger than the current node
        if l < heap_size and arr[l] > arr[i]:
            largest = l
        else:
            largest = i

        # If the right hand side is in this sub-array
        # check if it is larger than its parent
        if r < heap_size and arr[r] > arr[largest]:
            largest = r

        # If one of the current node's children is larger
        # swap the values and call max_heapify again to see if the current 
        # node needs to be moved further down the tree
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            max_heapify(arr, heap_size, largest)
            
    def build_max_heap(arr, hs):
    # Rearrange the initial array so that it is a valid max heap

        # Elements in arr[len(arr)/2 .. arr[len(arr)-1]] are leaves 
        # so are 1-element heaps already so just rearrange the other half:
        for i in range((len(arr) // 2) -1, -1, -1):
            max_heapify(arr, hs, i)

    # hs = heap size --> keep track of border between sorted and max-heap 
    # sections of array
    hs = len(arr)
    build_max_heap(arr, hs)

    # Iterate through unsorted section of array 
    for i in range(hs - 1, -1, -1):

        arr[0], arr[i] = arr[i], arr[0]
        hs -= 1
        max_heapify(arr, hs, 0)

    return(arr)


def counting_sort(arr, k=0):
    """Counting sort. Implementation based on pseudocode found in 
       Cormen et al., 2001, p. 168; Introduction to Algorithms, 2nd Ed.

    Args:
        arr (list of positive integers: The list to be sorted
        k (int): The maximum value in arr. Intended to be invoked as
                 counting_sort(arr, max(arr))

    Returns:
        list of integers: The sorted list
    """
    # On array with n = 10000:
    # %timeit max(y) 236 µs ± 2.38 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    if not k:
        k = max(arr)

    # output list and list for counting values; both filled with zeroes
    output = [0] * len(arr)
    counter = [0] * (k + 1)

    # Increment the values in the counter list at indices 
    # matching the numbers encountered in the input list
    for i in range(len(arr)):
        counter[arr[i]] = counter[arr[i]] + 1


    for i in range(1, k + 1):
        counter[i] = counter[i] + counter[i-1]

    for i in range(len(arr) - 1, -1, -1):
        output[counter[arr[i]] - 1 ] = arr[i]
        counter[arr[i]] = counter[arr[i]] - 1

    return output


# https://www.sanfoundry.com/python-program-implement-introsort/
def introsort(arr):

    def introsort_helper(arr, start, end, maxdepth):
        if end - start <= 1:
            return

        # https://aquarchitect.github.io/swift-algorithm-club/Introsort/
        elif end - start <= 20:
            insertion_sort(arr[start:end])
        elif maxdepth == 0:
            heapsort(arr[start:end])
        else:
            p = partition(arr, start, end - 1)
            introsort_helper(arr, start, p, maxdepth - 1)
            introsort_helper(arr, p, end, maxdepth - 1)


    maxdepth = (len(arr).bit_length() - 1)*2
    introsort_helper(arr, 0, len(arr), maxdepth)
 
    return arr


def benchmark(funcs, arr_sizes, reps):

    # Build dict to hold raw results
    raw_result = { func.__name__: { "n": { n: [0] * 10 for n in arr_sizes } } for func in funcs }

    # A list of lists to hold average times for each algorithm and sample size
    table = [[size for size in arr_sizes]]

    # Generate test arrays
    sample_arrs = [ [ randint(0, 100) for i in range(n) ] for n in arr_sizes ]

    # Iterate through the list of functions to be benchmarked -- funcs
    for func in funcs:

        # A list to hold the average times for the current algorithm
        results = []

        # Iterate through the list of lists of random ints
        for i, s in enumerate(sample_arrs):

            # A list to hold the time for each run
            times = []
            
            # Sort each input list this number of times
            for rep in range(reps):

                # Feedback for the user; prints algorithm, input list size, and iteration number
                print(f"{func.__name__}, n={arr_sizes[i]}, iteration {rep}")

                # Copy the current list so there's an unsorted list for each run
                sample_arr = s.copy()

                # Sort the input list, noting the start and end times
                start_time = time.time()
                func(sample_arr)
                end_time = time.time()

                # Save the time taken in ms
                times.append((end_time - start_time) * 1000)
                
                # Save the raw results for analysis and debugging
                raw_result[func.__name__]["n"][arr_sizes[i]][rep] = end_time - start_time

            # Add the average run time to the results list
            results.append(round(sum(times) / len(times), 3))

        # Add the row for the current algorithm to the output table
        table.append(results)

    # Write the raw times to timestamped json file
    fname_raw = f"bm_output/bm_raw_{time.strftime('%Y%m%d-%H%M%S')}.json"
    try:
        os.makedirs(os.path.dirname(fname_raw), exist_ok=True)
        with open(fname_raw, "w") as f:
            json.dump(raw_result, f)
    except IOError:
        print("Problem writing raw data")
    
    # Write table of average times in LaTeX format
    fname_tbl = f"bm_output/bm_table_{time.strftime('%Y%m%d-%H%M%S')}.tex"
    try:
        with open(fname_tbl, "w") as f:
            row_names = [ func.__name__ for func in funcs ]
            f.write(tabulate(table, headers="firstrow", showindex=row_names, tablefmt="latex"))
    except IOError:
        print("Problem writing results table")

    return table


def main():

    funcs = [insertion_sort, quicksort, heapsort, counting_sort, introsort]
    arr_sizes = [100, 250, 500, 750, 1000 ]#, 1250, 2500, 3750, 5000, 6250, 7500, 8750, 10000]
    result = benchmark(funcs, arr_sizes, 10)

    
 
    import matplotlib.pyplot as plt
    print(result)
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    plt.yscale('log')
    for p in range(len(result) - 1):
        print(len(result))

        plt.plot(result[0],result[p + 1], label=funcs[p].__name__)
    plt.legend()
    plt.show()

   

if __name__ == "__main__":
    main()


