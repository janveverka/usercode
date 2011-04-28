import FWCore.ParameterSet.Config as cms

def customise(process):
    #
    # sets limits to << 1 um
    #
    process.FlatVtxSmearingParameters.MinX = -0.00000001
    process.FlatVtxSmearingParameters.MaxX = 0.00000001
    process.FlatVtxSmearingParameters.MinY = -0.00000001
    process.FlatVtxSmearingParameters.MaxY = 0.00000001
    process.FlatVtxSmearingParameters.MinZ = -0.00000001
    process.FlatVtxSmearingParameters.MaxZ = 0.00000001

#     process.RECOSIMoutput.outputCommands.extend([
#         'drop *',
# #         'keep SimTracks_g4SimHits_*_*',
# #         'keep SimVertexs_g4SimHits_*_*',
#         'keep *_g4SimHits_*_*',
#         'keep recoPhotons_photons_*_*',
#         'keep recoPhotonCores_photonCore_*_*',
#         'keep *_PhotonIDProd_*_*',
#         'keep recoGsfElectronCores_gsfElectronCores_*_*',
#         'keep recoGsfElectrons_gsfElectrons_*_*',
#         'keep *_electronMergedSeeds_*_*',
#         'keep recoGsfTracks_electronGsfTracks_*_*',
#         'keep recoGsfTrackExtras_electronGsfTracks_*_*',
#         'keep *_ecalRecHit_*_*',
#         'keep EcalRecHitsSorted_reducedEcalRecHits*_*_*',
#         'keep *_caloRecHits_*_*',
#         'keep *_hcalRecHits_*_*',
#         'keep *_reducedHcalRecHits_*_*',
#     ])

    return process
