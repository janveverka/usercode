## All jobs
# JOBS_TO_LAUNCH="mm2011AB zmmg zjets ttbar wjets qcd20m ww wz zz"

## MC only
# JOBS_TO_LAUNCH="zmmg zjets ttbar wjets qcd20m ww wz zz"

## Custom list
JOBS_TO_LAUNCH="ww wz zz"
for JOB in $JOBS_TO_LAUNCH; do
    vg-analyze ${JOB}_cfg.py >& ${JOB}.log &
done

ps ux | grep vg-analyze | grep -v grep
