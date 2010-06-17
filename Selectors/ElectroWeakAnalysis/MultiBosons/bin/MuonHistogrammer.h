#ifndef ElectroWeakAnalysis_MultiBosons_MuonHistogrammer_h
#define ElectroWeakAnalysis_MultiBosons_MuonHistogrammer_h

/** \class MuonHistogrammer
 *  FWLite version of the HistoAnalyzer for pat::MuonCollection
 *  Creates histograms defined in a config file
 *  \author Jan Veverka, Caltech
 */

#include "DataFormats/FWLite/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/FWLite/interface/Handle.h"
// #include "FWCore/Utilities/interface/InputTag.h"
// #include "FWCore/ServiceRegistry/interface/Service.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "CommonTools/Utils/interface/ExpressionHisto.h"
#include "DataFormats/PatCandidates/interface/Muon.h"


class MuonHistogrammer {
public:
  /// ctor from parameter set
  MuonHistogrammer(const edm::ParameterSet &, fwlite::TFileService &);
  /// dtor
  ~MuonHistogrammer();
  /// process an event
  void analyze(const edm::EventBase &);
  /// process a base collection
  void analyze(const std::vector<pat::Muon> &);
  /// process a collection of shallow clone pointers to the base collection
  void analyze(const std::vector<reco::ShallowClonePtrCandidate> &);
private:
  /// label of the input collection
  edm::InputTag src_;
  /// vector of pointers to histograms
  std::vector<ExpressionHisto<pat::Muon>* > vhistograms_;
};

#endif
