---+ Introduction
This package contains software for the Caltech Zg->mmg analysis 
and needs the CMSSW FWLite.

---+ Setup Development Area
ssh -Y lxplus5.cern.ch
bash
cd $(mktemp -d -p /tmp/$(whoami))
export SCRAM_ARCH=slc5_amd64_gcc462
scram project CMSSW CMSSW_5_2_6
cd CMSSW_5_2_6/src
eval $(scram runtime -sh)
cvs co -d . UserCode/JanVeverka/Vgamma/Analysis/scripts/setup.sh
RTAG=HEAD
source $CMSSW_BASE/src/Vgamma/Analysis/scripts/setup.sh
