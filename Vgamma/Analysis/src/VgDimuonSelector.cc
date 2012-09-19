/**
 * \brief Implementation of the VgDimuonSelector class.
 * \author Jan Veverka, Caltech
 * \date 19 September 2012
 */
#include <math.h>
#include <string>
#include "FWCore/Utilities/interface/Exception.h"
#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"
#include "Vgamma/Analysis/interface/VgDimuonSelector.h"

using cit::VgDimuonSelector;
// using cit::VgEvent;
using namespace std;
//_____________________________________________________________________
/**
 * Constructor
 */
VgDimuonSelector::VgDimuonSelector(PSet const & cfg)
{
  init(cfg.getParameter<double>("minMass"));

  if (cfg.exists("cutsToIgnore"))
    setIgnoredCuts(cfg.getParameter<vector<string> >("cutsToIgnore"));

  retInternal_ = getBitTemplate();  
} // Ctor


//_____________________________________________________________________
/**
 * Destructor
 */
VgDimuonSelector::~VgDimuonSelector()
{} // Dtor


//_____________________________________________________________________
/**
 * Initialization
 */
void
VgDimuonSelector::init(const double & minMass)
{
  push_back("Inclusive", 0);
  push_back("minMass", minMass);

  set("Inclusive");
  set("minMass");
} // init()


//_____________________________________________________________________
/**
 * Selection interface.
 */
bool 
VgDimuonSelector::operator()(cit::VgCombinedCandidate const & dimu,
                             pat::strbitset & ret) 
{
  ret.set(false);
  setIgnored(ret);
  
  // 0. all muons
  passCut(ret, "Inclusive");

  // 1. dimuon mass is greater than a given minimum
  if (dimu.m() >= cut("minMass", double()) ||
      ignoreCut("minMass") )
    passCut(ret, "minMass");
  else return false;

  return (bool) ret;
} 
// VgDimuonSelector::operator()(VgCombinedCandidate const & dimu,
//                              pat::strbitset & ret))

