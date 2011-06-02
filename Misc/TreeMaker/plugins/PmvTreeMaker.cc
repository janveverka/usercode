#include "DataFormats/Candidate/interface/Candidate.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "Misc/TreeMaker/interface/BranchManager.h"
#include "Misc/TreeMaker/interface/GenBranchManager.h"
#include "Misc/TreeMaker/interface/PmvBranchManager.h"
// #include "Misc/TreeMaker/interface/PileupBranchManager.h"
#include "Misc/TreeMaker/interface/TreeMaker.h"

namespace cit {
  class PmvTreeMaker : public TreeMaker<reco::CandidateView> {
    public:
      explicit PmvTreeMaker(const edm::ParameterSet&);
      ~PmvTreeMaker() {}
    protected:
      virtual void analyze(const edm::Event&, const edm::EventSetup&);

      /// branch managers
      PmvBranchManager    pmv_   ;
//       PileupBranchManager pileup_;

  }; // end of class PmvTreeMaker declaration
} // end of namespace cit

using cit::PmvTreeMaker;

PmvTreeMaker::PmvTreeMaker( const edm::ParameterSet& cfg ) :
  TreeMaker<reco::CandidateView>( cfg ),
  pmv_   ( cfg ) //,
//   pileup_( cfg )
{
  pmv_   .init( *tree_ );
//   pileup_.init( *tree_ );
}

void
PmvTreeMaker::analyze( const edm::Event& iEvent,
                       const edm::EventSetup& iSetup )
{
  /// The order matters!!  The TreeMaker<...>::analyze(...) fills the tree_.
  /// The branch manager must get the data before the filling happens.
  pmv_.getData( iEvent, iSetup );
//   pileup_.getData( iEvent, iSetup );
  TreeMaker<reco::CandidateView>::analyze( iEvent, iSetup );
}


//define this as a plug-in
DEFINE_FWK_MODULE(PmvTreeMaker);
