'''
Database of samples used in the analysis

Jan Veverka, Caltech, 27 March 2013.
'''

from Vgamma.Analysis.records.realdatasamplerecord import RealDataSampleRecord
from Vgamma.Analysis.records.montecarlosamplerecord import MonteCarloSampleRecord

#==============================================================================
class SampleRegister(list):
    #__________________________________________________________________________
    def data(self, *args, **kwargs):
        '''
        Registers a data sample.
        '''
        self.append(RealDataSampleRecord(*args, **kwargs))

    #__________________________________________________________________________
    def mc(self, *args, **kwargs):
        '''
        Registers an MC sample
        '''
        self.append(MonteCarloSampleRecord(*args, **kwargs))

    #__________________________________________________________________________
    def get(self, name):
        '''
        Returns a sample matching the given name.
        '''
        match = []
        for sample in self:
            if sample.name == name:
                match.append(sample)
                
        if len(match) != 1:
            message = "Expect 1 sample with name `%s', got %d" % (
                name, len(match)
                )
            raise RuntimeError, message
        
        return match[0]
    ## End of get


#==============================================================================
def test():
    from Vgamma.Analysis.bookkeeping.samples import register
    print register.get("mm2011AB").__repr__()
    print register.get("zmmg").__repr__()


#==============================================================================
if __name__ == '__main__':
    test()
    import user
    