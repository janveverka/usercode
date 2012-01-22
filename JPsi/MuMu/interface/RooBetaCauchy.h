/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
 * This code was autogenerated by RooClassFactory                            * 
 * Jan Veverka, Caltech, 25 Nov 2011
 * The Beta-Cauchy PDF.
 * The meaning of Beta is the same as in
 * http://www.statistik.wiso.uni-erlangen.de/forschung/d0064.pdf
 * The Beta-Hyperbolic Secant (BHS) Distribution
 * Matthias J. Fischer, David Vaughan
 *****************************************************************************/

#ifndef JPSI_MUMU_ROOBETACAUCHY_H
#define JPSI_MUMU_ROOBETACAUCHY_H

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class RooBetaCauchy : public RooAbsPdf {
public:
  RooBetaCauchy() {} ; 
  RooBetaCauchy(const char *name, const char *title,
	      RooAbsReal& _x,
	      RooAbsReal& _mean,
	      RooAbsReal& _width,
	      RooAbsReal& _beta,
	      RooAbsReal& _theta);
  RooBetaCauchy(const RooBetaCauchy& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { 
    return new RooBetaCauchy(*this,newname); 
  }
  inline virtual ~RooBetaCauchy() { }

protected:

  RooRealProxy x ;
  RooRealProxy mean ;
  RooRealProxy width ;
  RooRealProxy beta ;
  RooRealProxy theta ;
  
  Double_t evaluate() const ;

private:

  ClassDef(RooBetaCauchy,1) // The Beta-Cauchy PDF
};
 
#endif
