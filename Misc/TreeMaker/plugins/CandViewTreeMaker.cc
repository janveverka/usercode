// -*- C++ -*-
//
// Package:   CandViewTreeMaker
// Class:    CandViewTreeMaker
//
/**\class CandViewTreeMaker CandViewTreeMaker.cc Misc/TreeMaker/src/CandViewTreeMaker.cc

 Description: [one line class summary]

 Implementation:
    [Notes on implementation]
*/
//
// Original Author:  Jan Veverka
//      Created:  Mon Apr  4 21:25:02 CEST 2011
// $Id: CandViewTreeMaker.cc,v 1.1 2011/04/18 15:55:21 veverka Exp $
//
//


#include "Misc/TreeMaker/interface/TreeMaker.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "FWCore/Framework/interface/MakerMacros.h"

namespace cit {
  typedef TreeMaker<reco::CandidateView> CandViewTreeMaker;
} // end of namespace cit


//define this as a plug-in
using cit::CandViewTreeMaker;
DEFINE_FWK_MODULE(CandViewTreeMaker);
