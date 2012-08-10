import FWCore.ParameterSet.Config as cms

muonUserFloats = [cms.InputTag('muonVertexing', x) for x in 'dxy dz'.split()]
muonUserFloats += [cms.InputTag('muonIsolation', x) for x in 'rho EA'.split()]

