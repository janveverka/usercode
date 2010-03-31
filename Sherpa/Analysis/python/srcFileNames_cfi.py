castorDir = "/castor/cern.ch/user/v/veverka/mc/Spring10/Sherpa"

standardList=[]
standardList100=[]
standardList200=[]
standardList500=[]
standardList1000=[]
for i in range(10):
  standardList += [ "sherpa_out_10000evts_job%d.root" % (i+1,) ]
  standardList100 += [ "sherpa_out_100evts_job%d.root" % (i+1,) ]
  standardList200 += [ "sherpa_out_200evts_job%d.root" % (i+1,) ]
  standardList500 += [ "sherpa_out_500evts_job%d.root" % (i+1,) ]
  standardList1000 += [ "sherpa_out_1000evts_job%d.root" % (i+1,) ]

# for the production with 0~3 jets there is only 1000 evts per file
standardList0j3=[]
for i in range(20):
  standardList0j3 += [ "sherpa_out_1000evts_job%d.root" % (i+1,) ]

standardDecays={"W": ["Ele", "Mu", "Tau", "Lep"], "Z": ["Ele", "Mu", "Nu", "EleMu"]}

castorFiles = {}
for VB in standardDecays.keys():
  for decay in standardDecays[VB]:
    castorFiles[VB + "g" + decay + "_0j2"] = standardList[:]

import copy
castorFilesFilter = copy.deepcopy(castorFiles)
castorFilesFilterJet10 = copy.deepcopy(castorFiles)
castorFilesFilter["WgEle_0j"] = standardList[:]

## modify the Zgamma with filter jet10
for decay in standardDecays["Z"]:
  castorFilesFilterJet10["Zg" + decay + "_0j2"] = standardList100[:] \
    + standardList200[:] + standardList500[:] + standardList1000[:]


## add the files with 0~3 jets
for VB in standardDecays.keys():
  for decay in standardDecays[VB]:
    castorFilesFilter[VB + "g" + decay + "_0j3"] = standardList0j3[:]

## some obsoleted stuff
#castorFiles["WgLep_0j1"] = [
    #"sherpa_out.root",
    #"sherpa_out_1K.root",
    #"sherpa_out_10K.root",
#]

#castorFiles["ZgNoTau_0j2"] = [
    ##"sherpa_out.root",
    ##"sherpa_out_1K.root",
    ##"sherpa_out_1K_2.root",
    ##"sherpa_out_42evts_job0.root"
#]

castorFiles["ZgNu_0j2"].remove(castorFiles["ZgNu_0j2"][0])

def prependPath(path, files):
  for i in range(len(files)):
    files[i] = path + files[i]

# prependPath("rfio:" + castorDir + "/WgLep_0j1/GEN/test/", files["castorWgLep_0j1"])
# prependPath("rfio:" + castorDir + "/ZgNoTau_0j2/GEN/test/", files["castorZgNoTau_0j2"])

for decay in castorFiles.keys():
  prefix = "rfio:%s/%s/GEN/test/" % (castorDir, decay)
  prependPath(prefix, castorFiles[decay])
for decay in castorFilesFilter.keys():
  prefix = "rfio:%s/%s/GEN/filter/" % (castorDir, decay)
  prependPath(prefix, castorFilesFilter[decay])
for decay in castorFilesFilterJet10.keys():
  prefix = "rfio:%s/%s/GEN/filterJet10/" % (castorDir, decay)
  prependPath(prefix, castorFilesFilterJet10[decay])
