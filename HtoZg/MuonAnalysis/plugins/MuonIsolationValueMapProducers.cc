// user include files
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "HtoZg/MuonAnalysis/interface/MuonIsolationValueMapProducer.h"

namespace cit {
  namespace hzg {
    
    typedef MuonIsolationValueMapProducer<
      reco::Muon
    > RecoMuonIsolationValueMapProducer;
    
    typedef MuonIsolationValueMapProducer<
      pat::Muon
    > PATMuonIsolationValueMapProducer;

  } // namespace hzg
} // namespace cit

using cit::hzg::RecoMuonIsolationValueMapProducer;
using cit::hzg::PATMuonIsolationValueMapProducer;

/// Define these as a plug-ins
DEFINE_FWK_MODULE(RecoMuonIsolationValueMapProducer);
DEFINE_FWK_MODULE(PATMuonIsolationValueMapProducer);

