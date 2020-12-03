def bubbleSort(list):
    swap = True
    while swap:
        print(list)
        swap = False
        for i in range(len(list)-1):
            if list[i]>list[i+1]:
                swap = True
                list[i+1], list[i] = list[i], list[i+1]
    return(list)


print(bubbleSort([6,8,1,4,10,7,8,9,3,2,5]))
