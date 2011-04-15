import FWCore.ParameterSet.Config as cms

process = cms.Process('GEOMETRY')

process.options = cms.untracked.PSet(

)

# Input source
process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('calogeom.root')
)

## Geometry, Detector Conditions and Pythia Decay Tables (needed for the vertexing)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "MC_311_V2::All"
# process.load("Configuration.StandardSequences.MagneticField_cff")
# process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("Geometry.CaloEventSetup.CaloGeometry_cff")
process.load("Geometry.CaloEventSetup.CaloTopology_cfi")

process.cga = cms.EDAnalyzer("CaloGeometryAnalyzer",
                                 fullEcalDump = cms.untracked.bool(True)
                             )


process.myprint = cms.OutputModule("AsciiOutputModule")

process.p = cms.Path(process.cga)
process.ep = cms.EndPath(process.myprint)