/**
 * Implementation of the VgBarrelPhotonHistoFiller class.
 * \author Jan Veverka, Caltech
 * \date 08 September 2012
 */

#include <math.h>
#include <iostream>
#include "TDirectory.h"
#include "TMath.h"
#include "Vgamma/Analysis/interface/VgPhoton.h"
#include "Vgamma/Analysis/interface/VgBarrelPhotonHistoFiller.h"

using namespace std;
using cit::VgBarrelPhotonHistoFiller;

/**
 * Ctor.
 */
VgBarrelPhotonHistoFiller::VgBarrelPhotonHistoFiller() : VgPhotonHistoFiller()
{} // Default ctor.


/**
 * Dtor.
 */
VgBarrelPhotonHistoFiller::~VgBarrelPhotonHistoFiller() {}


/**
 * Books the histograms.
 */
void
VgBarrelPhotonHistoFiller::bookHistograms()
{
  TDirectory * cwd = gDirectory;

  if (cwd->GetDirectory("Barrel")) cwd->cd("Barrel");
  else cwd->mkdir("Barrel")->cd();
  
  VgPhotonHistoFiller::bookHistograms();

  cwd->cd();
    
} // VgBarrelPhotonHistoFiller::bookHistograms(..)


/**
 * Fills the histograms.
 */
void
VgBarrelPhotonHistoFiller::fillHistograms(cit::VgEvent const& event)
{
  cit::VgLeafCandidates const & photons = event.photons();
  histos_["phoN"]->Fill(photons.size());
  /// Loop over photons
  for (cit::VgLeafCandidates::const_iterator pho = photons.begin();
       pho != photons.end(); ++pho) {
    if (cit::VgPhoton(*pho).isInBarrel()) fillCand(*pho);
  } /// Loop over photons  
} // VgBarrelPhotonHistoFiller::fillHistograms(..)

