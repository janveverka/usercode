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

#include <boost/shared_ptr.hpp>

#include "TFile.h"

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
    boost::shared_ptr<PSet> cfg_;
    VecBosTree *tree_;
    TFile *output_;
    Long64_t maxEventsInput_;
  }; // VecBosAnalyzer

} // namespace cit

#endif
