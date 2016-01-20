def binarySearchRange(alist, item):
    first = 0
    last = len(alist)-1
    found = False
    result = None
    while first<=last and not found:
        midpoint = (first + last)//2
        if alist[midpoint] == item:
            found = True
            #print alist[midpoint]
            result = (alist[midpoint],)
        elif first == last:
            if item < alist[midpoint]:
                result = (alist[midpoint-1], alist[midpoint])
                #print alist[midpoint-1], alist[midpoint]
            else:
                if midpoint == len(alist) - 1:
                    result = (alist[midpoint],)
                    #print alist[midpoint]
                else:
                    result = (alist[midpoint], alist[midpoint+1])
                    #print alist[midpoint], alist[midpoint+1]
            found = True
        else:
            if item < alist[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1
            if first > last:
                result = (alist[midpoint-1],alist[midpoint])
                #print alist[midpoint-1],alist[midpoint]
                found = True
    return result
