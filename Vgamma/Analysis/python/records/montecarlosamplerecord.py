'''
Defines the class MonteCarloSampleRecord.

Jan Veverka, Caltech, 27 March 2013.
'''

from Vgamma.Analysis.records.datasamplerecord import DataSampleRecord

#==============================================================================
class MonteCarloSampleRecord(DataSampleRecord):
    '''
    Holds information about a Monte Carlo sample
    used in the Vgamma analysis. In addition to the attributes
    inherited from DataSampleRecord, it holds:
      * cross_section - the cross section in picobarns 
    Possible extensions:
      * cross_section_type - LO, NLO, etc.?
    '''
    #__________________________________________________________________________
    def __init__(self,
                 name,
                 title = '',
                 latex_label = '',
                 data_type = 'MC',
                 cross_section = 0, # (pb)
                 ):

        if not data_type == 'MC':
            raise RuntimeError, "Expect data_type = 'MC', got %s" % data_type
        
        DataSampleRecord.__init__(self,
                                  name,
                                  title,
                                  latex_label,
                                  data_type)
                                  
        self.cross_section = float(cross_section)

    #__________________________________________________________________________
    def repr_attributes(
            self,
            attributes = ['cross_section']
            ):
        
        return DataSampleRecord.repr_attributes(
            self, 
            attributes,
            DataSampleRecord.repr_attributes(self)
            )
## End of MonteCarloSampleRecord
