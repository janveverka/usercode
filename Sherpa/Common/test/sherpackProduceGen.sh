job=${1:-WgEle_0j}
CMSSW_RELEASE=CMSSW_3_5_6
LIB_VERSION=3
NUM_EVENTS=10000

#### setup CMSSW release area
scramv1 project CMSSW $CMSSW_RELEASE
cd $CMSSW_RELEASE/src
eval `scramv1 ru -sh`

#### Make the project area
PROJECT=Sherpa
PACKAGE=$job
PROCESS_NAME=$job
mkdir -p $CMSSW_BASE/src/$PROJECT/$PACKAGE/test
cd $CMSSW_BASE/src/$PROJECT/$PACKAGE/test

#### Get the sherpack 
SHERPACK_DIR=sherpacks/test_lib${LIB_VERSION}
SHERPACK=sherpa_${PROCESS_NAME}_MASTER.tgz

## From the T3
T3_PATH=/mnt/hadoop/user/veverka/mc/Spring10/Sherpa
SHERPACK_T3_DIR=$T3_PATH/$SHERPACK_DIR
# scp t3-susy.ultralight.org:$SHERPACK_T3_DIR/$SHERPACK .

## From CASTOR
CASTOR_PATH=$CASTOR_HOME/mc/Spring10/Sherpa
SHERPACK_CASTOR_DIR=$CASTOR_PATH/$SHERPACK_DIR
# rfcp $SHERPACK_CASTOR_DIR/$SHERPACK .

## From AFS
AFS_PATH=/afs/cern.ch/cms/cit/veverka/data/mc/Spring10/Sherpa
SHERPACK_AFS_DIR=$AFS_PATH/$SHERPACK_DIR
cp $SHERPACK_AFS_DIR/$SHERPACK .

if [[ ! -f $SHERPACK ]]; then
  echo "Failed to get $SHERPACK" && \
  echo "Exiting."
fi

#### Prepare the sherpack
tar xzf $SHERPACK
ls -l ## debug
if [[ ! -d ../python ]]; then mkdir ../python; fi
mv sherpa_custom.py sherpa_${PROCESS_NAME}_cff.py ../python/

#### Update python symlinks
cd ..
scramv1 b
cd test

#### Run!
cmsDriver.py $PROJECT/$PACKAGE/sherpa_${PROCESS_NAME}_cff.py -s GEN \
  --conditions START3X_V25::All --datatier GEN-SIM-RAW --eventcontent RAWSIM \
  --customise $PROJECT/$PACKAGE/sherpa_custom.py \
  -n $NUM_EVENTS --no_exec \
  --fileout outputGEN.root \
  2>&1 | tee -a outputGEN.log
ls -l ## debug
cmsRun sherpa_${PROCESS_NAME}_cff_py_GEN.py \
  2>&1 | tee -a outputGEN.log

#### Store the output
OUTPUT_DIR=$job/GEN/sherpack_lib${LIB_VERSION}

## Prepare the T3 output path
T3_OUTPUT_PATH=$T3_PATH/$OUTPUT_DIR
T3_URL=t3-susy.ultralight.org
if ! ssh $T3_URL ls $T3_OUTPUT_PATH >& /dev/null; then
  ssh $T3_URL mkdir -p $T3_OUTPUT_PATH
fi

## Prepare the CASTOR ouput path
CASTOR_OUTPUT_PATH=$CASTOR_PATH/$OUTPUT_DIR
if ! nsls $CASTOR_OUTPUT_PATH >& /dev/null; then
  rfmkdir -p $CASTOR_OUTPUT_PATH
fi

## Prepare the AFS output path
AFS_OUTPUT_PATH=$AFS_PATH/$OUTPUT_DIR
if ! ls $AFS_OUTPUT_PATH >& /dev/null; then
  mkdir -p $AFS_OUTPUT_PATH
fi

## Get a unique and common output name
OUTPUT_VERSION=1
OUTPUT_NAME=outputGEN_${OUTPUT_VERSION}.root
while nsls $CASTOR_OUTPUT_PATH/$OUTPUT_NAME >& /dev/null \
  || ssh $T3_URL ls $T3_OUTPUT_PATH/$OUTPUT_NAME >& /dev/null \
  || ls $AFS_OUTPUT_PATH/$OUTPUT_NAME >& /dev/null; do
  ((OUTPUT_VERSION++))
  OUTPUT_NAME=outputGEN_${OUTPUT_VERSION}.root
done

## Store the output.
echo "Storing $CASTOR_OUTPUT_PATH/$OUTPUT_NAME"
rfcp outputGEN.root $CASTOR_OUTPUT_PATH/$OUTPUT_NAME

# echo "Storing $T3_URL:$T3_OUTPUT_PATH/$OUTPUT_NAME"
# scp outputGEN.root $T3_URL:$T3_OUTPUT_PATH/$OUTPUT_NAME

# echo "Storing $AFS_OUTPUT_PATH/$OUTPUT_NAME"
# cp outputGEN.root $AFS_OUTPUT_PATH/$OUTPUT_NAME

## Prepare the log.
mkdir log_${OUTPUT_VERSION}
mv *.log *.py ../python/*.py MIG* *.dat */Run.dat log_${OUTPUT_VERSION}
tar czf log.tgz log_${OUTPUT_VERSION} 
LOG_NAME=log_${OUTPUT_VERSION}.tgz

## Store the log.
echo "Storing $CASTOR_OUTPUT_PATH/$LOG_NAME"
rfcp log.tgz $CASTOR_OUTPUT_PATH/$LOG_NAME

# echo "Storing $T3_URL:$T3_OUTPUT_PATH/$LOG_NAME"
# scp log.tgz $T3_URL:$T3_OUTPUT_PATH/$LOG_NAME

# echo "Storing $AFS_OUTPUT_PATH/$LOG_NAME"
# rfcp log.tgz $AFS_OUTPUT_PATH/$LOG_NAME

#### Done!
echo "Exiting $0 with great success"'!'
