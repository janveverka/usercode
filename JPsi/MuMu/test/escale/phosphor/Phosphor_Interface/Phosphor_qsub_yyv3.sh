#!/bin/sh

QSUBDIR=/home/cmorgoth/phosphor/CMSSW_4_2_8_patch7/src/JPsi/MuMu/test/escale/phosphor/Phosphor_Interface/QsubScripts_sixie2


NEWDIR=`date | gawk '{ print $1 $2 $3"_" $6 }'`
RESULTS=sixie2
LOGS=sixie2_log

if [ -d $NEWDIR ]; then
	echo "DIR $NEWDIR exists."
	if [ -d $NEWDIR/$RESULTS ]; then
		echo "DIR $NEWDIR/$RESULTS exists."
	else
		mkdir $NEWDIR/$RESULTS
		echo "Creating DIR: $NEWDIR/$RESULTS."
	fi

	if [ -d $NEWDIR/$LOGS ]; then
		echo "DIR $NEWDIR/$LOGS exists."
	else
		mkdir $NEWDIR/$LOGS
		echo "Creating DIR: $NEWDIR/$LOGS."
	fi

		
else
	mkdir $NEWDIR
	echo "Creating DIR: $NEWDIR."
	mkdir $NEWDIR/$RESULTS
	echo "Creating DIR: $NEWDIR/$RESULTS."
	mkdir $NEWDIR/$LOGS
	echo "Creating DIR: $NEWDIR/$LOGS."
fi


for qfiles in $QSUBDIR/*.sge; do
    pwd; echo $qfiles; SGEFILE=$qfiles; echo $SGEFILE    
    if [ -a $SGEFILE ] 
	then 
	echo "QSUB"
	#qsub -j y -o `pwd` -q all.q $SGEFILE;
	#qsub -j y -o `pwd` -q all.q@compute-1-6.local,all.q@compute-0-1.local,all.q@compute-0-3.local,all.q@compute-1-7.local,all.q@compute-1-8.local,all.q@compute-1-9.local,all.q@compute-0-14.local,all.q@compute-0-2.local,all.q@compute-0-4.local,all.q@compute-0-6.local $SGEFILE;
	
	#qsub -j y -o `pwd` -q all.q@compute-1-5.local,all.q@compute-1-8.local,all.q@compute-1-9.local,all.q@compute-1-6.local,all.q@compute-1-0.local  $SGEFILE;
	qsub -j y -o $NEWDIR/$LOGS -q all.q@compute-1-6 $SGEFILE  -- $NEWDIR/$RESULTS;
	#sdfdf

    else

	echo "FILE $SGEFILE DOES NOT EXIT, DOING NOTHING"
    fi
    #cd $INITIALTOPDIR;
done



