'''
Defines dictionaries of records for samples used in the analysis

THIS MODULE IS OBSOLETE.  USE THE BOOKKEEPING PACKAGES DIRECTLY INSTEAD.

For example, instead of 
from Vgamma.Analysis.bookkeeping.samples import march2013mmg as mmg
use this:
from Vgamma.Analysis.bookkeeping.march2013mmg import samples as mmg

Rationale: No need to update this module when new bookkeeping backage
is added. Instead, copy __init__.py of an already existing package,
like march2013mmg.

Jan Veverka, Caltech, 27 March 2013.
'''

import Vgamma.Analysis.bookkeeping.march2013mmg as march2013mmg_package
import Vgamma.Analysis.bookkeeping.march2013eeg as march2013eeg_package
import Vgamma.Analysis.bookkeeping.test as test_package
from Vgamma.Analysis.bookkeeping.sampleregister import SampleRegister

march2013mmg = SampleRegister(march2013mmg_package)
march2013eeg = SampleRegister(march2013eeg_package)
test = SampleRegister(test_package)

#______________________________________________________________________________
def main():
    print repr(march2013mmg['mm2011AB'])
    print repr(march2013mmg['zmmg'])
    
#______________________________________________________________________________
if __name__ == '__main__':
    import user
    main()
