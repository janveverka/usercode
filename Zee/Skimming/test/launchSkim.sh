cmsRun patSkim_cfg.py print \
    isAOD=True inputFiles_clear \
    inputFiles_load=files_DoubleElectron_Run2011A-Apr22ReReco-v2_AOD.txt \
    isRealData=True \
    skimType=Dielectron \
    globalTag=GR_R_311_V2::All \
    hltProcessName=HLT \
    wantSummary=True \
    outputFile=data/skim_v3 \
    maxEvents=1000 \
    reportEvery=1