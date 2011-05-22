#include "CommonTools/UtilAlgos/interface/DeltaR.h"
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
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "Misc/TreeMaker/interface/GenBranchManager.h"

GenBranchManager::GenBranchManager(edm::ParameterSet const& iConfig) :
  src_( iConfig.getParameter<edm::InputTag>("src") ),
  genParticleSrc_( iConfig.getParameter<edm::InputTag>("genParticleSrc") ),
  sizeName_( iConfig.getUntrackedParameter<std::string>("sizeName", "Size") ),
//   manageSize_( iConfig.getUntrackedParameter<bool>("manageSize", false) ),
  isMC_( iConfig.getParameter<bool>("isMC") ),
  prefix_( iConfig.getUntrackedParameter<std::string>("prefix", "") ),
  b_MomPdgId_(0),
  b_MomStatus_(0),
  b_GMomPdgId_(0),
  b_GMomStatus_(0)
{}

GenBranchManager::~GenBranchManager() {}

void
GenBranchManager::init(TTree& tree)
{

  std::string branchName, leafList;
  branchName = prefix_ + "MomPdgId";
  leafList = branchName + "[" + sizeName_ + "]/I";
  b_MomPdgId_ = tree.Branch( branchName.c_str(),
                             &(MomPdgId_[0]),
                             leafList.c_str() );

  branchName = prefix_ + "MomStatus";
  leafList = branchName + "[" + sizeName_ + "]/I";
  b_MomStatus_ = tree.Branch( branchName.c_str(),
                              &(MomPdgId_[0]),
                              leafList.c_str() );

  branchName = prefix_ + "GMomPdgId";
  leafList = branchName + "[" + sizeName_ + "]/I";
  b_GMomPdgId_ = tree.Branch( branchName.c_str(),
                              &(MomPdgId_[0]),
                              leafList.c_str() );

  branchName = prefix_ + "GMomStatus";
  leafList = branchName + "[" + sizeName_ + "]/I";
  b_GMomStatus_ = tree.Branch( branchName.c_str(),
                               &(MomPdgId_[0]),
                               leafList.c_str() );

}

void
GenBranchManager::getData( const edm::Event& iEvent,
                           const edm::EventSetup& iSetup )
{
  LogDebug("SegFault") << "entering GenBranchManager::getData(...) ";

  typedef pat::Photon CandType;

  edm::Handle<edm::View<CandType> > srcCands;
  edm::Handle<reco::GenParticleCollection> genParticles;

  iEvent.getByLabel(src_, srcCands);
  iEvent.getByLabel(genParticleSrc_, genParticles);


  MomPdgId_ .clear();
  MomStatus_.clear();
  GMomPdgId_ .clear();
  GMomStatus_.clear();

  MomPdgId_.reserve( srcCands->size() );
  MomStatus_.reserve( srcCands->size() );
  GMomPdgId_.reserve( srcCands->size() );
  GMomStatus_.reserve( srcCands->size() );

  LogDebug("SegFault") << "loop over candidates ";
  // loop over source candidates
  for (size_t i=0; i < srcCands->size(); ++i) {
    LogDebug("SegFault") << "getting photon ";
    const CandType & cand = srcCands->at(i);
    bool foundMom = false;
    bool foundGMom = false;

    MomPdgId_  .push_back(0);
    MomStatus_ .push_back(0);
    GMomPdgId_ .push_back(0);
    GMomStatus_.push_back(0);

    // check if you find a gen match
    LogDebug("SegFault") << "Checking gen match";
    if (isMC_ && cand.genParticle(0) ) {
      // look for the gen match in the (pruned) gen particle collection
      reco::GenParticleCollection::const_iterator genMatch;
      LogDebug("SegFault") << "Looping over gen particles.";
      for ( genMatch = genParticles->begin();
            genMatch != genParticles->end(); ++genMatch ) {
        if (genMatch->pdgId()  == cand.genParticle(0)->pdgId() &&
            genMatch->status() == cand.genParticle(0)->status() &&
            genMatch->p4()     == cand.genParticle(0)->p4() )
        {
          LogDebug("SegFault") << "Found gen match";
          // found the gen match in gen particles.
          if (genMatch->numberOfMothers() > 0) {
            LogDebug("SegFault") << "Found gen match mom";
            foundMom = true;

            MomPdgId_ [i] = genMatch->mother(0)->pdgId();
            MomStatus_[i] = genMatch->mother(0)->status();
            LogDebug("SegFault") << "i MomPdgId MomStatus: "
                                 << i << " "
                                 << MomPdgId_ [i] << " "
                                 << MomStatus_[i];
          }

          LogDebug("SegFault") << "Checking gen match grand mom";
          if (foundMom == true && genMatch->mother(0)->numberOfMothers() > 0) {
            LogDebug("SegFault") << "Found gen match gand mom";
            foundGMom = true;

            GMomPdgId_ [i] = genMatch->mother(0)->mother(0)->pdgId();
            GMomStatus_[i] = genMatch->mother(0)->mother(0)->status();
            LogDebug("SegFault") << "i GMomPdgId GMomStatus: "
                                 << i << " "
                                 << GMomPdgId_ [i] << " "
                                 << GMomStatus_[i];
          }
          break;
        } // if found the gen match in gen particles.
      } // for loop over genParticles
    } // if found gen match

    LogDebug("SegFault") << "didn't find cand gen match mother";

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
  if (b_MomPdgId_ != 0) b_MomPdgId_->SetAddress( &(MomPdgId_[0]) );
  if (b_MomStatus_ != 0) b_MomStatus_->SetAddress( &(MomStatus_[0]) );
  if (b_GMomPdgId_ != 0) b_GMomPdgId_->SetAddress( &(GMomPdgId_[0]) );
  if (b_GMomStatus_ != 0) b_GMomStatus_->SetAddress( &(GMomStatus_[0]) );

  LogDebug("SegFault") << "exitting";
}
