/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $Id: RooRhoKeysPdf.h,v 1.2 2012/05/20 12:15:37 veverka Exp $
 * Authors:                                                                  *
 *   GR, Gerhard Raven,   UC San Diego,        raven@slac.stanford.edu       *
 *   DK, David Kirkby,    UC Irvine,         dkirkby@uci.edu                 *
 *   WV, Wouter Verkerke, UC Santa Barbara, verkerke@slac.stanford.edu       *
 *                                                                           *
 * Copyright (c) 2000-2005, Regents of the University of California          *
 *                          and Stanford University. All rights reserved.    *
 *                                                                           *
 * Redistribution and use in source and binary forms,                        *
 * with or without modification, are permitted according to the terms        *
 * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
 *                                                                           *
 * Modified by JV, Jan Veverka, Caltech, veverka@caltech.edu
 *  such that rho is an additional parameter.            
 *****************************************************************************/
#ifndef FWLITE_TOOLS_ROORHOKEYSPDF_H
#define FWLITE_TOOLS_ROORHOKEYSPDF_H

#include "RooAbsPdf.h"
#include "RooRealProxy.h"

class RooRealVar;

class RooRhoKeysPdf : public RooAbsPdf {
public:
  enum Mirror { NoMirror, MirrorLeft, MirrorRight, MirrorBoth,
		MirrorAsymLeft, MirrorAsymLeftRight,
		MirrorAsymRight, MirrorLeftAsymRight,
		MirrorAsymBoth };
  RooRhoKeysPdf() ;
  RooRhoKeysPdf(const char *name, const char *title,
		RooAbsReal& x, RooAbsReal& rho, RooDataSet& data, 
		Mirror mirror= NoMirror);
  RooRhoKeysPdf(const RooRhoKeysPdf& other, const char* name=0);
  virtual TObject* clone(const char* newname) const {
    return new RooRhoKeysPdf(*this,newname); 
  }
  virtual ~RooRhoKeysPdf();
  
  void LoadDataSet( RooDataSet& data);

protected:
  
  RooRealProxy _x ;
  RooRealProxy _rho ;
  Double_t evaluate() const;

private:
  
  Double_t evaluateFull(Double_t x) const;
  void calculateLookupTable() const;

  Int_t _nEvents;
  Double_t *_dataPts;  //[_nEvents]
  Double_t *_dataWgts; //[_nEvents]
  Double_t *_weights;  //[_nEvents]
  Double_t _sumWgt ;
  Double_t _sigmav;
  
  enum { _nPoints = 1000 };
  // Double_t *_lookupTable[_nPoints+1];
  Double_t *_lookupTable;
  
  Double_t g(Double_t x,Double_t sigma) const;

  Bool_t _mirrorLeft, _mirrorRight;
  Bool_t _asymLeft, _asymRight;

  // cached info on variable
  Char_t _varName[128];
  Double_t _lo, _hi, _binWidth;
  Double_t *_rhoSnapshot;
  
  ClassDef(RooRhoKeysPdf,1) // One-dimensional non-parametric kernel estimation p.d.f.
};

#endif
