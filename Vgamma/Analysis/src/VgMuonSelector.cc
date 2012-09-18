/**
 * \brief Implementation of the VgMuonSelector class.
 * \author Jan Veverka, Caltech
 * \date 18 September 2012
 */
#include <math.h>
#include <string>
#include "FWCore/Utilities/interface/Exception.h"
#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"
#include "Vgamma/Analysis/interface/VgMuonSelector.h"

using cit::VgMuonSelector;
// using cit::VgEvent;
using namespace std;
//_____________________________________________________________________
/**
 * Constructor
 */
VgMuonSelector::VgMuonSelector(PSet const & cfg)
{
  init( 
    // 1. muon is reconstructed as a "global muon" (out-in fit)
    (int) cfg.getParameter<bool>("isGlobalMuon") ? 1 : 0,
    // 2. maximum global muon fit normalized chi2
    cfg.getParameter<double>("maxNormChi2"),
    // 3. minimum number of valid muon hits matched to the global fit
    (int) cfg.getParameter<unsigned>("minMuonHits"),
    // 4. muon is reconsturcted as a "tracker muon" (in-out fit)
    (int) cfg.getParameter<bool>("isTrackerMuon") ? 1 : 0
  );

  if (cfg.exists("cutsToIgnore"))
    setIgnoredCuts(cfg.getParameter<vector<string> >("cutsToIgnore"));

  retInternal_ = getBitTemplate();  
} // Ctor


//_____________________________________________________________________
/**
 * Destructor
 */
VgMuonSelector::~VgMuonSelector()
{} // Dtor


//_____________________________________________________________________
/**
 * Initialization
 */
void
VgMuonSelector::init(
  // 1. muon is reconstructed as a "global muon" (out-in fit)
  const int & isGlobalMuon,
  // 2. maximum global muon fit normalized chi2
  const double & maxNormChi2,
  // 3. minimum number of valid muon hits matched to the global fit
  const int & minMuonHits,
  // 4. muon is reconsturcted as a "tracker muon" (in-out fit)
  const int & isTrackerMuon  
)
{
  push_back("Inclusive", 0);
  push_back("isGlobalMuon", isGlobalMuon);
  push_back("maxNormChi2", maxNormChi2);
  push_back("minMuonHits", minMuonHits);
  push_back("isTrackerMuon", isTrackerMuon);

  set("Inclusive");
  set("isGlobalMuon");
  set("maxNormChi2");
  set("minMuonHits");
  set("isTrackerMuon");  
} // init()


//_____________________________________________________________________
/**
 * Selection interface.
 */
bool 
VgMuonSelector::operator()(cit::VgLeafCandidate const & mu,
                           pat::strbitset &  ret) 
{
  ret.set(false);
  setIgnored(ret);

  cit::VgAnalyzerTree const & tree = mu.tree();
  unsigned i = mu.key();
  
  // 0. all muons
  passCut(ret, "Inclusive");

  // 1. muon is reconstructed as a "global muon" (out-in fit)
  unsigned globalMuon = 1<<1;
  int isGlobalMuon( (unsigned(tree.muType[i]) & globalMuon) ?  1 : 0 );
  if (isGlobalMuon == cut("isGlobalMuon", int()) ||
      ignoreCut("isGlobalMuon") )
    passCut(ret, "isGlobalMuon");
  else return false;

  // 2. maximum global muon fit normalized chi2
  if (tree.muChi2NDF[i] < cut("maxNormChi2", double()) ||
      ignoreCut("maxNormChi2") )
    passCut(ret, "maxNormChi2");
  else return false;

  // 3. minimum number of valid muon hits matched to the global fit
  if (tree.muNumberOfValidMuonHits[i]  >= cut("minMuonHits", int()) ||
      ignoreCut("minMuonHits") )
    passCut(ret, "minMuonHits");
  else return false;

  // 4. muon is reconsturcted as a "tracker muon" (in-out fit)
  unsigned trackerMuon = 1<<2;
  int isTrackerMuon( (unsigned(tree.muType[i]) & trackerMuon) ?  1 : 0 );
  if (isTrackerMuon == cut("isTrackerMuon", int()) ||
      ignoreCut("isTrackerMuon") )
    passCut(ret, "isTrackerMuon");
  else return false;

  return (bool) ret;
} 
// VgMuonSelector::operator()(VgLeafCandidate const & mu,
//                            pat::strbitset &  ret))

