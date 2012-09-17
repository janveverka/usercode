/**
 * \brief Implementation of the VgEventSelector class.
 * \author Jan Veverka, Caltech
 * \date 16 September 2012
 */
#include <math.h>
#include <string>
#include "FWCore/Utilities/interface/Exception.h"
#include "Vgamma/Analysis/interface/VgEventSelector.h"
using cit::VgEventSelector;
using cit::VgEvent;

//_____________________________________________________________________
/**
 * Constructor
 */
VgEventSelector::VgEventSelector(PSet const & cfg) :
  cfg_(cfg),
  selectedEvent_()
{} // Ctor


//_____________________________________________________________________
/**
 * Destructor
 */
VgEventSelector::~VgEventSelector()
{} // Dtor


//_____________________________________________________________________
/**
 * Selection interface.
 */
bool
VgEventSelector::operator()(VgEvent const& event, pat::strbitset & ret)
{
  /// Everything passes right now.
  ret.set(true);
  selectedEvent_.reset(new VgEvent(event));
  
  if (cfg_.getParameter<bool>("selectMuons") == true) {
    std::cout << "Selecting muons ..." << std::endl;
    /// Select muons
    cit::VgLeafCandidates selectedMuons;
    cit::VgLeafCandidates const & muons = event.muons();
    cit::VgAnalyzerTree const & tree = event.tree();
    /// Loop over muons
    for (cit::VgLeafCandidates::const_iterator mu = muons.begin();
          mu != muons.end(); ++mu) {
      unsigned i = mu->key();
      std::cout << "Checking muon " << i << std::endl;
      if (mu->pt() < 20.) continue;
      if (fabs(mu->eta()) > 2.4) continue;
      // is global muon
      if (!(unsigned(tree.muType[i]) & (1u << 1))) continue;
      if (tree.muNumberOfValidPixelHits[i] < 1) continue;
      selectedMuons.push_back(*mu);
      std::cout << "Muon " << i << " passed" << std::endl;
    } /// loop over muons
    if (selectedMuons.size() < 2) ret.set(false);
    std::cout << "Found " << selectedMuons.size() << " passing muons" << std::endl;
    selectedEvent_->putMuons(selectedMuons);
  } else {
    // Use all muons
    std::cout << "Ignoring muon selection ..." << std::endl;    
    selectedEvent_->putMuons(event.muons());
  }
      
  return ret;
} // bool operator()(..)

//_____________________________________________________________________
/**
 * Accessor.
 */
VgEvent const &
VgEventSelector::selectedEvent() const
{
  if (selectedEvent_.get() == 0) {
    std::string what = ("Cannot return selected event; no events "
			"have been selected yet.");
    throw cms::Exception("BadPreCondition") << what; 
  }
  return *selectedEvent_;
} // selectedEvents()

