# cmsDriver.py SingleGammaPt35_cfi.py \
#    -s GEN:ProductionFilterSequence,SIM,DIGI,L1,DIGI2RAW,HLT \
#    --conditions GlobalTag,MC_31X_V1::All \
#    --datatier 'GEN-SIM-RAW' \
#    --eventcontent RAWSIM \
#    -n 10 \
#    --no_exec

cmsDriver.py SingleGammaPt60_cfi.py \
    -s GEN,FASTSIM,HLT:GRun \
    --pileup=NoPileUp \
    --geometry DB \
    --conditions=auto:mc \
    --eventcontent=FEVTSIM \
    --datatier GEN-SIM-DIGI-RECO \
    -n 100 \
    --fileout file:fastsim.root \
    --no_exec
