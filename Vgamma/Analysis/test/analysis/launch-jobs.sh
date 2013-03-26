## All jobs
# JOBS_TO_LAUNCH="data zg2jmg5 zjets ttbar wjets qcd ww wz zz"
## MC only
# JOBS_TO_LAUNCH="zg2jmg5 zjets ttbar wjets qcd ww wz zz"
## Custom list
JOBS_TO_LAUNCH="ww wz zz"
for JOB in $JOBS_TO_LAUNCH; do
    vg-analyze ${JOB}_cfg.py >& ${JOB}.log &
done

ps ux | grep vg-analyze | grep -v grep
