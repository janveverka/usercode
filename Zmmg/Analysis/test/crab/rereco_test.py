# Auto generated configuration file
# using: 
# Revision: 1.303 
# Source: /cvs/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: step2 -s RAW2DIGI,L1Reco,RECO,DQM --data --datatier RECO,DQM --eventcontent RECO,DQM --conditions auto:com10 --scenario pp --no_exec --magField AutoFromDBCurrent --process reRECO --customise Configuration/DataProcessing/RecoTLR.customiseVALSKIM --inputCommands keep *,drop *_*_*_RECO --python_filename RECOVALSKIM_GR_R_42_V8.py
import FWCore.ParameterSet.Config as cms

process = cms.Process('reRECO')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('DQMOffline.Configuration.DQMOffline_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('DPGAnalysis.Skims.ZmmgSkim_cff')

# process.ecalRecHit.testNewInterCalibEB = True
# process.ecalRecHit.pathInterCalibFile = "lib/slc5_amd64_gcc434/interCalibConstants.pizetaRun2011Brun175832to177878.EcalBarrel.txtlaserdata_20111122_158851_180363"
# process.ecalRecHit.testNewInterCalibEE = False
# process.ecalRecHit.pathInterCalibFileEE = "lib/slc5_amd64_gcc434/interCalibConstants.pizetaRun2011Brun175832to177878.EcalEndcap.txtlaserdata_20111122_158851_180363lto420-620_progr_data_20111122"

process.maxEvents = cms.untracked.PSet(
    #input = cms.untracked.int32(200),
    output = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
   # fileNames = cms.untracked.vstring('/store/data/Run2011A/DoubleElectron/RAW-RECO/ZElectron-05Jul2011ReReco-ECAL-v1/0000/7ED4D0EC-97A7-E011-9282-003048678FF4.root'),
   fileNames = cms.untracked.vstring(
      '/store/data/Run2011B/DoubleMu/RAW-RECO/ZMu-PromptSkim-v1/0000/A4352A59-51DD-E011-902F-00261894393C.root',
      '/store/data/Run2011B/DoubleMu/RAW-RECO/ZMu-PromptSkim-v1/0000/4A4D3933-46DD-E011-8EEB-003048678F62.root'
   ),
   inputCommands = cms.untracked.vstring('keep *', 
                                         #'drop *_*_*_RECO'
                                         )
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    # SkipEvent = cms.untracked.vstring('ProductNotFound')
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.303 $'),
    annotation = cms.untracked.string('step2 nevts:1'),
    name = cms.untracked.string('PyReleaseValidation')
)

# Output definition

process.RECOoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RECOEventContent.outputCommands,
    fileName = cms.untracked.string('step2_RAW2DIGI_L1Reco_RECO_DQM.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('RECO')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('reconstruction_step')
    ),
    
)
process.RECOoutput.outputCommands.append('drop *_*_*_RECO')


from RecoJets.Configuration.RecoPFJets_cff import *
process.kt6PFJetsForRhoComputationEtaMaxDefault = kt6PFJets.clone(doRhoFastjet = True)

process.kt6PFJetsForRhoComputationEtaMax25 = kt6PFJets.clone(Rho_EtaMax = 2.5,doRhoFastjet = True)


process.recoAnalyzer = cms.EDAnalyzer("RecoAnalyzer",
                                      outputFile = cms.string('zrereco_anal.root'),
                                      trigResultTag = cms.untracked.InputTag('TriggerResults','','HLT'),
                                      trigSummaryTag =  cms.untracked.InputTag('hltTriggerSummaryAOD','','HLT'),
                                      
                                      saveAllTracks = cms.untracked.bool(False),
                                      saveLaserCorrSeedCrystal = cms.untracked.bool(True),
                                      saveAllRecHitsSC = cms.untracked.bool(True),
                                      # added this MIG
                                      rhoCorrection    = cms.untracked.InputTag('kt6PFJetsForRhoComputationEtaMax25','rho'),
                                      rhoCorrection2    = cms.untracked.InputTag('kt6PFJetsForRhoComputationEtaMaxDefault','rho'),
                                      
                                      ecalRecHitBarrel = cms.untracked.InputTag('ecalRecHit','EcalRecHitsEB'),
                                      ecalRecHitEndcap = cms.untracked.InputTag('ecalRecHit','EcalRecHitsEE'),
                                      
                                      
                                      debugLevel = cms.int32(0)
                                      )

