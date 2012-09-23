'''
A command line tool to copy a histogram from one file to another.

USAGE: source.root/hist destination.root
This would copy the histogram named "hist" from source.root to destination.root.
'''
import os
import re
import sys
import ROOT

# source = /home/cms/veverka/Vgamma2011/VgKitV14/MC/ZZ_TuneZ2_Fall11.root/VgAnalyzerKit/hEvents

#______________________________________________________________________________
def main():
    '''
    Main entry point for execution.
    '''
    if len(sys.argv) != 3:
        print 'Illegal arguments: ', sys.argv
        print_usage()
    
    source = sys.argv[1]
    destination = sys.argv[2]
    
    hist = gethist(source)
    puthist(hist, destination)
    # print parsepath(destination)
## End of main.
    

#______________________________________________________________________________
def print_usage():
    '''
    Prints usage information for this tool.
    '''
    print 'USAGE: rootcp source.root/hist destination.root'
## End of print_usage()


#______________________________________________________________________________
def parsepath(path):
    '''
    Splits file.root/name to file.root and name.
    Both file.root and name may be prepended with path.
    '''
    root_tokens = []
    ospath = path
    
    ## Find the file
    while not re.match('.+\.root$', ospath):
        ospath, rootname = os.path.split(ospath)
        root_tokens.append(rootname)
        if ospath == '' or ospath == os.path.sep:
            raise RuntimeError, "Illegal path: %s" % path
    
    root_tokens.reverse()
    
    if root_tokens:
        rootpath = os.path.join(*root_tokens)
    else:
        rootpath = ''
    
    return ospath, rootpath
## End of parsepath()


#______________________________________________________________________________
def gethist(path):
    '''
    Returns a clone of the histogram from the given file.
    '''
    filename, histname = parsepath(path)
    rootfile = ROOT.TFile.Open(filename, "read")
    hist = rootfile.Get(histname)
    if not hist:
        raise RuntimeError, "Didn't find `%s' in `%s'" % (histname, filename)
    histclone = hist.Clone()
    histclone.SetDirectory(None)
    rootfile.Close()
    return histclone
## End of gethist(path)


#______________________________________________________________________________
def puthist(hist, destination):
    '''
    Stores hist in the destination.
    '''
    ## Parse the destination path in the two parts
    filename, dirname = parsepath(destination)
    
    if not os.path.isfile(filename):
        raise RuntimeError, "File `%s' does not exist" % filename
      
    rootfile = ROOT.TFile.Open(filename, "update")
    if not rootfile:
        raise RuntimeError, "Couldn't open `%s'!" % filename
    
    if dirname:
        rootdir = rootfile.Get(dirname)
        if not rootdir:
            msg = "Didn't find `%s' in `%s'" % (dirname, filename)
            raise RuntimeError, msg
    else:
        rootdir = rootfile

    if rootdir.Get(hist.GetName()):
        print "WARNING: rootcp.py: `%s' already contains `%s" % (destination,
                                                                 hist.GetName())
        
    hist.SetDirectory(rootdir)
    rootfile.Write()

    rootfile.Close()

## End of puthist
    
#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
