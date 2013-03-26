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
vg-analyze vg_test_cfg.py
root -l vg_test.root

---+ Run Unit Tests
vg-run-unit-tests

---+ Debugging with GDB
Compile with debugging information:
scram b clean
scram b USER_CXXFLAGS="-ggdb\ -Wall" Vgamma/Analysis
Quick gdb tutorial:
http://www.cs.cmu.edu/~gilpin/tutorial/
Run vg-analyze in gdb with the vg_test_cfg.py config as an argument:
gdb --args vg-analyze vg_test_cfg.py
(gdb) run
Set Breakpoint:
(gdb) break cit::VgEventSelector::operator()
Step through lines:
(gdb) step
Step through lines without entering called functions:
(gdb) next
Quit:
(gdb) quit

---+ Make the Data/MC Plots (Experimental)
cd $CMSSW_BASE/src/Vgamma/Analysis/test/analysis
. launch-jobs.sh
## Make sure all jobs finish
. ../make-data-mc-plots.sh
