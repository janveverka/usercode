'''
Defines the class DataSampleRecord.

Jan Veverka, Caltech, 27 March 2013.
'''

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
    #__________________________________________________________________________
    def __init__(self,
                 name,
                 title = '',
                 latex_label = '',
                 data_type = '',
                 ):
        if not title:
            title = name
        if not latex_label:
            latex_label = title
        self.name = str(name)
        self.title = str(title)
        self.latex_label = str(latex_label)
        self.data_type = str(data_type)
        
    #__________________________________________________________________________
    def str_attributes(self):
        attributes = 'name title latex_label data_type'.split()
        return ', '.join([str(getattr(self, attr)) for attr in attributes])
    
    #__________________________________________________________________________
    def repr_attributes(
            self, 
            attributes = 'name title latex_label data_type'.split(),
            prefix = '',
            ):
        ret_items = []
        if prefix:
            ret_items.append(prefix)
        for attribute in attributes:
            value = getattr(self, attribute)
            ret_items.append('%s = %s' % (attribute, value.__repr__()))
        return ',\n    '.join(ret_items)

    ##__________________________________________________________________________
    #def repr_attributes(self):
        #attributes = 'name title latex_label data_type'.split()
        #return ',\n    '.join([
            #'a = ' + getattr(self, a).__repr__() for a in attributes
            #])
    
    #__________________________________________________________________________
    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self.str_attributes())
        
    #__________________________________________________________________________
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.repr_attributes())
    
## End of DataSampleRecord
