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

