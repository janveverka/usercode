/**
 * \file HtoZg/CommonAnalysis/interface/PhotonIsolationValueMapProducer.h
 * \brief Defines Producer of Custom Isolation Related Variables
 * Defines an EDProducer template class producing photon value maps of rho,
 * and EAs (effective areas) for the photon isolation and rho corrected
 * PF-based isolations based on charged hadrons, neutral hadrons and photons.
 * They have the instance labels rho and EA, so the values maps are named
 * *_*_rho_*, *_*_{charged,neutral,photon}EA_*, and 
 * *_*_{charged,neutral,photon}Iso_*
 * PhotonType (reco or pat) is the template paramter.
 * Configuration parameters:
 *      photonSource - InputTag of the source photon collection
 *      rhoSource    - InputTag of the source rho value from FastJet
 *      vertexSource - InputTag of the source vertex collection
 *      pfSource     - InputTag of the source PF candidate collection
 *      
 * \author Jan Veverka, Caltech
 * \date 8 August 2012
 */

#ifndef HtoZg_CommonAnalysis_PhotonIsolationValueMapProducer_h
#define HtoZg_CommonAnalysis_PhotonIsolationValueMapProducer_h

// system include files
#include <algorithm>
#include <math.h>
#include <memory>
#include <string>
#include <vector>

/// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/OwnVector.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"

#include "EGamma/EGammaAnalysisTools/interface/PFIsolationEstimator.h"
#include "HtoZg/CommonAnalysis/interface/PhotonEffectiveArea.h"

namespace cit {
  namespace hzg {
    /**
     * \class PhotonIsolationValueMapProducer 
     */
    template <typename PhotonType>
    class PhotonIsolationValueMapProducer : public edm::EDProducer {
    public:
      explicit PhotonIsolationValueMapProducer(const edm::ParameterSet&);
      ~PhotonIsolationValueMapProducer();
    private:
      virtual void produce(edm::Event&, const edm::EventSetup&);
      
      // ----------member data ---------------------------
      void putMap(edm::Event & iEvent,
                  edm::Handle<edm::View<PhotonType> >& photons,
                  std::vector<float>& vertexingData,
                  const std::string& name);
      edm::InputTag photonSource_;
      edm::InputTag rhoSource_   ;
      edm::InputTag pfSource_    ;
      edm::InputTag vertexSource_;
      PFIsolationEstimator isolator_;
      // PhotonEffectiveArea eaGetter_;
    }; /// class PhotonIsolationValueMapProducer
    
    /**
     * Constructor
     */
    template <typename PhotonType>
    PhotonIsolationValueMapProducer<PhotonType>::PhotonIsolationValueMapProducer(
      const edm::ParameterSet& iConfig
      ):
      photonSource_(iConfig.getParameter<edm::InputTag>("photonSource")),
      rhoSource_   (iConfig.getParameter<edm::InputTag>("rhoSource"   )),
      pfSource_    (iConfig.getParameter<edm::InputTag>("pfSource"    )),
      vertexSource_(iConfig.getParameter<edm::InputTag>("vertexSource"))
    {
      produces<edm::ValueMap<float> >("rho"                        );
      produces<edm::ValueMap<float> >("chargedHadronEA"            );
      produces<edm::ValueMap<float> >("neutralHadronEA"            );
      produces<edm::ValueMap<float> >("photonEA"                   );
      produces<edm::ValueMap<float> >("pfChargedHadron"            );
      produces<edm::ValueMap<float> >("pfNeutralHadron"            );
      produces<edm::ValueMap<float> >("pfPhoton"                   );
      produces<edm::ValueMap<float> >("pfChargedHadronRhoCorrected");
      produces<edm::ValueMap<float> >("pfNeutralHadronRhoCorrected");
      produces<edm::ValueMap<float> >("pfPhotonRhoCorrected"       );
      
      isolator_.initializePhotonIsolation(kTRUE);
      isolator_.setConeSize(0.3);
      isolator_.setDeltaRVetoBarrelCharged(.02);
      isolator_.setDeltaRVetoEndcapCharged(.02);
      isolator_.setRectangleDeltaEtaVetoBarrelPhotons(.015);
      //isolator_.setDeltaRVetoEndcapPhotons(0.00864 * fabs(sinh(1.5)) * 4);
    } /// Constructor
    
    /**
     * Destructor
     */
    template <typename PhotonType>
    PhotonIsolationValueMapProducer<PhotonType>::~PhotonIsolationValueMapProducer()
    {
    } /// Destructor
    
