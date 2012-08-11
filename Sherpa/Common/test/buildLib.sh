JOB=${1:-WgEle_0j}
CMSSW_RELEASE=CMSSW_3_5_8
## Sherpa production version
##+ none - Sherpa 1.1.2 with CMSSW_3_5_6 in March 2010
##+ 2 - Sherpa 1.2.1 with CMSSW_3_5_8 in May 2010
VERSION=2

## setup CMSSW release area
scramv1 project CMSSW $CMSSW_RELEASE
cd $CMSSW_RELEASE/src
eval `scramv1 ru -sh`

## get the code
# cvs co -d Sherpa/Common UserCode/JanVeverka/Sherpa/Common
cvs co -d Sherpa/$JOB UserCode/JanVeverka/Sherpa/$JOB
cvs co -r V00-03-10 GeneratorInterface/SherpaInterface
cp GeneratorInterface/SherpaInterface/data/*SherpaLibs.sh Sherpa/$JOB/test
rm -rf GeneratorInterface/SherpaInterface

## keep the temporary directory for debugging
sed -i 's:rm -rf ./SHERPATMP:# rm -rf ./SHERPATMP:' Sherpa/$JOB/test/MakeSherpaLibs.sh

## prepare data card
cd Sherpa/$JOB/test
tar -czf sherpa_${JOB}_cards.tgz Run.dat Analysis.dat

## run step 1
##+ `-c' option is for Comix only
(time ./MakeSherpaLibs.sh -i ./ -p $JOB -c) >& step1.out

## run step 2
(time ./PrepareSherpaLibs.sh -i ./ -p $JOB -a Sherpa/$JOB -m LOCAL) >& step2.out

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
I=0
NAME=${JOB}_res${I}.tgz
DESTINATION=$CASTOR_HOME/mc/Spring10/Sherpa_v${VERSION}/libs
# DESTINATION=$CASTOR_HOME
while nsls $DESTINATION | grep -q $NAME; do
	((I++))
	NAME=${JOB}_res${I}.tgz
done

## store output
cd ../..
tar czf res.tgz $JOB
rfcp res.tgz $DESTINATION/$NAME
cd ../..

## done!
echo "Exiting $0 with great success!"
