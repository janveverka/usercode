/**
 * Definition of the VgAnalyzer class.
 * 
 * Facilitates the analysis of the Vg ntuples.  Produces histograms
 * and stores them in a root file.
 * 
 * Jan Veverka, Caltech, 08 September 2012.
 */

#ifndef Vgamma_Analysis_VgAnalyzer_h
#define Vgamma_Analysis_VgAnalyzer_h

#include <map>
#include <string>
#include <boost/ptr_container/ptr_vector.hpp>
#include <boost/shared_ptr.hpp>

#include "TFile.h"
#include "TH1.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"
#include "Vgamma/Analysis/interface/VgHistoManager.h"


//_____________________________________________________________________
namespace cit {

  class VgAnalyzer {
  public:
    typedef edm::ParameterSet PSet;
    typedef boost::ptr_vector<VgHistoManager> HistoManagers;
    VgAnalyzer(boost::shared_ptr<PSet>);
    ~VgAnalyzer();
    void run();
  private:
    void init();
    void parseConfiguration();
    void parseInputs();
    void parseOutputs();
    void parseHistograms();
    void setBranchesStatus();
    void reportEvent(Long64_t);
    boost::shared_ptr<PSet> cfg_;
    VgAnalyzerTree *tree_;
    TFile *output_;
    Long64_t maxEventsInput_;
    Long64_t reportEvery_;    
    std::string titleStyle_;
    HistoManagers histoManagers_;
  }; // VgAnalyzer

} // namespace cit

#endif
