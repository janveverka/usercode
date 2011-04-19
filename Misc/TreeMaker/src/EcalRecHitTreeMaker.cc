// -*- C++ -*-
//
// Package:   TreeMaker
// Class:    EcalRecHitTreeMaker
//
/**\class EcalRecHitTreeMaker EcalRecHitTreeMaker.cc Misc/TreeMaker/src/EcalRecHitTreeMaker.cc

 Description: [one line class summary]

 Implementation:
    [Notes on implementation]
*/
//
// Original Author:  Jan Veverka
//      Created:  Mon Apr  4 21:25:02 CEST 2011
// $Id: EcalRecHitTreeMaker.cc,v 1.8 2011/04/17 22:14:12 veverka Exp $
//
//


#include "Misc/TreeMaker/interface/TreeMaker.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "FWCore/Framework/interface/MakerMacros.h"

namespace cit {
  typedef TreeMaker<EcalRecHitCollection, Double_t> EcalRecHitTreeMaker;
} // end of namespace cit


//define this as a plug-in
using cit::EcalRecHitTreeMaker;
DEFINE_FWK_MODULE(EcalRecHitTreeMaker);
