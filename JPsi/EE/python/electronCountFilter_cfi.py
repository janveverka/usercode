import FWCore.ParameterSet.Config as cms

electronCountFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("gsfElectrons"),
    minNumber = cms.uint32(1)
)

if __name__ == "__main__": import user