PROJECT=Sherpa
PACKAGE=$job
PROCESS_NAME=$job
NUM_EVENTS=100

cmsDriver.py $PROJECT/$PACKAGE/sherpa_${PROCESS_NAME}_cff.py -s GEN \
  --conditions START3X_V25::All --datatier GEN-SIM-RAW --eventcontent RAWSIM \
  --customise $PROJECT/$PACKAGE/sherpa_custom.py -n $NUM_EVENTS --no_exec \
  --fileout outputGEN.root
cmsRun sherpa_${PROCESS_NAME}_cff_py_GEN.py