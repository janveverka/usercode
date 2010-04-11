## Customize this part
CMSSW_RELEASE=CMSSW_3_5_6

# create working area
WORK_BASE=/wntmp/veverka/$RANDOM
mkdir -p $WORK_BASE
cd $WORK_BASE

# create a new release
source $HOME/bat/setup-local-cmssw-slc5.sh
scramv1 project CMSSW $CMSSW_RELEASE
cd $CMSSW_RELEASE/src/
eval `scramv1 runtime -sh`
