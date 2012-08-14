## Recipe to check out and compile the Caltech HtoZg analysis cod
## Assumes BASH and CMSSW_5_2_x environment.
## USAGE: RTAG=HtoZg_42x; $CMSSW_BASE/src/HtoZg/MuonAnalysis/scripts/setup.sh
## Jan Veverka, Caltech, 8 August 2012

# RTAG=HtoZg_sync_2012_cutbased_muons_uptoId
# RTAG=HtoZg_sync_2012_cutbased_muons_uptoPhotonId
# RTAG=HtoZg_sync_2012_cutbased_muons_round1
# RTAG=HtoZg_sync_2012_cutbased_muons_round2
# RTAG=HtoZg_42x
# RTAG=V42-00-01 ## Compiles in 42x
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
    ## The tagged version doesn't compile in 42x. Downgrade it to an
    ## an older one that seems to work.
    cvs up -r 1.2 \
        EGamma/EGammaAnalysisTools/test/ElectronIsoAnalyzer.cc && \
    ## Custom single-level H/E calculation backported to 42x
    ## https://twiki.cern.ch/twiki/bin/view/CMS/HoverE2012
    addpkg RecoEgamma/EgammaElectronAlgos && \
    cvs up -r CMSSW_5_2_2 \
        RecoEgamma/EgammaElectronAlgos/src/ElectronHcalHelper.cc \
        RecoEgamma/EgammaElectronAlgos/interface/ElectronHcalHelper.h && \
    cvs co -r CMSSW_5_2_2 RecoEgamma/EgammaIsolationAlgos && \
    ## Compile all the packages
    scramv1 build -j4

