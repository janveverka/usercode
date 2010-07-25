#include <map>
#include <string>

#include "TH1.h"
#include "TMath.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/Candidate/interface/VertexCompositeCandidate.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"


#include "JPsi/MuMu/interface/DimuonsTree.h"

class DimuonsNtupelizer : public edm::EDAnalyzer {

public:
  explicit DimuonsNtupelizer(const edm::ParameterSet&);
  ~DimuonsNtupelizer();
  
private:
  typedef math::XYZPoint Point;

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
  
  DimuonsTree dimuonsTree_;

  // input tags  
  edm::InputTag photonSrc_;
  edm::InputTag muonSrc_;
  edm::InputTag dimuonSrc_;
  edm::InputTag beamSpotSrc_;
  edm::InputTag primaryVertexSrc_;

};

#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

DimuonsNtupelizer::DimuonsNtupelizer(const edm::ParameterSet& iConfig):
  dimuonsTree_(),
  photonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("photonSrc")),
  muonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("muonSrc")),
  dimuonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("dimuonSrc")),
  beamSpotSrc_(iConfig.getUntrackedParameter<edm::InputTag>("beamSpotSrc")),
  primaryVertexSrc_(iConfig.getUntrackedParameter<edm::InputTag>("primaryVertexSrc"))
{
}

DimuonsNtupelizer::~DimuonsNtupelizer()
{
}

/// dxy parameter. (This is the transverse impact parameter w.r.t. to beamSpot, see DataFormats/TrackReco/interface/TrackBase.h
double DimuonsNtupelizer::dxy(const reco::VertexCompositeCandidate& cand,
                              const Point& beamSpot
                              ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  return (- vx * cand.py() + vy * cand.px() ) / cand.pt();
}


/// dsz parameter, see DataFormats/TrackReco/interface/TrackBase.h
double DimuonsNtupelizer::dsz(const reco::VertexCompositeCandidate& cand,
                              const Point& beamSpot
                              ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  double vz = cand.vz() - beamSpot.Z();
  return vz * cand.pt() / cand.p() - (vx * cand.px() + vy * cand.py() ) / cand.pt() * (cand.pz() / cand.p() );
}


/// dz parameter (= dsz/cos(lambda)). This is the track z0 w.r.t beamSpot, 
double DimuonsNtupelizer::dz(const reco::VertexCompositeCandidate& cand,
                             const Point& beamSpot
                             ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  double vz = cand.vz() - beamSpot.Z();
  return vz - (vx * cand.px() + vy * cand.py() ) / cand.pt() * (cand.pz() / cand.pt() );
}

/// rho parameter = distance in the xy-plane
double DimuonsNtupelizer::rho(const reco::VertexCompositeCandidate& cand,
                              const Point& beamSpot
                              ) const
{
  double vx = cand.vx() - beamSpot.X();
  double vy = cand.vy() - beamSpot.Y();
  return sqrt(vx*vx + vy*vy);
}


