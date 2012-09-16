/**
 * \brief Class Implementation
 * \author Jan Veverka
 * \date 15 September 2008
 */
#include <assert.h>
#include <iostream>
#include <exception>
#include "Vgamma/Analysis/interface/VgLeafCandidate.h"

using cit::VgLeafCandidate;

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

    case kElectron:
      if ((Int_t)key_ >= tree_.nEle) {
	std::cerr << "VgLeafCandidate::init(): key=" << key_
		  << " outside of range nEle=" << tree_.nEle << "!"
		  << std::endl << std::flush;
	throw 3;
      }
      momentum_.SetPtEtaPhiM(tree_.elePt [key_],
                             tree_.eleEta[key_],
                             tree_.elePhi[key_],
                             kElectronMass);
      break;
      
    case kMuon:
      if ((Int_t)key_ >= tree_.nMu) {
	std::cerr << "VgLeafCandidate::init(): key=" << key_
		  << " outside of range nEle=" << tree_.nMu << "!"
		  << std::endl << std::flush;
	throw 4;
      }
      momentum_.SetPtEtaPhiM(tree_.muPt [key_],
                             tree_.muEta[key_],
                             tree_.muPhi[key_],
                             kMuonMass);
      break;
      
    case kPhoton:
      if ((Int_t)key_ >= tree_.nPho) {
	std::cerr << "VgLeafCandidate::init(): key=" << key_
		  << " outside of range nEle=" << tree_.nPho << "!"
		  << std::endl << std::flush;
	throw 5;
      }
      momentum_.SetPtEtaPhiM(tree_.phoEt [key_],
                             tree_.phoEta[key_],
                             tree_.phoPhi[key_],
                             kPhotonMass);
      break;
      
    case kCombined:
      std::cerr << "VgLeafCandidate::init(): Illegal ParticleType = kCombined"
                << std::endl << std::flush;
      throw 1;
      
    default:
      /// This should never happen.
      std::cerr << "VgLeafCandidate::init(): Unknown ParticleType: "
                << type_ << std::endl << std::flush;
      throw 2;
  }
} // init
