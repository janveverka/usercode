#include "Misc/TreeMaker/interface/TreeMaker.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "Misc/TreeMaker/interface/BranchManager.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "Misc/TreeMaker/interface/DiphotonGenBranchManager.h"

namespace cit {
  class DiphotonGenCandViewTreeMaker : public TreeMaker<reco::CandidateView> {
    public:
      explicit DiphotonGenCandViewTreeMaker(const edm::ParameterSet&);
      ~DiphotonGenCandViewTreeMaker() {}
    protected:
      virtual void analyze(const edm::Event&, const edm::EventSetup&);

      /// branch managers
      DiphotonGenBranchManager genVars_;

  }; // end of class DiphotonGenCandViewTreeMaker declaration
} // end of namespace cit

using cit::DiphotonGenCandViewTreeMaker;

DiphotonGenCandViewTreeMaker::DiphotonGenCandViewTreeMaker( const edm::ParameterSet& cfg ) :
  TreeMaker<reco::CandidateView>( cfg ),
  genVars_( cfg )
{
  genVars_.init( *tree_ );
}

void
DiphotonGenCandViewTreeMaker::analyze( const edm::Event& iEvent,
                                       const edm::EventSetup& iSetup )
{
  /// The order matters!!  The TreeMaker<...>::analyze(...) fills the tree_.
  /// The branch manager must get the data before the filling happens.
  genVars_.getData( iEvent, iSetup );
  TreeMaker<reco::CandidateView>::analyze( iEvent, iSetup );
}


//define this as a plug-in
DEFINE_FWK_MODULE(DiphotonGenCandViewTreeMaker);
