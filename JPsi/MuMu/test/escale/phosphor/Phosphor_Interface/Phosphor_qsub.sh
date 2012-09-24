#!/bin/sh

INITIALTOPDIR=`pwd`

for idir in RPVgluinodir_M_*; do
    cd $idir; pwd; SGEFILE=`ls -1 | grep '\.sge'`; echo $SGEFILE    
    if [ -a NuclearInteractionOutputFile.txt ] 
	then 
	echo "nothing"
    else
	echo "qsub"
	#qsub -j y -o `pwd` -q all.q $SGEFILE;
	qsub -j y -o `pwd` -q all.q@compute-0-1.local,all.q@compute-0-3.local,all.q@compute-1-6.local,all.q@compute-1-7.local,all.q@compute-1-8.local,all.q@compute-1-9.local,all.q@compute-0-14.local,all.q@compute-0-2.local,all.q@compute-0-4.local,all.q@compute-0-6.local   $SGEFILE;
    fi
    cd $INITIALTOPDIR;
done



