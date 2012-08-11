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
 *      target - string describing the target of isolation; one of
 *              Data2011, Data2012
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
#include <algorithm>

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

#include "HtoZg/CommonAnalysis/interface/ValueMapPutter.h"
#include "Muon/MuonAnalysisTools/interface/MuonEffectiveArea.h"

namespace cit {
  namespace hzg {
    /**
     * \class MuonIsolationValueMapProducer 
     */
    template <typename MuonType>
    class MuonIsolationValueMapProducer : public edm::EDProducer {
    public:
      typedef MuonEffectiveArea::MuonEffectiveAreaType   Type;
      typedef MuonEffectiveArea::MuonEffectiveAreaTarget Target;
      explicit MuonIsolationValueMapProducer(const edm::ParameterSet&);
      ~MuonIsolationValueMapProducer();
    private:
      virtual void produce(edm::Event&, const edm::EventSetup&);
      
      // ----------member data ---------------------------
      edm::InputTag muonSource_;
      edm::InputTag rhoSource_ ;
      Type   type_  ;
      Target target_;
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
      type_   = MuonEffectiveArea::kMuGammaAndNeutralHadronIso04;
      
      std::string target;
      target = iConfig.getUntrackedParameter<std::string>("target", 
                                                          "Data2012");
      if (target == "Data2011") {
        target_ = MuonEffectiveArea::kMuEAData2011;
      } else if (target == "Data2012") {
        target_ = MuonEffectiveArea::kMuEAData2012;
      } else {
        throw cms::Exception("InvalidInput")
                << "\'target\' must be one of: "
                << "Data2011 Data2012";
      }
        
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
     
            
      typename edm::View<MuonType>::const_iterator iMu = muons->begin();
      for (; iMu < muons->end(); ++iMu) {
        float iRho = float(*rhoHandle);
        float iEA  = MuonEffectiveArea::GetMuonEffectiveArea(type_, iMu->eta(),
                                                             target_);
        double chIso04 = iMu->pfIsolationR04().sumChargedHadronPt;   
        double phIso04 = iMu->pfIsolationR04().sumPhotonEt;          
        double nhIso04 = iMu->pfIsolationR04().sumNeutralHadronEt;
        
        float iCombIso = chIso04 + std::max(0., 
                                            nhIso04 + phIso04 - iEA * iRho);

        rho    .push_back(iRho    );
        EA     .push_back(iEA     );
        combIso.push_back(iCombIso);
      } // loop over muons

      ValueMapPutter putMap;
      
      putMap(iEvent, muons, rho    , "rho"    );
      putMap(iEvent, muons, EA     , "EA"     );
      putMap(iEvent, muons, combIso, "combIso");

    } /// produce(..)    
  } // namespace cit::hzg
} // namespace cit

#endif
