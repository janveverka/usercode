PROJECT=Sherpa
PACKAGE=WgEle_0j2
PROCESS_NAME=WgEle_0j2
NUM_EVENTS=1

#step1
cmsDriver.py  $PROJECT/$PACKAGE/sherpa_${PROCESS_NAME}_cff.py \
  -s GEN,SIM,DIGI,L1,DIGI2RAW,HLT --conditions START3X_V25::All \
  --datatier GEN-SIM-RAW --eventcontent RAWSIM  \
  --customise $PROJECT/$PACKAGE/sherpa_custom.py -n $NUM_EVENTS --no_exec \
  --fileout outputGENDIGIHLT.root
cmsRun sherpa_${PROCESS_NAME}_cff_py_GEN_SIM_DIGI_L1_DIGI2RAW_HLT.py

#step2
cmsDriver.py step2 -s RAW2DIGI,RECO --conditions START3X_V25::All \
  --datatier GEN-SIM-RECO --eventcontent RECOSIM -n $NUM_EVENTS --no_exec \
  --filein file:outputGENDIGIHLT.root
cmsRun step2_RAW2DIGI_RECO.py