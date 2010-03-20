job=ZgMu_0j

## setup CMSSW release area
cmsrel CMSSW_3_5_4
cd CMSSW_3_5_4/src
cmsenv

## get the code
cvs co -d Sherpa/Template UserCode/JanVeverka/Sherpa/Template
cvs co -d Sherpa/$job UserCode/JanVeverka/Sherpa/$job
cp Sherpa/Template/test/*.sh Sherpa/$job/test

## prepare data card
cd Sherpa/$job/test
tar -czf sherpa_${job}_cards.tgz Run.dat

## run step 1
(time ./MakeSherpaLibs.sh -i ./ -p $job) >& step1.out

## run step 2
(time ./PrepareSherpaLibs.sh -d $CMSSW_BASE -i ./ -p $job -a Sherpa/$job -m LOCAL) >& step2.out

## run step 3
cat >> sherpa_cfg.py <<EOF
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    moduleSeeds = cms.PSet(generator = cms.untracked.uint32(3310)),
    sourceSeed = cms.untracked.uint32(123456)
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
EOF