void
DimuonsNtupelizer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  dimuonsTree_.initLeafVariables();

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
  iEvent.getByLabel(beamSpotSrc_, beamSpot);
  
  edm::Handle<edm::View<reco::Vertex> > primaryVertices;
  iEvent.getByLabel(primaryVertexSrc_, primaryVertices);

  // loop over dimuons
  reco::VertexCompositeCandidateView::const_iterator dimuon;
  for(dimuon = dimuons->begin(), int i=0;
      dimuon != dimuons->end(); ++dimuon, ++i) {

    // get the daughters
    const reco::Candidate * dau1 = dimuon->daughter(0)->masterClone().get();
    const reco::Candidate * dau2 = dimuon->daughter(1)->masterClone().get();
    const pat::Muon * mu1 = dynamic_cast<const pat::Muon*>(dau1);
    const pat::Muon * mu2 = dynamic_cast<const pat::Muon*>(dau2);
  
    dimuonsTree_.run   = iEvent.run();
    dimuonsTree_.lumi  = iEvent.id().luminosityBlock();
    dimuonsTree_.event = iEvent.id().event();

    // set the dimuon variables
    dimuonsTree_.mass[i]       = dimuon->mass();
    dimuonsTree_.pt         = dimuon->pt();
    dimuonsTree_.eta        = dimuon->eta();
    dimuonsTree_.phi        = dimuon->phi();
    dimuonsTree_.y          = dimuon->y();
    dimuonsTree_.p          = dimuon->p();
    dimuonsTree_.charge     = dimuon->charge();
    dimuonsTree_.vProb  = TMath::Prob(dimuon->vertexChi2(),
                                      dimuon->vertexNdof()
                                      );

    dimuonsTree_.vrho   = rho(*dimuon);
    dimuonsTree_.vrhoBS = rho(*dimuon, beamSpot->position() );
    dimuonsTree_.vrhoPV = rho(*dimuon, primaryVertices->at(0).position() );
    dimuonsTree_.vx     = dimuon->vx();
    dimuonsTree_.vxBS   = dimuon->vx() - beamSpot->position().X();
    dimuonsTree_.vxPV   = dimuon->vx() - primaryVertices->at(0).position().X();
    dimuonsTree_.vy     = dimuon->vy();
    dimuonsTree_.vyBS   = dimuon->vy() - beamSpot->position().Y();
    dimuonsTree_.vyPV   = dimuon->vy() - primaryVertices->at(0).position().Y();
    dimuonsTree_.vz     = dimuon->vz();
    dimuonsTree_.vzBS   = dimuon->vz() - beamSpot->position().Z();
    dimuonsTree_.vzPV   = dimuon->vz() - primaryVertices->at(0).position().Z();

    dimuonsTree_.d0    = - dxy(*dimuon);
    dimuonsTree_.d0BS  = - dxy(*dimuon, beamSpot->position() );
    dimuonsTree_.d0PV  = - dxy(*dimuon, primaryVertices->at(0).position() );
    dimuonsTree_.dz    = dz(*dimuon);
    dimuonsTree_.dzBS  = dz(*dimuon, beamSpot->position() );
    dimuonsTree_.dzPV  = dz(*dimuon, primaryVertices->at(0).position() );
    dimuonsTree_.dsz   = dsz(*dimuon);
    dimuonsTree_.dszBS = dsz(*dimuon, beamSpot->position() );
    dimuonsTree_.dszPV = dsz(*dimuon, primaryVertices->at(0).position() );
//    dimuonsTree_.pdgId  = dimuon->pdgId();
    double cosOpeningAngle = (mu1->momentum().Dot( mu2->momentum() ) ) / ( mu1->p() * mu2->p() );
    dimuonsTree_.backToBack = 0.5 * (1. - cosOpeningAngle);

    // set the daughter leafs
    dimuonsTree_.mu1Pt                      = mu1->pt();
    dimuonsTree_.mu2Pt                      = mu2->pt();
    dimuonsTree_.mu1Eta                     = mu1->eta();
    dimuonsTree_.mu2Eta                     = mu2->eta();
    dimuonsTree_.mu1Phi                     = mu1->phi();
    dimuonsTree_.mu2Phi                     = mu2->phi();
    dimuonsTree_.mu1P                       = mu1->p();
    dimuonsTree_.mu2P                       = mu2->p();
    dimuonsTree_.mu1Charge                  = mu1->charge();
    dimuonsTree_.mu2Charge                  = mu2->charge();
    dimuonsTree_.mu1SiNormalizedChi2        = mu1->innerTrack()->normalizedChi2();
    dimuonsTree_.mu2SiNormalizedChi2        = mu2->innerTrack()->normalizedChi2();
    dimuonsTree_.mu1SiD0                    = mu1->innerTrack()->d0();
    dimuonsTree_.mu2SiD0                    = mu2->innerTrack()->d0();
    dimuonsTree_.mu1SiD0BS                  = - mu1->innerTrack()->dxy( beamSpot->position() );
    dimuonsTree_.mu2SiD0BS                  = - mu2->innerTrack()->dxy( beamSpot->position() );
    dimuonsTree_.mu1SiD0PV                  = - mu1->innerTrack()->dxy( primaryVertices->at(0).position() );
    dimuonsTree_.mu2SiD0PV                  = - mu2->innerTrack()->dxy( primaryVertices->at(0).position() );
    dimuonsTree_.mu1SiDz                    = mu1->innerTrack()->dz();
    dimuonsTree_.mu2SiDz                    = mu2->innerTrack()->dz();
    dimuonsTree_.mu1SiDzBS                  = mu1->innerTrack()->dz( beamSpot->position() );
    dimuonsTree_.mu2SiDzBS                  = mu2->innerTrack()->dz( beamSpot->position() );
    dimuonsTree_.mu1SiDzPV                  = mu1->innerTrack()->dz( primaryVertices->at(0).position() );
    dimuonsTree_.mu2SiDzPV                  = mu2->innerTrack()->dz( primaryVertices->at(0).position() );
    dimuonsTree_.mu1SiDsz                   = mu1->innerTrack()->dsz();
    dimuonsTree_.mu2SiDsz                   = mu2->innerTrack()->dsz();
    dimuonsTree_.mu1SiDszBS                 = mu1->innerTrack()->dsz( beamSpot->position() );
    dimuonsTree_.mu2SiDszBS                 = mu2->innerTrack()->dsz( beamSpot->position() );
    dimuonsTree_.mu1SiDszPV                 = mu1->innerTrack()->dsz( primaryVertices->at(0).position() );
    dimuonsTree_.mu2SiDszPV                 = mu2->innerTrack()->dsz( primaryVertices->at(0).position() );
    dimuonsTree_.mu1SiHits                  = mu1->innerTrack()->found();
    dimuonsTree_.mu2SiHits                  = mu2->innerTrack()->found();
    dimuonsTree_.mu1PixelHits               = mu1->innerTrack()->hitPattern().numberOfValidPixelHits();
    dimuonsTree_.mu2PixelHits               = mu2->innerTrack()->hitPattern().numberOfValidPixelHits();
    dimuonsTree_.mu1IsGlobalMuon            = mu1->isGlobalMuon();
    dimuonsTree_.mu2IsGlobalMuon            = mu2->isGlobalMuon();
    dimuonsTree_.mu1IsTrackerMuon           = mu1->isTrackerMuon();
    dimuonsTree_.mu2IsTrackerMuon           = mu2->isTrackerMuon();
    dimuonsTree_.mu1IsTMLastStationAngTight = mu1->muonID("TMLastStationAngTight");
    dimuonsTree_.mu2IsTMLastStationAngTight = mu2->muonID("TMLastStationAngTight");
    dimuonsTree_.mu1IsTrackerMuonArbitrated = mu1->muonID("TrackerMuonArbitrated");
    dimuonsTree_.mu2IsTrackerMuonArbitrated = mu2->muonID("TrackerMuonArbitrated");
    dimuonsTree_.mu1TrackIso                = mu1->trackIso();
    dimuonsTree_.mu2TrackIso                = mu2->trackIso();
    dimuonsTree_.mu1EcalIso                 = mu1->ecalIso();
    dimuonsTree_.mu2EcalIso                 = mu2->ecalIso();
    dimuonsTree_.mu1HcalIso                 = mu1->hcalIso();
    dimuonsTree_.mu2HcalIso                 = mu2->hcalIso();

    dimuonsTree_.Fill();
  }
}

void 
DimuonsNtupelizer::beginJob()
{
  // register to the TFileService
  edm::Service<TFileService> fs;
  
  // book the tree:
  dimuonsTree_.init( fs->make<TTree>("dimuons", "dimuons tree") );
}

void 
DimuonsNtupelizer::endJob() 
{
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(DimuonsNtupelizer);
