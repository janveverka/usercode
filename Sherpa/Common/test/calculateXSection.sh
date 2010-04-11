sample=WgEle_0j2
version=0
CMSSW_RELEASE=CMSSW_3_5_6_path1

# cd /tmp/veverka
cmsrel $CMSSW_RELEASE
cd $CMSSW_RELEASE/src/
cmsenv
mkdir Sherpa
cd Sherpa


rfcp $CASTOR_HOME/mc/Spring10/Sherpa/${sample}_res${version}.tgz .
tar xzvf ${sample}_res${version}.tgz
cd ${sample}/test/SherpaRun
newshr=`scramv1 tool info sherpa | grep BASE | cut -f 2 -d "="`
if [ "${SHERPA_SHARE_PATH=$}"   = "" ]; then export SHERPA_SHARE_PATH=${newshr}/share/SHERPA-MC;     fi
if [ "${SHERPA_INCLUDE_PATH=$}" = "" ]; then export SHERPA_INCLUDE_PATH=${newshr}/include/SHERPA-MC; fi
if [ "${SHERPA_LIBRARY_PATH=$}" = "" ]; then export SHERPA_LIBRARY_PATH=${newshr}/lib/SHERPA-MC;     fi
sherpaexe=`find ${newshr} -type f -name Sherpa`
cat > Analysis.dat <<EOF
BEGIN_ANALYSIS {
  LEVEL Hadron;
  PATH_PIECE Norm/;
  Statistics FinalState;
} END_ANALYSIS;
EOF
$sherpaexe ANALYSIS=1 ANALYSIS_OUTPUT=Analysis_1/ EVENTS=1000 "RANDOM_SEED=55 134"
tail Analysis_*/Norm/Stat*