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
  init(     cfg.getParameter<double>("minPt"         ),  //  1
            cfg.getParameter<double>("maxAbsEta"     ),  //  2
       (int)cfg.getParameter<bool  >("isGlobalMuon"  ),  //  3
            cfg.getParameter<double>("maxNormChi2"   ),  //  4
            cfg.getParameter<int   >("minChamberHits"),  //  5
            cfg.getParameter<int   >("minStations"   ),  //  6
            cfg.getParameter<double>("maxAbsDxy"     ),  //  7
            cfg.getParameter<double>("maxAbsDz"      ),  //  8
            cfg.getParameter<int   >("minPixelHits"  ),  //  9
            cfg.getParameter<int   >("minTkHits"     ),  // 10
            cfg.getParameter<double>("maxCombRelIso" )); // 11

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
VgMuonSelector::init(const double & minPt         , //  1
                     const double & maxAbsEta     , //  2
                     const int    & isGlobalMuon  , //  3
                     const double & maxNormChi2   , //  4
                     const int    & minChamberHits, //  5
                     const int    & minStations   , //  6
                     const double & maxAbsDxy     , //  7
                     const double & maxAbsDz      , //  8
                     const int    & minPixelHits  , //  9
                     const int    & minTkHits     , // 10
                     const double & maxCombRelIso ) // 11
{
  push_back("Inclusive"     , 0             ); //  0
  push_back("minPt"         , minPt         ); //  1
  push_back("maxAbsEta"     , maxAbsEta     ); //  2  
  push_back("isGlobalMuon"  , isGlobalMuon  ); //  3
  push_back("maxNormChi2"   , maxNormChi2   ); //  4
  push_back("minChamberHits", minChamberHits); //  5
  push_back("minStations"   , minStations   ); //  6  
  push_back("maxAbsDxy"     , maxAbsDxy     ); //  7  
  push_back("maxAbsDz"      , maxAbsDz      ); //  8  
  push_back("minPixelHits"  , minPixelHits  ); //  9  
  push_back("minTkHits"     , minTkHits     ); // 10  
  push_back("maxCombRelIso" , maxCombRelIso ); // 11  

  set("Inclusive"     ); //  0
  set("minPt"         ); //  1
  set("maxAbsEta"     ); //  2
  set("isGlobalMuon"  ); //  3
  set("maxNormChi2"   ); //  4
  set("minChamberHits"); //  5
  set("minStations"   ); //  6
  set("maxAbsDxy"     ); //  7
  set("maxAbsDz"      ); //  8
  set("minPixelHits"  ); //  9
  set("minTkHits"     ); // 10
  set("maxCombRelIso" ); // 11
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
  
  //  1. minimum transverse momentum
  if (mu.pt() > cut("minPt", double()) || 
      ignoreCut("minPt"         )) 
    passCut(ret, "minPt"         );
  else return false;

  //  2. maximum pseudo-rapidity absolute value
  if (fabs(mu.eta()) < cut("maxAbsEta", double()) || 
      ignoreCut("maxAbsEta"     )) 
    passCut(ret, "maxAbsEta"     );
  else return false;

  // 3. muon is reconstructed as a "global muon" (out-in fit)
  unsigned globalMuon = 1<<1;
  int isGlobalMuon( (unsigned(tree.muType[i]) & globalMuon) ?  1 : 0 );
  if (cut("isGlobalMuon", int()) == isGlobalMuon ||
      ignoreCut("isGlobalMuon") )
    passCut(ret, "isGlobalMuon");
  else return false;

  // 4. maximum global muon fit normalized chi2
  if (tree.muChi2NDF[i] < cut("maxNormChi2", double()) ||
      ignoreCut("maxNormChi2") )
    passCut(ret, "maxNormChi2");
  else return false;

  //  5. minimum number of valid muon chamber hits matched to the 
  //     global fit
  if (tree.muNumberOfValidMuonHits[i]  >= cut("minChamberHits", int()) ||
      ignoreCut("minChamberHits") )
    passCut(ret, "minChamberHits");
  else return false;

  //  6. minimum number of muon stations with matched segments
  //     (global track: out-in fit)
  if (tree.muStations[i] >= cut("minStations", int()) || 
      ignoreCut("minStations"   )) 
    passCut(ret, "minStations"   );
  else return false;

  //  7. maximum inner track transverse impact parameter w.r.t the vertex
  //     absolute value
  if (fabs(tree.muPVD0[i]) < cut("maxAbsDxy", double()) || 
      ignoreCut("maxAbsDxy"     )) 
    passCut(ret, "maxAbsDxy"     );
  else return false;

  //  8. maximum inner track transverse impact parameter w.r.t the vertex
  //     absolute value
  if (fabs(tree.muPVDz[i]) < cut("maxAbsDz", double()) || 
      ignoreCut("maxAbsDz"      )) 
    passCut(ret, "maxAbsDz"      );
  else return false;

  //  9. minimum number of pixel hits
  if (tree.muNumberOfValidPixelHits[i] >= cut("minPixelHits", int()) ||
      ignoreCut("minPixelHits"  )) 
    passCut(ret, "minPixelHits"  );
  else return false;

  // 10. minimum number of tracker (pixels + strips) hits
  if (tree.muNumberOfValidTrkHits[i] >= cut("minTkHits", int()) || 
      ignoreCut("minTkHits"     )) 
    passCut(ret, "minTkHits"     );
  else return false;

  // 11. Sum of the Tracker, ECAL and HCAL isolations
  //     within a cone of DR < 0.3 around  the muon direction
  //     (vetoing a cone of 0.015 around that direction for the tracker
  //     isloation) divided by muon pt.
  double combIso = tree.muIsoEcal[i] + tree.muIsoHcal[i] + tree.muIsoTrk[i];
  double combIsoPUcorr = combIso - tree.rho * TMath::Pi() * 0.3 * 0.3;
  double combRelIso = combIsoPUcorr / mu.pt();
  if (combRelIso < cut("maxCombRelIso" , double()) || 
      ignoreCut("maxCombRelIso" )) 
    passCut(ret, "maxCombRelIso" );
  else return false;

  return (bool) ret;
} 
// VgMuonSelector::operator()(VgLeafCandidate const & mu,
//                            pat::strbitset &  ret))

