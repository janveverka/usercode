import sys
import os

print "Switching to batch mode ..."
sys.argv.append( '-b' )

import ROOT
import MuMuGammaChain
# from makeFsrHistos import templateSel
# from makeFsrHistos import bfiles, bchain

## Configuration
chains = MuMuGammaChain.getChains(MuMuGammaChain.bfiles,
                                  MuMuGammaChain.bpath
                                  )
chain = chains["data38x"]


chain.SetAlias("pt1", "muGenPt[dau1]")
chain.SetAlias("pt2", "muGenPt[dau2]")
chain.SetAlias("eta1", "muGenEta[dau1]")
chain.SetAlias("eta2", "muGenEta[dau2]")
chain.SetAlias("phi1", "muGenPhi[dau1]")
chain.SetAlias("phi2", "muGenPhi[dau2]")
chain.SetAlias("mm", "mmgDimuon")
chain.SetAlias("mu1", "dau1[mmgDimuon]")
chain.SetAlias("mu2", "dau2[mmgDimuon]")
chain.SetAlias("g", "mmgPhoton")

outputFileName = "kRatio-Sep17ReReco_v2json_and_PromptRecov2_v3json_34ipb.txt"

outputExpression = "kRatio(mmgMass, mass[mm]):phoPt[g]:phoEta[g]"

def makeSelection(cuts):
  return " & ".join("(%s)" % cut for cut in cuts)

photonId = makeSelection([
    "phoPt[g] > 10",
    "phoEcalIso[g] < 4.2 + 0.006 * phoPt[g]",
    "phoHcalIso[g] < 2.2 + 0.0025 * phoPt[g]",
    "phoTrackIso[g] < 2.0 + 0.001 * phoPt[g]",
    "phoHadronicOverEm[g] < 0.05",
    "((abs(phoEta[g]) > 1.5 & phoSigmaIetaIeta[g] < 0.03) || (phoSigmaIetaIeta[g] < 0.013))",
    "!phoHasPixelSeed"
    ])

selection = makeSelection([
    "isBaselineCand[mm]",
    "orderByVProb[mm] == 0",
    "mass[mm] > 40",
    "mass[mm] < 85",
    "abs(mmgMass-zMassPdg()) < 4",
    "nPhotons > 0",
    "mmgPhoton == 0", # require the hardest photon in the events
    "abs(phoScEta[g]) < 2.5",
    "abs(phoEta[g]) < 1.4442 || abs(phoEta[g]) > 1.566",
    "5 < phoPt[g]",
    "phoSeedRecoFlag[g] != 2",       # DATA ONLY! EcalRecHit::kOutOfTime = 2
    "phoSeedSeverityLevel[g] != 4",  # DATA ONLY! EcalSeverityLevelAlgo::kWeird = 4
    "phoSeedSeverityLevel[g] != 5",  # DATA ONLY! EcalSeverityLevelAlgo::kBad = 5
    "phoSeedSwissCross[g] < 0.95",   # extra spike cleaning check
    "mmgDeltaRNear < 0.5 || (%s)" % photonId,
    ])

## To reproduce Lyons selection do
##+   selection + "& phoPt[g]>10 & mmgDeltaRNear<0.8 & muPt[mmgMuonFar]>30

ROOT.gROOT.LoadMacro("resolutionErrors.C+")

print "Dumping `%s'" % outputExpression
print "  from `%s' " % "', `".join(bfiles["data38x"])
print "  to `%s'"    % outputFileName
print "  for `%s'"   % selection

print "Going trhough %d input entries ..." % chain.GetEntries()

chain.Draw(outputExpression, selection, "goff")
outputSize = chain.GetSelectedRows()

print "Writing to %d entries `%s'" % (outputSize, outputFileName)
outputFile = open(outputFileName, "w")
ascii = "\n".join(["%.6g\t%.6g\t%.6g" %
                   (chain.GetV1()[i],chain.GetV2()[i],chain.GetV3()[i],)
                   for i in range(outputSize)
                   ])
outputFile.write("# " + outputExpression.replace(":", "\t") + "\n")
outputFile.write(ascii + "\n")
outputFile.close()
print "... Done."
