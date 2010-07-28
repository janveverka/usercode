// #include <map>
// #include <string>
#include <iostream>

#include "TH1.h"
#include "TMath.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/CandUtils/interface/AddFourMomenta.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/UtilAlgos/interface/DeltaR.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Candidate/interface/VertexCompositeCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/CaloRecHit/interface/CaloCluster.h"

#include "JPsi/MuMu/interface/MuMuGammaTree.h"

class MuMuGammaTreeMaker : public edm::EDAnalyzer {

public:
  explicit MuMuGammaTreeMaker(const edm::ParameterSet&);
  ~MuMuGammaTreeMaker();

private:
  typedef math::XYZPoint Point;
  typedef math::XYZVector Vector;
  typedef math::XYZTLorentzVector LorentzVector;

  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  double dxy(const reco::VertexCompositeCandidate&,
             const Point& beamSpot = Point(0,0,0)
             ) const;
  double dz(const reco::VertexCompositeCandidate&,
            const Point& beamSpot = Point(0,0,0)
            ) const;
  double dsz(const reco::VertexCompositeCandidate&,
             const Point& beamSpot = Point(0,0,0)
             ) const;
  double rho(const reco::VertexCompositeCandidate&,
             const Point& beamSpot = Point(0,0,0)
             ) const;

  MuMuGammaTree tree_;

  // input tags
  edm::InputTag photonSrc_;
  edm::InputTag muonSrc_;
  edm::InputTag dimuonSrc_;
  edm::InputTag beamSpotSrc_;
  edm::InputTag primaryVertexSrc_;
  edm::InputTag ebClusterSrc_;
  bool isMC_;

};

#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

MuMuGammaTreeMaker::MuMuGammaTreeMaker(const edm::ParameterSet& iConfig):
  tree_(),
  photonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("photonSrc")),
  muonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("muonSrc")),
  dimuonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("dimuonSrc")),
  beamSpotSrc_(iConfig.getUntrackedParameter<edm::InputTag>("beamSpotSrc")),
  primaryVertexSrc_(iConfig.getUntrackedParameter<edm::InputTag>("primaryVertexSrc")),
  ebClusterSrc_(iConfig.getUntrackedParameter<edm::InputTag>("ebClusterSrc")),
  isMC_(iConfig.getUntrackedParameter<bool>("isMC"))
{
}

MuMuGammaTreeMaker::~MuMuGammaTreeMaker()
{
}

/// dxy parameter. (This is the transverse impact parameter w.r.t. to beamSpot, see DataFormats/TrackReco/interface/TrackBase.h
double MuMuGammaTreeMaker::dxy(const reco::VertexCompositeCandidate& cand,
                              const Point& beamSpot
                              ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  return (- vx * cand.py() + vy * cand.px() ) / cand.pt();
}


/// dsz parameter, see DataFormats/TrackReco/interface/TrackBase.h
double MuMuGammaTreeMaker::dsz(const reco::VertexCompositeCandidate& cand,
                              const Point& beamSpot
                              ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  double vz = cand.vz() - beamSpot.Z();
  return vz * cand.pt() / cand.p() - (vx * cand.px() + vy * cand.py() ) / cand.pt() * (cand.pz() / cand.p() );
}


/// dz parameter (= dsz/cos(lambda)). This is the track z0 w.r.t beamSpot,
double MuMuGammaTreeMaker::dz(const reco::VertexCompositeCandidate& cand,
                             const Point& beamSpot
                             ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  double vz = cand.vz() - beamSpot.Z();
  return vz - (vx * cand.px() + vy * cand.py() ) / cand.pt() * (cand.pz() / cand.pt() );
}

/// rho parameter = distance in the xy-plane
double MuMuGammaTreeMaker::rho(const reco::VertexCompositeCandidate& cand,
                              const Point& beamSpot
                              ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  return sqrt(vx*vx + vy*vy);
}


void
MuMuGammaTreeMaker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  tree_.initLeafVariables();


  // get muon collection
  edm::Handle<edm::View<pat::Muon> > muons;
  iEvent.getByLabel(muonSrc_,muons);

  // get photon collection
  edm::Handle<edm::View<pat::Photon> > photons;
  iEvent.getByLabel(photonSrc_,photons);

  // get dimuon collection
  edm::Handle<reco::VertexCompositeCandidateView> dimuons;
  iEvent.getByLabel(dimuonSrc_,dimuons);

  edm::Handle<reco::BeamSpot> beamSpot;
  if (!isMC_) iEvent.getByLabel(beamSpotSrc_, beamSpot);

  edm::Handle<edm::View<reco::Vertex> > primaryVertices;
  if (!isMC_) iEvent.getByLabel(primaryVertexSrc_, primaryVertices);

  edm::Handle<edm::View<reco::CaloCluster> > ebClusters;
  iEvent.getByLabel(ebClusterSrc_, ebClusters);



  tree_.run   = iEvent.run();
  tree_.lumi  = iEvent.id().luminosityBlock();
  tree_.event = iEvent.id().event();

  // TODO: ADD THE HLT BITS
