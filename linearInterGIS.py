import random
import sys

#function to calculate intermediate points on a linear line between two points
#it takes a polyline points as list of list, rFactor to randomize interval as inputs and
#output results in a xlsx file
def interpolate(data, interval, rFactor, row,fh):
    i = 0
    start = data[0][0] + interval
    while i < len(data) -1:
        try:
            slope = (data[i+1][1] - data[i][1])/(data[i+1][0] - data[i][0])
        except ZeroDivisionError:
            i+= 1
            continue
            print "hell"
        while start  < data[i+1][0]:
            ycord = data[i][1] + slope*(start - data[i][0])
            strl = "1000;" + str(row) +";;;;;0;" + str(start) + ";" + str(ycord) + ";0;10.000;0;0\n";
            fh.write(strl)
            row = row +1
            if rFactor:
                start = start + interval*(1 + random.uniform(-0.5, 0.5))
            else:
                start = start + interval
        i+= 1
    if (row%100) == 0:
        sys.stdout.write('.')
    return row

def linearInterpolate(fPath, interval, rFactor):
    print "Started"
    #file handler for file
    f = open(fPath, "r")
    fh = open("output.net", "w")
    header ="$VISION\n* Universitaet Stuttgart Fakultaet 2 Bau+Umweltingenieurwissenschaften Stuttgart\n* 12/14/17\n*\n* Table: Version block\n*\n$VERSION:VERSNR;FILETYPE;LANGUAGE;UNIT\n10.000;Net;ENG;KM\n\n*\n* Table: POI categories\n*\n$POICATEGORY:NO;CODE;NAME;COMMENT;PARENTCATNO\n1000;LP;LinkPoints;;0\n\n*\n* Table: Points of interest: LinkPoints (1000)\n*\n$POIOFCAT_1000:CATNO;NO;CODE;NAME;COMMENT;IMAGEFILENAME;USEIMAGEFILE;XCOORD;YCOORD;SURFACEID;IMAGEHEIGHT;USEIMAGEHEIGHT;IMAGEANGLE\n"
    fh.write(header)
    row = 1
    # loop through a file and read a line at a time
    for line in f:
        #read between paranthesis and convert to a list of strings
        d = line[line.find("(")+1:line.find(")")].replace(','," ").split()
        if not d:
            continue
        i = 0
        data = []
        #loop through the list and convert to list of lists of floats
        while i <= len(d)-1:
            data.append([float(d[i]), float(d[i+1])])
            i+=2;
        #function call to calculate intermediate points
        row = interpolate(data, interval, rFactor, row, fh)
    print "\nCompleted Successfully"
    f.close()
    fh.close()

