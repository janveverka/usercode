/**
 * \brief Class Implementation
 * \author Jan Veverka
 * \date 15 September 2008
 */
#include <assert.h>
#include <iostream>
#include "FWCore/Utilities/interface/Exception.h"
#include "Vgamma/Analysis/interface/VgLeafCandidate.h"

using cit::VgLeafCandidate;

typedef cms::Exception Bad;

const double VgLeafCandidate::kElectronMass = 0.510998928e-3;
const double VgLeafCandidate::kMuonMass     = 105.65836668e-3;
const double VgLeafCandidate::kPhotonMass   = 0.;

//______________________________________________________________________________
/// Default Ctor 
VgLeafCandidate::VgLeafCandidate(VgAnalyzerTree const &tree, ParticleType type, 
                                 unsigned key) : 
  VgCandidate(),
  tree_(tree),
  key_(key)
{
  type_ = type;
  init();
} // ctor


//______________________________________________________________________________
void
VgLeafCandidate::init()
{
  switch (type_) {
  //_____________
  case kElectron:
    if ((Int_t)key_ >= tree_.nEle)
      throw Bad("BadKey") << "key=" << key_
		      << " outside of range nEle=" << tree_.nEle << "!";
    momentum_.SetPtEtaPhiM(tree_.elePt [key_],
			   tree_.eleEta[key_],
			   tree_.elePhi[key_],
			   kElectronMass);
    break;
      
  //_____________
  case kMuon:
    if ((Int_t)key_ >= tree_.nMu)
      throw Bad("BadKey") << "key=" << key_
		      << " outside of range nMu=" << tree_.nMu << "!";
    momentum_.SetPtEtaPhiM(tree_.muPt [key_],
			   tree_.muEta[key_],
			   tree_.muPhi[key_],
			   kMuonMass);
    break;
      
  //_____________
  case kPhoton:
    if ((Int_t)key_ >= tree_.nPho)
      throw Bad("BadKey") << "key=" << key_
		      << " outside of range nPho=" << tree_.nPho << "!";
    momentum_.SetPtEtaPhiM(tree_.phoEt [key_],
			   tree_.phoEta[key_],
			   tree_.phoPhi[key_],
			   kPhotonMass);
    break;
      
  //_____________
  case kCombined:
    throw Bad("BadParticleType") << "Illegal ParticleType = kCombined";
    
  //_____________
  default:
    /// This should never happen.
    throw Bad("BadParticleType") << "Unknown ParticleType: " << type_;
  } // switch(type_)
} // init
