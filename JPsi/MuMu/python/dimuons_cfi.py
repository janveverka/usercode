import FWCore.ParameterSet.Config as cms

dimuons = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string('0 < mass'),
    checkCharge = cms.bool(False),
    decay = cms.string('selectedPatMuons selectedPatMuons')
)

dimuonsOS = dimuons.clone(
    checkCharge = True,
    decay = 'selectedPatMuons@+ selectedPatMuons@-'
)

dimuonsSS = dimuonsOS.clone(decay = 'selectedPatMuons@+ selectedPatMuons@+')

dimuonsGGOS = dimuonsOS.clone(decay = 'glbMuons@+ glbMuons@-' )
dimuonsGGSS = dimuonsOS.clone(decay = 'glbMuons@+ glbMuons@+' )

dimuonsGTOS = dimuonsOS.clone(decay = 'glbMuons@+ trkMuons@-' )
dimuonsGTSS = dimuonsOS.clone(decay = 'glbMuons@+ trkMuons@+' )

dimuonsTTOS = dimuonsOS.clone(decay = 'trkMuons@+ trkMuons@-' )
dimuonsTTSS = dimuonsOS.clone(decay = 'trkMuons@+ trkMuons@+' )


