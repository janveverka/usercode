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
 * Static data
 */
const double VgPhotonSelector::kBarrelIsoEffectiveAreaTracker  = 0.0167;
const double VgPhotonSelector::kBarrelIsoEffectiveAreaEcal     = 0.183 ;
const double VgPhotonSelector::kBarrelIsoEffectiveAreaHcal     = 0.062 ;
const double VgPhotonSelector::kEndcapsIsoEffectiveAreaTracker = 0.032 ;
const double VgPhotonSelector::kEndcapsIsoEffectiveAreaEcal    = 0.090 ;
const double VgPhotonSelector::kEndcapsIsoEffectiveAreaHcal    = 0.180 ;
const double VgPhotonSelector::kIsoPtSlopeTracker = 0.001 ;
const double VgPhotonSelector::kIsoPtSlopeEcal    = 0.006 ;
const double VgPhotonSelector::kIsoPtSlopeHcal    = 0.0025;

//_____________________________________________________________________
/**
 * Constructor
 */
VgPhotonSelector::VgPhotonSelector(PSet const & cfg)
{
  init(
    // 1. minimum photon pt
    cfg.getParameter<double>("minPt"),
    // 2. minimum supercluster absolute pseudorapidity |eta|   
    cfg.getParameter<double>("minAbsEtaSC"),
    // 3. maximum supercluster absolute pseudorapidity |eta|   
    cfg.getParameter<double>("maxAbsEtaSC"),
    // 4. maximum shower width \sigma_{i\eta i\eta}
    cfg.getParameter<double>("maxSihih"),    
    // 5. has pixel match
    (int) cfg.getParameter<bool  >("hasPixelMatch"),
    // 6. maximum tracker isolation
    cfg.getParameter<double>("maxTrackIso"),
    // 7. maximum ECAL isolation
    cfg.getParameter<double>("maxEcalIso"),
    // 8. maximum HCAL isolation
    cfg.getParameter<double>("maxHcalIso")
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
VgPhotonSelector::init(const double & minPt        , // 1
		       const double & minAbsEtaSC  , // 2
		       const double & maxAbsEtaSC  , // 3
		       const double & maxSihih     , // 4
		       const int    & hasPixelMatch, // 5
		       const double & maxTrackIso  , // 6
		       const double & maxEcalIso   , // 7
		       const double & maxHcalIso   ) // 8
{
  push_back("Inclusive"    , 0            ); // 0
  push_back("minPt"        , minPt        ); // 1
  push_back("minAbsEtaSC"  , minAbsEtaSC  ); // 2
  push_back("maxAbsEtaSC"  , maxAbsEtaSC  ); // 3
  push_back("maxSihih"     , maxSihih     ); // 4
  push_back("hasPixelMatch", hasPixelMatch); // 5
  push_back("maxTrackIso"  , maxTrackIso  ); // 6
  push_back("maxEcalIso"   , maxEcalIso   ); // 7
  push_back("maxHcalIso"   , maxHcalIso   ); // 8

  set("Inclusive"    ); // 0
  set("minPt"        ); // 1
  set("minAbsEtaSC"  ); // 2
  set("maxAbsEtaSC"  ); // 3
  set("maxSihih"     ); // 4
  set("hasPixelMatch"); // 5
  set("maxTrackIso"  ); // 6
  set("maxEcalIso"   ); // 7
  set("maxHcalIso"   ); // 8
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
  double rho = tree.rho;
  double scAbsEta = fabs(tree.phoSCEta[i]);
  double iso = 0.;
  
  // 0. all photons
  passCut(ret, "Inclusive");

  // 1. minimum photon pt
  if (pho.pt() > cut("minPt", double()) ||
      ignoreCut("minPt") )
    passCut(ret, "minPt");
  else return false;

  // 2. maximum supercluster absolute pseudorapidity |eta|
  if (scAbsEta > cut("minAbsEtaSC", double()) ||
      ignoreCut("minAbsEtaSC") )
    passCut(ret, "minAbsEtaSC");
  else return false;

  // 3. maximum supercluster absolute pseudorapidity |eta|
  if (scAbsEta < cut("maxAbsEtaSC", double()) ||
      ignoreCut("maxAbsEtaSC") )
    passCut(ret, "maxAbsEtaSC");
  else return false;

  // 4. maximum shower width
  if (tree.phoSigmaIEtaIEta[i] < cut("maxSihih", double()) ||
      ignoreCut("maxSihih")) 
    passCut(ret, "maxSihih");
  else return false;

  // 5. has pixel match
  if ((bool)tree.phohasPixelSeed[i] == (bool)cut("hasPixelMatch", int()) ||
      ignoreCut("hasPixelMatch")) 
    passCut(ret, "hasPixelMatch");
  else return false;

  // 6. maximum tracker isolation
  iso = tree.phoTrkIsoHollowDR04[i] - kIsoPtSlopeTracker * pho.pt();
  iso -= rho * effectiveArea(scAbsEta, kIsoTracker);
  if (iso < cut("maxTrackIso", double()) ||
      ignoreCut("maxTrackIso")) 
    passCut(ret, "maxTrackIso");
  else return false;

  // 7. maximum ECAL isolation
  iso = tree.phoEcalIsoDR04[i] - kIsoPtSlopeEcal * pho.pt();
  iso -= rho * effectiveArea(scAbsEta, kIsoEcal);
  if (cut("maxEcalIso", double()) ||
      ignoreCut("maxEcalIso")) 
    passCut(ret, "maxEcalIso");
  else return false;

  // 8. maximum HCAL isolation
  iso = tree.phoHcalIsoDR04[i] - kIsoPtSlopeHcal * pho.pt();
  iso -= rho * effectiveArea(scAbsEta, kIsoHcal);
  if (cut("maxHcalIso", double()) ||
      ignoreCut("maxHcalIso")) 
    passCut(ret, "maxHcalIso");
  else return false;

  return (bool) ret;
} 
// VgPhotonSelector::operator()(VgLeafCandidate const & pho,
//                            pat::strbitset &  ret))


//_____________________________________________________________________
/**
 * Returns the effective area for this kind of isolation
 */
double
VgPhotonSelector::effectiveArea(double scAbsEta, IsolationType type) const
{
  switch (type) {
  case kIsoTracker:
    if (scAbsEta < 1.5) return kBarrelIsoEffectiveAreaTracker;
    else return kEndcapsIsoEffectiveAreaTracker;
  case kIsoEcal:
    if (scAbsEta < 1.5) return kBarrelIsoEffectiveAreaEcal;
    else return kEndcapsIsoEffectiveAreaEcal;
  case kIsoHcal:
    if (scAbsEta < 1.5) return kBarrelIsoEffectiveAreaHcal;
    else return kEndcapsIsoEffectiveAreaHcal;
  default:
    /// This should never happen
    ostringstream msg;
    msg << "VgPhotonSelector::effectiveArea(..): Unknown isolation type: "
        << type;
    throw cms::Exception("BadPhotonIsolationType") << msg.str();
    break;
  } // switch(type)
  /// This should never happen either
  ostringstream msg;
  msg << "VgPhotonSelector::effectiveArea(..): Logic error";
  throw cms::Exception("LogicError") << msg.str();
  return 0.;
}
// double
// VgPhotonSelector::effectiveArea(double scEta, IsolationType type) const
