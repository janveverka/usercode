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
//_____________________________________________________________________
/**
 * Constructor
 */
VgEventSelector::VgEventSelector(PSet const & cfg) :
  selectedEvent_(),
  selectMuons_(cfg.getParameter<bool>("selectMuons")),
  selectPhoton_(cfg.getUntrackedParameter<bool>("selectPhoton", false))
{
  init();

  if (cfg.existsAs<vector<string> >("cutsToIgnore"))
    setIgnoredCuts(cfg.getParameter<vector<string> >("cutsToIgnore"));
} // Ctor


//_____________________________________________________________________
/**
 * Destructor
 */
VgEventSelector::~VgEventSelector()
{} // Dtor


//_____________________________________________________________________
/**
 * Initialization
 */
void
VgEventSelector::init()
{
  push_back("selectMuons", selectMuons_);
  push_back("selectPhoton", selectPhoton_);

  set("selectMuons");
  set("selectPhoton");
} // init()


//_____________________________________________________________________
/**
 * Selection interface.
 */
bool
VgEventSelector::operator()(VgEvent const& event, pat::strbitset & ret)
{
  /// Everything passes right now.
  ret.set(false);
  selectedEvent_.reset(new VgEvent(event));

  if (selectMuons_ == true) {
    /// Select muons
    cit::VgLeafCandidates selectedMuons;
    cit::VgLeafCandidates const & muons = event.muons();
    cit::VgAnalyzerTree const & tree = event.tree();
    /// Loop over muons
    for (cit::VgLeafCandidates::const_iterator mu = muons.begin();
          mu != muons.end(); ++mu) {
      unsigned i = mu->key();
      if (mu->pt() < 20.) continue;
      if (fabs(mu->eta()) > 2.4) continue;
      // is global muon
      if (!(unsigned(tree.muType[i]) & (1u << 1))) continue;
      if (tree.muNumberOfValidPixelHits[i] < 1) continue;
      selectedMuons.push_back(*mu);
    } /// loop over muons
    if (ignoreCut("selectMuons") || selectedMuons.size() >= 2) 
      passCut(ret, "selectMuons");
    cout << "selected muons: " << selectedMuons.size() << endl;
    selectedEvent_->putMuons(selectedMuons);
  } else {
    // Use all muons
    passCut(ret, "selectMuons");
    cout << "selected muons: " << event.muons().size() << endl;
    selectedEvent_->putMuons(event.muons());
  }
      
  if (ignoreCut("selectPhoton") || true)
    passCut(ret, "selectPhoton");

  print(cout);
  cout << "ret: " << (bool)ret << endl;
  
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

