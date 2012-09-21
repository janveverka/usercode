/**
 * \brief Implementation of the VgDileptonSelector class.
 * \author Jan Veverka, Caltech
 * \date 19 September 2012
 */
#include <math.h>
#include <string>
#include "FWCore/Utilities/interface/Exception.h"
#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"
#include "Vgamma/Analysis/interface/VgDileptonSelector.h"

using cit::VgDileptonSelector;
// using cit::VgEvent;
using namespace std;
//_____________________________________________________________________
/**
 * Constructor
 */
VgDileptonSelector::VgDileptonSelector(PSet const & cfg)
{
  init(cfg.getParameter<int>("charge"),
       cfg.getParameter<double>("minMass"));

  if (cfg.exists("cutsToIgnore"))
    setIgnoredCuts(cfg.getParameter<vector<string> >("cutsToIgnore"));

  retInternal_ = getBitTemplate();  
} // Ctor


//_____________________________________________________________________
/**
 * Destructor
 */
VgDileptonSelector::~VgDileptonSelector()
{} // Dtor


//_____________________________________________________________________
/**
 * Initialization
 */
void
VgDileptonSelector::init(const int & charge, const double & minMass)
{
  push_back("Inclusive", 0);
  push_back("charge", charge);
  push_back("minMass", minMass);

  set("Inclusive");
  set("charge");
  set("minMass");
} // init()


//_____________________________________________________________________
/**
 * Selection interface.
 */
bool 
VgDileptonSelector::operator()(cit::VgCombinedCandidate const & ll,
                             pat::strbitset & ret) 
{
  ret.set(false);
  setIgnored(ret);
  
  // 0. all leptons
  passCut(ret, "Inclusive");

  // 1. require charge equal to the given charge
  if (ll.charge() == cut("charge", int()) || ignoreCut("charge"))
    passCut(ret, "charge");
  else return false;

  // 2. dilepton mass is greater than a given minimum
  if (ll.m() >= cut("minMass", double()) || ignoreCut("minMass"))
    passCut(ret, "minMass");
  else return false;

  return (bool) ret;
} 
// VgDileptonSelector::operator()(VgCombinedCandidate const & ll,
//                              pat::strbitset & ret))

