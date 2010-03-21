# init
name=Zg

# cleanup
todelete=`ls -d *.tgz *.log *.dat *.sh *.py *.root SHERPATMP SherpaRun MIG* 2>/dev/null`
echo "deleting `echo $todelete| tr '\n' ' '`"
for i in $todelete; do
	# echo deleting $i
	if [ -d $i ]; then rm -r $i
	else rm $i;	fi
done

# step 1
base=$CMSSW_BASE/src/Sherpa/Template/test
cp $base/Run_${name}.dat Run.dat
tar -czf sherpa_${name}_cards.tgz Run.dat
cp $base/MakeSherpaLibs.sh .
(time nohup ./MakeSherpaLibs.sh  -i ./ -p $name) >& run1.log &
tail -f run1.log

# step 2
base=$CMSSW_BASE/src/Sherpa/Template/test
name=$(ls sherpa*cards.tgz | awk -F_ '{print $2}')
cp $base/PrepareSherpaLibs.sh .
path=$(pwd | tr '/' '\n' | tail -3 | head -2 | tr '\n' ' ' | awk '{print $1 "/" $2}')
(time ./PrepareSherpaLibs.sh -d $CMSSW_BASE -i ./ -p $name -a $path -m LOCAL) >& run2.log &
tail -f run2.log

# step 3
cat >> sherpa_cfg.py <<EOF
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    moduleSeeds = cms.PSet(generator = cms.untracked.uint32(3310)),
    sourceSeed = cms.untracked.uint32(123456)
)
EOF
(time nohup cmsRun sherpa_cfg.py) >& run3.log &
tail -f run3.log
