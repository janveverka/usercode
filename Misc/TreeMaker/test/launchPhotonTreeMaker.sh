# DATASET=GluGluToHToGG_M-120_7TeV-powheg-pythia6_Winter10_InclusiveVGammaSkim_v4
# INPUT_FILES=files_GluGluToHToGG_M-120_7TeV-powheg-pythia6_Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1-InclusiveVGammaSkim_v4.dat

DATASET=GJets_TuneD6T_HT-40To100_7TeV-madgraph_Winter10_JetVGammaSkim_v4
INPUT_FILES=files_GJets_TuneD6T_HT-40To100_7TeV-madgraph_Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1-JetVGammaSkim_v4.dat

TOTALSECTIONS=8
# SECTION=3
# for SECTION in `seq 25 32`; do
for SECTION in `seq $TOTALSECTIONS`; do
  nohup cmsRun photonTreeMaker_cfg.py print \
    inputFiles_clear \
    inputFiles_load=$INPUT_FILES \
    maxEvents=-1 \
    reportEvery=1000 \
    outputFile=/wntmp/veverka/PhotonTree_${DATASET} \
    totalSections=$TOTALSECTIONS \
    section=$SECTION \
  >& gTree_${DATASET}_${SECTION}of${TOTALSECTIONS}.out &
done
