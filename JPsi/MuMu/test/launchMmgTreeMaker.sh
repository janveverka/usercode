DATASET=DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia
TOTALSECTIONS=8
SECTION=3
for SECTION in `seq $TOTALSECTIONS`; do
  nohup cmsRun makeMuMuGammaTree_cfg.py print \
    datasetPath=/mnt/hadoop/user/veverka/DimuonVGammaSkim_v3/ \
    dataset=$DATASET \
    maxEvents=-1 \
    isMC=yes \
    globalTag=START38_V12::All \
    totalSections=$TOTALSECTIONS \
    section=$SECTION \
  >& mmgTree_${DATASET}_${SECTION}of${TOTALSECTIONS}.out &
done

DATASET=Mu
TOTALSECTIONS=8
SECTION=3
for SECTION in `seq $TOTALSECTIONS`; do
  nohup cmsRun makeMuMuGammaTree_cfg.py print \
    datasetPath=/mnt/hadoop/user/veverka/DimuonVGammaSkim_v3/ \
    dataset=$DATASET \
    maxEvents=-1 \
    isMC=no \
    globalTag=FT_R_38X_V14A::All \
    jsonFile=Cert_136033-149442_7TeV_Nov4ReReco_Collisions10_JSON.txt \
    totalSections=$TOTALSECTIONS \
    section=$SECTION \
  >& mmgTree_${DATASET}_${SECTION}of${TOTALSECTIONS}.out &
done