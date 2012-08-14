// user include files
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "HtoZg/CommonAnalysis/interface/EgammaIdValueMapProducer.h"

namespace cit {
  namespace hzg {
    
    typedef EgammaIdValueMapProducer<
      reco::Photon
    > PhotonIdValueMapProducer;
    
    typedef EgammaIdValueMapProducer<
      pat::Photon
    > PATPhotonIdValueMapProducer;

  } // namespace hzg
} // namespace cit

using cit::hzg::PhotonIdValueMapProducer;
using cit::hzg::PATPhotonIdValueMapProducer;

/// Define these as a plug-ins
DEFINE_FWK_MODULE(PhotonIdValueMapProducer);
DEFINE_FWK_MODULE(PATPhotonIdValueMapProducer);

