import FWCore.ParameterSet.Config as cms

MuMuGammaTree = cms.EDAnalyzer("TreeMaker",
  name = cms.untracked.string("mmg"),
  title = cms.untracked.string("mmg TreeMaker"),
  src = cms.InputTag("cleanPatPhotonsTriggerMatch"),
  prefix = cms.untracked.string("pho"),
  sizeName = cms.untracked.string("nPhotons"),
  variables = cms.VPSet()
)

branches = """Pt                pt
              Eta               eta
              ScEta             superCluster.eta
              Phi               phi
              EcalIso           ecalIso
              HcalIso           hcalIso
              TrackIso          trackIso
              SigmaIetaIeta     sigmaIetaIeta
              HadronicOverEm    hadronicOverEm
              HasPixelSeed      hasPixelSeed
              SeedRecoFlag      userInt("photonUserData:seedRecoFlag")
              SeedSeverityLevel userInt("photonUserData:seedSeverityLevel")
              MaxEnergyXtal     maxEnergyXtal
              E3x3              e3x3
              SeedSwissCross    userInt("photonUserData:seedSwissCross")
              SeedE1OverE9      userInt("photonUserData:seedE1OverE9")
              R9                r9 
              ESC               superCluster.energy 
              ESCRaw            superCluster.rawEnergy
              E5x5              e5x5""".split("\n")

genBranches =  """GenMatchPdgId     genParticle.pdgId
                  GenMatchStatus    genParticle.status
                  GenPt             genParticle.pt
                  GenEta            genParticle.eta
                  GenPhi            genParticle.phi""".split("\n")

#                  GenMatchMomPdgId  genParticle.mother(0).pdgId
#                  GenMatchMomStatus genParticle.mother(0).status

for line in  branches:
    tag, var = line.split()
    MuMuGammaTree.variables.append(
        cms.PSet(
            tag = cms.untracked.string(tag),
            quantity = cms.untracked.string(var)
        )
    )

for line in genBranches: 
    tag, var = line.split()
    MuMuGammaTree.variables.append(
        cms.PSet(
            tag = cms.untracked.string(tag),
            quantity = cms.untracked.PSet(
                ifCondition = cms.untracked.string("genParticlesSize > 0"),
                thenQuantity = cms.untracked.string(var),
                elseQuantity = cms.untracked.string("0")
            )
        )
    )

