/**
 * \file HtoZg/MuonAnalysis/interface/MuonVertexingValueMapProducer.h
 * \brief Defines Producer of Tight Muon ID Variables that Involve Vertex
 * Defines an EDProducer template class producing muon value maps of dxy and dz w.r.t.
 * the primary vertex. Muon type (reco or pat) is the template paramters.
 * They have the instance labels dxy and dz, so the values maps are named
 * *_*_dxy_* and *_*_dz_*.
 * Configuration parameters:
 *      muonSource - InputTag of the source muon collection
 *      vertexSource - InputTag of the source vertex collection
 * \author Jan Veverka, Caltech
 * \date 1 August 2012
 */

#ifndef HtoZg_MuonAnalysis_MuonVertexingValueMapProducer_h
#define HtoZg_MuonAnalysis_MuonVertexingValueMapProducer_h

// system include files
#include <memory>
#include <string>
#include <vector>

/// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

// #include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/OwnVector.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "HtoZg/CommonAnalysis/interface/ValueMapPutter.h"

namespace cit {
  namespace hzg {
    /**
     * \class MuonVertexingValueMapProducer 
     */
    template <typename MuonType>
    class MuonVertexingValueMapProducer : public edm::EDProducer {
    public:
      explicit MuonVertexingValueMapProducer(const edm::ParameterSet&);
      ~MuonVertexingValueMapProducer();
    private:
      virtual void produce(edm::Event&, const edm::EventSetup&);
      
      // ----------member data ---------------------------
      edm::InputTag muonSource_;
      edm::InputTag vertexSource_;
    }; /// class MuonVertexingValueMapProducer
    
    /**
     * Constructor
     */
    template <typename MuonType>
    MuonVertexingValueMapProducer<MuonType>::MuonVertexingValueMapProducer (
      const edm::ParameterSet& iConfig
      ):
      muonSource_(iConfig.getParameter<edm::InputTag>("muonSource")),
      vertexSource_(iConfig.getParameter<edm::InputTag>("vertexSource"))
    {
      produces<edm::ValueMap<float> >("dxy");
      produces<edm::ValueMap<float> >("dz");
    } /// Constructor
    
    /**
     * Destructor
     */
    template <typename MuonType>
    MuonVertexingValueMapProducer<MuonType>::~MuonVertexingValueMapProducer()
    {
    } /// Destructor
    
    /**
     * Method called for each event
     */
    template <typename MuonType>
    void
    MuonVertexingValueMapProducer<MuonType>::produce (
      edm::Event& iEvent, const edm::EventSetup& iSetup
      )
    {
      // using namespace std;
      // using namespace edm;

      edm::Handle<edm::View<MuonType> > muons;
      edm::Handle<reco::VertexCollection> vertices; 
      
      iEvent.getByLabel(muonSource_, muons);
      iEvent.getByLabel(vertexSource_, vertices);

      std::vector<float> dxy;
      std::vector<float> dz;
     
      bool foundVertex = false;
      
      if (vertices->size() > 0) {
        foundVertex = true;
      }
      reco::Vertex::Point const& vtx = vertices->begin()->position();
 
      typename edm::View<MuonType>::const_iterator iMu = muons->begin();
      for (; iMu < muons->end(); ++iMu) {
        const reco::TrackRef trk = iMu->innerTrack();
        if (!foundVertex || trk.isNull()) {
          /// Cannot compute vertexing info, use dummy values.
          dxy.push_back(-999);
          dz .push_back(-999);
          continue;
        }
        dxy.push_back(iMu->innerTrack()->dxy(vtx));
        dz .push_back(iMu->innerTrack()->dz (vtx));
      } // loop over muons

      ValueMapPutter putMap;
      
      putMap(iEvent, muons, dxy, "dxy");
      putMap(iEvent, muons, dz , "dz" );

    } /// produce(..)
    
  } // namespace cit::hzg
} // namespace cit

#endif
