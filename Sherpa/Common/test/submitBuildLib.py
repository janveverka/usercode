## Customize this part
maxJets = 3
# vbosons = ["W", "Z"]
vdecays = {"W" : ["Ele", "Mu", "Tau"],
           "Z" : ["Ele", "Mu", "Tau", "Nu"] }
#vbosons = ["W"]
#vdecays = {"W": ["Lep", "Tau"]}
#queueForNJets = {0:"1nh80", 1:"1nh80", 2:"1nw80", 3:"2nw", 4:"2nw"}
queueForNJets = {0:"cmscaf1nh", 1:"cmscaf1nh", 2:"cmscaf1nw", 3:"cmscaf1nw", 4:"2nw"}
jobFile = "buildLibs.sh"

## Some initialization
import os
# get absolute path to the job file
jobFile = os.getcwd() + "/" + jobFile

## produce the submission commands for Vgamma
for vboson in vdecays.keys():
  for decay in vdecays[vboson]:
    for njets in range(maxJets+1):
      if not njets:
        job = "%sg%s_0j" % (vboson, decay, )
      else:
        job = "%sg%s_0j%d" % (vboson, decay, njets)
      print "bsub -q %5s %s %s" % (queueForNJets[njets], jobFile, job)


