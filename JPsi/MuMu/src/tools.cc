//******************************************//
// author: Jan Veverka, Caltech
// date: 23 November 2011
//
//
//  TODO list:
//
//
//
//  Modified by:
//
//******************************************//

#include <iostream>
#include "TH1.h"
#include "TAxis.h"
#include "TMath.h"
#include "TLorentzVector.h"

#include "JPsi/MuMu/interface/tools.h"

using namespace std;

Double_t zMassPdg() { return 91.1876; }

Double_t Oplus(Double_t a, Double_t b) { return TMath::Sqrt(a*a + b*b); }

Double_t Oplus(Double_t a, Double_t b, Double_t c) { 
  return TMath::Sqrt(a*a + b*b + c*c); 
}


///-----------------------------------------------------------------------------
Double_t muonSigmaPtOverPt(Double_t pt, Double_t eta) {
  /// Muon pt relative error sigma(pt_mu)/pt, see fig. 17 of AN2008_097_v3.pdf
  /// Normalized to 1 for Pt < 10 GeV
  Double_t ptFactor = pt < 10. ? 1 : -5 + 6  * TMath::Log10(pt);

  /// Muon pt relative error as a function of eta
  /// CMS PAS TRK-10-004 eq. (5)
  Double_t b[] = {1.61, 5e-3, 1.9e-2, 1.4e-2, 1.5};
  Double_t etaFactor;
  if (TMath::Abs(eta) < b[0]) {
    Double_t b0MinusB4 = b[0] - b[4];
    Double_t c = b[2] + b[3] + b0MinusB4 * b0MinusB4 - b[1] * b[0] * b[0];
    etaFactor = c + b[1] * eta * eta;
  } else {
    Double_t absEtaMinusB4 = TMath::Abs(eta) - b[4];
    etaFactor = b[2] + b[3] * absEtaMinusB4 * absEtaMinusB4;
  }
  return ptFactor * etaFactor;
}

///-----------------------------------------------------------------------------
/// see CMS IN 2000/028 for EE, 2008 JINST 3 S08004 and CMS DN-2007/12 for EB
Double_t photonSigmaEOverE(Double_t E, Double_t eta){
  if (TMath::Abs(eta) < 1.5) {
    Double_t s = 0.035;
    Double_t n = 0.15;
    Double_t c = 0.02;
    Double_t sTerm = s / TMath::Sqrt(E);
    Double_t nTerm = n / E;
    return TMath::Sqrt(sTerm * sTerm + nTerm * nTerm + c * c);
  } else {
    Double_t s = 0.05;
    Double_t n = 0.45;
    Double_t c = 0.06;
    Double_t sTerm = s / TMath::Sqrt(E);
    Double_t nTerm = n / E;
    return TMath::Sqrt(sTerm * sTerm + nTerm * nTerm + c * c);
  }
}

///-----------------------------------------------------------------------------
Double_t photonSigmaPtOverPt(Double_t pt, Double_t eta){
  return photonSigmaEOverE(pt * TMath::CosH(eta), eta);
}

///-----------------------------------------------------------------------------
Double_t phoEtrue(Double_t mmMass) {
  return 0.5*(zMassPdg()*zMassPdg() - mmMass*mmMass) / mmMass;
}

///-----------------------------------------------------------------------------
Double_t phoEmeas(Double_t mmgMass, Double_t mmMass) {
  return 0.5 * (mmgMass*mmgMass - mmMass*mmMass) / mmMass;
}

///-----------------------------------------------------------------------------
Double_t kRatio(Double_t mmgMass, Double_t mmMass) {
  return phoEtrue(mmMass) / phoEmeas(mmgMass, mmMass);
}

///-----------------------------------------------------------------------------
Double_t inverseK(Double_t mmgMass, Double_t mmMass) {
  return  phoEmeas(mmgMass, mmMass) / phoEtrue(mmMass);
}

///-----------------------------------------------------------------------------
Double_t scaledMmgMass10(Double_t scale3,
			 Double_t pt1, Double_t eta1, Double_t phi1,
			 Double_t pt2, Double_t eta2, Double_t phi2,
			 Double_t pt3, Double_t eta3, Double_t phi3)
{
  TLorentzVector p1, p2, p3;
  p1.SetPtEtaPhiM(pt1, eta1, phi1, 0);
  p2.SetPtEtaPhiM(pt2, eta2, phi2, 0);
  p3.SetPtEtaPhiM((1+scale3)*pt3, eta3, phi3, 0);
  return (p1+p2+p3).M();
}

///-----------------------------------------------------------------------------
Double_t scaledMmgMass3(Double_t sfactor, Double_t mmgMass, Double_t mmMass)
{
  Double_t mm2 = mmMass*mmMass;
  Double_t mmg2 = mmgMass*mmgMass;
  return TMath::Sqrt(mm2 + sfactor * (mmg2 - mm2));
}

///-----------------------------------------------------------------------------
/// Smeared photon energy given the scale and resolution and reference
/// scale and resolution and the reco and gen energies.
Double_t phoSmearE(Double_t scale, Double_t resolution,
		   Double_t refScale, Double_t refResolution,
		   Double_t phoE, Double_t phoGenE)
{
  /// Normalized photon response
  Double_t t = (phoE / phoGenE - 1. - refScale) / refResolution;
  /// Inject back the desired scale and resolution
  return phoGenE * (1. + scale + resolution * t);
}

