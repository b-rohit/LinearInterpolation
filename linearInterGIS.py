import numpy as np
import random
import sys


def coord_add(data, l, fh, rand, row):
    i = 0
    np.seterr(divide='ignore', invalid='ignore')
    while i < len(data) -1:
        a = np.array(data[i])
        b = np.array(data[i+1])
        r = b - a
        rn = np.linalg.norm(a - b)
        try:
            n = r / rn
        except ZeroDivisionError:
            i+= 1
            continue
        sign = 0
        if r[0] > 0:
            sign = 1
        else:
            sign =-1
        while a[0]<=b[0]*sign:
            strl = "1000;" + str(row) +";;;;;0;" + str(a[0]) + ";" + str(a[1]) + ";0;10.000;0;0\n"
            a = a + n * l*random.uniform(0, 1)*rand
            fh.write(strl)
            row+= 1
        i+=1
    return row


def linearInterpolate(fPath, interval, rFactor):
    print "Started ..."
    #file handler for file
    f = open(fPath, "r")
    fh = open("Output.net", "w")
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
        row = coord_add(data, interval, fh, rFactor, row)
    print "Completed Successfully"
    fh.close()
    f.close()
    return row

