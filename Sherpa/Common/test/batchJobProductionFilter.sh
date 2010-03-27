## this file script is meant to be redirected in the bsub command
## usage: bsub < batchJobProductionFilter.sh JOB_NAME=ZgEleMu_0j2 JOB_NUMBER=0 MAX_EVENTS=42

# set default values for parameters
if [[ -z $JOB_NAME   ]]; then JOB_NAME=WgLep_0j; fi
if [[ -z $JOB_NUMBER ]]; then JOB_NUMBER=0;       fi
if [[ -z $MAX_EVENTS ]]; then MAX_EVENTS=100;     fi

SOURCE=$CASTOR_HOME/mc/Spring10/Sherpa
OUTPUT=$CASTOR_HOME/mc/Spring10/Sherpa/$JOB_NAME/GEN/test

## setup CMSSW release area
scramv1 project CMSSW CMSSW_3_5_4
cd CMSSW_3_5_4/src
eval `scramv1 ru -sh`

## get the filter
cvs co -r HEAD -d Sherpa/Analysis/python UserCode/JanVeverka/Sherpa/Analysis/python/genFilter_cfi.py

## get the code
mkdir Sherpa && cd Sherpa
rfcp $SOURCE/${JOB_NAME}_res0.tgz .
tar xzf ${JOB_NAME}_res0.tgz
cd $JOB_NAME/test
rm -r SHERPATMP
scram b Sherpa

## change the random seed
SEED1=$(date +%s)
((SEED1+=$PPID))
((SEED1+=$JOB_NUMBER))
((SEED1%=900000000))
SEED2=$SEED1
((SEED2+=$(date +%s)))
((SEED2%=900000000))

## clean old config and root files
if [[ -f sherpa_out.root ]]; then
  rm sherpa_out.root
fi

if [[ -f sherpa_cfg.py ]]; then
  rm sherpa_cfg.py
fi

## make new config file
cat > sherpa_cfg.py <<VERBATIM
import FWCore.ParameterSet.Config as cms

process = cms.Process("runSherpa")
process.load('Sherpa/$JOB_NAME/sherpa_cfi')
process.load("Configuration.StandardSequences.SimulationRandomNumberGeneratorSeeds_cff")
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(
    output = cms.untracked.int32($MAX_EVENTS)
)
process.randomEngineStateProducer = cms.EDProducer("RandomEngineStateProducer")
process.p1 = cms.Path(process.randomEngineStateProducer)
process.load("Sherpa.Analysis.genFilter_cfi")
process.path = cms.Path(process.generator * process.genFilter)
process.sherpa_out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('sherpa_out.root'),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("path")
    )
)
process.outpath = cms.EndPath(process.sherpa_out)
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    moduleSeeds = cms.PSet(generator = cms.untracked.uint32($SEED1)),
    sourceSeed = cms.untracked.uint32($SEED2)
)
VERBATIM

(time cmsRun sherpa_cfg.py) >& sherpa_cfg.out

## get unique output name
OUTPUT_FILE=sherpa_out_${MAX_EVENTS}evts_job${JOB_NUMBER}.root
I=0
while nsls $OUTPUT | grep -q $OUTPUT_FILE; do
	((I++))
	OUTPUT_FILE=sherpa_out_${MAX_EVENTS}evts_job${JOB_NUMBER}_${I}.root
done
LOG_FILE=log_${OUTPUT_FILE%*.root}.tgz
## store output

tar czf $LOG_FILE sherpa_cfg.out
rfcp $LOG_FILE $OUTPUT
rfcp sherpa_out.root $OUTPUT/$OUTPUT_FILE

echo "Exiting $0 for MAX_EVENTS, JOB_NAME, JOB_NUMBER: $MAX_EVENTS $JOB_NAME $JOB_NUMBER"
