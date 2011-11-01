#include "JPsi/MuMu/interface/RooChi2Calculator.h"
/**
  * Implementation of the RooChi2Calculator calss
  * Jan Veverka, Caltech, 26 October 2011
  */

#include <iostream>

#include "RooCurve.h"
#include "RooMsgService.h"

using namespace cit;
using namespace std;

/// Make this a ROOT class
ClassImp(RooChi2Calculator)

///----------------------------------------------------------------------------
RooChi2Calculator::RooChi2Calculator(RooPlot const * plot) :
  plot_(plot),
  _nominalBinWidth(1)
{}


///----------------------------------------------------------------------------
RooChi2Calculator::~RooChi2Calculator()
{}


///----------------------------------------------------------------------------
RooHist*
RooChi2Calculator::residHist(const char *histname, const char* curvename,
                             bool normalize)
const
{
  // Create and return RooHist containing  residuals w.r.t to given curve->
  // If normalize is true, the residuals are normalized by the histogram
  // errors creating a RooHist with pull values


  // Find curve object
  RooCurve* curve = (RooCurve*) plot_->findObject(curvename,
                                                  RooCurve::Class());
  if (!curve) {
    coutE(InputArguments) << "RooPlot::residHist(" << plot_->GetName()
                          << ") cannot find curve" << endl ;
    return 0 ;
  }

  // Find histogram object
  RooHist* hist = (RooHist*) plot_->findObject(histname,
                                               RooHist::Class()) ;
  if (!hist) {
    coutE(InputArguments) << "RooPlot::residHist(" << GetName()
                          << ") cannot find histogram" << endl ;
    return 0 ;
  }


  // Copy all non-content properties from hist
  RooHist* ret = new RooHist(_nominalBinWidth) ;
  if (normalize) {
    ret->SetName(Form("pull_%s_%s", hist->GetName(), curve->GetName())) ;
    ret->SetTitle(Form("Pull of %s and %s", hist->GetTitle(),
                       curve->GetTitle())) ;
  } else {
    ret->SetName(Form("resid_%s_%s", hist->GetName(), curve->GetName())) ;
    ret->SetTitle(Form("Residual of %s and %s", hist->GetTitle(),
                       curve->GetTitle())) ;
  }

  // Determine range of curve
  Double_t xstart, xstop, y ;
#if ROOT_VERSION_CODE >= ROOT_VERSION(4,0,1)
  curve->GetPoint(0, xstart, y) ;
  curve->GetPoint(curve->GetN()-1,xstop,y) ;
#else
  const_cast<RooCurve&>(curve).GetPoint(0, xstart, y) ;
  const_cast<RooCurve&>(curve).GetPoint(curve->GetN()-1, xstop, y) ;
#endif

  // Add histograms, calculate Poisson confidence interval on sum value
  for(Int_t i=0 ; i < hist->GetN() ; i++) {
    Double_t x, point;
#if ROOT_VERSION_CODE >= ROOT_VERSION(4,0,1)
    hist->GetPoint(i,x,point) ;
#else
    const_cast<RooHist&>(hist).GetPoint(i,x,point) ;
#endif

    // Only calculate pull for bins inside curve range
    if (x<xstart || x>xstop) continue ;

    Double_t xl = x - hist->GetErrorXlow(i);
    Double_t xh = x + hist->GetErrorXhigh(i);
    Double_t yy = point - curve->average(xl, xh);
    Double_t dyl = hist->GetErrorYlow(i) ;
    Double_t dyh = hist->GetErrorYhigh(i) ;
    if (normalize) {
        Double_t norm = (yy>0?dyl:dyh);
	if (norm==0.) {
	  coutW(Plotting) << "cit::RooChi2Calculator::resisHist(histname ="
                          << hist->GetName() << ", ...) WARNING: point "
                          << i << " has zero error, setting residual to zero"
                          << endl ;
	  yy=0 ;
	  dyh=0 ;
	  dyl=0 ;
	} else {
	  yy   /= norm;
	  dyh /= norm;
	  dyl /= norm;
	}
    }
    ret->addBinWithError(x,yy,dyl,dyh);
  }
  return ret;
}
