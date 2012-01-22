/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
 * This code was autogenerated by RooClassFactory                            * 
 * Jan Veverka, Caltech, 25 Nov 2011                                         *
 * The relativistic Breit-Wigner PDF
 *****************************************************************************/

#ifndef JPSI_MUMU_ROORELATIVISTICBREITWIGNER_H
#define JPSI_MUMU_ROORELATIVISTICBREITWIGNER_H

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class RooRelativisticBreitWigner : public RooAbsPdf {
public:
  RooRelativisticBreitWigner() {} ; 
  RooRelativisticBreitWigner(const char *name, const char *title,
	      RooAbsReal& _x,
	      RooAbsReal& _mean,
	      RooAbsReal& _width);
  RooRelativisticBreitWigner(const RooRelativisticBreitWigner& other, 
			     const char* name=0) ;
  virtual TObject* clone(const char* newname) const { 
    return new RooRelativisticBreitWigner(*this,newname); 
  }
  inline virtual ~RooRelativisticBreitWigner() { }

protected:

  RooRealProxy x ;
  RooRealProxy mean ;
  RooRealProxy width ;
  
  Double_t evaluate() const ;

private:

  ClassDef(RooRelativisticBreitWigner,1) // The Relativistic Breit-Wigner PDF
};
 
#endif
