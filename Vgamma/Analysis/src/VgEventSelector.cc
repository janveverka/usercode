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
using namespace std;
//_____________________________________________________________________________
/**
 * Constructor
 */
VgEventSelector::VgEventSelector(PSet const & cfg) :
  selectedEvent_(),
  passesMuonCuts_(cfg.getParameter<PSet>("muonCuts"))
{
  init(
    cfg.getParameter<bool>("selectMuons"),
    cfg.getParameter<bool>("selectPhoton"),
  );

  if (cfg.existsAs<vector<string> >("cutsToIgnore"))
    setIgnoredCuts(cfg.getParameter<vector<string> >("cutsToIgnore"));
} // Ctor


//_____________________________________________________________________________
/**
 * Destructor
 */
VgEventSelector::~VgEventSelector()
{} // Dtor


//_____________________________________________________________________________
/**
 * Initialization
 */
void
VgEventSelector::init(const bool & selectMuons, const bool & selectPhoton)
{
  push_back("selectMuons", selectMuons);
  push_back("selectPhoton", selectPhoton);

  set("selectMuons");
  set("selectPhoton");
} // init()


//_____________________________________________________________________________
/**
 * Selection interface.
 */
bool
VgEventSelector::operator()(VgEvent const& event, pat::strbitset & ret)
{
  /// Everything passes right now.
  ret.set(false);
  selectedEvent_.reset(new VgEvent(event));

  if (ignoreCut("selectMuons") == false) {
    /// Select muons
    cit::VgLeafCandidates selectedMuons;
    /// Loop over muons
    for (cit::VgLeafCandidates::const_iterator mu = event.muons().begin();
          mu != event.muons().end(); ++mu) {
      if (passesMuonCuts_(*mu)) selectedMuons.push_back(*mu);
    } /// loop over muons
    selectedEvent_->putMuons(selectedMuons);
  }
  
  if (ignoreCut("selectMuons") || selectedEvent_->muons().size() >= 2)
    passCut(ret, "selectMuons");
  // cout << "selected muons: " << selectedEvent_->muons().size() << endl;

  if (ignoreCut("selectPhoton") || selectedEvent_->photons().size() > 0)
    passCut(ret, "selectPhoton");

  // print(cout);
  // cout << "ret: " << (bool)ret << endl;
  
  return ret;
} // bool operator()(..)


//_____________________________________________________________________________
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
} // end of:
// VgEvent const &
// VgEventSelector::selectedEvent() const


//_____________________________________________________________________________
/**
 * Summary output
 */
void
VgEventSelector::printCutflows(ostream & out) const
{
  out << "Event Cut Flow:" << endl;
  print(out);
  
  out << "Muons Cut Flow:" << endl;
  passesMuonCuts_.print(out);
} // end of:
// void
// VgEventSelector::printCutflows(ostream & out) const

