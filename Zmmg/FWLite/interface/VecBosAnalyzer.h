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

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "Zmmg/FWLite/interface/VecBosTree.h"

//_____________________________________________________________________
namespace cit {

  class VecBosAnalyzer {
  public:
    VecBosAnalyzer(boost::shared_ptr<edm::ParameterSet>);
    ~VecBosAnalyzer();    
  private:
    void init();    
    boost::shared_ptr<edm::ParameterSet> cfg_;    
  }; // VecBosAnalyzer

} // namespace cit

#endif
