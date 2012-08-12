'''
Provides expression strings that define muon selection.
'''

## These are muons that pass all the cuts for the Tight ID [1] 
## [1] https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId



tight_id = '''
    (
        abs(eta) < 2.4 &&
        isGlobalMuon = 1 && 
        isPFMuon = 1 && 
        globalTrack().isNonnull &&
        innerTrack().isNonnull &&
        globalTrack().normalizedChi2 < 10. &&
        globalTrack().hitPattern().numberOfValidMuonHits > 0  &&
        numberOfMatchedStations > 1 &&
        innerTrack().hitPattern().numberOfValidPixelHits > 0 &&
        innerTrack().hitPattern().trackerLayersWithMeasurement > 5 &&
        abs(userFloat("muonVertexing:dxy")) < 0.2 &&
        abs(userFloat("muonVertexing:dz")) < 0.5
    )
    '''

tight_isolation = '(userFloat("muonIsolation:combIso")/pt < 0.12)'