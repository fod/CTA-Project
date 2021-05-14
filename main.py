# main.py
# CTA-Project sorting algorithms
# Author: Fiachra O' Donoghue

from random import randint
from tabulate import tabulate
import json
import time
import os
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib import cm


def insertion_sort(arr):
    """Insertion sort. Based on pseudocode found in Cormen et al., 2001, p. 17; 
       Introduction to Algorithms, 2nd Ed.

    Args:
        list of comparables: A list of elements which are 
                             comparable using <, >, =; i.e.
                             implement __lt__, __gt__, and __eq__

    Returns:
        list: A reference to the sorted list
    """

    # Iterate through list starting at second element
    # The value at arr[i] is the key
    for j in range(1, len(arr)):
        
        # The key and its neighbour to the left
        key = arr[j]
        i = j - 1

        # Until the start of the list is reached 
        # or an element greater than the key is found:
        while i > 0 and arr[i] > key:

            # Swap the key value with the value to its left
            arr[i + 1] = arr[i]

            # Decrement the index variable so that it tracks the position of the key
            i -= 1

        arr[i + 1] = key

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
                
                # ...move the end index to the right
                end_idx += 1

                # then swap the value at the end index and the current value so that 
                # everything to the left of the end index is less than the pivot
                arr[end_idx], arr[i] = arr[i], arr[end_idx]

        # Finally, swap the value to the right of the end index with the
        # pivot so the pivot sits between the sub list of values less than it 
        # and the sublist of values greater than it
        arr[end_idx + 1], arr[pivot_idx] = arr[pivot_idx], arr[end_idx + 1]

        # The value to the right of the end index is the pivot 
        # just used and is the border between the two new partitions
        return end_idx + 1


def quicksort(arr, start_idx=0, pivot_idx=0, first_run=True):
    """Quicksort. Based on pseudocode found in Cormen et al., 2001, p. 146; 
       Introduction to Algorithms, 2nd Ed.

    Args:
        arr (list):                 The list to be sorted. Elements must be 
                                    comparable using <, >, =; i.e.
                                    implement __lt__, __gt__, and __eq__

        start_idx (int, optional):  The index of the start of the first partition. Defaults to 0.

        pivot_idx (int, optional):  The index of the pivot value. Defaults to 0.

        first_run (bool, optional): Flag indicating the first run in the recursive stack.
                                    Used to intitalise the pivot index at the last element 
                                    of the list, arr. Set to False in all recursive calls to
                                    partition(). Defaults to True.

    Returns:
        list: A reference to the sorted list
    """

    # first_run flag allows the default pivot to be the last element in the list
    if first_run:
        pivot_idx = len(arr) - 1

    # The base condition - if start_idx = pivot_idx the sublist must
    # only be one element long
    if start_idx <= pivot_idx:

        # The partition function returns the pivot for the new sublist
        partition_border = partition(arr, start_idx, pivot_idx)

        # Recursively call quicksort on the two sublists produced from the last partition
        quicksort(arr, start_idx, partition_border - 1, first_run=False)
        quicksort(arr, partition_border + 1, pivot_idx, first_run=False)
        
    return arr


def heapsort(arr):
    """Heapsort. Based on pseudocode found in Cormen et al., 2001, pp. 128-136; 
       Introduction to Algorithms, 2nd Ed.

    Args:
        arr (list of comparables): The list to be sorted. Elements must be 
                                   comparable using <, >, =; i.e.
                                   implement __lt__, __gt__, and __eq__

    Returns:
        list: A reference to the sorted list
    """


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

    # hs = heap size --> keep track of border 
    # between sorted and max-heap sections of array
    heap_size = len(arr)
    build_max_heap(arr, heap_size)

    # Iterate from right to left through unsorted section of array 
    for i in range(heap_size - 1, -1, -1):

        # The top value in the heap will be the max so swap it to the end
        arr[0], arr[i] = arr[i], arr[0]
        
        # Move the border between the heap sub-array and the 
        # sorted sub array to the left
        heap_size -= 1
        # Call max_heapify again on the new smaller heap
        max_heapify(arr, heap_size, 0)

    # return the sorted array
    return(arr)


def counting_sort(arr, k=0):
    """Counting sort. Implementation based on pseudocode found in 
       Cormen et al., 2001, p. 168; Introduction to Algorithms, 2nd Ed.

    Args:
        arr (list of positive integers: The list to be sorted
        k (int): The maximum value in arr. Intended to be invoked as
                 counting_sort(arr, max(arr))

    Returns:
        list: A reference to the sorted list
    """

    # Set k to the maximum value in the array
    # The overhead of doing this is:
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

    # To each value in the counter list, add the previous value
    # This gives a count of how many elements are equal to or less than
    # each value in the original array i.e. a -1-based position of the last
    # incidence of each value in the sorted output
    for i in range(1, k + 1):
        counter[i] = counter[i] + counter[i-1]

    # Working backwards through the original array...
    for i in range(len(arr) - 1, -1, -1):
        # ...place each value from the orignal array in the 
        # output array at the position held for that value
        # in the counter array
        output[counter[arr[i]] - 1 ] = arr[i]
        # Decrement the counter for that value so that the position held
        # is correct for th next instance of that value that's encountered
        counter[arr[i]] = counter[arr[i]] - 1  

    return output


