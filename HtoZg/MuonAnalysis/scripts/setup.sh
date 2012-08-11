## Recipe to check out and compile the Caltech HtoZg analysis cod
## Assumes BASH and CMSSW_5_2_x environment.
## USAGE: source $CMSSW_BASE/src/HtoZg/MuonAnalysis/scripts/setup.sh
## Jan Veverka, Caltech, 8 August 2012

# RTAG=HtoZg_sync_2012_cutbased_muons_uptoId
# RTAG=HtoZg_sync_2012_cutbased_muons_uptoPhotonId
RTAG=HtoZg_sync_2012_cutbased_muons_round1
# RTAG=HEAD
cd $CMSSW_BASE/src && \
    cvs co -r $RTAG -d HtoZg/CommonAnalysis \
        UserCode/JanVeverka/HtoZg/CommonAnalysis && \
    cvs co -r $RTAG -d HtoZg/MuonAnalysis \
        UserCode/JanVeverka/HtoZg/MuonAnalysis && \
    cvs co -r $RTAG -d Misc/TreeMaker \
        UserCode/JanVeverka/Misc/TreeMaker && \
    cvs co -D 8/8/12 -d Muon/MuonAnalysisTools \
        UserCode/sixie/Muon/MuonAnalysisTools && \
    cvs co -r V00-00-21 -d EGamma/EGammaAnalysisTools \
        UserCode/EGamma/EGammaAnalysisTools && \
    cvs up -r 1.13 \
        EGamma/EGammaAnalysisTools/interface/PFIsolationEstimator.h && \
    cvs up -r 1.22 \
        EGamma/EGammaAnalysisTools/src/PFIsolationEstimator.cc && \
    scramv1 build -j4
