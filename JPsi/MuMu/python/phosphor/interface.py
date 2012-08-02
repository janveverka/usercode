#!/cms/sw/slc5_amd64_gcc434/external/python/2.6.4-cms14/bin/python
import getopt
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

#import ConfigParser, StringIO
from configparser import parse_cfg_file
from phosphorcalculator import init, init_cfg_file, process_real_data, process_monte_carlo, outro
from globals import Globals
#from Phosphor_Globals import debug, version, verbose, cfg_file, use_real_data
from globals import version, verbose, debug, cfg_file, use_real_data

sw = ROOT.TStopwatch()
sw2 = ROOT.TStopwatch()




#=== MAIN =====================================================================

def main():

    sw.Start()
    sw2.Start()
    global  version, verbose, debug, cfg_file, use_real_data
    
    print 'ARGV      :', sys.argv[1:]

    try:
        options, remainder = getopt.gnu_getopt(sys.argv[1:], 'o:c:vdh', ['cfg_file=','output=','verbose','debug','version=','help',])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

        
    for opt, arg in options:
        #   print 'OPT: ', opt, 'ARG: ', arg
        
        if opt in ('-c', '--cfg_file'):
            cfg_file = arg    
        elif opt in ('-o', '--output'):
            Globals.outputfile = arg
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-d', '--debug'):
            debug = True
        elif opt == '--version':
            version = arg
        elif opt in ('h','--help'):
            print '========================HERE THE HELP WILL BE PUT!!! HAHA========================================'
            sys.exit(2)
    if debug:
        print 'VERSION   :', version
        print 'VERBOSE   :', verbose
        print 'OUTPUT    :', Globals.outputfile
        print 'REMAINING :', remainder

    if cfg_file == 'empty':

        if debug:
            print "USING NAME AS CONFIGURATION FILE"
        init()
        
        if use_real_data:
            process_real_data()
        else:
            process_monte_carlo()

    else:

        Globals.cuts.append('mmMass + mmgMass < 180')
        Globals.cuts.append('minDeltaR < 1.5')
        
        if debug:
            print 'Calling Parse Configuration File Function------>:'
            
        parse_cfg_file(cfg_file)
        init_cfg_file()
        
        if Globals.DataType == 'data':
            process_real_data()
        elif Globals.DataType == 'mc':
            process_monte_carlo()
        else:
            raise RuntimeError, 'Wrong Data Type, Please Try DataType = data or DataType = mc'

    outro()

if __name__ == '__main__':
    main()
