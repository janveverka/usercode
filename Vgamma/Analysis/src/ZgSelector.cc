/**
 * \brief Implementation of the ZgSelector class.
 * \author Jan Veverka, Caltech
 * \date 19 September 2012
 */
#include <iostream>
#include <math.h>
#include <sstream>
#include <string>
#include "TMath.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"
#include "Vgamma/Analysis/interface/VgCandidate.h"
#include "Vgamma/Analysis/interface/ZgSelector.h"

using cit::ZgSelector;
// using cit::VgEvent;
using namespace std;
//_____________________________________________________________________
/**
 * Constructor
 */
ZgSelector::ZgSelector(PSet const & cfg)
{
  init(cfg.getParameter<double>("minDeltaR"));

  if (cfg.exists("cutsToIgnore"))
    setIgnoredCuts(cfg.getParameter<vector<string> >("cutsToIgnore"));

  retInternal_ = getBitTemplate();  
} // Ctor


//_____________________________________________________________________
/**
 * Destructor
 */
ZgSelector::~ZgSelector()
{} // Dtor


//_____________________________________________________________________
/**
 * Initialization
 */
void
ZgSelector::init(const double & minDeltaR)
{
  push_back("Inclusive", 0);
  push_back("minDeltaR", minDeltaR);

  set("Inclusive");
  set("minDeltaR");
} // init()


//_____________________________________________________________________
/**
 * Selection interface.
 */
bool 
ZgSelector::operator()(cit::VgCombinedCandidate const & zg,
		       pat::strbitset & ret) 
{
  ret.set(false);
  setIgnored(ret);
  
  // Check if we have a got the mu mu gamma right.
  VgLeafCandidate const & lep1 = zg.daughter(0);
  VgLeafCandidate const & lep2 = zg.daughter(1);
  VgLeafCandidate const & pho  = zg.daughter(2);

  if (lep1.type() != cit::VgCandidate::kElectron &&
      lep1.type() != cit::VgCandidate::kMuon) {
    ostringstream msg;
    msg << "ZgSelector::operator(): Expect daughter 0 of type " 
        << cit::VgCandidate::kElectron << " or " 
        << cit::VgCandidate::kMuon << " but got " 
        << lep1.type();
    throw cms::Exception("BadZgCand") << msg.str();                                     
  }  

  if (lep1.type() != lep2.type()) {
    ostringstream msg;
    msg << "ZgSelector::operator(): Expect daughter 0 and 1 of the same type "
        << cit::VgCandidate::kElectron << " or " 
        << cit::VgCandidate::kMuon << " but got " 
        << lep1.type() << " and " << lep2.type();
    throw cms::Exception("BadZgCand") << msg.str();                                     
  }  

  if (pho.type() != cit::VgCandidate::kPhoton) {
    ostringstream msg;
    msg << "ZgSelector::operator(): Expect daughter 2 of type " 
        << cit::VgCandidate::kPhoton << " but got " << pho.type();
    throw cms::Exception("BadZgCand") << msg.str();
  }

  double dr1 = pho.momentum().DeltaR(lep1.momentum());
  double dr2 = pho.momentum().DeltaR(lep2.momentum());

  // 0. All Zg candidates
  passCut(ret, "Inclusive");

  // 1. Delta R(lepton, photon) is greate than given cut.
  if (TMath::Min(dr1, dr2) >= cut("minDeltaR", double()) ||
      ignoreCut("minDeltaR") )
    passCut(ret, "minDeltaR");
  else return false;

  return (bool) ret;
} 
// ZgSelector::operator()(VgCombinedCandidate const & zg,
//                           pat::strbitset & ret)

