'''
Defines the class DataSampleRecord.

Jan Veverka, Caltech, 27 March 2013.
'''

import pprint
import cStringIO

_fields = '''name title latex_label data_type source_filenames source_tree
             skim_filenames skim_tree tree_version
             total_processed_events'''.split()

#==============================================================================
class DataSampleRecord:
    '''
    Holds information about a data sample used in the Vgamma analysis:
      * name - a unique identifier for use in algorithms, 
               it should be a valid C++ symbol,
      * title - for logging and reports, plain ASCII,
      * latex_label - for plot legends and latex autogeneration,
      * data_type - "data" or "MC"
    Possible extensions:
      castor_path,
      susy_hadoop_path,
      susy_raid_path,
      higgs_hadoop_path,
      data_files, 
      skimmed_data_files,
      tree_version, 
      histogram_file,    
    '''
    _fields = _fields
    #__________________________________________________________________________
    def __init__(self,
                 name,
                 title = '',
                 latex_label = '',
                 data_type = '',
                 source_filenames = [],
                 source_tree = '',
                 skim_filenames = [],
                 skim_tree = '',
                 tree_version = '',
                 total_processed_events = -1,
                 ):
        if not title:
            title = name
        if not latex_label:
            latex_label = title
        self.name = str(name)
        self.title = str(title)
        self.latex_label = str(latex_label)
        self.data_type = str(data_type)
        self.source_filenames = list(source_filenames)
        self.source_tree = str(source_tree)
        self.skim_filenames = list(skim_filenames)
        self.skim_tree = str(skim_tree)
        self.tree_version = str(tree_version)
        self.total_processed_events = int(total_processed_events)
        
    #__________________________________________________________________________
    def str_fields(self):
        return ', '.join([str(getattr(self, attr)) for attr in self._fields])
    
    #__________________________________________________________________________
    def repr_fields(self, 
                    fields = _fields):
        ret_items = []
        max_len = max(map(len, fields))
        for field in fields:
            padding = max_len - len(field) + 1
            #value = getattr(self, field).__repr__()
            #output = cStringIO.StringIO()
            #pprint.pprint(getattr(self, field), output)
            #value = output.getvalue()
            #output.close()
            value = pprint.pformat(getattr(self, field), indent=8)
            ret_items.append('%s%*s = %s' % (field, padding, ' ', value))
        return ',\n    '.join(ret_items)
    
    #__________________________________________________________________________
    def __str__(self):
        return '\n    '.join([self.__class__.__name__ + '(',
                              self.str_fields(),
                              ')'])
        
    #__________________________________________________________________________
    def __repr__(self):
        return '\n    '.join([self.__class__.__name__ + '(',
                              self.repr_fields(),
                              ')'])
    
    #__________________________________________________________________________
    def get_total_processed_events(self, verbosity=0):
        total = 0
        import ROOT
        for filename in self.source_filenames:
            source = ROOT.TFile.Open(filename)
            histogram = source.Get('VgAnalyzerKit/hEvents')
            processed_events = int(histogram.GetBinContent(1))
            if verbosity > 0:
                print processed_events, 'in', source.GetName()
            total += processed_events
            source.Close()
        return total
    
## End of DataSampleRecord
