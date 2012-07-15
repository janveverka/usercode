## Here is an example of commands for bash on LXPLUS that create the directory 
## $DESTINATION on EOS and then copy there all the root files from the local 
## directory $SRCDIR
## 
## USAGE: Customize the defintions of SRCDIR and DESTINATION and then
##        copy and paste line by line in the terminal with bash on LXPLUS.

DATASET=veverka-Run2011B-ZMu-PromptSkim-v1_ZmmgSkim_11Jul2012ReReco-34c7662f33afe9c365c1014c516a8097_FNAL_RecoAnalyzerV00-00-02b
SRCDIR=/tmp/veverka/$DATASET/v1
DESTINATION=/store/group/alca_ecalcalib/veverka/DoubleMu/$DATASET/v1
echo "eos mkdir -p $DESTINATION"
eos mkdir -p $DESTINATION
for f in $(ls $SRCDIR/*.root); do
    C="cmsStage $f $DESTINATION" 
    echo $C
    echo 
    eval $C
done
