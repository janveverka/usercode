#include "CommonTools/UtilAlgos/interface/DeltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
// #include "DataFormats/PatCandidates/interface/PATObject.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
// #include "DataFormats/PatCandidates/interface/Muon.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "Misc/TreeMaker/interface/DiphotonGenBranchManager.h"

DiphotonGenBranchManager::DiphotonGenBranchManager(edm::ParameterSet const& iConfig) :
  src_( iConfig.getParameter<edm::InputTag>("src") ),
  genParticleSrc_( iConfig.getParameter<edm::InputTag>("genParticleSrc") ),
  sizeName_( iConfig.getUntrackedParameter<std::string>("sizeName", "Size") ),
//   manageSize_( iConfig.getUntrackedParameter<bool>("manageSize", false) ),
  isMC_( iConfig.getParameter<bool>("isMC") ),
  prefix_( iConfig.getUntrackedParameter<std::string>("prefix", "") ),
  b_Mom1PdgId_(0),
  b_Mom1Status_(0),
  b_GMom1PdgId_(0),
  b_GMom1Status_(0),
  b_pho1MinDEtaGenEle_(0),
  b_pho1MinDPhiGenEle_(0),
  b_pho1GenElePt_(0),
  b_pho1GenEleCharge_(0),
  b_Mom2PdgId_(0),
  b_Mom2Status_(0),
  b_GMom2PdgId_(0),
  b_GMom2Status_(0),
  b_pho2MinDEtaGenEle_(0),
  b_pho2MinDPhiGenEle_(0),
  b_pho2GenElePt_(0),
  b_pho2GenEleCharge_(0)
{}

DiphotonGenBranchManager::~DiphotonGenBranchManager() {}

void
DiphotonGenBranchManager::init(TTree& tree)
{

  std::string branchName, leafList;

  branchName = prefix_ + "Mom1PdgId";
  leafList = branchName + "[" + sizeName_ + "]/I";
  b_Mom1PdgId_ = tree.Branch( branchName.c_str(),
                              &(Mom1PdgId_[0]),
                              leafList.c_str() );

  branchName = prefix_ + "Mom1Status";
  leafList = branchName + "[" + sizeName_ + "]/I";
  b_Mom1Status_ = tree.Branch( branchName.c_str(),
                               &(Mom1PdgId_[0]),
                               leafList.c_str() );

  branchName = prefix_ + "GMom1PdgId";
  leafList = branchName + "[" + sizeName_ + "]/I";
  b_GMom1PdgId_ = tree.Branch( branchName.c_str(),
                               &(Mom1PdgId_[0]),
                               leafList.c_str() );

  branchName = prefix_ + "pho1.minDEtaGenEle";
  leafList = branchName + "[" + sizeName_ + "]/F";
  b_pho1MinDEtaGenEle_ = tree.Branch( branchName.c_str(),
                                      &(pho1MinDEtaGenEle_[0]),
                                      leafList.c_str() );

  branchName = prefix_ + "pho1.minDPhiGenEle";
  leafList = branchName + "[" + sizeName_ + "]/F";
  b_pho1MinDPhiGenEle_ = tree.Branch( branchName.c_str(),
                                      &(pho1MinDPhiGenEle_[0]),
                                      leafList.c_str() );

  branchName = prefix_ + "pho1.genElePt";
  leafList = branchName + "[" + sizeName_ + "]/F";
  b_pho1GenElePt_ = tree.Branch( branchName.c_str(),
                                 &(pho1GenElePt_[0]),
                                 leafList.c_str() );

  branchName = prefix_ + "pho1.genEleCharge";
  leafList = branchName + "[" + sizeName_ + "]/I";
  b_pho1GenEleCharge_ = tree.Branch( branchName.c_str(),
                                     &(pho1GenEleCharge_[0]),
                                     leafList.c_str() );

  branchName = prefix_ + "Mom2PdgId";
  leafList = branchName + "[" + sizeName_ + "]/I";
  b_Mom2PdgId_ = tree.Branch( branchName.c_str(),
                              &(Mom2PdgId_[0]),
                              leafList.c_str() );

  branchName = prefix_ + "Mom2Status";
  leafList = branchName + "[" + sizeName_ + "]/I";
  b_Mom2Status_ = tree.Branch( branchName.c_str(),
                               &(Mom2PdgId_[0]),
                               leafList.c_str() );

  branchName = prefix_ + "GMom2PdgId";
  leafList = branchName + "[" + sizeName_ + "]/I";
  b_GMom2PdgId_ = tree.Branch( branchName.c_str(),
                               &(Mom2PdgId_[0]),
                               leafList.c_str() );

  branchName = prefix_ + "GMom2Status";
  leafList = branchName + "[" + sizeName_ + "]/I";
  b_GMom2Status_ = tree.Branch( branchName.c_str(),
                                &(Mom2PdgId_[0]),
                                leafList.c_str() );

  branchName = prefix_ + "pho2.minDEtaGenEle";
  leafList = branchName + "[" + sizeName_ + "]/F";
  b_pho2MinDEtaGenEle_ = tree.Branch( branchName.c_str(),
                                      &(pho2MinDEtaGenEle_[0]),
                                      leafList.c_str() );

  branchName = prefix_ + "pho2.minDPhiGenEle";
  leafList = branchName + "[" + sizeName_ + "]/F";
  b_pho2MinDPhiGenEle_ = tree.Branch( branchName.c_str(),
                                      &(pho2MinDPhiGenEle_[0]),
                                      leafList.c_str() );

  branchName = prefix_ + "pho2.genElePt";
  leafList = branchName + "[" + sizeName_ + "]/F";
  b_pho2GenElePt_ = tree.Branch( branchName.c_str(),
                                 &(pho2GenElePt_[0]),
                                 leafList.c_str() );

  branchName = prefix_ + "pho2.genEleCharge";
  leafList = branchName + "[" + sizeName_ + "]/I";
  b_pho2GenEleCharge_ = tree.Branch( branchName.c_str(),
                                     &(pho2GenEleCharge_[0]),
                                     leafList.c_str() );

}

