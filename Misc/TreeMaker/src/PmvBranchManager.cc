#include "CommonTools/UtilAlgos/interface/DeltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterFunctionFactory.h"

#include "Misc/TreeMaker/interface/PmvBranchManager.h"

PmvBranchManager::PmvBranchManager(edm::ParameterSet const& iConfig) :
  crackCorrector_( EcalClusterFunctionFactory::get()->create(
                     "EcalClusterCrackCorrection",
                     iConfig ) ),
  src_( iConfig.getParameter<edm::InputTag>("src") ),
  genParticleSrc_( iConfig.getParameter<edm::InputTag>("genParticleSrc") ),
  primaryVertexSrc_( iConfig.getParameter<edm::InputTag>("primaryVertexSrc") ),
  sizeName_( iConfig.getUntrackedParameter<std::string>("sizeName") ),
  isMC_( iConfig.getParameter<bool>("isMC") ),
  b_phoMomPdgId_(0),
  b_phoMomStatus_(0),
  b_isFSR_(0),
  b_isISR_(0),
  b_phoIEtaX_(0),
  b_phoIPhiY_(0),
  b_muNearIEtaX_(0),
  b_muNearIPhiY_(0),
  b_muNearIsEB_(0),
  b_muNearIndex_(0),
  b_phoGenE_(0),
  b_phoGenEt_(0),
  b_phoGenEta_(0),
  b_phoCrackCorr_(0)
{}

PmvBranchManager::~PmvBranchManager() {}

void
PmvBranchManager::init(TTree& tree)
{
  tree.Branch("nVertices", &nVertices_, "nVertices/I");

  std::string leafList;
  leafList = std::string("phoMomPdgId") + "[" + sizeName_ + "]/I";
  b_phoMomPdgId_ = tree.Branch("phoMomPdgId", &(phoMomPdgId_[0]), leafList.c_str() );

  leafList = std::string("phoMomStatus") + "[" + sizeName_ + "]/I";
  b_phoMomStatus_= tree.Branch("phoMomStatus", &(phoMomStatus_[0]), leafList.c_str() );

  leafList = std::string("isFSR") + "[" + sizeName_ + "]/I";
  b_isFSR_ = tree.Branch("isFSR", &(isFSR_[0]), leafList.c_str() );

  leafList = std::string("isISR") + "[" + sizeName_ + "]/I";
  b_isISR_ = tree.Branch("isISR", &(isISR_[0]), leafList.c_str() );

  leafList = std::string("phoIEtaX") + "[" + sizeName_ + "]/I";
  b_phoIEtaX_ = tree.Branch("phoIEtaX", &(phoIEtaX_[0]), leafList.c_str() );

  leafList = std::string("phoIPhiY") + "[" + sizeName_ + "]/I";
  b_phoIPhiY_ = tree.Branch("phoIPhiY", &(phoIPhiY_[0]), leafList.c_str() );

  leafList = std::string("muNearIEtaX") + "[" + sizeName_ + "]/I";
  b_muNearIEtaX_ = tree.Branch("muNearIEtaX", &(muNearIEtaX_[0]), leafList.c_str() );

  leafList = std::string("muNearIPhiY") + "[" + sizeName_ + "]/I";
  b_muNearIPhiY_ = tree.Branch("muNearIPhiY", &(muNearIPhiY_[0]), leafList.c_str() );

  leafList = std::string("muNearIsEB") + "[" + sizeName_ + "]/I";
  b_muNearIsEB_ = tree.Branch("muNearIsEB", &(muNearIsEB_[0]), leafList.c_str() );

  leafList = std::string("muNearIndex") + "[" + sizeName_ + "]/I";
  b_muNearIndex_ = tree.Branch("muNearIndex", &(muNearIndex_[0]), leafList.c_str() );

  leafList = std::string("phoGenE") + "[" + sizeName_ + "]/F";
  b_phoGenE_ = tree.Branch("phoGenE", &(phoGenE_[0]), leafList.c_str() );

  leafList = std::string("phoGenEt") + "[" + sizeName_ + "]/F";
  b_phoGenEt_ = tree.Branch("phoGenEt", &(phoGenEt_[0]), leafList.c_str() );

  leafList = std::string("phoGenEta") + "[" + sizeName_ + "]/F";
  b_phoGenEta_ = tree.Branch("phoGenEta", &(phoGenEta_[0]), leafList.c_str() );

  leafList = std::string("phoCrackCorr") + "[" + sizeName_ + "]/F";
  b_phoCrackCorr_ = tree.Branch("phoCrackCorr", &(phoCrackCorr_[0]), leafList.c_str() );
}

