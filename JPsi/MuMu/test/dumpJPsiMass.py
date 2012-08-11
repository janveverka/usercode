import ROOT

## Configuration
inputFiles = ["muNtuples.root", "minimumBiasNtuples.root"]
minJMass = 0.
maxJMass = 15.
charge = 0
categoriesToDump = ["gg", "gt", "tt"]
chargeLabel = "ss" # os = opposite sign, ss = same sign
maxEventsInput = 999999999

chain = ROOT.TChain("Events")
for f in inputFiles: chain.Add(f)
chain.SetScanField(0)

## Build the selection
for category in categoriesToDump:
  massLabel = category + chargeLabel + "JPsiMass"
  chargeLabel = category + chargeLabel + "Charge"
  selection = "%g < %s & %s < %g & %s = %d" % (minJMass, massLabel, massLabel, maxJMass, chargeLabel, charge)
  print "Dumping `%s' for `%s ...'" % (massLabel, selection)
  chain.Scan(massLabel, selection, "", maxEventsInput)