def introsort(arr):
    """Introsort. Based on code found at 
    https://www.sanfoundry.com/python-program-implement-introsort/
    with the addition of insertion sort for lists smaller than 20 elements
    based on a pseudocode implementation at
    # https://aquarchitect.github.io/swift-algorithm-club/Introsort/

    Args:
        arr (list of comparables): the list to be sorted


    Returns:
        list: A reference to the sorted list
    """

    def introsort_helper(arr, start, end, maxdepth):
        # Calls quicksort's partition algorithm until partition size reaches 20
        # r max recursion depth is reached


        # Base condition -- 
        if end - start <= 1:
            return

        # if parttion size <= 20 sort it with insertion sort
        elif end - start <= 20:
            insertion_sort(arr[start:end])

        # if max recursion depth has been reached, use quicksort to avoid O(n^2)
        elif maxdepth == 0:
            heapsort(arr[start:end])

        # Otherwise use quicksort
        else:
            p = partition(arr, start, end - 1)
            introsort_helper(arr, start, p, maxdepth - 1)
            introsort_helper(arr, p, end, maxdepth - 1)

    # max depth = 2 times floor of log base 2 of the length of the list
    # taken from https://www.sanfoundry.com/python-program-implement-introsort/
    maxdepth = (len(arr).bit_length() - 1)*2
    introsort_helper(arr, 0, len(arr), maxdepth)
 
    return arr


def benchmark(funcs, arr_sizes, reps=10, intrange=(0, 100), writeraw=False):
    """Benchmarking for sorting algorithms. Repeatedly sorts random input using passed algorithms
       and returns mean times taken for each algorithm/input size ccombination. 

    Args:
        funcs (list of functions):     A list of functions inplementing sorting algorithms
                                       that are available to the benchmarking function 
        arr_sizes (list of ints):      For each value, n, in this list, a list of random integers
                                       of length n will be generated
        reps (int, optional):          The number of times each algorithm will be run on each sample. 
                                       Defaults to 10.
        intrange (tuple, optional):    The range of values to use in the sample lists. Defaults to (0, 100).
        writeraw (boolean, optional):  If true, a timestamped json file of raw times is written to disk.
                                       Defaults to False.

    Returns:
        list of lists of floats:    A table containing the mean times for each algorithm/input size 
                                    combination
    """

    # If arr_sizes is created using range() there's a good chance it ocntains a 0
    if 0 in arr_sizes:
        print("Warning: there is a 0 in the list of array sizes. A zero-sized list is not permitted")
        return

    # Build dict to hold raw results
    raw_result = { func.__name__: { "n": { n: [0] * 10 for n in arr_sizes } } for func in funcs }

    # A list of lists to hold average times for each algorithm and sample size
    table = [[size for size in arr_sizes]]

    # Generate test arrays
    sample_arrs = [ [ randint(intrange[0], intrange[1]) for i in range(n) ] for n in arr_sizes ]

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

    # Write the raw times and input arrays to timestamped json file
    if writeraw:
        raw_data = {"input": sample_arrs, "times": raw_result }
        fname = f"bm_output/bm_raw_{time.strftime('%Y%m%d-%H%M%S')}.json"
        try:
            # try to create output directory if it doesn't exist already
            os.makedirs(os.path.dirname(fname), exist_ok=True)
            with open(fname, "w") as f:
                json.dump(raw_data, f)
        except IOError:
            print("Problem writing raw data")
    
    # Return benchmark results
    return table


def write_plot(result, funcs, exclude=0, yscale="linear"):
# Generate plots of the returned time data

    # Plot style
    style.use('seaborn')

    # Create figure and axes
    fig, ax = plt.subplots()

    # Set y-scale (log or linear)
    plt.yscale(yscale)

    # Set colours
    colours = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", 
                "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan"]

    # Plot each series
    for p in range(exclude, len(result) - 1):
        plt.plot(result[0],result[p + 1], 
        label=funcs[p].__name__.capitalize().replace("_"," "), color=colours[p])

    # Set title, labels, and legend    
    ax.set_title("Sorting algorithm running times for increasing input sizes")
    ax.set_xlabel("input size n")
    ax.set_ylabel(f"running time (ms){' - log scale' if yscale == 'log' else ''}")
    plt.legend()

    # Save the figure
    fig.savefig(f"bm_output/plot_{str(exclude)}_{yscale}_{time.strftime('%Y%m%d-%H%M%S')}")



def main():

    # Set up function and test size lists
    funcs = [insertion_sort, quicksort, heapsort, counting_sort, introsort]
    arr_sizes = [100, 250, 500, 750, 1000, 1250, 2500, 3750, 5000, 6250, 7500, 8750, 10000]
    #arr_sizes = [5, 10 , 15, 20, 25, 30, 35, 40, 45, 50]
    # Run the benchmarks
    result = benchmark(funcs, arr_sizes)

    # Write latex table of benchmark results
    fname_tbl = f"bm_output/bm_table_{time.strftime('%Y%m%d-%H%M%S')}.tex"
    tabledata = result.copy()
    tabledata[0] =  ["\\textbf{" + str(t) + "}" for t in tabledata[0]]
    row_names = [ "\\textbf{" + func.__name__.capitalize().replace('_',' ') + "}" for func in funcs ]            
    table = tabulate(tabledata, 
                    headers="firstrow", 
                    showindex=row_names, 
                    tablefmt="latex_raw",
                    stralign="right",
                    floatfmt=".3f")
    try:
        with open(fname_tbl, "w") as f:
            f.write(table)
    except IOError:
        print("Problem writing results table")

   
    # Plot of output from all algorithms, linear y-scale
    write_plot(result, funcs)

    # Exclude insertion sort to get a better 
    # comparison of the more efficient algorithms
    write_plot(result, funcs, exclude=1)
   
    # Include all algorithms but plot on a log scale
    write_plot(result, funcs, yscale="log")

    
if __name__ == "__main__":
    main()


