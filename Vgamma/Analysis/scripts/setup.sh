## Recipe to check out and compile the Caltech Vgamma analysis code
## Assumes BASH and CMSSW_5_2_x environment.
## USAGE: source setup.sh
## Jan Veverka, Caltech, 15 September 2012
RTAG=${RTAG:-HEAD}
cd $CMSSW_BASE/src && \
    cvs co -r $RTAG -d Vgamma/Analysis \
        UserCode/JanVeverka/Vgamma/Analysis && \
    scramv1 build -j4