void
DiphotonGenBranchManager::getData( const edm::Event& iEvent,
                                   const edm::EventSetup& iSetup )
{
  LogDebug("SegFault") << "entering DiphotonGenBranchManager::getData(...) ";

  typedef reco::CompositeCandidate CandType;
  typedef pat::Photon DauType;

  edm::Handle<edm::View<CandType> > srcCands;
  edm::Handle<reco::GenParticleCollection> genParticles;

  iEvent.getByLabel(src_, srcCands);
  iEvent.getByLabel(genParticleSrc_, genParticles);

  Mom1PdgId_  .clear();
  Mom1Status_ .clear();
  GMom1PdgId_ .clear();
  GMom1Status_.clear();
  pho1MinDEtaGenEle_.clear();
  pho1MinDPhiGenEle_.clear();
  pho1GenElePt_.clear();
  pho1GenEleCharge_.clear();

  Mom2PdgId_  .clear();
  Mom2Status_ .clear();
  GMom2PdgId_ .clear();
  GMom2Status_.clear();
  pho2MinDEtaGenEle_.clear();
  pho2MinDPhiGenEle_.clear();
  pho2GenElePt_.clear();
  pho2GenEleCharge_.clear();

  Mom1PdgId_  .reserve( srcCands->size() );
  Mom1Status_ .reserve( srcCands->size() );
  GMom1PdgId_ .reserve( srcCands->size() );
  GMom1Status_.reserve( srcCands->size() );
  pho1MinDEtaGenEle_.reserve( srcCands->size() );
  pho1MinDPhiGenEle_.reserve( srcCands->size() );
  pho1GenElePt_.reserve( srcCands->size() );
  pho1GenEleCharge_.reserve( srcCands->size() );


  Mom2PdgId_  .reserve( srcCands->size() );
  Mom2Status_ .reserve( srcCands->size() );
  GMom2PdgId_ .reserve( srcCands->size() );
  GMom2Status_.reserve( srcCands->size() );
  pho2MinDEtaGenEle_.reserve( srcCands->size() );
  pho2MinDPhiGenEle_.reserve( srcCands->size() );
  pho2GenEleCharge_ .reserve( srcCands->size() );

  LogDebug("SegFault") << "loop over candidates ";
  // loop over source candidates
  for (size_t i=0; i < srcCands->size(); ++i) {
//     LogDebug("SegFault") << "getting photon ";
    const CandType & cand = srcCands->at(i);

    bool foundMom1  = false;
    bool foundGMom1 = false;
    bool foundMom2  = false;
    bool foundGMom2 = false;

    Mom1PdgId_  .push_back(0);
    Mom1Status_ .push_back(0);
    GMom1PdgId_ .push_back(0);
    GMom1Status_.push_back(0);
    pho1MinDEtaGenEle_.push_back( 999 );
    pho1MinDPhiGenEle_.push_back( 999 );
    pho1GenElePt_     .push_back( 0 );
    pho1GenEleCharge_ .push_back( 0 );


    Mom2PdgId_  .push_back(0);
    Mom2Status_ .push_back(0);
    GMom2PdgId_ .push_back(0);
    GMom2Status_.push_back(0);
    pho2MinDEtaGenEle_.push_back( 999 );
    pho2MinDPhiGenEle_.push_back( 999 );
    pho2GenElePt_     .push_back( 0 );
    pho2GenEleCharge_ .push_back( 0 );

    // get the daughters
    const DauType & dau1 = dynamic_cast<const DauType&> (
                             * cand.daughter(0)->masterClonePtr().get()
                           );

    const DauType & dau2 = dynamic_cast<const DauType&> (
                             * cand.daughter(1)->masterClonePtr().get()
                           );

    // check if you find a gen match for dau1
//     LogDebug("SegFault") << "Checking gen match for dau1";
    if (isMC_ && dau1.genParticle(0) ) {
      // look for the gen match in the (pruned) gen particle collection
      reco::GenParticleCollection::const_iterator genMatch;
//       LogDebug("SegFault") << "Looping over gen particles.";
      for ( genMatch = genParticles->begin();
            genMatch != genParticles->end(); ++genMatch ) {
        if (genMatch->pdgId()  == dau1.genParticle(0)->pdgId() &&
            genMatch->status() == dau1.genParticle(0)->status() &&
            genMatch->p4()     == dau1.genParticle(0)->p4() )
        {
//           LogDebug("SegFault") << "Found gen match";
          // found the gen match in gen particles.
          if (genMatch->numberOfMothers() > 0) {
//             LogDebug("SegFault") << "Found gen match mom";
            foundMom1 = true;

            Mom1PdgId_ [i] = genMatch->mother(0)->pdgId();
            Mom1Status_[i] = genMatch->mother(0)->status();
/*            LogDebug("SegFault") << "i MomPdgId MomStatus: "
                                 << i << " "
                                 << Mom1PdgId_ [i] << " "
                                 << Mom1Status_[i];*/
          }

//           LogDebug("SegFault") << "Checking gen match grand mom";
          if (foundMom1 == true && genMatch->mother(0)->numberOfMothers() > 0) {
//             LogDebug("SegFault") << "Found gen match gand mom";
            foundGMom1 = true;

            GMom1PdgId_ [i] = genMatch->mother(0)->mother(0)->pdgId();
            GMom1Status_[i] = genMatch->mother(0)->mother(0)->status();
//             LogDebug("SegFault") << "i GMomPdgId GMomStatus: "
//                                  << i << " "
//                                  << GMom1PdgId_ [i] << " "
//                                  << GMom1Status_[i];
          }
          break;
        } // if found the gen match in gen particles.
      } // for loop over genParticles
    } // if found dau1 gen match

    // check if you find a gen match for dau2
    if (isMC_ && dau2.genParticle(0) ) {
      // look for the gen match in the (pruned) gen particle collection
      reco::GenParticleCollection::const_iterator genMatch;
      for ( genMatch = genParticles->begin();
            genMatch != genParticles->end(); ++genMatch ) {
        if (genMatch->pdgId()  == dau2.genParticle(0)->pdgId() &&
            genMatch->status() == dau2.genParticle(0)->status() &&
            genMatch->p4()     == dau2.genParticle(0)->p4() )
        {
          // found the gen match in gen particles.
          if (genMatch->numberOfMothers() > 0) {
            foundMom2 = true;

            Mom2PdgId_ [i] = genMatch->mother(0)->pdgId();
            Mom2Status_[i] = genMatch->mother(0)->status();
          }

          if (foundMom2 == true && genMatch->mother(0)->numberOfMothers() > 0) {
            foundGMom2 = true;

            GMom2PdgId_ [i] = genMatch->mother(0)->mother(0)->pdgId();
            GMom2Status_[i] = genMatch->mother(0)->mother(0)->status();
          }
          break;
        } // if found the gen match in gen particles.
      } // for loop over genParticles
    } // if found dau2 gen match


    // Find the nearest gen electron for both daughters.
    DeltaR<const DauType, const reco::GenParticle> deltaR;
    DeltaPhi<const DauType, const reco::GenParticle> deltaPhi;
    float minDR1 = 999.;
    float minDR2 = 999.;

    // Loop over gen electrons.
    LogDebug("EleMatch") << "Looping over gen electrons";
    for ( reco::GenParticleCollection::const_iterator
          genEle = genParticles->begin();
          genEle != genParticles->end(); ++genEle ) {

      if ( TMath::Abs( genEle->pdgId() ) != 11 ) continue;

      float dr1 = deltaR(dau1, *genEle);
      float dr2 = deltaR(dau2, *genEle);

      if (dr1 < minDR1) {
        // Found the nearest electron for daughter 1 so far.
        minDR1 = dr1;
        pho1MinDEtaGenEle_ [i] = dau1.eta() - genEle->eta();
        pho1MinDPhiGenEle_ [i] = deltaPhi(dau1, *genEle);
        pho1GenElePt_[i] = genEle->pt();
        pho1GenEleCharge_[i] = genEle->charge();

        LogDebug("EleMatch") << "i dr1 deta1 dphi1 elept: "
                              << i << " "
                              << dr1 << " "
                              << pho1MinDEtaGenEle_[i] << " "
                              << pho1MinDPhiGenEle_[i] << " "
                              << pho1GenElePt_ [i];
      }

      if (dr2 < minDR2) {
        // Found the nearest electron for daughter 2 so far.
        minDR2 = dr2;
        pho2MinDEtaGenEle_ [i] = dau2.eta() - genEle->eta();
        pho2MinDPhiGenEle_ [i] = deltaPhi(dau2, *genEle);
        pho2GenElePt_[i] = genEle->pt();
        pho2GenEleCharge_[i] = genEle->charge();

        LogDebug("EleMatch") << "i dr2 deta2 dphi2 elept: "
                              << i << " "
                              << dr2 << " "
                              << pho2MinDEtaGenEle_[i] << " "
                              << pho2MinDPhiGenEle_[i] << " "
                              << pho2GenElePt_ [i];
      }

    }  // End loop over gen electrons.

//     LogDebug("SegFault") << "didn't find dau2 gen match mother";

//     if (foundMom == false) {
//       // didn't find cand gen match mother
//       MomPdgId_[i] = 0;
//       MomStatus_[i] = 0;
//     }
//
//     if (foundGMom == false) {
//       // didn't find cand gen match grand mother
//       GMomPdgId_[i] = 0;
//       GMomStatus_[i] = 0;
//     }

  } // end of loop over src candidates

  LogDebug("SegFault") << "updating branch addresses";

  // Reset the branch address, the vector may have been reallocated
  if (b_Mom1PdgId_ != 0) b_Mom1PdgId_->SetAddress( &(Mom1PdgId_[0]) );
  if (b_Mom1Status_ != 0) b_Mom1Status_->SetAddress( &(Mom1Status_[0]) );
  if (b_GMom1PdgId_ != 0) b_GMom1PdgId_->SetAddress( &(GMom1PdgId_[0]) );
  if (b_GMom1Status_ != 0) b_GMom1Status_->SetAddress( &(GMom1Status_[0]) );
  if (b_pho1MinDEtaGenEle_ != 0)
    b_pho1MinDEtaGenEle_->SetAddress( &(pho1MinDEtaGenEle_[0]) );
  if (b_pho1MinDPhiGenEle_ != 0)
    b_pho1MinDPhiGenEle_->SetAddress( &(pho1MinDPhiGenEle_[0]) );
  if (b_pho1GenElePt_ != 0)
    b_pho1GenElePt_->SetAddress( &(pho1GenElePt_[0]) );
  if (b_pho1GenEleCharge_ != 0)
    b_pho1GenEleCharge_->SetAddress( &(pho1GenEleCharge_[0]) );

  if (b_Mom2PdgId_ != 0) b_Mom2PdgId_->SetAddress( &(Mom2PdgId_[0]) );
  if (b_Mom2Status_ != 0) b_Mom2Status_->SetAddress( &(Mom2Status_[0]) );
  if (b_GMom2PdgId_ != 0) b_GMom2PdgId_->SetAddress( &(GMom2PdgId_[0]) );
  if (b_GMom2Status_ != 0) b_GMom2Status_->SetAddress( &(GMom2Status_[0]) );
  if (b_pho2MinDEtaGenEle_ != 0)
    b_pho2MinDEtaGenEle_->SetAddress( &(pho2MinDEtaGenEle_[0]) );
  if (b_pho2MinDPhiGenEle_ != 0)
    b_pho2MinDPhiGenEle_->SetAddress( &(pho2MinDPhiGenEle_[0]) );
  if (b_pho2GenElePt_ != 0)
    b_pho2GenElePt_->SetAddress( &(pho2GenElePt_[0]) );
  if (b_pho2GenEleCharge_ != 0)
    b_pho2GenEleCharge_->SetAddress( &(pho2GenEleCharge_[0]) );

  LogDebug("SegFault") << "exitting";
}
