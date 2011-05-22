#include "Misc/TreeMaker/interface/TreeMaker.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "Misc/TreeMaker/interface/BranchManager.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "Misc/TreeMaker/interface/GenBranchManager.h"

namespace cit {
  class GenCandViewTreeMaker : public TreeMaker<reco::CandidateView> {
    public:
      explicit GenCandViewTreeMaker(const edm::ParameterSet&);
      ~GenCandViewTreeMaker() {}
    protected:
      virtual void analyze(const edm::Event&, const edm::EventSetup&);

      /// branch managers
      GenBranchManager genVars_;

  }; // end of class GenCandViewTreeMaker declaration
} // end of namespace cit

using cit::GenCandViewTreeMaker;

GenCandViewTreeMaker::GenCandViewTreeMaker( const edm::ParameterSet& cfg ) :
  TreeMaker<reco::CandidateView>( cfg ),
  genVars_( cfg )
{
  genVars_.init( *tree_ );
}

void
GenCandViewTreeMaker::analyze( const edm::Event& iEvent,
                               const edm::EventSetup& iSetup )
{
  /// The order matters!!  The TreeMaker<...>::analyze(...) fills the tree_.
  /// The branch manager must get the data before the filling happens.
  genVars_.getData( iEvent, iSetup );
  TreeMaker<reco::CandidateView>::analyze( iEvent, iSetup );
}


//define this as a plug-in
DEFINE_FWK_MODULE(GenCandViewTreeMaker);
