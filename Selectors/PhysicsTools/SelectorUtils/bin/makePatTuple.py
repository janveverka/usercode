# This is an example PAT configuration showing the usage of PAT on full sim samples

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# note that you can use a bunch of core tools of PAT
# to taylor your PAT configuration; for a few examples
# uncomment the following lines

from PhysicsTools.PatAlgos.tools.coreTools import *
#removeCleaning(process)
#removeMCMatching(process, 'Muons')
#removeAllPATObjectsBut(process, ['Muons'])
#removeSpecificPATObjects(process, ['Electrons', 'Muons', 'Taus'])

# let it run
process.p = cms.Path(
    process.patDefaultSequence
    )

from PhysicsTools.PatAlgos.tools.trigTools import *
switchOnTrigger( process )


# ----------------------------------------------------
# You might want to change some of these default
# parameters
# ----------------------------------------------------
# process.GlobalTag.globaltag =  "MC_36Y_V10::All"    ##  (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
process.GlobalTag.globaltag =  "START36_V10::All"    ##  (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)

ttbarFileNames = """
6A0E324C-E970-DF11-990B-00304867900C.root
7EFD4501-E170-DF11-A4D0-0026189438D4.root
B0DE958B-DF70-DF11-98E6-002618943857.root
B6E7AB58-E870-DF11-A182-0026189438CB.root
DEDA4044-F270-DF11-8FFC-00261894392B.root
""".split()

zmmFileNames = """
16F4C9D1-1B71-DF11-B488-0018F3D095FE.root
185791CC-1C71-DF11-AA5F-001A92971B5E.root
5EB55CC3-2471-DF11-A173-0026189438A2.root
6AA61BFD-1A71-DF11-A5DC-00261894392B.root
EC3EEC2F-2071-DF11-BB00-003048679296.root
""".split()

wmFileNames = """
6262A450-EA70-DF11-9C9C-00261894391C.root
6C94A1E2-F170-DF11-8C9B-0026189437FD.root
789FDCED-E970-DF11-83AC-001A92810ADE.root
F00CCA06-EA70-DF11-ADDA-002618943951.root
""".split()

ttbarPath = "/castor/cern.ch/cms/store/relval/CMSSW_3_6_2/RelValTTbar/GEN-SIM-RECO/START36_V10-v1/0002"
zmmPath = "/castor/cern.ch/cms/store/relval/CMSSW_3_6_2/RelValZMM/GEN-SIM-RECO/START36_V10-v1/0002"
wmPath = "/castor/cern.ch/cms/store/relval/CMSSW_3_6_2/RelValWM/GEN-SIM-RECO/START36_V10-v1/0002"

# process.source.fileNames = ["rfio:" + zmmPath + "/" + f for f in zmmFileNames]
# process.source.fileNames = ["rfio:" + ttbarPath + "/" + f for f in ttbarFileNames]
process.source.fileNames = ["rfio:" + wmPath + "/" + f for f in wmFileNames]
                                    ##  (e.g. 'file:AOD.root')

process.maxEvents.input = 10000          ##  (e.g. -1 to run on all events)
process.out.outputCommands += [ "keep *_offlinePrimaryVertices_*_*" ]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)

#process.out.fileName = "zmm_pat.root"            ##  (e.g. 'myTuple.root')
#process.out.fileName = "ttbar_pat.root"            ##  (e.g. 'myTuple.root')
process.out.fileName = "wm_pat.root"            ##  (e.g. 'myTuple.root')

process.options.wantSummary = False ##  (False to suppress the long output at the end of the job)

## Some simple filtering
process.countPatJets.minNumber = 1
process.countPatLeptons.minNumber = 1


