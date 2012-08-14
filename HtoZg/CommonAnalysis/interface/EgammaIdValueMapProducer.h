/**
 * \file HtoZg/CommonAnalysis/interface/EgammaIdValueMapProducer.h
 * \brief Defines Producer of Custom Identification Related Variables
 * Defines an EDProducer template class producing photon or electron
 * value maps of new single-tower H/E backported to CMSSW_4_2_X as 
 * described at https://twiki.cern.ch/twiki/bin/view/CMS/HoverE2012
 * #New_H_E_in_CMSSW_4_2_X_and_later
 * 
 * It has the instance label "hadTowOverEm" - same as the reco::Photon
 * method in 52x - so that the product label is
 * *_*_hadTowOverEm_*
 * 
 * CandType (reco or pat Photon or (Gsf)Electron) is the template paramter.
 * 
 * Configuration parameters:
 *      src - InputTag of the source E/gamma candidate collection
 *      
 * \author Jan Veverka, Caltech
 * \date 14 August 2012
 */

#ifndef HtoZg_CommonAnalysis_EgammaIdValueMapProducer_h
#define HtoZg_CommonAnalysis_EgammaIdValueMapProducer_h

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

#include "RecoEgamma/EgammaElectronAlgos/interface/ElectronHcalHelper.h"

#include "HtoZg/CommonAnalysis/interface/ValueMapPutter.h"

namespace cit {
  namespace hzg {
    /**
     * \class EgammaIdValueMapProducer 
     */
    template <typename CandType>
    class EgammaIdValueMapProducer : public edm::EDProducer {
    public:
      explicit EgammaIdValueMapProducer(const edm::ParameterSet&);
      ~EgammaIdValueMapProducer();
    private:
      virtual void produce(edm::Event&, const edm::EventSetup&);
      
      // ----------member data ---------------------------
      edm::InputTag src_;
      ElectronHcalHelper *hcalHelper_;
    }; /// class EgammaIdValueMapProducer
    
    /**
     * Constructor
     */
    template <typename CandType>
    EgammaIdValueMapProducer<CandType>::EgammaIdValueMapProducer(
      const edm::ParameterSet& iConfig
      ):
      src_(iConfig.getParameter<edm::InputTag>("src")),
      hcalHelper_(0)
    {
      produces<edm::ValueMap<float> >("hadTowOverEm");
      
      /// Initialize the hcalHelper_
      ElectronHcalHelper::Configuration hcalCfg;
      hcalCfg.hOverEConeSize = 0.15;
      hcalCfg.useTowers = true;
      hcalCfg.hcalTowers = edm::InputTag("towerMaker");
      hcalCfg.hOverEPtMin = 0;
      hcalHelper_ = new ElectronHcalHelper(hcalCfg);
    } /// Constructor
    
    /**
     * Destructor
     */
    template <typename CandType>
    EgammaIdValueMapProducer<CandType>::~EgammaIdValueMapProducer()
    {
      if (hcalHelper_ != 0) delete hcalHelper_;
    } /// Destructor
    
    /**
     * Method called for each event
     */
    template <typename CandType>
    void
    EgammaIdValueMapProducer<CandType>::produce(
      edm::Event& iEvent, const edm::EventSetup& iSetup
      )
    {
      edm::Handle<edm::View<CandType> > cands;      
      iEvent.getByLabel(src_, cands);
      
      std::vector<float> hoeValues;
      
      hcalHelper_->checkSetup(iSetup);
      hcalHelper_->readEvent(iEvent);
                
      typename edm::View<CandType>::const_iterator iCand = cands->begin();
      for (; iCand < cands->end(); ++iCand) {
        
        std::vector<CaloTowerDetId> 
        hcalTowersBehindClusters = hcalHelper_->hcalTowersBehindClusters(
          *(iCand->superCluster())
        );
        
        float hcalDepth1 = hcalHelper_->hcalESumDepth1BehindClusters(
          hcalTowersBehindClusters
        );
        
        float hcalDepth2 = hcalHelper_->hcalESumDepth2BehindClusters(
          hcalTowersBehindClusters
        );
        
        float hOverE2012 = (hcalDepth1 + hcalDepth2);
        hOverE2012 /= iCand->superCluster()->energy();
  
        hoeValues.push_back(hOverE2012);
                        
      } // loop over candidates

      ValueMapPutter putMap;      
      putMap(iEvent, cands, hoeValues, "hadTowOverEm");

    } /// produce(..)
    
  } // namespace cit::hzg
} // namespace cit

#endif
