'''
This is a template containing boiler plate code to speed up starting
new macros for making plots and various studies.

It only prints a message discribing itself.

USAGE: python -i test_template.py

Jan Veverka, Caltech, 6 May 2012
'''

import os
import ROOT
import FWLite.Tools.roofit as roo

import FWLite.Tools.cmsstyle as cmsstyle
import FWLite.Tools.canvases as canvases
import FWLite.Tools.legend as legend
import FWLite.Tools.latex as latex


#______________________________________________________________________________
def main():
    '''This is the entry point to execution.'''
    print 'Welcome to test_template - a simple template for new modules.'
    print 'Exiting test_template with success!'
## End of main().


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user