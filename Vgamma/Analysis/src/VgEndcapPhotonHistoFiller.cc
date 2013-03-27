/**
 * Implementation of the VgEndcapPhotonHistoFiller class.
 * \author Jan Veverka, Caltech
 * \date 08 September 2012
 */

#include <math.h>
#include <iostream>
#include "TDirectory.h"
#include "TMath.h"
#include "Vgamma/Analysis/interface/VgPhoton.h"
#include "Vgamma/Analysis/interface/VgEndcapPhotonHistoFiller.h"

using namespace std;
using cit::VgEndcapPhotonHistoFiller;

/**
 * Ctor.
 */
VgEndcapPhotonHistoFiller::VgEndcapPhotonHistoFiller() : VgPhotonHistoFiller()
{} // Default ctor.


/**
 * Dtor.
 */
VgEndcapPhotonHistoFiller::~VgEndcapPhotonHistoFiller() {}


/**
 * Books the histograms.
 */
void
VgEndcapPhotonHistoFiller::bookHistograms()
{
  TDirectory * cwd = gDirectory;

  if (cwd->GetDirectory("Endcaps")) cwd->cd("Endcaps");
  else cwd->mkdir("Endcaps")->cd();
  
  VgPhotonHistoFiller::bookHistograms();

  cwd->cd();
    
} // VgEndcapPhotonHistoFiller::bookHistograms(..)


/**
 * Fills the histograms.
 */
void
VgEndcapPhotonHistoFiller::fillHistograms(cit::VgEvent const& event)
{
  cit::VgLeafCandidates const & photons = event.photons();
  histos_["phoN"]->Fill(photons.size());
  /// Loop over photons
  for (cit::VgLeafCandidates::const_iterator pho = photons.begin();
       pho != photons.end(); ++pho) {
    if (!cit::VgPhoton(*pho).isInBarrel()) {
      fillCand(*pho, event.weight());
    }
  } /// Loop over photons  
} // VgEndcapPhotonHistoFiller::fillHistograms(..)