///-----------------------------------------------------------------------------
/// Photon energy smearing factor relative to the reference reco energy 
/// given the scale and resolution and reference
/// scale and resolution and the reco and gen energies.
Double_t phoSmearF(Double_t scale, Double_t resolution,
		   Double_t refScale, Double_t refResolution,
		   Double_t phoE, Double_t phoGenE)
{
  return phoSmearE(scale, resolution, refScale, refResolution, phoE, phoGenE) / 
         phoE;
}

///-----------------------------------------------------------------------------
/// mmg mass smeared for 
/// given photon energy scale and resolution and reference
/// scale and resolution and the reco and gen energies.
Double_t mmgMassPhoSmearE(Double_t scale, Double_t resolution,
			  Double_t refScale, Double_t refResolution,
			  Double_t phoE, Double_t phoGenE,
			  Double_t mmgMass, Double_t mmMass)
{
  Double_t sfactor = phoSmearF(scale, resolution, refScale, refResolution, phoE,
			       phoGenE);
  return scaledMmgMass3(sfactor, mmgMass, mmMass);
}

///-----------------------------------------------------------------------------
Double_t scaledDimuonPhotonMass(Double_t scale2,
				Double_t pt1, Double_t eta1, Double_t phi1, Double_t m1,
				Double_t pt2, Double_t eta2, Double_t phi2)
{
  // 1: dimuon, 2: photon
  TLorentzVector p1, p2;
  p1.SetPtEtaPhiM(pt1, eta1, phi1, m1);
  p2.SetPtEtaPhiM( (1 + scale2) * pt2, eta2, phi2, 0);
  return (p1 + p2).M();
}

///-----------------------------------------------------------------------------
Double_t twoBodyMass(Double_t pt1, Double_t eta1, Double_t phi1, Double_t m1,
		     Double_t pt2, Double_t eta2, Double_t phi2, Double_t m2)
{
  // 1: massless particle 1, 2: massless particle 2
  TLorentzVector p1, p2;
  p1.SetPtEtaPhiM(pt1, eta1, phi1, m1);
  p2.SetPtEtaPhiM(pt2, eta2, phi2, m2);
  return (p1 + p2).M();
}

///-----------------------------------------------------------------------------
Double_t threeBodyMass(Double_t pt1, Double_t eta1, Double_t phi1, Double_t m1,
		       Double_t pt2, Double_t eta2, Double_t phi2, Double_t m2,
		       Double_t pt3, Double_t eta3, Double_t phi3, Double_t m3)
{
    // 1: massless particle 1, 2: massless particle 2
  TLorentzVector p1, p2, p3;
  p1.SetPtEtaPhiM(pt1, eta1, phi1, m1);
  p2.SetPtEtaPhiM(pt2, eta2, phi2, m2);
  p3.SetPtEtaPhiM(pt3, eta3, phi3, m3);
  return (p1 + p2 + p3).M();
}

///-----------------------------------------------------------------------------
Double_t effSigma(TH1 * hist)
{

  TAxis *xaxis = hist->GetXaxis();
  Int_t nb = xaxis->GetNbins();
  if(nb < 10) {
    cout << "effsigma: Not a valid histo. nbins = " << nb << endl;
    return 0.;
  }
  
  Double_t bwid = xaxis->GetBinWidth(1);
  if(bwid == 0) {
    cout << "effsigma: Not a valid histo. bwid = " << bwid << endl;
    return 0.;
  }
  // Double_t xmax = xaxis->GetXmax();
  Double_t xmin = xaxis->GetXmin();
  Double_t ave = hist->GetMean();
  Double_t rms = hist->GetRMS();

  Double_t total=0.;
  for(Int_t i=0; i<nb+2; i++) {
    total+=hist->GetBinContent(i);
  }
  if(total < 100.) {
    cout << "effsigma: Too few entries " << total << endl;
    return 0.;
  }
  Int_t ierr=0;
  Int_t ismin=999;
  
  Double_t rlim=0.683*total;
  Int_t nrms=rms/(bwid);    // Set scan size to +/- rms
  if(nrms > nb/10) nrms=nb/10; // Could be tuned...

  Double_t widmin=9999999.;
  for(Int_t iscan=-nrms;iscan<nrms+1;iscan++) { // Scan window centre
    Int_t ibm=(ave-xmin)/bwid+1+iscan;
    Double_t x=(ibm-0.5)*bwid+xmin;
    Double_t xj=x;
    Double_t xk=x;
    Int_t jbm=ibm;
    Int_t kbm=ibm;
    Double_t bin=hist->GetBinContent(ibm);
    total=bin;
    for(Int_t j=1;j<nb;j++){
      if(jbm < nb) {
        jbm++;
        xj+=bwid;
        bin=hist->GetBinContent(jbm);
        total+=bin;
        if(total > rlim) break;
      }
      else ierr=1;
      if(kbm > 0) {
        kbm--;
        xk-=bwid;
        bin=hist->GetBinContent(kbm);
        total+=bin;
        if(total > rlim) break;
      }
      else ierr=1;
    }
    Double_t dxf=(total-rlim)*bwid/bin;
    Double_t wid=(xj-xk+bwid-dxf)*0.5;
    if(wid < widmin) {
      widmin=wid;
      ismin=iscan;
    }   
  }
  if(ismin == nrms || ismin == -nrms) ierr=3;
  if(ierr != 0) cout << "effsigma: Error of type " << ierr << endl;
  
  return widmin;
  
}
/// end of cit::effSigma
