'''
Defines the class RealDataSampleRecord.

Jan Veverka, Caltech, 27 March 2013.
'''

from Vgamma.Analysis.records.datasamplerecord import DataSampleRecord

#==============================================================================
class RealDataSampleRecord(DataSampleRecord):
    '''
    Holds information about a data sample of real collision data
    used in the Vgamma analysis. In addition to the attributes
    inherited from DataSampleRecord, it holds:
      * lumi - integrated luminosity in inverse femtobarns 1/fb
    Possible extensions:
      * pileup_target - corresponding PU distribution in data
    '''
    #__________________________________________________________________________
    def __init__(self,
                 name,
                 title = '',
                 latex_label = '',
                 data_type = 'data',
                 lumi = 0, # (1/fb)
                 ):
        
        if not data_type == 'data':
            raise RuntimeError, "Expect data_type = 'data', got %s" % data_type
        
        DataSampleRecord.__init__(self,
                                  name,
                                  title,
                                  latex_label,
                                  data_type)
        self.lumi = float(lumi)
        
    #__________________________________________________________________________
    def repr_attributes(
            self,
            attributes = ['lumi']
            ):
        
        return DataSampleRecord.repr_attributes(
            self, 
            attributes,
            DataSampleRecord.repr_attributes(self)
            )
## End of RealDataSampleRecord
