'''
Database of samples used in the analysis

Jan Veverka, Caltech, 27 March 2013.
'''
import imp
import os
from Vgamma.Analysis.records.realdatasamplerecord import RealDataSampleRecord
from Vgamma.Analysis.records.montecarlosamplerecord import MonteCarloSampleRecord

_MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')

#==============================================================================
class SampleRegister(dict):
    #__________________________________________________________________________
    def __init__(self, package):
        self.package = package
        self.package_contents = package_contents(package)
        for name in self.package_contents:
            record = record_from_module(name, package.__path__)
            self[record.name] = record
        
    ##__________________________________________________________________________
    #def find(self, name):
        #'''
        #Returns a sample matching the given name.
        #'''
        #match = []
        #for sample in self:
            #if sample.name == name:
                #match.append(sample)
                
        #if len(match) != 1:
            #message = "Expect 1 sample with name `%s', got %d" % (
                #name, len(match)
                #)
            #raise RuntimeError, message
        
        #return match[0]


#==============================================================================
def package_contents(package):
    '''
    Returns a set of modules contained in a given package.
    Example: package_contents('Vgamma/Analysis')
    >>> set(['Analysis'])
    Inspired by http://stackoverflow.com/questions/487971/is-there-a-standard-way-to-list-names-of-python-modules-in-a-package
    '''
    package_name = package.__name__.replace('.', '/')
    file, pathname, description = imp.find_module(package_name)
    if file:
        raise ImportError('Not a package: %r', package_name)
    # Use a set because some may be both source and compiled.
    contents = set([os.path.splitext(module)[0]
        for module in os.listdir(pathname)
        if module.endswith(_MODULE_EXTENSIONS)])
    if '__init__' in contents:
        contents.remove('__init__')
        subpackages = [module for module in os.listdir(pathname)
            if (os.path.isdir(os.path.join(pathname, module)) and
                os.path.isfile(os.path.join(pathname, module, '__init__.py')))]
        contents = contents.union(set(subpackages))
    return contents
        

#==============================================================================
def record_from_module(name, path):
    '''
    record_in_path(name, path) -> name from path.name
    '''
    found = imp.find_module(name, path)
    module = imp.load_module(name, *found)
    return getattr(module, name)
        

#==============================================================================
def test():
    from Vgamma.Analysis.bookkeeping.samples import mumugamma as register
    print register["mm2011AB"].__repr__()
    print register["zmmg"].__repr__()


#==============================================================================
if __name__ == '__main__':
    test()
    import user
    