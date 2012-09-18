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
cvs co -d Vgamma/Analysis/scripts \
    UserCode/JanVeverka/Vgamma/Analysis/scripts/setup.sh
RTAG=HEAD
source $CMSSW_BASE/src/Vgamma/Analysis/scripts/setup.sh
# cp /afs/cern.ch/user/v/veverka/work/data/Vgamma2011/test/WJets_mmgSkim_test.root \
#  /tmp/$(whoami)

---+ Go to Permanent Development Area
ssh -Y lxplus5.cern.ch
bash
cd /afs/cern.ch/user/v/veverka/work/releases/CMSSW_5_2_5_ecalpatch1/src
eval $(scram runtime -sh)
cp /afs/cern.ch/user/v/veverka/work/data/Vgamma2011/test/WJets_mmgSkim_test.root \
  /tmp/$(whoami)
cd $CMSSW_BASE/src/Vgamma/Analysis/test

---+ Test the Analysis
cd $CMSSW_BASE/src/Vgamma/Analysis/test
analyze-vgamma vg_test_cfg.py
root -l vg_test.root