void
PmvBranchManager::getData( const edm::Event& iEvent,
                           const edm::EventSetup& iSetup )
{
  crackCorrector_->init( iSetup );

  LogDebug("SegFault") << "entering PmvBranchManager::getData(...) ";
  edm::Handle<edm::View<reco::Vertex> > primaryVertices;
  edm::Handle<reco::CompositeCandidateView> mmgCands;
  edm::Handle<reco::GenParticleCollection> genParticles;

  iEvent.getByLabel(primaryVertexSrc_, primaryVertices);
  iEvent.getByLabel(src_, mmgCands);
  iEvent.getByLabel(genParticleSrc_, genParticles);

  nVertices_ = primaryVertices->size();

  phoMomPdgId_ .clear();
  phoMomStatus_.clear();
  isFSR_.clear();
  isISR_.clear();
  phoIEtaX_.clear();
  phoIPhiY_.clear();
  muNearIEtaX_.clear();
  muNearIPhiY_.clear();
  muNearIsEB_.clear();
  muNearIndex_.clear();

  phoMomPdgId_.reserve( mmgCands->size() );
  phoMomStatus_.reserve( mmgCands->size() );
  isFSR_.reserve( mmgCands->size() );
  isISR_.reserve( mmgCands->size() );
  phoIEtaX_.reserve( mmgCands->size() );
  phoIPhiY_.reserve( mmgCands->size() );
  muNearIEtaX_.reserve( mmgCands->size() );
  muNearIPhiY_.reserve( mmgCands->size() );
  muNearIsEB_.reserve( mmgCands->size() );
  muNearIndex_.reserve( mmgCands->size() );

  phoGenE_.reserve( mmgCands->size() );
  phoGenEt_.reserve( mmgCands->size() );
  phoGenEta_.reserve( mmgCands->size() );
  phoCrackCorr_.reserve( mmgCands->size() );

  LogDebug("SegFault") << "loop over candidates ";
  // loop over mmg candidates
  for (size_t i=0; i < mmgCands->size(); ++i) {
    phoGenE_[i] = -1;
    phoGenEt_[i] = -1;
    phoGenEta_[i] = -99;
    phoCrackCorr_[i] = 1.;
    LogDebug("SegFault") << "getting photon ";
    const pat::Photon &
    photon = * ((const pat::Photon *)
              mmgCands->at(i).daughter("photon")->masterClonePtr().get());
    bool found = false;
    // check if you find a gen match
    LogDebug("SegFault") << "Checking gen match";
    if (isMC_ && photon.genParticle(0) ) {
      // look for the gen match in the (pruned) gen particle collection
      reco::GenParticleCollection::const_iterator genMatch;
      LogDebug("SegFault") << "Looping over gen particles.";
      for (genMatch = genParticles->begin(); genMatch != genParticles->end(); ++genMatch) {
        if (genMatch->pdgId()  == photon.genParticle(0)->pdgId() &&
            genMatch->status() == photon.genParticle(0)->status() &&
            genMatch->p4()     == photon.genParticle(0)->p4() )
        {
          LogDebug("SegFault") << "Found gen match";
          // found the gen match in gen particles.
          phoGenE_[i] = genMatch->energy();
          phoGenEt_[i] = genMatch->pt();
          phoGenEta_[i] = genMatch->eta();
          if (genMatch->numberOfMothers() > 0) {
              found = true;

              phoMomPdgId_ [i] = genMatch->mother(0)->pdgId();
              phoMomStatus_[i] = genMatch->mother(0)->status();

              // These criteria for ISR and FSR are specific for POWHEG + Pythia
              if (genMatch->pdgId() == 22 && abs(phoMomPdgId_[i]) == 22 &&
                  phoMomStatus_[i] == 3)
                isISR_[i] = 1;
              else
                isISR_[i] = 0;

              if (genMatch->pdgId() == 22 && abs(phoMomPdgId_[i]) == 13)
                isFSR_[i] = 1;
              else
                isFSR_[i] = 0;
          }
          break;
        } // if found the gen match in gen particles.
      } // for loop over genParticles
    } // if found gen match

    LogDebug("SegFault") << "didn't find photon gen match mother";

    if (!found) {
      // didn't find photon gen match mother
      phoMomPdgId_[i] = 0;
      phoMomStatus_[i] = 0;
      isISR_[i] = 0;
      isFSR_[i] = 0;
    }

    phoCrackCorr_[i] = getCrackCorrectionFactor( * photon.superCluster() );

    DetId id = photon.superCluster()->seed()->seed();
    phoIEtaX_[i] = photon.isEB() ? EBDetId(id).ieta() : EEDetId(id).ix();
    phoIPhiY_[i] = photon.isEB() ? EBDetId(id).iphi() : EEDetId(id).iy();

    // Extract the near muon
    const reco::CompositeCandidate * dimuon;
    const pat::Muon * muon1;
    const pat::Muon * muon2;
    const pat::Muon * nearMuon;
    const pat::Muon * farMuon;

    dimuon = (const reco::CompositeCandidate*) mmgCands->at(i).daughter("dimuon")->masterClonePtr().get();
    muon1 = (const pat::Muon*) dimuon->daughter("muon1")->masterClonePtr().get();
    muon2 = (const pat::Muon*) dimuon->daughter("muon2")->masterClonePtr().get();

    // Decide which muon is near and which is far
    DeltaR<pat::Muon, pat::Photon> deltaR;
    double dr1 = deltaR(*muon1, photon);
    double dr2 = deltaR(*muon2, photon);
    double drNear = dr1;

    if (dr1 < dr2) {
      nearMuon = muon1; farMuon  = muon2; drNear = dr1; muNearIndex_[i] = 1;
    } else {
      nearMuon = muon2; farMuon  = muon1; drNear = dr2; muNearIndex_[i] = 2;
    }

    if ( nearMuon->isEnergyValid() ) {
      DetId id = nearMuon->calEnergy().ecal_id;
      if (id.subdetId() == EcalBarrel) {
        muNearIEtaX_[i] = EBDetId(id).ieta();
        muNearIPhiY_[i] = EBDetId(id).iphi();
        muNearIsEB_[i] = 1;
      } else {
        muNearIEtaX_[i] = EEDetId(id).ix();
        muNearIPhiY_[i] = EEDetId(id).iy();
        muNearIsEB_[i] = 0;
      }
    } else {
      muNearIEtaX_[i] = 0;
      muNearIPhiY_[i] = 0;
      muNearIsEB_[i] = -1;
    }// end if nearMuon->isEnergyValid()

  } // end of loop over mmg candidates

  LogDebug("SegFault") << "updating branch addresses";

  // Reset the branch address, the vector may have been reallocated
  if (b_phoMomPdgId_ != 0) b_phoMomPdgId_->SetAddress( &(phoMomPdgId_[0]) );
  if (b_phoMomStatus_ != 0) b_phoMomStatus_->SetAddress( &(phoMomStatus_[0]) );
  if (b_isFSR_ != 0) b_isFSR_->SetAddress( &(isFSR_[0]) );
  if (b_isISR_ != 0) b_isISR_->SetAddress( &(isISR_[0]) );
  if (b_phoIEtaX_ != 0) b_phoIEtaX_->SetAddress( &(phoIEtaX_[0]) );
  if (b_phoIPhiY_ != 0) b_phoIPhiY_->SetAddress( &(phoIPhiY_[0]) );
  if (b_muNearIEtaX_ != 0) b_muNearIEtaX_->SetAddress( &(muNearIEtaX_[0]) );
  if (b_muNearIPhiY_ != 0) b_muNearIPhiY_->SetAddress( &(muNearIPhiY_[0]) );
  if (b_muNearIsEB_ != 0) b_muNearIsEB_->SetAddress( &(muNearIsEB_[0]) );
  if (b_muNearIndex_ != 0) b_muNearIndex_->SetAddress( &(muNearIndex_[0]) );
  if (b_phoGenE_ != 0) b_phoGenE_->SetAddress( &(phoGenE_[0]) );
  if (b_phoGenEt_ != 0) b_phoGenEt_->SetAddress( &(phoGenEt_[0]) );
  if (b_phoGenEta_ != 0) b_phoGenEta_->SetAddress( &(phoGenEta_[0]) );
  if (b_phoCrackCorr_ != 0) b_phoCrackCorr_->SetAddress( &(phoCrackCorr_[0]) );

  LogDebug("SegFault") << "exitting";
}

float
PmvBranchManager::getCrackCorrectionFactor( const reco::SuperCluster & sc )
const
{
//   double crackcor = 1.;
  double correctedEnergy = 0.;
  for ( reco::CaloCluster_iterator cIt = sc.clustersBegin();
        cIt != sc.clustersEnd(); ++cIt )
  {
    const reco::CaloCluster & cc = **cIt;
/*    crackcor *= (
                  (
                    sc.rawEnergy() +
                    cc.energy() * ( crackCorrector_->getValue(cc) - 1. )
                  ) / sc.rawEnergy()
                );*/
    correctedEnergy += cc.energy() * crackCorrector_->getValue(cc); // new way
  }
  return correctedEnergy / sc.rawEnergy(); // new way
//   return crackcor;
} // PmvBranchManager::getClusterCorrectionFactor
