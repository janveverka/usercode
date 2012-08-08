import FWCore.ParameterSet.Config as cms
import FWCore.PythonUtilities.LumiList as LumiList

#______________________________________________________________________________
def apply(json, source):
    '''
    Takes a pool source module configuraiton
    and a filename of a JSON file and extends the configuation
    such that the pool source filters on the JSON file.
    '''
    lumis = LumiList.LumiList(filename=json).getCMSSWString().split(',')
    if not hasattr(source, 'lumisToProcess'):
        source.lumisToProcess = cms.untracked(cms.VLuminosityBlockRange())
    source.lumisToProcess.extend(lumis)
## End of apply(...)

