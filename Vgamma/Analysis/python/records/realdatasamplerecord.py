'''
Defines the class RealDataSampleRecord.

Jan Veverka, Caltech, 27 March 2013.
'''

from Vgamma.Analysis.records.datasamplerecord import DataSampleRecord

_fields = ['lumi_per_pb']

#==============================================================================
class RealDataSampleRecord(DataSampleRecord):
    '''
    Holds information about a data sample of real collision data
    used in the Vgamma analysis. In addition to the attributes
    inherited from DataSampleRecord, it holds:
      * lumi_per_pb - integrated luminosity in inverse femtobarns 1/pb
    Possible extensions:
      * pileup_target - corresponding PU distribution in data
    '''
    
    _fields = _fields
    
    #__________________________________________________________________________
    def __init__(self,
                 ## Inherited from DataSampleRecord
                 name,
                 title = '',
                 latex_label = '',
                 data_type = 'data',
                 source_filenames = [],
                 source_tree = '',
                 skim_filenames = [],
                 skim_tree = '',
                 tree_version = '',
                 total_processed_events = -1,
                 ## Unique to MonteCarloSampleRecord
                 lumi_per_pb = 0, # (1/pb)
                 ):
        
        if not data_type == 'data':
            raise RuntimeError, "Expect data_type = 'data', got %s" % data_type
        
        DataSampleRecord.__init__(self,
                                  name,
                                  title,
                                  latex_label,
                                  data_type,
                                  source_filenames,
                                  source_tree,
                                  skim_filenames,
                                  skim_tree,
                                  tree_version,
                                  total_processed_events)
        self.lumi_per_pb = float(lumi_per_pb)
        
    #__________________________________________________________________________
    def repr_fields(self,
                    fields = DataSampleRecord._fields + _fields):
        return DataSampleRecord.repr_fields(self, fields)
## End of RealDataSampleRecord
