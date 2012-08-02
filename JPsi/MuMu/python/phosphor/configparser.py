#=== IMPORTS ==================================================================
import sys
import ConfigParser, StringIO
from globals import Globals, version, debug
#from Phosphor_Interface import debug

#=== CONSTANTS ================================================================

# section name for options without section:
NOSECTION = 'NOSECTION'


#=== CLASSES ==================================================================

class SimpleConfigParser(ConfigParser.RawConfigParser):
    """
    Simple configuration file parser: based on ConfigParser from the standard
    library, slightly modified to parse configuration files without sections.

    Inspired from an idea posted by Fredrik Lundh:
    http://mail.python.org/pipermail/python-dev/2002-November/029987.html
    """

    def read(self, filename):
        text = open(filename).read()
        #print 'text: ', text
        print "[%s]\n" % NOSECTION + text
        f = StringIO.StringIO("[%s]\n" % NOSECTION + text)
        self.readfp(f, filename)

    def getoption(self, option):
        'get the value of an option'
        return self.get(NOSECTION, option)


    def getoptionslist(self):
        'get a list of available options'
        return self.options(NOSECTION)


    def hasoption(self, option):
        """
        return True if an option is available, False otherwise.
        (NOTE: do not confuse with the original has_option)
        """
        return self.has_option(NOSECTION, option)

def parse_cfg_file(cfg_file):

    global debug
   
    cp = SimpleConfigParser()

    if debug:
        print 'Parsing %s...' % cfg_file

    cp.read(cfg_file)

    # Phosphor_Globals.DataType = cp.getoption('datatype')

   
    print '******************DATA TYPE*************************************', Globals.cuts

    #return 
    if debug:
        print 'Sections:', cp.sections()
  
        
    if debug:
        print 'getoptionslist():', cp.getoptionslist()
        
    for option in cp.getoptionslist():

        #print DataType
        
        if debug:
            print "getoption('%s') = '%s'" % (option, cp.getoption(option))
        if option=='datatype':
            Globals.DataType = cp.getoption(option)
            print 'DATA TYPE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', Globals.DataType
            continue
        elif option=='detectortype':
            Globals.DetectorType = cp.getoption(option)
            if Globals.DetectorType=='EE':
                Globals.cuts.append('!phoIsEB')
                continue
            elif Globals.DetectorType=='EB':
                Globals.cuts.append('phoIsEB')
                continue
            else:
                raise RuntimeError, 'Wrong Detector Type, Please Try EE or EB'
                
        elif option=='treeversion':
            Globals.model_tree_version = Globals.data_tree_version = cp.getoption(option)
            continue
        elif option=='ptlow':
            Globals.cuts.append('phoPt >= %s' % cp.getoption(option))
            if debug:
                print '===CUTS===', Globals.cuts
            continue
        elif option=='pthigh':
            Globals.cuts.append('phoPt < %s' % cp.getoption(option))
            if debug:
                print '===CUTS===', Globals.cuts
            continue
        elif option=='r9low':
            Globals.cuts.append('phoR9 >= %s' % cp.getoption(option))
            if debug:
                print '===CUTS===', Globals.cuts
            continue
        elif option=='r9high':
            Globals.cuts.append('phoR9 < %s' % cp.getoption(option))
            if debug:
                print '===CUTS===', Globals.cuts
            continue
            
        if debug:
            print "has option('wrongname') =", cp.hasoption('wrongname')
