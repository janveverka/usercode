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
  passesMuonCuts_(cfg.getParameter<PSet>("muonCuts")),
  passesDimuonCuts_(cfg.getParameter<PSet>("dimuonCuts")),
  passesPhotonCuts_(cfg.getParameter<PSet>("photonCuts"))
{
  init(
    cfg.getParameter<bool>("selectMuons"),
    cfg.getParameter<bool>("selectDimuons"),
    cfg.getParameter<bool>("selectPhoton")
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
VgEventSelector::init(const bool & selectMuons,
                      const bool & selectDimuons,
                      const bool & selectPhoton)
{
  push_back("selectMuons", selectMuons);
  push_back("selectDimuons", selectDimuons);
  push_back("selectPhoton", selectPhoton);

  set("selectMuons");
  set("selectDimuons");
  set("selectPhoton");
} // init()


//_____________________________________________________________________________
/**
 * Selection interface.
 */
bool
VgEventSelector::operator()(VgEvent const& event, pat::strbitset & ret)
{
  ret.set(false);
  selectedEvent_.reset(new VgEvent(event));

  if (considerCut("selectMuons")) selectMuons();
  if (ignoreCut("selectMuons") || selectedEvent_->muons().size() >= 2)
    passCut(ret, "selectMuons");
  else return false;

  selectedEvent_->combineMuonsToDimuons();
  if (considerCut("selectDimuons")) selectDimuons();
  if (ignoreCut("selectDimuons") || selectedEvent_->dimuons().size() > 0)
    passCut(ret, "selectDimuons");
  else return false;
 
  if (considerCut("selectPhoton")) selectPhotons(); 
  if (ignoreCut("selectPhoton") || selectedEvent_->photons().size() > 0)
    passCut(ret, "selectPhoton");
  else return false;
  
  selectedEvent_->combineDimuonsAndPhotonsToMmgCands();

  // print(cout);
  // cout << "ret: " << (bool)ret << endl;
  
  return (bool) ret;
} // bool operator()(..)


//_____________________________________________________________________________
/**
 * Applies muon cuts to muons in the *selectedEvent_ and stores the passing
 * muons back in the *selectedEvent_.
 * 
 * Precondition: *selectedEvent_ has been created.
 * Postcondition: *selectedEvent_ contains only selected muons.
 */
void
VgEventSelector::selectMuons() 
{
  /// Loop over muons
  cit::VgLeafCandidates const & sourceMuons = selectedEvent_->muons();
  cit::VgLeafCandidates selectedMuons;
  for (cit::VgLeafCandidates::const_iterator mu = sourceMuons.begin();
        mu != sourceMuons.end(); ++mu) {
    if (passesMuonCuts_(*mu)) selectedMuons.push_back(*mu);
  } /// Loop over muons
  selectedEvent_->putMuons(selectedMuons);  
} 
// void
// VgEventSelector::selectMuons() 


//_____________________________________________________________________________
/**
 * Applies dimuon cuts to dimuons in the *selectedEvent_ and stores the passing
 * dimuons back in the *selectedEvent_.
 * 
 * Precondition: *selectedEvent_ has been created and muons have been combined
 *                to dimuons.
 * Postcondition: *selectedEvent_ contains only selected dimuons.
 */
void
VgEventSelector::selectDimuons() 
{
  /// Loop over dimuons
  cit::VgCombinedCandidates const & sourceDimuons = selectedEvent_->dimuons();
  cit::VgCombinedCandidates selectedDimuons;
  for (cit::VgCombinedCandidates::const_iterator dimu = sourceDimuons.begin();
       dimu != sourceDimuons.end(); ++dimu) {
    if (passesDimuonCuts_(*dimu)) selectedDimuons.push_back(*dimu);
  } /// Loop over dimuons
  selectedEvent_->putDimuons(selectedDimuons);  
} 
// void
// VgEventSelector::selectDimuons() 


//_____________________________________________________________________________
/**
 * Applies photon cuts to photons in the *selectedEvent_ and stores the passing
 * photons back in the *selectedEvent_.
 * 
 * Precondition: *selectedEvent_ has been created.
 * Postcondition: *selectedEvent_ contains only selected photons.
 */
void
VgEventSelector::selectPhotons() 
{
  /// Loop over photons
  cit::VgLeafCandidates const & sourcePhotons = selectedEvent_->photons();
  cit::VgLeafCandidates selectedPhotons;
  for (cit::VgLeafCandidates::const_iterator pho = sourcePhotons.begin();
        pho != sourcePhotons.end(); ++pho) {
    if (passesPhotonCuts_(*pho)) selectedPhotons.push_back(*pho);
  } /// Loop over photons
  selectedEvent_->putPhotons(selectedPhotons);  
} 
// void
// VgEventSelector::selectPhotons() 


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
  out << "Event:" << endl;
  print(out);
  
  if (considerCut("selectMuons")) {
    out << "Muons:" << endl;
    passesMuonCuts_.print(out);
  }

  if (considerCut("selectPhoton")) {
    out << "Photons:" << endl;
    passesPhotonCuts_.print(out);
  }

  if (considerCut("selectDimuons")) {
    out << "Dimuons:" << endl;
    passesDimuonCuts_.print(out);
  }

} // end of:
// void
// VgEventSelector::printCutflows(ostream & out) const


