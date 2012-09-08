/**
 * Implementation of the VgHistoManager class.
 * \author Jan Veverka, Caltech
 * \date 08 September 2012
 */

#include "Vgamma/Analysis/interface/VgHistoManager.h"
#include "Vgamma/Analysis/interface/VgMuonHistoFiller.h"
#include "Vgamma/Analysis/interface/VgPhotonHistoFiller.h"
#include "Vgamma/Analysis/interface/VgMCPileupHistoFiller.h"
#include "Vgamma/Analysis/interface/VgPileupHistoFiller.h"

using cit::VgHistoManager;

/**
 * Constructor
 */
VgHistoManager::VgHistoManager(VgAnalyzerTree const& tree,
                               TDirectory & output) 
{
  TDirectory *cwd = gDirectory;
  output.cd();  
  
  fillers_.push_back(new VgMuonHistoFiller    (tree, histos_, &tree.nMu ));
  fillers_.push_back(new VgPhotonHistoFiller  (tree, histos_, &tree.nPho));
  fillers_.push_back(new VgMCPileupHistoFiller(tree, histos_            ));
  fillers_.push_back(new VgPileupHistoFiller  (tree, histos_            ));
  
  bookHistograms();
  
  cwd->cd();
} // VgHistoManager::VgHistoManager(..)


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


/**
 * Fills all histograms.
 */
void 
VgHistoManager::fillHistograms()
{
  /// Loop over histo fillers
  for (VgHistoFillerCollection::iterator filler = fillers_.begin();
       filler != fillers_.end(); ++filler) {
    (*filler)->fillHistograms();
  }    
} // VgHistoManager::fillHistograms()

