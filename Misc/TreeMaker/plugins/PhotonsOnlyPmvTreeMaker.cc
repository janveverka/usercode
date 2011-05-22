#include "Misc/TreeMaker/interface/TreeMaker.h"
#include "Misc/TreeMaker/interface/BranchManager.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "SimDataFormats/Track/interface/SimTrackContainer.h"
// #include "SimDataFormats/Vertex/interface/SimVertex.h"
// #include "SimDataFormats/Vertex/interface/SimVertexContainer.h"

namespace cit {
  class FastSimTreeMaker : public TreeMaker<EcalRecHitCollection, Double_t> {
    public:
      explicit FastSimTreeMaker(const edm::ParameterSet&);
      ~FastSimTreeMaker() {}
    protected:
      virtual void analyze(const edm::Event&, const edm::EventSetup&);

      /// branch managers
      BranchManager<edm::SimTrackContainer> simTrackVars_;

  }; // end of class FastSimTreeMaker declaration
} // end of namespace cit

using cit::FastSimTreeMaker;

FastSimTreeMaker::FastSimTreeMaker( const edm::ParameterSet& cfg ) :
  TreeMaker<EcalRecHitCollection, Double_t>( cfg ),
  simTrackVars_( cfg.getParameter<edm::ParameterSet>( "simTrackBranches" ) )
{
  simTrackVars_.init( *tree_ );
}

void
FastSimTreeMaker::analyze( const edm::Event& iEvent,
                           const edm::EventSetup& iSetup )
{
  /// The order matters!!  The TreeMaker<...>::analyze(...) fills the tree_.
  /// The branch manager must get the data before the filling happens.
  simTrackVars_.getData( iEvent, iSetup );
  TreeMaker<EcalRecHitCollection, Double_t>::analyze( iEvent, iSetup );
}


//define this as a plug-in
DEFINE_FWK_MODULE(FastSimTreeMaker);
