## Customize this part
SAMPLE=${1:-WgEle_0j}
VERSION=3
CMSSW_RELEASE=CMSSW_3_5_6_patch1

# create working area
WORK_BASE=/wntmp/veverka/`basename $0`/$RANDOM
mkdir -p $WORK_BASE
cd $WORK_BASE

# create a new release
source $HOME/bin/setup-afs-cmssw-slc5.sh
scramv1 project CMSSW $CMSSW_RELEASE
cd $CMSSW_RELEASE/src/
eval `scramv1 runtime -sh`
mkdir Sherpa
cd Sherpa


SHERPA_T3_PATH=/mnt/hadoop/user/veverka/mc/Spring10/Sherpa
cp $SHERPA_T3_PATH/libs/${SAMPLE}_res${VERSION}.tgz .
tar xzf ${SAMPLE}_res${VERSION}.tgz
cd ${SAMPLE}/test/SherpaRun
SHERPA_BASE_PATH=`scramv1 tool info sherpa | grep BASE | cut -f 2 -d "="`
if [ "${SHERPA_SHARE_PATH=$}"   = "" ]; then
  export SHERPA_SHARE_PATH=${SHERPA_BASE_PATH}/share/SHERPA-MC;
fi
if [ "${SHERPA_INCLUDE_PATH=$}" = "" ]; then
  export SHERPA_INCLUDE_PATH=${SHERPA_BASE_PATH}/include/SHERPA-MC;
fi
if [ "${SHERPA_LIBRARY_PATH=$}" = "" ]; then
  export SHERPA_LIBRARY_PATH=${SHERPA_BASE_PATH}/lib/SHERPA-MC;
fi
SHERPA_EXE=`find ${SHERPA_BASE_PATH} -type f -name Sherpa`
cat > Analysis.dat <<EOF
BEGIN_ANALYSIS {
  LEVEL Hadron;
  PATH_PIECE Norm/;
  Statistics FinalState;
} END_ANALYSIS;
EOF
ln -s ../MIG*
$SHERPA_EXE ANALYSIS=1 ANALYSIS_OUTPUT=Analysis_1/ EVENTS=1000 "RANDOM_SEED=$RANDOM $RANDOM"
tail Analysis_*/Norm/Stat*

## Store output.
OUTPUT_PATH=$SHERPA_T3_PATH/xsections
OUTPUT_VERSION=1
OUTPUT_NAME=xsec_${SAMPLE}_lib${VERSION}_${OUTPUT_VERSION}.dat
while ls $OUTPUT_PATH/$OUTPUT_NAME >& /dev/null; do
  ((OUTPUT_VERSION++))
  OUTPUT_NAME=xsec_${SAMPLE}_lib${VERSION}_${OUTPUT_VERSION}.dat
done
cp Analysis_*/Norm/Stat* $OUTPUT_PATH/$OUTPUT_NAME