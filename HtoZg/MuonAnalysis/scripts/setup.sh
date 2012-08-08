## Recipe to check out and compile the Caltech HtoZg analysis cod
## Assumes BASH and CMSSW_5_2_x environment.
## USAGE: source $CMSSW_BASE/src/HtoZg/MuonAnalysis/scripts/setup.sh
## Jan Veverka, Caltech, 8 August 2012

RTAG=HEAD
cd $CMSSW_BASE/src && \
    cvs co -r $RTAG -d HtoZg/CommonAnalysis \
        UserCode/JanVeverka/HtoZg/CommonAnalysis && \
    cvs co -r $RTAG -d HtoZg/MuonAnalysis \
        UserCode/JanVeverka/HtoZg/MuonAnalysis && \
    cvs co -r $RTAG -d Misc/TreeMaker \
        UserCode/JanVeverka/Misc/TreeMaker && \
    cvs co -D 8/8/12 -d Muon/MuonAnalysisTools \
        UserCode/sixie/Muon/MuonAnalysisTools && \
    scramv1 build -j4
