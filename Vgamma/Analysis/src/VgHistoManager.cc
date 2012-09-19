/**
 * Implementation of the VgHistoManager class.
 * \author Jan Veverka, Caltech
 * \date 08 September 2012
 */

#include "FWCore/Utilities/interface/Exception.h"
#include "Vgamma/Analysis/interface/VgDimuonHistoFiller.h"
#include "Vgamma/Analysis/interface/VgHistoManager.h"
#include "Vgamma/Analysis/interface/VgMCPileupHistoFiller.h"
#include "Vgamma/Analysis/interface/VgMMGHistoFiller.h"
#include "Vgamma/Analysis/interface/VgMuonHistoFiller.h"
#include "Vgamma/Analysis/interface/VgPhotonHistoFiller.h"
#include "Vgamma/Analysis/interface/VgPileupHistoFiller.h"

using namespace std;
using cit::VgHistoManager;
typedef cms::Exception Bad;


//_____________________________________________________________________
/**
 * Constructor
 */
VgHistoManager::VgHistoManager(VgAnalyzerTree const& tree,
                               TDirectory & output,
                               PSet const& cfg, bool isMC) :
  cfg_(cfg),
  isMC_(isMC),
  selector_(cfg.getParameter<PSet>("selection")),
  output_(output)
{
  TDirectory *cwd = gDirectory;
  output.cd();  
  
  vector<string> fillers = cfg.getParameter<vector<string> >("do");
  for (vector<string>::const_iterator filler = fillers.begin();
       filler != fillers.end(); ++filler) {
    if (*filler == string("Muons")) {
      fillers_.push_back(new VgMuonHistoFiller(tree, histos_));
    } else if (*filler == string("Photons")) {
      fillers_.push_back(new VgPhotonHistoFiller(tree, histos_));
    } else if (*filler == string("Dimuons")) {
      fillers_.push_back(new VgDimuonHistoFiller(tree, histos_));
    } else if (*filler == string("mmgCands")) {
      fillers_.push_back(new VgMMGHistoFiller(tree, histos_));
    } else if (*filler == string("Pileup")) {
      fillers_.push_back(new VgPileupHistoFiller(tree, histos_));
      if (isMC == true) {
        fillers_.push_back(new VgMCPileupHistoFiller(tree, histos_));
      }
    } else {
      throw Bad("BadConfiguration") << "Don't know how to do histograms"
                                    << " for `" << *filler << "'"
                                    << " in `" << output.GetName() << "'";
    }
  }
  
  bookHistograms();
  
  cwd->cd();
} // VgHistoManager::VgHistoManager(..)


//_____________________________________________________________________
/**
 * Dtor.
 */
VgHistoManager::~VgHistoManager() 
{
  /// Delete all the histo fillers.
  for (VgHistoFillerCollection::iterator filler = fillers_.begin();
       filler != fillers_.end(); ++filler) {
    delete *filler;
  }  
} // VgHistoManager::~VgHistoManager()


//_____________________________________________________________________
/**
 * Books all histograms.
 */
void 
VgHistoManager::bookHistograms()
{
  /// Loop over histo fillers
  for (VgHistoFillerCollection::iterator filler = fillers_.begin();
       filler != fillers_.end(); ++filler) {
    (*filler)->bookHistograms();
  }    
} // VgHistoManager::bookHistograms()


//_____________________________________________________________________
/**
 * Applies selection and fills all histograms.
 */
void 
VgHistoManager::fillHistograms(VgEvent const& event)
{
  pat::strbitset ret = selector_.getBitTemplate();
  if (selector_(event, ret)) {
    /// Loop over histo fillers
    for (VgHistoFillerCollection::iterator filler = fillers_.begin();
         filler != fillers_.end(); ++filler) {
      (*filler)->fillHistograms(selector_.selectedEvent());
    } /// Loop over histo fillers
  } /// if (selector_(event))
} // VgHistoManager::fillHistograms()


//_____________________________________________________________________
/**
 * Prints summary report.
 */
void 
VgHistoManager::print(ostream & out) const
{
  selector_.printCutflows(out);
} 
// void 
// VgHistoManager::print(ostream & out)

