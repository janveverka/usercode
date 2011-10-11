## Source this file on lxplus5.cern.ch to reproduce plots
## of EBDetId fiducial flags.
cd /tmp/`whoami`
cd `mktemp -d -p .`
cmsrel CMSSW_4_2_8
cd CMSSW_4_2_8/src/
cmsenv
cvs co -d Misc/Random UserCode/JanVeverka/Misc/Random
python -i Misc/Random/test/check_fiducial_flags.py 
