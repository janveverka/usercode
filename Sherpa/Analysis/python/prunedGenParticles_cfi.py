import FWCore.ParameterSet.Config as cms

prunedGenParticles = cms.EDProducer("GenParticlePruner",
    src = cms.InputTag("genParticles"),
    select = cms.vstring(
      #"drop *",
      ## Keep the hard scattering process with all ancesstors, children and
      ##+ grand children.      
      #"++keep+ status = 2 & numberOfMothers > 0 & mother(0).status = 3",
      ## Keep signal particles and their families.
      "++keep+ " + ' & '.join([
          'status = 1',
          '(abs(pdgId) = 11 | abs(pdgId) = 13 | pdgId = 22)',
          'numberOfMothers > 0',
          'mother(0).numberOfMothers > 0',
          'mother(0).mother(0).status = 3',
          ]),
      ## Drop all the soft and out of acceptance particles
      #"drop (status = 1 | status = 2) & (pt < 1.5 | abs(eta) > 5)",
    )
)

if __name__ == "__main__": import user
