job=${1:-WgLep_0j2}
jobnumber=${2:-0}
source=$CASTOR_HOME/mc/Spring10/Sherpa
output=$CASTOR_HOME/mc/Spring10/Sherpa/$job/GEN/test
MAXEVENTS=${3:-100}

## setup CMSSW release area
scramv1 project CMSSW CMSSW_3_5_4
cd CMSSW_3_5_4/src
eval `scramv1 ru -sh`

## get the code
mkdir Sherpa && cd Sherpa
rfcp $source/${job}_res0.tgz .
tar xzf ${job}_res0.tgz
cd $job/test
rm -r SHERPATMP
scram b Sherpa/$job

## change the random seed
SEED1=$(date +%s)
((SEED1+=$PPID))
((SEED1+=$jobnumber))
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
process.load('Sherpa/$job/sherpa_cfi')
process.load("Configuration.StandardSequences.SimulationRandomNumberGeneratorSeeds_cff")
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32($MAXEVENTS)
)
process.randomEngineStateProducer = cms.EDProducer("RandomEngineStateProducer")
process.p1 = cms.Path(process.randomEngineStateProducer)
process.path = cms.Path(process.generator)
process.sherpa_out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('sherpa_out.root')
)
process.outpath = cms.EndPath(process.sherpa_out)
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    moduleSeeds = cms.PSet(generator = cms.untracked.uint32($SEED1)),
    sourceSeed = cms.untracked.uint32($SEED2)
)
VERBATIM

(time cmsRun sherpa_cfg.py) >& sherpa_cfg.out

## get unique output name
name=sherpa_out_${MAXEVENTS}evts_job${jobnumber}.root
i=0
while nsls $output | grep -q $name; do
	((i++))
	name=sherpa_out_${MAXEVENTS}evts_job${jobnumber}_${i}.root
done
logfile=log_${name%*.root}.tgz
## store output

tar czf $logfile sherpa_cfg.out
rfcp $logfile $output
rfcp sherpa_out.root $output/$name

echo "Exiting $0 with great success!"
