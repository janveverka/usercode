// user include files
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "HtoZg/CommonAnalysis/interface/PhotonIsolationValueMapProducer.h"

namespace cit {
  namespace hzg {
    
    typedef PhotonIsolationValueMapProducer<
      reco::Photon
    > RecoPhotonIsolationValueMapProducer;
    
    typedef PhotonIsolationValueMapProducer<
      pat::Photon
    > PATPhotonIsolationValueMapProducer;

  } // namespace hzg
} // namespace cit

using cit::hzg::RecoPhotonIsolationValueMapProducer;
using cit::hzg::PATPhotonIsolationValueMapProducer;

/// Define these as a plug-ins
DEFINE_FWK_MODULE(RecoPhotonIsolationValueMapProducer);
DEFINE_FWK_MODULE(PATPhotonIsolationValueMapProducer);

