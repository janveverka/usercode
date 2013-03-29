'''
Defines dictionaries of records for samples used in the analysis

Jan Veverka, Caltech, 27 March 2013.
'''

import Vgamma.Analysis.bookkeeping.march2013mmg as mmg_package
import Vgamma.Analysis.bookkeeping.march2013eeg as eeg_package
import Vgamma.Analysis.bookkeeping.test as test_package
from Vgamma.Analysis.bookkeeping.sampleregister import SampleRegister

mumugamma = SampleRegister(mmg_package)
eegamma = SampleRegister(eeg_package)
test = SampleRegister(test_package)

#______________________________________________________________________________
def main():
    print repr(mumugamma['mm2011AB'])
    print repr(mumugamma['zmmg'])
    
#______________________________________________________________________________
if __name__ == '__main__':
    import user
    main()
