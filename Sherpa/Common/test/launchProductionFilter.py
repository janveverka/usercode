vdecays = {"W" : ["Ele", "Mu", "Tau", "Lep"],
           "Z" : ["Ele", "Mu", "Nu"] }
nJets=3
nJobs=10
maxEvents=1000
queue="1nd"

for v in vdecays.keys():
  if v=="W":
    continue
  for d in vdecays[v]:
    if (nJets==3 and v=="Z" and d=="EleMu") \
    or (nJets==2 and v=="Z" and d=="Nu"):
      continue
    jobname = "%sg%s_0j%d" % (v, d, nJets)
    print "for JOB_NUMBER in `seq %d`; do bsub -q %s `pwd`/batchJobProductionFilter.sh %s $JOB_NUMBER %d; done" % (nJobs, queue, jobname, maxEvents)

