#include "DataFormats/Candidate/interface/Candidate.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "Misc/TreeMaker/interface/BranchManager.h"
#include "Misc/TreeMaker/interface/GenBranchManager.h"
#include "Misc/TreeMaker/interface/PmvBranchManager.h"
#include "DataFormats/CaloRecHit/interface/CaloRecHit.h"
// #include "Misc/TreeMaker/interface/PileupBranchManager.h"
#include "Misc/TreeMaker/interface/TreeMaker.h"

namespace cit {
  class ZeePrimeTreeMaker : public TreeMaker<reco::CandidateView> {
    public:
      explicit ZeePrimeTreeMaker(const edm::ParameterSet&);
      ~ZeePrimeTreeMaker() {}
      typedef edm::ParameterSet PSet;
    protected:
      virtual void analyze(const edm::Event&, const edm::EventSetup&);

      /// branch managers
      BranchManager<reco::CandidateView> photonVars_;
      BranchManager<reco::CandidateView> uncleanPhotonVars_;
      BranchManager<CaloRecHit> ecalRechitVars_;

  }; // end of class ZeePrimeTreeMaker declaration
} // end of namespace cit

using cit::ZeePrimeTreeMaker;

ZeePrimeTreeMaker::ZeePrimeTreeMaker( const edm::ParameterSet& cfg ) :
  TreeMaker<reco::CandidateView>( cfg ),
  photonVars_        ( cfg.getParameter<PSet>( "photons"        ) ),
  uncleanPhotonVars_ ( cfg.getParameter<PSet>( "uncleanPhotons" ) ),
  ecalRechitVars_    ( cfg.getParameter<PSet>( "ecalRechits"    ) ),
{
  photonVars_       .init( *tree_ );
  uncleanPhotonVars_.init( *tree_ );
  ecalRechitVars_   .init( *tree_ );
}

void
ZeePrimeTreeMaker::analyze( const edm::Event& iEvent,
                            const edm::EventSetup& iSetup )
{
  /// The order matters!!  The TreeMaker<...>::analyze(...) fills the tree_.
  /// The branch manager must get the data before the filling happens.
  photonVars_       .getData( iEvent, iSetup );
  uncleanPhotonVars_.getData( iEvent, iSetup );
  ecalRechitVars_   .getData( iEvent, iSetup );

  TreeMaker<reco::CandidateView>::analyze( iEvent, iSetup );
}


//define this as a plug-in
DEFINE_FWK_MODULE(ZeePrimeTreeMaker);
