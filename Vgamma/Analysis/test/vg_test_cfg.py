import os
import socket
import FWCore.ParameterSet.Config as cms

_hostname = socket.gethostname()
if 'lxplus' in _hostname:
    dataset_path = '/afs/cern.ch/user/v/veverka/work/data/Vgamma2011/test'
elif  _hostname == 'Jan-Veverkas-MacBook-Pro.local':
    dataset_path = '/Users/veverka/Work/Data/Vgamma2011/test'

process = cms.Process('VgammaAnalysis')

process.inputs = cms.PSet(
    fileNames = cms.vstring(),
    treeName = cms.string('EventTree'),
    )

for filename in '''
                mmgSkim_test100.root
                '''.split():
    process.inputs.fileNames.append(
        os.path.join(dataset_path, filename)
        )

process.outputs = cms.PSet(
    outputName = cms.string('vg_test.root')
    )
    
process.maxEvents = cms.PSet(
    input = cms.untracked.int64(1000),
    reportEvery = cms.untracked.int64(100)
    )
    
process.options = cms.PSet(
    titleStyle = cms.string("mpl")
    )

