PROCESS_NAME=${1:-WgEle_0j2}
LIB_VERSION=3
CMSSW_RELEASE=CMSSW_3_5_6

## setup CMSSW release area
scramv1 project CMSSW $CMSSW_RELEASE
cd $CMSSW_RELEASE/src
eval `scramv1 ru -sh`

## get the code
# cvs co -d Sherpa/Common UserCode/JanVeverka/Sherpa/Common
cvs co -r V00-03-04 GeneratorInterface/SherpaInterface
scramv1 build

mkdir Sherpa
T3_PATH=/mnt/hadoop/user/veverka/mc/Spring10/Sherpa

## start here if you already have CMSSW realease area
# get the libraries
cd $CMSSW_BASE/src/Sherpa
# scp t3-susy.ultralight.org:$T3_PATH/libs/${PROCESS_NAME}_res${LIB_VERSION}.tgz .
CASTOR_PATH=$CASTOR_HOME/mc/Spring10/Sherpa
rfcp $CASTOR_PATH/libs/${PROCESS_NAME}_res${LIB_VERSION}.tgz .
tar xzf ${PROCESS_NAME}_res${LIB_VERSION}.tgz
cd $PROCESS_NAME/test

# do the actual PROCESS_NAME - prepare the sherpack!
./PrepareSherpaLibs.sh -i ./ -p $PROCESS_NAME -a Sherpa/$PROCESS_NAME -m PROD 2>&1 \
  | tee step2b.out

## store the output on the T3
T3_OUTPUT_PATH=$T3_PATH/sherpacks/test_lib${LIB_VERSION}
T3_URL=t3-susy.ultralight.org
if ! ssh $T3_URL ls $T3_OUTPUT_PATH >& /dev/null; then
  ssh $T3_URL mkdir -p $T3_OUTPUT_PATH
fi
scp sherpa_${PROCESS_NAME}_MASTER.tgz $T3_URL:$T3_OUTPUT_PATH

## Store the ouptut on CASTOR
CASTOR_OUTPUT_PATH=$CASTOR_PATH/sherpacks/test_lib${LIB_VERSION}
if ! nsls $CASTOR_OUTPUT_PATH >& /dev/null; then
  rfmkdir -p $CASTOR_OUTPUT_PATH
fi
rfcp sherpa_${PROCESS_NAME}_MASTER.tgz $CASTOR_OUTPUT_PATH

## clean up
cd $CMSSW_BASE/..
rm -rf $CMSSW_BASE

## done!
echo "Exiting $0 with great success!"
