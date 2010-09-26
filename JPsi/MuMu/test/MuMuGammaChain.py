from basicRoot import *

inputFiles = """
MuMuGammaTree_MinimumBias_Commissioning10-SD_Mu-Jun14thSkim_v1_132440-137028.root
MuMuGammaTree_Mu_Run2010A-Jun14thReReco_v1_135803-137436.root
MuMuGammaTree_Mu_Run2010A-Jul16thReReco-v1_139559-140159.root
MuMuGammaTree_Mu_Run2010A-PromptReco-v4_140160-140399.root
MuMuGammaTree_Mu_Run2010A-PromptReco-v4_140400-141961.root
MuMuGammaTree_Mu_Run2010A-PromptReco-v4_141962-142264_DCSTRONLY.root
MuMuGammaTree_Mu_Run2010A-PromptReco-v4_137437-139558_v2.root
""".split()

inputFiles = """
MuMuGammaTree_132440-135802_MinimumBias_Commissioning10-SD_Mu-Jun14thSkim_v1.root
MuMuGammaTree_135803-137436_Mu_Run2010A-Jun14thReReco_v1.root
MuMuGammaTree_137437-139558_Mu_Run2010A-PromptReco-v4b.root
MuMuGammaTree_139559-140159_Mu_Run2010A-Jul16thReReco-v1.root
MuMuGammaTree_140160-144114_Mu_Run2010A-PromptReco-v4.root
""".split()

chain = TChain("MuMuGammaTree/mmg")

for f in inputFiles:
  print "Loading ", f
  chain.Add(f)

print "Total entries in the chain:", chain.GetEntries()



#####################################################################
#####################################################################
#####################################################################
# MONTE CARLO
inputFilesMC = """
MuMuGammaTree_Zmumu_Spring10.root
""".split()

chainMC = TChain("MuMuGammaTree/mmg")

for f in inputFilesMC:
  print "Loading ", f
  chainMC.Add(f)

print "Total entries in the MC chain:", chainMC.GetEntries()

if __name__ == "__main__": import user

