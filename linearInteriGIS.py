import xlsxwriter
import random
import sys

#function to calculate intermediate points on a linear line between two points
#it takes a polyline points as list of list, rFactor to randomize interval as inputs and
#output results in a xlsx file
def interpolate(data, interval, rFactor, row, worksheet):
    i = 0
    start = data[0][0] + interval
    while i < len(data) -1:
        slope = (data[i+1][1] - data[i][1])/(data[i+1][0] - data[i][0])
        while start  < data[i+1][0]:
            ycord = data[i][1] + slope*(start - data[i][0])
            worksheet.write(row, 0,     start)
            worksheet.write(row, 1, ycord)
            row = row +1
            if rFactor:
                start = start + interval*(1 + random.uniform(-0.5, 0.5))
            else:
                start = start + interval
        i+= 1
        sys.stdout.write('.')
    return row

def linearInterpolate(fPath, interval, rFactor):
    workbook = xlsxwriter.Workbook('interpolateddata.xlsx')
    worksheet = workbook.add_worksheet()
    #file handler for file
    f = open(fPath, "r")
    row = 0
    # loop through a file and read a line at a time
    for line in f:
        #read between paranthesis and convert to a list of strings
        d = line[line.find("(")+1:line.find(")")].replace(','," ").split()
        i = 0
        data = []
        #loop through the list and convert to list of lists of floats
        while i <= len(d)-1:
            data.append([float(d[i]), float(d[i+1])])
            i+=2;
        #function call to calculate intermediate points
        row = interpolate(data, interval, rFactor, row, worksheet)
    print "Completed Successfully"
    f.close()
    workbook.close()

