xname = "scale"
xunit = "(%)"
# fileToParse = "res_scaleScan_100k.out"
fileToParse = "resolutionScan4_trueCut1.00_100k.out"
numberOfLastLinesToParse = 11
outputSuffix = "_scaleScan_100k"

## column for the x variable
ix, iex = (0, 1)

## dictionary holding info about variables in the format
## yname: (value_column, error_column, unit)
paramInfo = {
    "scale":      (2, 3, "(%)"),
    "resolution": (4, 5, "(%)"),
    "cut"       : (6, 7, ""),
    "power"     : (8, 9, ""),
    }

## initialize the data dictionaries
xdata, ydata, exdata, eydata = {}, {}, {}, {}

for var in paramInfo.keys():
    xdata[var], ydata[var], exdata[var], eydata[var] = [], [], [], []

lines = file(fileToParse).read().split("\n")


for yname, (iy, iey, yunit) in paramInfo.items():
    #output = file("%s_vs_%s%s.dat" % (yname, xname, outputSuffix), "w")
    #output.write(
        #"# true_%s %s   model_%s %s    true_%s_error %s    model_%s_error %s\n" %
        #(xname, xunit, yname, yunit, xname, xunit, yname, yunit)
        #)
    for line in lines[-numberOfLastLinesToParse-1:]:
        if len(line) == 0 or line[0] == "#": continue
#         print "Parsing `%s'" % line
        x, y, ex, ey = tuple( [float( line.split() [i] ) for i in [ix, iy, iex, iey] ] )
        #x = x+100.
        #output.write( "% 8.3g   % 8.3g   %8.2g   %8.2g\n" % (x, y, ex, ey) )
        xdata[yname].append(x)
        ydata[yname].append(y)
        exdata[yname].append(ex)
        eydata[yname].append(ey)
    #output.close()
