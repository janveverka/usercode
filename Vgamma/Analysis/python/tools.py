import os

#______________________________________________________________________________
def load_input_files(listname):
    '''
    Returns a list of filenames stored in the given file.
    Assumes that the list name is relative to Vgamma/Analysis/data
    '''
    path = os.path.join(os.environ['CMSSW_BASE'], 'src/Vgamma/Analysis/data',
                        listname)
    input_files = []
    with open(path) as f:
        for line in f:
            input_files.append(line.strip())
    return input_files
## End of load_input_files(..)

  