    /**
     * Method called for each event
     */
    template <typename PhotonType>
    void
    PhotonIsolationValueMapProducer<PhotonType>::produce(
      edm::Event& iEvent, const edm::EventSetup& iSetup
      )
    {
      edm::Handle<edm::View<PhotonType> >      photons     ;
      edm::Handle<double>                      rhoHandle   ; 
      edm::Handle<reco::PFCandidateCollection> pfHandle    ; 
      edm::Handle<reco::VertexCollection>      vertices    ; 
      
      iEvent.getByLabel(photonSource_, photons  );
      iEvent.getByLabel(rhoSource_   , rhoHandle);
      iEvent.getByLabel(pfSource_    , pfHandle );
      iEvent.getByLabel(vertexSource_, vertices );
      
      std::vector<float> rhoValues;
      
      std::vector<float> chEAValues;
      std::vector<float> nhEAValues;
      std::vector<float> phEAValues;
      
      std::vector<float> chIsoValues;
      std::vector<float> nhIsoValues;
      std::vector<float> phIsoValues;
      
      std::vector<float> chRhoCorrIsoValues;
      std::vector<float> nhRhoCorrIsoValues;
      std::vector<float> phRhoCorrIsoValues;
     
      float rho = float(*rhoHandle);
      const reco::PFCandidateCollection * pfCandidates = pfHandle.product();
      edm::Ref<reco::VertexCollection> vertex(vertices, 0);
      
      const PhotonEffectiveArea::Type chType = PhotonEffectiveArea::kCharged03;
      const PhotonEffectiveArea::Type nhType = PhotonEffectiveArea::kNeutral03;
      const PhotonEffectiveArea::Type phType = PhotonEffectiveArea::kPhoton03 ;
            
      typename edm::View<PhotonType>::const_iterator iPho = photons->begin();
      for (; iPho < photons->end(); ++iPho) {
        const PhotonType * pho = &(*iPho);
        
        double scEta = pho->superCluster()->eta();

        double chEA = PhotonEffectiveArea::get(chType, scEta);
        double nhEA = PhotonEffectiveArea::get(nhType, scEta);
        double phEA = PhotonEffectiveArea::get(phType, scEta);
        
        isolator_.setDeltaRVetoEndcapPhotons(0.00864 * fabs(sinh(scEta)) * 4);
        isolator_.fGetIsolation(pho, pfCandidates, vertex, vertices); 
        
        double chIso = isolator_.getIsolationCharged();
        double nhIso = isolator_.getIsolationNeutral();
        double phIso = isolator_.getIsolationPhoton ();
        
        double chRhoCorrIso = std::max(0., chIso - rho * chEA);
        double nhRhoCorrIso = std::max(0., nhIso - rho * nhEA);
        double phRhoCorrIso = std::max(0., phIso - rho * phEA);
        
        rhoValues         .push_back(rho         );
        
        chEAValues        .push_back(chEA        );
        nhEAValues        .push_back(nhEA        );
        phEAValues        .push_back(phEA        );

        chIsoValues       .push_back(chIso       );
        nhIsoValues       .push_back(nhIso       );
        phIsoValues       .push_back(phIso       );
        
        chRhoCorrIsoValues.push_back(chRhoCorrIso);
        nhRhoCorrIsoValues.push_back(nhRhoCorrIso);
        phRhoCorrIsoValues.push_back(phRhoCorrIso);
                
      } // loop over photons

      putMap(iEvent, photons, rhoValues         , "rho"                        );
      
      putMap(iEvent, photons, chEAValues        , "chargedHadronEA"            );
      putMap(iEvent, photons, nhEAValues        , "neutralHadronEA"            );
      putMap(iEvent, photons, phEAValues        , "photonEA"                   );      
      
      putMap(iEvent, photons, chIsoValues       , "pfChargedHadron"            );
      putMap(iEvent, photons, nhIsoValues       , "pfNeutralHadron"            );
      putMap(iEvent, photons, phIsoValues       , "pfPhoton"                   );

      putMap(iEvent, photons, chRhoCorrIsoValues, "pfChargedHadronRhoCorrected");
      putMap(iEvent, photons, nhRhoCorrIsoValues, "pfNeutralHadronRhoCorrected");
      putMap(iEvent, photons, phRhoCorrIsoValues, "pfPhotonRhoCorrected"       );

    } /// produce(..)
    
    /**
     * Helper method that puts one value map in the event.
     */
    template <typename PhotonType>
    void
    PhotonIsolationValueMapProducer<PhotonType>::putMap (
      edm::Event & iEvent,
      edm::Handle<edm::View<PhotonType> >& photons,
      std::vector<float>& data,
      const std::string& name
      )
    {
      using namespace std;
      using namespace edm;

      auto_ptr<ValueMap<float> > prod(new ValueMap<float>());
      typename ValueMap<float>::Filler filler (*prod);
      filler.insert(photons, data.begin(), data.end());
      filler.fill();
      iEvent.put(prod, name);
    } // PhotonIsolationValueMapProducer<PhotonType>::putMap(...)    
  } // namespace cit::hzg
} // namespace cit

#endif
