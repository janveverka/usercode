job=${1:-ZgMu_0j}

## setup CMSSW release area
scramv1 project CMSSW CMSSW_3_5_4
cd CMSSW_3_5_4/src
eval `scramv1 ru -sh`

## get the code
cvs co -r V01-00-00 -d Sherpa/Common UserCode/JanVeverka/Sherpa/Common
cvs co -r V01-00-00 -d Sherpa/$job UserCode/JanVeverka/Sherpa/$job
cp Sherpa/Common/test/{MakeSherpaLibs,PrepareSherpaLibs}.sh Sherpa/$job/test

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
(time cmsRun sherpa_cfg.py) >& step3.out

## get unique output name
i=0
name=${job}_res${i}.tgz
# destination=$CASTOR_HOME/mc/Spring10/Sherpa
destination=$CASTOR_HOME/mc/Spring10/Sherpa
while nsls $destination | grep -q $name; do
	((i++))
	name=${job}_res${i}.tgz
done
 
## store output
cd ../..
tar czf res.tgz $job
rfcp res.tgz $destination/$name
cd ../..
echo "Exiting $0 with great success!"
