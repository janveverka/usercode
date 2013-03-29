'''
Defines the class MonteCarloSampleRecord.

Jan Veverka, Caltech, 27 March 2013.
'''

from Vgamma.Analysis.records.datasamplerecord import DataSampleRecord

_fields = ['cross_section_in_pb']

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
    
    _fields = _fields
    
    #__________________________________________________________________________
    def __init__(self,
                 ## Inherited from DataSampleRecord
                 name,
                 title = '',
                 latex_label = '',
                 data_type = 'MC',
                 source_filenames = [],
                 skim_filenames = [],
                 total_processed_events = -1,
                 ## Unique to MonteCarloSampleRecord
                 cross_section_in_pb = 0, # (pb)
                 ):

        if not data_type == 'MC':
            raise RuntimeError, "Expect data_type = 'MC', got %s" % data_type
        
        DataSampleRecord.__init__(self,
                                  name,
                                  title,
                                  latex_label,
                                  data_type,
                                  source_filenames,
                                  skim_filenames,
                                  total_processed_events)
                                  
        self.cross_section_in_pb = float(cross_section_in_pb)

    #__________________________________________________________________________
    def repr_fields(self, fields = DataSampleRecord._fields + _fields):
        return DataSampleRecord.repr_fields(self, fields)
## End of MonteCarloSampleRecord
