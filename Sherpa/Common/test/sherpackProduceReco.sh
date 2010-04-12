job=${1:-WgEle_0j}
CMSSW_RELEASE=CMSSW_3_5_6
LIB_VERSION=3
NUM_EVENTS=100

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

#### Set Sherpa paths
AFS_PATH=/afs/cern.ch/cms/cit/veverka/data/mc/Spring10/Sherpa
CASTOR_PATH=$CASTOR_HOME/mc/Spring10/Sherpa
T3_PATH=/mnt/hadoop/user/veverka/mc/Spring10/Sherpa

#### Get the sherpack
SHERPACK=sherpa_${PROCESS_NAME}_MASTER.tgz
SHERPACK_DIR=sherpacks/test_lib${LIB_VERSION}

## From the T3
SHERPACK_T3_DIR=$T3_PATH/$SHERPACK_DIR
# scp t3-susy.ultralight.org:$SHERPACK_T3_DIR/$SHERPACK .

## From CASTOR
SHERPACK_CASTOR_DIR=$CASTOR_PATH/$SHERPACK_DIR
# rfcp $SHERPACK_CASTOR_DIR/$SHERPACK .

## From AFS
SHERPACK_AFS_DIR=$AFS_PATH/$SHERPACK_DIR
cp $SHERPACK_AFS_DIR/$SHERPACK .

## Did we get it?
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

###############################################################################
###### Step 2
###############################################################################

#### Run!
## Make the config file
cmsDriver.py  $PROJECT/$PACKAGE/sherpa_${PROCESS_NAME}_cff.py \
  -s GEN,SIM,DIGI,L1,DIGI2RAW,HLT --conditions START3X_V25::All \
  --datatier GEN-SIM-RAW --eventcontent RAWSIM  \
  --customise=Validation/Performance/TimeMemoryInfo.py \
  -n $NUM_EVENTS --no_exec \
  --fileout outputGENDIGIHLT.root

## Some extra gymnastics to workaround not being able to use
## +two customization files
#   --customise=$PROJECT/$PACKAGE/sherpa_custom.py \
STEP1_CFG=sherpa_${PROCESS_NAME}_cff_py_GEN_SIM_DIGI_L1_DIGI2RAW_HLT.py
cat >> $STEP1_CFG << END_HERE
process.genParticles.abortOnUnknownPDGCode = False
END_HERE

## Here we go!
cmsRun  $STEP1_CFG 2>&1 | tee -a step1.log

#### Store the step1 output on the T3, AFS and CASTOR
OUTPUT_DIR=$job/RAWSIM/sherpack_lib${LIB_VERSION}

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
OUTPUT_NAME=outputGENDIGIHLT_${OUTPUT_VERSION}.root
while nsls $CASTOR_OUTPUT_PATH/$OUTPUT_NAME >& /dev/null \
  || ssh $T3_URL ls $T3_OUTPUT_PATH/$OUTPUT_NAME >& /dev/null \
  || ls $AFS_OUTPUT_PATH/$OUTPUT_NAME >& /dev/null; do
  ((OUTPUT_VERSION++))
  OUTPUT_NAME=outputGENDIGIHLT_${OUTPUT_VERSION}.root
done

## Store the output.
echo "Storing $CASTOR_OUTPUT_PATH/$OUTPUT_NAME"
rfcp outputGENDIGIHLT.root $CASTOR_OUTPUT_PATH/$OUTPUT_NAME

# echo "Storing $T3_URL:$T3_OUTPUT_PATH/$OUTPUT_NAME"
# scp outputGEN.root $T3_URL:$T3_OUTPUT_PATH/$OUTPUT_NAME

# echo "Storing $AFS_OUTPUT_PATH/$OUTPUT_NAME"
# cp outputGENDIGIHLT.root $AFS_OUTPUT_PATH/$OUTPUT_NAME

## Store the log.
tar czf log.tgz step1.log
LOG_NAME=log_${OUTPUT_VERSION}.tgz

echo "Storing $CASTOR_OUTPUT_PATH/$LOG_NAME"
rfcp log.tgz $CASTOR_OUTPUT_PATH/$LOG_NAME

# echo "Storing $T3_URL:$T3_OUTPUT_PATH/$LOG_NAME"
# scp log.tgz $T3_URL:$T3_OUTPUT_PATH/$LOG_NAME

echo "Storing $AFS_OUTPUT_PATH/$LOG_NAME"
cp log.tgz $AFS_OUTPUT_PATH/$LOG_NAME

###############################################################################
###### Step 2
###############################################################################

#### Run!
cmsDriver.py step2 -s RAW2DIGI,RECO --conditions START3X_V25::All \
  --datatier GEN-SIM-RECO --eventcontent RECOSIM -n $NUM_EVENTS --no_exec \
  --filein file:outputGENDIGIHLT.root
cmsRun step2_RAW2DIGI_RECO.py 2>&1 | tee -a step2.log

#### Store the step2 output on the T3, AFS and CASTOR
OUTPUT_DIR=$job/RECO/sherpack_lib${LIB_VERSION}

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

## Use the same output version as in step 1!
OUTPUT_NAME=reco_${OUTPUT_VERSION}.root

## Store the output.
echo "Storing $CASTOR_OUTPUT_PATH/$OUTPUT_NAME"
rfcp step2_RAW2DIGI_RECO.root $CASTOR_OUTPUT_PATH/$OUTPUT_NAME

# echo "Storing $T3_URL:$T3_OUTPUT_PATH/$OUTPUT_NAME"
# scp step2_RAW2DIGI_RECO.root $T3_URL:$T3_OUTPUT_PATH/$OUTPUT_NAME

# echo "Storing $AFS_OUTPUT_PATH/$OUTPUT_NAME"
# cp step2_RAW2DIGI_RECO.root $AFS_OUTPUT_PATH/$OUTPUT_NAME

#### Done!
echo "Exiting $0 with great success"'!'

