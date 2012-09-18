/**
 * \brief Implementation of the VgPhotonSelector class.
 * \author Jan Veverka, Caltech
 * \date 18 September 2012
 */
#include <math.h>
#include <string>
#include "FWCore/Utilities/interface/Exception.h"
#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"
#include "Vgamma/Analysis/interface/VgPhotonSelector.h"

using cit::VgPhotonSelector;
using namespace std;
//_____________________________________________________________________
/**
 * Constructor
 */
VgPhotonSelector::VgPhotonSelector(PSet const & cfg)
{
  init(
    // 1. minimum photon pt
    cfg.getParameter<double>("minPt"),
    // 2. maximum supercluster absolute pseudorapidity |eta|   
    cfg.getParameter<double>("maxAbsEtaSC")
  );

  if (cfg.exists("cutsToIgnore"))
    setIgnoredCuts(cfg.getParameter<vector<string> >("cutsToIgnore"));

  retInternal_ = getBitTemplate();  
} // Ctor


//_____________________________________________________________________
/**
 * Destructor
 */
VgPhotonSelector::~VgPhotonSelector()
{} // Dtor


//_____________________________________________________________________
/**
 * Initialization
 */
void
VgPhotonSelector::init(
      // 1. minimum photon pt
      const double & minPt,
      // 2. maximum supercluster |eta|
      const double & maxAbsEtaSC
)
{
  push_back("Inclusive", 0);
  push_back("minPt", minPt);
  push_back("maxAbsEtaSC", maxAbsEtaSC);

  set("Inclusive");
  set("minPt");
  set("maxAbsEtaSC");
} // init()


//_____________________________________________________________________
/**
 * Selection interface.
 */
bool 
VgPhotonSelector::operator()(cit::VgLeafCandidate const & pho,
                           pat::strbitset &  ret) 
{
  ret.set(false);
  setIgnored(ret);

  cit::VgAnalyzerTree const & tree = pho.tree();
  unsigned i = pho.key();
  
  // 0. all photons
  passCut(ret, "Inclusive");

  // 1. minimum photon pt
  if (pho.pt() >= cut("minPt", double()) ||
      ignoreCut("minPt") )
    passCut(ret, "minPt");
  else return false;

  // 2. maximum supercluster absolute pseudorapidity |eta|
  if (tree.phoSCEta[i] <= cut("maxAbsEtaSC", double()) ||
      ignoreCut("maxAbsEtaSC") )
    passCut(ret, "maxAbsEtaSC");
  else return false;

  return (bool) ret;
} 
// VgPhotonSelector::operator()(VgLeafCandidate const & pho,
//                            pat::strbitset &  ret))

