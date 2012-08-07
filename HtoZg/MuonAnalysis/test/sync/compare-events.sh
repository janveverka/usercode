EVENTLIST=$(cat events_unique_caltech.txt)
FILE1=muonDump1_ZJets.txt
FILE2=caltech.txt
grep pt $FILE1 | cut -d ' ' -f 2-
for E in $EVENTLIST:
    echo '==='
    grep $E $FILE1 | cut -d ' ' -f 2-
    echo '---'
    grep $E $FILE2 | cut -d ' ' -f 4-
  

  