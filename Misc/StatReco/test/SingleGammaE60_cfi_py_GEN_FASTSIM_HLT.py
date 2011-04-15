# Auto generated configuration file
# using: 
# Revision: 1.284.2.2 
# Source: /cvs_server/repositories/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: SingleGammaE60_cfi.py -s GEN,FASTSIM,HLT:GRun --beamspot Flat --pileup NoPileUp --geometry Ideal --conditions auto:mc --eventcontent FEVTSIM --datatier GEN-SIM-DIGI-RECO -n 100 --fileout file:fastsim.root --customise Misc/StatReco/NoSmearBeamSpot_cff.py --no_exec
import FWCore.ParameterSet.Config as cms

process = cms.Process('HLT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('FastSimulation.PileUpProducer.PileUpSimulator_NoPileUp_cff')
process.load('FastSimulation.Configuration.Geometries_MC_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('FastSimulation.Configuration.FamosSequences_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedParameters_cfi')
process.load('FastSimulation.Configuration.HLT_GRun_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FastSimulation.Configuration.EventContent_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.284.2.2 $'),
    annotation = cms.untracked.string('SingleGammaE60_cfi.py nevts:100'),
    name = cms.untracked.string('PyReleaseValidation')
)

# Output definition

process.FEVTSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    outputCommands = process.FEVTSIMEventContent.outputCommands,
    fileName = cms.untracked.string('file:fastsim.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RECO')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.simulation = cms.Sequence(process.simulationWithFamos)
process.HLTEndSequence = cms.Sequence(process.reconstructionWithFamos)
process.FlatVtxSmearingParameters.type = cms.string("Flat")
process.famosSimHits.VertexGenerator = process.FlatVtxSmearingParameters
process.famosPileUp.VertexGenerator = process.FlatVtxSmearingParameters
process.GlobalTag.globaltag = 'MC_311_V2::All'

process.generator = cms.EDProducer("FlatRandomEGunProducer",
    PGunParameters = cms.PSet(
        PartID = cms.vint32(22),
        MaxEta = cms.double(-0.0488368),
        MaxPhi = cms.double(-0.129658),
        MinEta = cms.double(-0.0488369),
        MinE = cms.double(59.999),
        MinPhi = cms.double(-0.129659),
        MaxE = cms.double(60.001)
    ),
    Verbosity = cms.untracked.int32(0),
    psethack = cms.string('single gamma E 60'),
    AddAntiParticle = cms.bool(True),
    firstRun = cms.untracked.uint32(1)
)


# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen_genonly)
process.reconstruction = cms.Path(process.reconstructionWithFamos)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.FEVTSIMoutput_step = cms.EndPath(process.FEVTSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.reconstruction,process.FEVTSIMoutput_step])
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 

# customisation of the process


# Automatic addition of the customisation function from Misc.StatReco.NoSmearBeamSpot_cff

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


process = customise(process)


# End of customisation functions
