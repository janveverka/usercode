job=${1:-WgMu_0j}
CMSSW_RELEASE=CMSSW_3_5_6

## setup CMSSW release area
scramv1 project CMSSW $CMSSW_RELEASE
cd $CMSSW_RELEASE/src
eval `scramv1 ru -sh`

## get the code
# cvs co -d Sherpa/Common UserCode/JanVeverka/Sherpa/Common
cvs co -r V00-03-04 GeneratorInterface/SherpaInterface
cvs co -d Sherpa/$job UserCode/JanVeverka/Sherpa/$job
scramv1 build

cp GeneratorInterface/SherpaInterface/data/*SherpaLibs.sh Sherpa/$job/test
## keep the temporary directory for debugging
sed -i 's:rm -rf ./SHERPATMP:# rm -rf ./SHERPATMP:' Sherpa/$job/test/MakeSherpaLibs.sh

## prepare data card
cd Sherpa/$job/test
tar -czf sherpa_${job}_cards.tgz Run.dat Analysis.dat

## run step 1
(time ./MakeSherpaLibs.sh -i ./ -p $job) >& step1.out

## run step 2
(time ./PrepareSherpaLibs.sh -i ./ -p $job -a Sherpa/$job -m LOCAL) >& step2.out

## run step 3
cat >> sherpa_cfg.py <<EOF
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    moduleSeeds = cms.PSet(generator = cms.untracked.uint32(3310)),
    sourceSeed = cms.untracked.uint32(123456)
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
EOF
(time cmsRun sherpa_cfg.py) >& step3.out

## get unique output name
i=0
name=${job}_res${i}.tgz
destination=$CASTOR_HOME/mc/Spring10/Sherpa/libs
# destination=$CASTOR_HOME
while nsls $destination | grep -q $name; do
	((i++))
	name=${job}_res${i}.tgz
done

## store output
cd ../..
tar czf res.tgz $job
rfcp res.tgz $destination/$name
cd ../..

## done!
echo "Exiting $0 with great success!"
