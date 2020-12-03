from math import*
from pylab import*

def XRDcomponents(XRD):    #function to convert raw data into components so it can be graphed and label its peaks
    fullXRD = []
    for point in XRD:    #for loop to split each element into individual components
        fullXRD.append(point.split()) 
    for point in fullXRD:    
        for component in range(len(point)):
            try:   #try to convert each point to a float
                point[component] = float(point[component])
            except:    #Exception will raise when attempting to convert a peak to float
                if point[component] != "peak":    #ignore the element denoting that the point is a peak
                    point[component] = point[component].strip("*")    #strip the element of the "*"
                    point[component] = float(point[component])    #convert the component to a float
                    point.append("peak")    #append "peak" to denote that the point is a peak
    XRDx = []
    XRDy = []
    for point in fullXRD:    #split the list of points into x, y components
        XRDx.append(point[0])
        XRDy.append(point[1])
    return fullXRD, XRDx, XRDy

def peaks(fullXRD):    #creates a list of the peaks components and its index
    peaksList = []
    peaksTheta = []
    for i in range(len(fullXRD)):
        x = fullXRD[i]
        if x[-1] == "peak":
            peaksList.append([x[0], x[1], i])
            peaksTheta.append(x[0])
    '''To find the midpoints, the "mathematical function" will be split into a smaller function this next section of will be
    determining an appropriate interval for the function to be split to'''
    minDelta = 1000    #start at a large arbituary number
    for i in range(len(peaksList)):
        for j in range(len(peaksList)):
            Delta = abs(peaksList[i][2]-peaksList[j][2])     #go through every x component in the list of peaks
            if 0 < Delta < minDelta:     #find the smallest difference between peaks, half of that will be the radius for the interval 
                minDelta = Delta     
    return peaksList, minDelta//2, peaksTheta

def midpoints(peaksList, fullXRD, minDelta):
    midpoints = []
    for i in range(len(peaksList)):    #iterates accross each peak 
        tempXRD = fullXRD[peaksList[i][2] - minDelta:peaksList[i][2] + minDelta]    #limits to only values within a small radius around the peak
        firstH = tempXRD[:len(tempXRD) // 2]    #looks at the left side of the peak around the radius
        secondH = tempXRD[len(tempXRD) // 2:]    #looks at the right side of the peak around the radius
        currentPeak = peaksList[i][1]
        desiredMid = currentPeak / 2
        halves = [firstH,secondH]
        for halve in halves:
            minDiff = desiredMid
            closestData = []
            for v in range(len(halve)):    #looks for the smallest difference between y-val and the desired val
                delta = abs(desiredMid - halve[v][1])    #and returns the point closest to the desired point from the dataset
                if 0 < delta < minDiff:
                    minDiff = delta
                    closestData = halve[v]
            midpoints.append(closestData)
    return midpoints
   
def calculateTao(Data,peaks):
    taoList = []
    for i in range(0, len(Data),2):    #calculates the particle size obtained from each peak
        Beta = Data[i+1][0]-Data[i][0]
        tao = 0.9*(0.07107)/((Beta)*cos(peaks[int(i/2)]/2))
        taoList.append(tao)
    Average = 0
    for i in taoList:    # averages all of the tao values and returns it
        Average += i
    return Average/len(taoList)

def XRD_Analysis(filename):
    XRD = open(filename, "r")
    XRD = XRD.readlines()
    fullXRD, XRDx, XRDy = XRDcomponents(XRD)
    plot(XRDx,XRDy)
    print("Graph for", filename, "\/")
    show()
    peaksList, minDelta, peaksTheta = peaks(fullXRD)
    Data = midpoints(peaksList, fullXRD, minDelta)
    finalTao = calculateTao(Data, peaksTheta)
    print("The particle size for", filename, "is", finalTao, "nm")
    return finalTao
    
XRD_Analysis("XRD_Example1.txt")
XRD_Analysis("XRD_Example2.txt")