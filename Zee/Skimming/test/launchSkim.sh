# cmsRun patSkim_cfg.py print \
#     isAOD=True inputFiles_clear \
#     inputFiles_load=files_DoubleElectron_Run2011A-Apr22ReReco-v2_AOD.txt \
#     isRealData=True \
#     skimType=Dielectron \
#     globalTag=GR_R_311_V2::All \
#     hltProcessName=HLT \
#     wantSummary=True \
#     outputFile=data/skim_v3 \
#     maxEvents=1000 \
#     reportEvery=1

cmsRun patSkim_cfg.py print \
    isAOD=True inputFiles_clear \
    inputFiles_load=files_ZeeSpring11.txt \
    isRealData=False \
    skimType=Dielectron \
    globalTag=START311_V2::All \
    hltProcessName=REDIGI311X \
    wantSummary=True \
    outputFile=test_mc \
    outEvents=10 \
    reportEvery=1 \
    >& test_mc.out &

