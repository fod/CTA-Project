# main.py
# CTA-Project sorting algorithms
# Author: Fiachra O' Donoghue

def insertion_sort(arr):

    for i in range(1, len(arr)):
        while () arr[i] < arr[i - 1]:
            arr[i], arr[i - 1] = arr[i - 1], arr[i]

    print (arr)



def main():
    insertion_sort([5,3,4,1,2,])

if __name__ == "__main__":
    main()