# process.out_step = cms.EndPath(process.recoAnalyzer )




#process.DQMoutput = cms.OutputModule("PoolOutputModule",
##    splitLevel = cms.untracked.int32(0),
#    outputCommands = process.DQMEventContent.outputCommands,
#    fileName = cms.untracked.string('step2_RAW2DIGI_L1Reco_RECO_DQM_inDQM.root'),
##    dataset = cms.untracked.PSet(
#        filterName = cms.untracked.string(''),
#        dataTier = cms.untracked.string('DQM')
#    )
#)

# Additional output definition

# Other statements
#process.GlobalTag.globaltag = 'GR_R_42_V8::All'
#process.GlobalTag.globaltag ="FT_R_42_V13A::All"
#process.GlobalTag.globaltag ="GR_R_42_V14A::All"
#process.GlobalTag.globaltag ="FT_R_42_V17A::All"
process.GlobalTag.globaltag ="GR_R_42_V24::All"

process.GlobalTag.toGet = cms.VPSet(
    cms.PSet(record = cms.string("EcalIntercalibConstantsRcd"),
             tag = cms.string("EcalIntercalibConstants_V20120613_PhiSymmetryPiZeroElectron2010V3Combination_EtaScaleAllR9"),
             connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_ECAL")
             ),
   cms.PSet(record = cms.string("EcalLaserAPDPNRatiosRcd"),
            tag = cms.string("EcalLaserAPDPNRatios_data_20120131_158851_183320"),
            connect = cms.untracked.string("frontier://PromptProd/CMS_COND_42X_ECAL_LAS")
            ),
   cms.PSet(record = cms.string('EcalLaserAlphasRcd'),
            tag = cms.string('EcalLaserAlphas_EB_sic1_btcp152_EE_sic1_btcp116'),
            connect = cms.untracked.string('frontier://FrontierInt/CMS_COND_ECAL')
            ),
   cms.PSet(record = cms.string("EcalADCToGeVConstantRcd"),
             tag = cms.string("EcalADCToGeVConstant_Bon2011_V20120613"),
             connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_ECAL")
             )
    )

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.dqmoffline_step = cms.Path(process.DQMOffline)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOoutput_step = cms.EndPath(process.RECOoutput)
#process.DQMoutput_step = cms.EndPath(process.DQMoutput)

# Schedule definition
#process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.dqmoffline_step,process.endjob_step,process.RECOoutput_step,process.DQMoutput_step)

#process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.RECOoutput_step)

# process.rhocomputeDefaultEtaMax = cms.Sequence(process.kt6PFJetsForRhoComputationEtaMax25*process.kt6PFJetsForRhoComputationEtaMaxDefault)
# process.rhopath2 = cms.Path(process.rhocomputeDefaultEtaMax)

#process.schedule = cms.Schedule(process.rhopath2,process.out_step)

# process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.rhopath2,process.out_step)
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.RECOoutput_step)

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.RecoTLR
##from Configuration.DataProcessing.RecoTLR import customiseVALSKIM 
from Configuration.GlobalRuns.reco_TLR_42X import *

#call to customisation function customiseVALSKIM imported from Configuration.DataProcessing.RecoTLR
##process = customiseVALSKIM(process)
process = customisePPData(process)

# End of customisation functions

# Filter all paths with the skim filter sequence
for path in process.paths:
    getattr(process, path)._seq = process.ZmmgSkimSeq * getattr(process, path)._seq 


