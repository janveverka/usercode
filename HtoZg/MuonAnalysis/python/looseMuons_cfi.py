import FWCore.ParameterSet.Config as cms

## These are muons that pass all the cuts for the Tight ID [1] that
## can be implemented by the string parser. The vertexing cuts
## dxy < 0.2 and dz < 0.5 are missing.
## [1] https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId
looseMuons = cms.EDFilter('MuonSelector',
    src = cms.InputTag('muons'),
    cut = cms.string('''
        pt > 20 &&
        abs(eta) < 2.4 &&
        isGlobalMuon = 1 && 
        isPFMuon = 1 && 
        !globalTrack().isNull &&
        !innerTrack().isNull &&
        globalTrack().normalizedChi2 < 10. &&
        globalTrack().hitPattern().numberOfValidMuonHits > 0  &&
        numberOfMatchedStations > 1 &&
        innerTrack().hitPattern().numberOfValidPixelHits > 0 &&
        innerTrack().hitPattern().trackerLayersWithMeasurement > 5
        '''),
    filter = cms.bool(True)                                
    )

