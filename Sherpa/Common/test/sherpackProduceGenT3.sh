## Customize this part
job=${0:-WgMu_0j}
CMSSW_RELEASE=CMSSW_3_5_6_patch1

# create working area
WORK_BASE=/wntmp/veverka/`basename $0`/$RANDOM
mkdir -p $WORK_BASE
cd $WORK_BASE

# create a new release
source $HOME/bat/setup-afs-cmssw-slc5.sh
scramv1 project CMSSW $CMSSW_RELEASE
cd $CMSSW_RELEASE/src/
eval `scramv1 runtime -sh`

PROJECT=Sherpa
PACKAGE=$job
PROCESS_NAME=$job
NUM_EVENTS=100

## Make the project area
mkdir -p $CMSSW_BASE/src/$PROJECT/$PACKAGE/test
cd !$

## Get the sherpack
SHERPA_T3_PATH=/mnt/hadoop/user/veverka/mc/Spring10/Sherpa
cp $SHERPA_T3_PATH/sherpacks/test/sherpa_${PROCESS_NAME}_MASTER.tgz .

## Prepare the sherpack
tar xzf sherpa_${PROCESS_NAME}_MASTER.tgz
mkdir ../python
mv sherpa_custom.py ../python/
mv sherpa_${PROCESS_NAME}_cff.py ../python/

## Update python symlinks
cd ..
scramv1 b
cd test

# Run!
cmsDriver.py $PROJECT/$PACKAGE/sherpa_${PROCESS_NAME}_cff.py -s GEN \
  --conditions START3X_V25::All --datatier GEN-SIM-RAW --eventcontent RAWSIM \
  --customise $PROJECT/$PACKAGE/sherpa_custom.py -n $NUM_EVENTS --no_exec \
  --fileout outputGEN.root
cmsRun sherpa_${PROCESS_NAME}_cff_py_GEN.py

## Store the output.
OUTPUT_PATH=$SHERPA_T3_PATH/GEN/$job
if [[ ! -d $OUTPUT_PATH ]]; then
  mkdir -p $OUTPUT_PATH
fi
OUTPUT_VERSION=1
OUTPUT_NAME=outputGEN_${OUTPUT_VERSION}.root
while ls $OUTPUT_PATH/$OUTPUT_NAME >& /dev/null; do
  ((OUTPUT_VERSION++))
  OUTPUT_NAME=outputGEN_${OUTPUT_VERSION}.root
done
cp outputGEN.root $OUTPUT_PATH/$OUTPUT_NAME
