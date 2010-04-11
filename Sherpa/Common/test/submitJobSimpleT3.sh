EXECUTABLE=${1}

function print_help() {
  echo "usage: $0 <executable> [<stdout path> [<stderr path>]]"
}

## Fix input parameters
if [[ -z $EXECUTABLE ]]; then
  print_help && exit
fi

if [[ -z $STDOUT_PATH ]]; then
  STDOUT_PATH=$PWD
fi

if [[ -z $STDERR_PATH ]]; then
  STDERR_PATH=$STDOUT_PATH
fi

# Get a unique job name
JOB_NUMBER=1
JOB=`basename $EXECUTABLE`
JOB=${JOB%*.*}_job${JOB_NUMBER}.sh
while ls $JOB >& /dev/null; do
  ((JOB_NUMBER++))
  JOB=`basename $EXECUTABLE`
  JOB=${JOB%*.*}_job${JOB_NUMBER}.sh
done

cat > $JOB << END_OF_HERE_DOCUMENT
#!/bin/sh
#
# request Bourne shell as shell for job
#$ -S /bin/sh
#$ -e $STDERR_PATH
#$ -o $STDOUT_PATH

$@
END_OF_HERE_DOCUMENT

## Submit the job
qsub $JOB