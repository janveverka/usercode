PROCESS_NAME=${1:-WgEle_0j}
CMSSW_RELEASE=CMSSW_3_5_8
## Sherpa production version
##+ none - Sherpa 1.1.2 with CMSSW_3_5_6 in March 2010
##+ 2 - Sherpa 1.2.1 with CMSSW_3_5_8 in May 2010
PROJECT_VERSION=2
## UserCode/JanVeverka/Sherpa release tag
TAG=V01-01-00

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

## get unique output name
CASTOR_PATH=$CASTOR_HOME/mc/Spring10/Sherpa_v${PROJECT_VERSION}
CASTOR_OUTPUT_PATH=$CASTOR_PATH/sherpacks
# SHERPACK_VERSION=0
# NAME=sherpa_${PROCESS_NAME}_v${SHERPACK_VERSION}_MASTER.tgz
# while nsls $CASTOR_OUTPUT_PATH | grep -q $NAME; do
# 	((SHERPACK_VERSION++))
# 	NAME=sherpa_${PROCESS_NAME}_v${SHERPACK_VERSION}_MASTER.tgz
# done

## Store output on CASTOR
# rfcp sherpa_${PROCESS_NAME}_MASTER.tgz $CASTOR_OUTPUT_PATH/$NAME
rfcp sherpa_${PROCESS_NAME}_MASTER.tgz $CASTOR_OUTPUT_PATH

## clean up
cd $CMSSW_BASE/..
rm -rf $CMSSW_BASE

## done!
echo "Exiting $0 with great success."
