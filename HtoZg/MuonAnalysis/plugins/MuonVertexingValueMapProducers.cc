// user include files
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "HtoZg/MuonAnalysis/interface/MuonVertexingValueMapProducer.h"

namespace cit {
  namespace hzg {
    
    typedef MuonVertexingValueMapProducer<
      reco::Muon
    > RecoMuonVertexingValueMapProducer;
    
    typedef MuonVertexingValueMapProducer<
      pat::Muon
    > PATMuonVertexingValueMapProducer;

  } // namespace hzg
} // namespace cit

using cit::hzg::RecoMuonVertexingValueMapProducer;
using cit::hzg::PATMuonVertexingValueMapProducer;

/// Define these as a plug-ins
DEFINE_FWK_MODULE(RecoMuonVertexingValueMapProducer);
DEFINE_FWK_MODULE(PATMuonVertexingValueMapProducer);

