/**
 * Definition of the VecBosAnalyzer class.
 * 
 * Facilitates the analysis of the VecBos ntuples.  Produces histograms
 * and stores them in a root file.
 * 
 * Jan Veverka, Caltech, 12 June 2012.
 */

#ifndef ZMMG_FWLITE_VECBOSANALYZER_H
#define ZMMG_FWLITE_VECBOSANALYZER_H

#include <map>
#include <string>
#include <boost/shared_ptr.hpp>

#include "TFile.h"
#include "TH1.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "Zmmg/FWLite/interface/VecBosTree.h"

//_____________________________________________________________________
namespace cit {

  class VecBosAnalyzer {
  public:
    typedef edm::ParameterSet PSet;
    VecBosAnalyzer(boost::shared_ptr<PSet>);
    ~VecBosAnalyzer();
    void run();
  private:
    void init();
    void parseConfiguration();
    void parseInputs();
    void parseOutputs();
    void setBranchesStatus();
    void bookHistograms();
    void bookPileupHistograms();
    void bookPhotonHistograms();
    void bookMuonHistograms();
    void setMplStyleTitles();
    void setMplStyleTitlesForPileupHistograms();
    void setMplStyleTitlesForPhotonHistograms();
    void setMplStyleTitlesForMuonHistograms();
    void fillHistograms();
    void fillPileupHistograms();
    void fillHistogramsForPhotonIndex(Int_t);
    void fillHistogramsForMuonIndex(Int_t);
    void reportEvent(Long64_t);
    boost::shared_ptr<PSet> cfg_;
    VecBosTree *tree_;
    TFile *output_;
    Long64_t maxEventsInput_;
    Long64_t reportEvery_;    
    std::map<std::string, TH1*> histos_;
    std::string titleStyle_;
  }; // VecBosAnalyzer

} // namespace cit

#endif