/*  tree_.L1DoubleMuOpen    = dimuon->L1DoubleMuOpen();
  tree_.HLT_Mu3           = dimuon->HLT_Mu3();
  tree_.HLT_Mu9           = dimuon->HLT_Mu9();*/

  tree_.nDimuons = dimuons->size();
  if (tree_.nDimuons > MuMuGammaTree::maxDimuons)
    tree_.nDimuons = MuMuGammaTree::maxDimuons;

  tree_.nMuons = muons->size();
  if (tree_.nMuons > MuMuGammaTree::maxMuons)
    tree_.nMuons = MuMuGammaTree::maxMuons;

  // loop over dimuons
  reco::VertexCompositeCandidateView::const_iterator dimuon;
  int i;
  for(dimuon = dimuons->begin(), i=0;
      i < tree_.nDimuons; ++dimuon, ++i) {


    tree_.mass[i]              = dimuon->mass();
    tree_.pt[i]                = dimuon->pt();
    tree_.eta[i]               = dimuon->eta();
    tree_.phi[i]               = dimuon->phi();
    tree_.y[i]                 = dimuon->y();
    tree_.p[i]                 = dimuon->p();
    tree_.charge[i]            = dimuon->charge();

    tree_.vProb [i] = TMath::Prob(dimuon->vertexChi2(),
                                      dimuon->vertexNdof()
                                      );
    tree_.vrho  [i] = rho(*dimuon);
    tree_.vrhoBS[i] = rho(*dimuon, isMC_ ? Point(0,0,0) : beamSpot->position() );
    tree_.vrhoPV[i] = rho(*dimuon, isMC_ ? Point(0,0,0) : primaryVertices->at(0).position() );
    tree_.vx    [i] = dimuon->vx();
    tree_.vxBS  [i] = dimuon->vx() - (isMC_ ? 0 : beamSpot->position().X());
    tree_.vxPV  [i] = dimuon->vx() - (isMC_ ? 0 : primaryVertices->at(0).position().X());
    tree_.vy    [i] = dimuon->vy();
    tree_.vyBS  [i] = dimuon->vy() - (isMC_ ? 0 : beamSpot->position().Y());
    tree_.vyPV  [i] = dimuon->vy() - (isMC_ ? 0 : primaryVertices->at(0).position().Y());
    tree_.vz    [i] = dimuon->vz();
    tree_.vzBS  [i] = dimuon->vz() - (isMC_ ? 0 : beamSpot->position().Z());
    tree_.vzPV  [i] = dimuon->vz() - (isMC_ ? 0 : primaryVertices->at(0).position().Z());

    tree_.d0   [i] = - dxy(*dimuon);
    tree_.d0BS [i] = - dxy(*dimuon, isMC_ ? Point(0,0,0) : beamSpot->position() );
    tree_.d0PV [i] = - dxy(*dimuon, isMC_ ? Point(0,0,0) : primaryVertices->at(0).position() );
    tree_.dz   [i] = dz(*dimuon);
    tree_.dzBS [i] = dz(*dimuon, isMC_ ? Point(0,0,0) : beamSpot->position() );
    tree_.dzPV [i] = dz(*dimuon, isMC_ ? Point(0,0,0) : primaryVertices->at(0).position() );
    tree_.dsz  [i] = dsz(*dimuon);
    tree_.dszBS[i] = dsz(*dimuon, isMC_ ? Point(0,0,0) : beamSpot->position() );
    tree_.dszPV[i] = dsz(*dimuon, isMC_ ? Point(0,0,0) : primaryVertices->at(0).position() );
    const double pdgMassJPsi  =  3.097,
                 pdgMassPsi2S =  3.686,
                 pdgMassY1S   =  9.460,
                 pdgMassY2S   = 10.023,
                 pdgMassY3S   = 10.355,
                 pdgMassZ     = 91.187;
    const int pdgIdJPsi  =    443,
              pdgIdPsi2S = 100443,
              pdgIdY1S   =    553,
              pdgIdY2S   = 100553,
              pdgIdY3S   = 200553,
              pdgIdZ     =     23;

    const double epsilon = 0.025;
    if ( dimuon->charge() == 0 ) {
      if ( dimuon->mass() > (1. - epsilon) * pdgMassJPsi &&
           dimuon->mass() < (1. + epsilon) * pdgMassJPsi )
        tree_.pdgId[i] = pdgIdJPsi;
      else if ( dimuon->mass() > (1. - epsilon) * pdgMassPsi2S &&
                dimuon->mass() < (1. + epsilon) * pdgMassPsi2S )
        tree_.pdgId[i] = pdgIdPsi2S;
      else if ( dimuon->mass() > (1. - epsilon) * pdgMassY1S &&
                dimuon->mass() < (1. + epsilon) * pdgMassY1S )
        tree_.pdgId[i] = pdgIdY1S;
      else if ( dimuon->mass() > (1. - epsilon) * pdgMassY2S &&
                dimuon->mass() < 0.5 * (pdgMassY2S + pdgMassY3S) )
        tree_.pdgId[i] = pdgIdY2S;
      else if ( dimuon->mass() >= 0.5 * (pdgMassY2S + pdgMassY3S) &&
                dimuon->mass() < (1. + epsilon) * pdgMassY3S)
        tree_.pdgId[i] = pdgIdY3S;
      else if ( dimuon->mass() > (1. - epsilon) * pdgMassZ &&
                dimuon->mass() < (1. + epsilon) * pdgMassZ)
        tree_.pdgId[i] = pdgIdZ;
    } else {
      tree_.pdgId[i] = 0;
    }

    // get the daughters
    const reco::CandidateBaseRef dau1 = dimuon->daughter(0)->masterClone();
    const reco::CandidateBaseRef dau2 = dimuon->daughter(1)->masterClone();
    double cosOpeningAngle = dau1->momentum().Dot(dau2->momentum()) /
                             ( dau1->p() * dau2->p() );
    tree_.backToBack[i] = 0.5 * (1. - cosOpeningAngle);

    tree_.dau1[i] = dau1.key();
    tree_.dau2[i] = dau2.key();
  } // loop over dimuons

  // loop over muons
  edm::View<pat::Muon>::const_iterator mu;
  for(mu = muons->begin(), i=0; i < tree_.nMuons; ++mu, ++i) {
    // set the daughter leafs
    tree_.muPt[i]                      = mu->pt();
    tree_.muEta[i]                     = mu->eta();
    tree_.muPhi[i]                     = mu->phi();
    tree_.muP[i]                       = mu->p();
    tree_.muCharge[i]                  = mu->charge();
    tree_.muSiNormalizedChi2[i]        = mu->innerTrack()->normalizedChi2();
    tree_.muSiD0[i]                    = mu->innerTrack()->d0();
    tree_.muSiD0BS[i]                  = - mu->innerTrack()->dxy( isMC_ ? Point(0,0,0) : beamSpot->position() );
    tree_.muSiD0PV[i]                  = - mu->innerTrack()->dxy( isMC_ ? Point(0,0,0) : primaryVertices->at(0).position() );
    tree_.muSiDz[i]                    = mu->innerTrack()->dz();
    tree_.muSiDzBS[i]                  = mu->innerTrack()->dz( isMC_ ? Point(0,0,0) : beamSpot->position() );
    tree_.muSiDzPV[i]                  = mu->innerTrack()->dz( isMC_ ? Point(0,0,0) : primaryVertices->at(0).position() );
    tree_.muSiDsz[i]                   = mu->innerTrack()->dsz();
    tree_.muSiDszBS[i]                 = mu->innerTrack()->dsz( isMC_ ? Point(0,0,0) : beamSpot->position() );
    tree_.muSiDszPV[i]                 = mu->innerTrack()->dsz( isMC_ ? Point(0,0,0) : primaryVertices->at(0).position() );
    tree_.muSiHits[i]                  = mu->innerTrack()->found();
    tree_.muPixelHits[i]               = mu->innerTrack()->hitPattern().numberOfValidPixelHits();
    // count stations
    unsigned nStations = 0, stationMask = mu->stationMask();
    for (; stationMask; nStations++)
      stationMask &= stationMask - 1; // clear the least significant bit set
    tree_.muStations[i]                = nStations;
    tree_.muVz[i]                      = mu->vz();
    tree_.muIsGlobalMuon[i]            = mu->isGlobalMuon();
    tree_.muIsTrackerMuon[i]           = mu->isTrackerMuon();
    tree_.muIsTMLastStationAngTight[i] = mu->muonID("TMLastStationAngTight");
    tree_.muIsTrackerMuonArbitrated[i] = mu->muonID("TrackerMuonArbitrated");
    tree_.muTrackIso[i]                = mu->trackIso();
    tree_.muEcalIso[i]                 = mu->ecalIso();
    tree_.muHcalIso[i]                 = mu->hcalIso();
//     tree_.muHltMu9Match[i]             = mu->hltMu9Match();
  } // loop over muons

  tree_.applyJPsiSelection();
  tree_.applyYSelection();
  tree_.applyZSelection();

  tree_.setOrderByMuQAndPt();
  tree_.setOrderByVProb();

  tree_.setCorrectedMassJPsi();
  tree_.setCorrectedMassY();

  // choose a primary dimuon
  int primaryDimuon = -1;
  for (i=0; i < tree_.nDimuons && primaryDimuon < -1; ++i)
    if (tree_.isZCand[i] && 60. < tree_.mass[i])
      primaryDimuon = i;
  for (i=0; i < tree_.nDimuons && primaryDimuon < -1; ++i)
    if (tree_.isYCand[i] && 8. < tree_.mass[i] && tree_.mass[i] < 12.)
      primaryDimuon = i;
  for (i=0; i < tree_.nDimuons && primaryDimuon < -1; ++i)
    if (tree_.isJPsiCand[i] && 2.6 < tree_.mass[i] && tree_.mass[i] < 3.5)
      primaryDimuon = i;
  for (i=0; i < tree_.nDimuons && primaryDimuon < -1; ++i)
    if (tree_.orderByVProb[i] == 0)
      primaryDimuon = i;
  if (primaryDimuon < 0) // this should never happen
    primaryDimuon = 0;

  // set the photon vertex to the vertex of the primary dimuon
  Point phoVertex = (*dimuons)[primaryDimuon].vertex();


  // loop over photons
  int nPhotons = photons->size();
  if ( nPhotons <= MuMuGammaTree::maxPhotons)
    tree_.nPhotons = nPhotons;
  else
    tree_.nPhotons = MuMuGammaTree::maxPhotons;

  tree_.nMuMuGammas = tree_.nPhotons; // use primary dimuons only

  // loop over photons
  edm::View<pat::Photon>::const_iterator pho;
  for (pho = photons->begin(), i=0; i < tree_.nPhotons; ++i, ++pho) {
    tree_.phoPt[i] = pho->pt();
    tree_.phoEta[i] = pho->eta();
    tree_.phoPhi[i] = pho->phi();
    tree_.phoEcalIso[i] = pho->ecalIso();
    tree_.phoHcalIso[i] = pho->hcalIso();
    tree_.phoTrackIso[i] = pho->trackIso();
    tree_.phoHadronicOverEm[i] = pho->hadronicOverEm();
    tree_.phoSigmaIetaIeta[i] = pho->sigmaIetaIeta();

    reco::CompositeCandidate dimuon = (*dimuons)[primaryDimuon];
    reco::CompositeCandidate mmg;
    mmg.addDaughter(dimuon, "dimuon");
    mmg.addDaughter(*pho, "photon");
    AddFourMomenta addP4;
    addP4.set(mmg);
    tree_.mmgMass[i] = mmg.mass();
    tree_.mmgDimuon[i] = primaryDimuon;
    tree_.mmgPhoton[i] = i;

    DeltaR<pat::Photon, reco::Candidate> deltaR;
    double dr1 = deltaR( *pho, *dimuon.daughter(0) );
    double dr2 = deltaR( *pho, *dimuon.daughter(1) );
    if (dr1 < dr2)  tree_.mmgDeltaRNear[i] = dr1;
    else            tree_.mmgDeltaRNear[i] = dr2;


  } // loop over photons


  // loop over ebclusters
/*  edm::View<reco::CaloCluster>::const_iterator cluster;
  for(cluster = ebClusters->begin(), i=0; i < tree_.nPhotons; ++cluster, ++i) {

    Vector phoDirection = cluster->position() - phoVertex;
    Vector phoP = cluster->energy() * phoDirection.unit();
    LorentzVector phoP4( phoP.x(), phoP.y(), phoP.z(), cluster->energy() );
    reco::LeafCandidate pho(0, phoP4, phoVertex);

    tree_.phoPt[i] = pho.pt();
  }*/


  // only store interesting events
  tree_.Fill();
}

void
MuMuGammaTreeMaker::beginJob()
{
  // register to the TFileService
  edm::Service<TFileService> fs;

  // book the tree:
  std::cout << "MuMuGammaTreeMaker: booking tree" << std::endl;
  TTree * tree = fs->make<TTree>("mmg", "MuMuGamma tree");
  tree_.init(tree);
  tree_.initGamma(tree);
}

void
MuMuGammaTreeMaker::endJob()
{
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MuMuGammaTreeMaker);
