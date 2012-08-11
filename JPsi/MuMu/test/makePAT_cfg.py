import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.coreTools import *
removeAllPATObjectsBut(process, ["Muons"])
removeMCMatching(process)

# process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
# from PhysicsTools.PatAlgos.tools.trigTools import *
# switchOnTrigger( process )
# switchOnTriggerMatchEmbedding( process )

process.load("JPsi.MuMu.dimuons_cfi")
process.load("JPsi.MuMu.dimuonsFilter_cfi")
process.dimuonsSequence = cms.Sequence(
  process.dimuons * process.dimuonsFilter
)

process.p = cms.Path(
  process.patDefaultSequence * process.dimuonsSequence
)

process.GlobalTag.globaltag = "GR_R_37X_V6A::All"

import JPsi.MuMu.CS_Onia_June9thSkim_v1_FilesAtFnal_cff as June9thSkim
process.source.fileNames = cms.untracked.vstring(June9thSkim.fileNames[:])

process.maxEvents.input = 1000
# process.out.fileName = "pat_test.root"
#process.out.fileName = "/uscms/home/veverka/nobackup/CS_Onia_June9thSkim_v1_PAT.root"
process.out.fileName = "DimuonSkim.root"
process.options.wantSummary = False
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.selectedPatMuons.cut = '(isTrackerMuon=1 || isGlobalMuon=1) & pt > 0.0 & abs(eta) < 3.0'

