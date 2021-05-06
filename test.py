# Python3 program to check whether a
# given array represents a max-heap or not
 
# Returns true if arr[i..n-1]
# represents a max-heap
def isHeap(arr, i, n):
     
# If a leaf node
    if i >= int((n - 2) / 2):
        return True
     
    # If an internal node and is greater
    # than its children, and same is
    # recursively true for the children
    if(arr[i] >= arr[2 * i + 1] and
       arr[i] >= arr[2 * i + 2] and
       isHeap(arr, 2 * i + 1, n) and
       isHeap(arr, 2 * i + 2, n)):
        return True
     
    return False
 
# Driver Code
if __name__ == '__main__':
    arr = [16, 10, 9, 2, 1, 8]

    n = len(arr) - 1
 
    if isHeap(arr, 0, n):
        print("Yes")
    else:
        print("No")

    def partition(arr, start_idx, pivot_idx):
    # A nested function which performs the list partitioning for quicksort
        

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