PROCESS_NAME=${1:-WgEle_0j}
CMSSW_RELEASE=CMSSW_3_5_8
## Sherpa production version
##+ none - Sherpa 1.1.2 with CMSSW_3_5_6 in March 2010
##+ 2 - Sherpa 1.2.1 with CMSSW_3_5_8 in May 2010
PROJECT_VERSION=2
## UserCode/JanVeverka/Sherpa release tag
TAG=V01-01-03

## setup CMSSW release area
scramv1 project CMSSW $CMSSW_RELEASE
cd $CMSSW_RELEASE/src
eval `scramv1 ru -sh`

## get the code
# cvs co -d Sherpa/Common UserCode/JanVeverka/Sherpa/Common
cvs co -r $TAG -d Sherpa/$PROCESS_NAME UserCode/JanVeverka/Sherpa/$PROCESS_NAME
cvs co -r $TAG -d Sherpa/Common UserCode/JanVeverka/Sherpa/Common
cp Sherpa/Common/test/*SherpaLibs.sh Sherpa/$PROCESS_NAME/test
rm -rf Sherpa/Common
scramv1 build

## keep the temporary directory for debugging
sed -i 's:rm -rf ./SHERPATMP:# rm -rf ./SHERPATMP:' Sherpa/$PROCESS_NAME/test/MakeSherpaLibs.sh

## prepare data card
cd Sherpa/$PROCESS_NAME/test
tar -czf sherpa_${PROCESS_NAME}_cards.tgz Run.dat Analysis.dat

## run step 1
##+ `-c' option is for Comix only
(time ./MakeSherpaLibs.sh -i ./ -p $PROCESS_NAME -c) >& step1.out

## run step 2
(time ./PrepareSherpaLibs.sh -i ./ -p $PROCESS_NAME -a Sherpa/$PROCESS_NAME -m PROD) >& step2.out

#### Store the sherpack
SHERPACK_DIR=mc/Spring10/Sherpa_v${PROJECT_VERSION}/sherpacks
SHERPACK=sherpa_${PROCESS_NAME}_MASTER.tgz

## On the T3
T3_PATH=/mnt/hadoop/user/veverka
SHERPACK_T3_DIR=$T3_PATH/$SHERPACK_DIR
ssh t3-susy.ultralight.org \
  "if [[ ! -d $SHERPACK_T3_DIR ]]; then mkdir -p $SHERPACK_T3_DIR; fi"
scp $SHERPACK t3-susy.ultralight.org:$SHERPACK_T3_DIR

## On CASTOR
SHERPACK_CASTOR_DIR=$CASTOR_HOME/$SHERPACK_DIR
if ! nsls $SHERPACK_CASTOR_DIR >& /dev/null; then
  rfmkdir -p $SHERPACK_CASTOR_DIR
fi
rfcp $SHERPACK $SHERPACK_CASTOR_DIR

## On the AFS
AFS_PATH=/afs/cern.ch/cms/cit/veverka/data
SHERPACK_AFS_DIR=$AFS_PATH/$SHERPACK_DIR
if [[ ! -d $SHERPACK_AFS_DIR ]]; then
  mkdir -p $SHERPACK_CASTOR_DIR
fi
cp $SHERPACK $SHERPACK_AFS_DIR

## clean up
cd $CMSSW_BASE/..
rm -rf $CMSSW_BASE

## done!
echo "Exiting $0 with great success."
