/**
 * \brief Implementation of the VgEventSelector class.
 * \author Jan Veverka, Caltech
 * \date 16 September 2012
 */
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
  return true;
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

