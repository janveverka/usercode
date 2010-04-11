job=${1:-ZgMu_0j}
version=0
CMSSW_RELEASE=CMSSW_3_5_6_patch1

## setup CMSSW release area
scramv1 project CMSSW $CMSSW_RELEASE
cd $CMSSW_RELEASE/src
eval `scramv1 ru -sh`

## get the code
# cvs co -d Sherpa/Common UserCode/JanVeverka/Sherpa/Common
cvs co -r V00-03-04 GeneratorInterface/SherpaInterface
scramv1 build

mkdir Sherpa
SHERPA_T3_PATH=/mnt/hadoop/user/veverka/mc/Spring10/Sherpa

## start here if you already have CMSSW realease area
# get the libraries
cd $CMSSW_BASE/src/Sherpa
scp t3-susy.ultralight.org:$SHERPA_T3_PATH/libs/${job}_res${version}.tgz .
tar xzf ${job}_res${version}.tgz
cd $job/test

# do the actual job - prepare the sherpack!
./PrepareSherpaLibs.sh -i ./ -p $job -a Sherpa/$job -m PROD 2>1 | tee step2b.out

## store the output
scp sherpa*MASTER*.tgz t3-susy.ultralight.org:$SHERPA_T3_PATH/sherpacks/test

## clean up
cd $CMSSW_BASE/..
rm -rf $CMSSW_BASE

## done!
echo "Exiting $0 with great success!"
