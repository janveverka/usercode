#!/bin/bash

# set default values for parameters
JOB_NAME=${1:-ZgNu_0j2}
JOB_NUMBER=${2:-0}
MAX_EVENTS=${3:-42}

SOURCE=$CASTOR_HOME/mc/Spring10/Sherpa

## CUSTOMIZE HERE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# OUTPUT=$CASTOR_HOME/mc/Spring10/Sherpa/$JOB_NAME/GEN/filterJet10
OUTPUT=$CASTOR_HOME/mc/Spring10/Sherpa/$JOB_NAME/GEN/filter

## setup CMSSW release area
scramv1 project CMSSW CMSSW_3_5_4
cd CMSSW_3_5_4/src
eval `scramv1 ru -sh`

## get the filter
cvs co -r HEAD -d Sherpa/Analysis/python UserCode/JanVeverka/Sherpa/Analysis/python/genFilter_cfi.py

## get the code
cd Sherpa

## CUSTOMIZE HERE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# res0 : jet pt > 20 GeV, parton pt > 10 GeV
# res1 : jet pt > 10 GeV, parton pt > 10 GeV (doesn't work)
# res2 : jet pt > 10 GeV, no parton pt cut
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
echo "Log saved in $OUTPUT/$LOG_FILE"

rfcp sherpa_out.root $OUTPUT/$OUTPUT_FILE
echo "Output saved in $OUTPUT/$OUTPUT_FILE"

echo "Exiting $0 for MAX_EVENTS, JOB_NAME, JOB_NUMBER: $MAX_EVENTS $JOB_NAME $JOB_NUMBER"
