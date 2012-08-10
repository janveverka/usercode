/**
 * \file HtoZg/MuonAnalysis/interface/MuonIsolationValueMapProducer.h
 * \brief Defines Producer of Custom Isolation Related Variables
 * Defines an EDProducer template class producing muon value maps of rho and 
 * EA (effective area) for the muon isolation.
 * Muon type (reco or pat) is the template paramters.
 * They have the instance labels rho and EA, so the values maps are named
 * *_*_rho_* and *_*_EA_*.
 * Configuration parameters:
 *      muonSource - InputTag of the source muon collection
 *      rhoSource - InputTag of the source vertex collection
 *      
 * \author Jan Veverka, Caltech
 * \date 8 August 2012
 */

#ifndef HtoZg_MuonAnalysis_MuonIsolationValueMapProducer_h
#define HtoZg_MuonAnalysis_MuonIsolationValueMapProducer_h

// system include files
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

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/OwnVector.h"

#include "Muon/MuonAnalysisTools/interface/MuonEffectiveArea.h"

namespace cit {
  namespace hzg {
    /**
     * \class MuonIsolationValueMapProducer 
     */
    template <typename MuonType>
    class MuonIsolationValueMapProducer : public edm::EDProducer {
    public:
      typedef MuonEffectiveArea::MuonEffectiveAreaType   EAType;
      typedef MuonEffectiveArea::MuonEffectiveAreaTarget EATarget;
      explicit MuonIsolationValueMapProducer(const edm::ParameterSet&);
      ~MuonIsolationValueMapProducer();
    private:
      virtual void produce(edm::Event&, const edm::EventSetup&);
      
      // ----------member data ---------------------------
      void putMap(edm::Event & iEvent,
                  edm::Handle<edm::View<MuonType> >& muons,
                  std::vector<float>& vertexingData,
                  const std::string& name);
      edm::InputTag muonSource_;
      edm::InputTag rhoSource_ ;
    }; /// class MuonIsolationValueMapProducer
    
    /**
     * Constructor
     */
    template <typename MuonType>
    MuonIsolationValueMapProducer<MuonType>::MuonIsolationValueMapProducer (
      const edm::ParameterSet& iConfig
      ):
      muonSource_(iConfig.getParameter<edm::InputTag>("muonSource")),
      rhoSource_ (iConfig.getParameter<edm::InputTag>("rhoSource" ))
    {
      produces<edm::ValueMap<float> >("rho"    );
      produces<edm::ValueMap<float> >("EA"     );
      produces<edm::ValueMap<float> >("combIso");
    } /// Constructor
    
    /**
     * Destructor
     */
    template <typename MuonType>
    MuonIsolationValueMapProducer<MuonType>::~MuonIsolationValueMapProducer()
    {
    } /// Destructor
    
    /**
     * Method called for each event
     */
    template <typename MuonType>
    void
    MuonIsolationValueMapProducer<MuonType>::produce (
      edm::Event& iEvent, const edm::EventSetup& iSetup
      )
    {
      // using namespace std;
      // using namespace edm;

      edm::Handle<edm::View<MuonType> > muons;
      edm::Handle<double>               rhoHandle; 
      
      iEvent.getByLabel(muonSource_, muons    );
      iEvent.getByLabel(rhoSource_ , rhoHandle);

      std::vector<float> rho    ;
      std::vector<float> EA     ;
      std::vector<float> combIso;
     
      
      EAType   eaType   = MuonEffectiveArea::kMuGammaAndNeutralHadronIso04;
      EATarget eaTarget = MuonEffectiveArea::kMuEAData2012;
      
      typename edm::View<MuonType>::const_iterator iMu = muons->begin();
      for (; iMu < muons->end(); ++iMu) {
        float iRho = float(*rhoHandle);
        float iEA  = MuonEffectiveArea::GetMuonEffectiveArea(eaType, iMu->eta(),
                                                             eaTarget);
        double chIso04 = iMu->pfIsolationR04().sumChargedHadronPt;   
        double phIso04 = iMu->pfIsolationR04().sumPhotonEt;          
        double nhIso04 = iMu->pfIsolationR04().sumNeutralHadronEt;
        
//         float iCombIso = nhIso04 + phIso04 - iEA * iRho;
//         if (iCombIso < 0.) {
//           iCombIso = 0.;
//         }
//         iCombIso += chIso04;
        
        float iCombIso = chIso04 + max(0., nhIso04 + phIso04 - iEA * iRho);
        
        rho    .push_back(iRho    );
        EA     .push_back(iEA     );
        combIso.push_back(iCombIso);
      } // loop over muons

      putMap(iEvent, muons, rho    , "rho"    );
      putMap(iEvent, muons, EA     , "EA"     );
      putMap(iEvent, muons, combIso, "combIso");

    } /// produce(..)
    
    /**
     * Helper method that puts one value map in the event.
     */
    template <typename MuonType>
    void
    MuonIsolationValueMapProducer<MuonType>::putMap (
      edm::Event & iEvent,
      edm::Handle<edm::View<MuonType> >& muons,
      std::vector<float>& data,
      const std::string& name
      )
    {
      using namespace std;
      using namespace edm;

      auto_ptr<ValueMap<float> > prod(new ValueMap<float>());
      typename ValueMap<float>::Filler filler (*prod);
      filler.insert(muons, data.begin(), data.end());
      filler.fill();
      iEvent.put(prod, name);
    } /// MuonIsolationValueMapProducer<MuonType>::putMap(...)    
  } // namespace cit::hzg
} // namespace cit

#endif
