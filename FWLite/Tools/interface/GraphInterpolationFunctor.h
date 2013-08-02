#ifndef FWLITE_TOOLS_GRAPHINTERPOLATIONFUNCTOR_H
#define FWLITE_TOOLS_GRAPHINTERPOLATIONFUNCTOR_H

#include "TObject.h"
#include "TGraph.h"

/**
  * Wrapper around TGraph::Eval.
  * Creates a function that interpolates a graph given at 
  * construction.
  * Jan Veverka, MIT,  2 August 2013
  */

class GraphInterpolationFunctor : public TObject {
public:
  GraphInterpolationFunctor(const TGraph &);
  virtual ~GraphInterpolationFunctor();

  /// Print info about this class.
  Double_t operator()(Double_t x);

  /// Make this a ROOT class.
  /// Use 1 as the 2nd arg to store class in a ROOT file.
  ClassDef(GraphInterpolationFunctor,0)
private:
  TGraph graph_;
};  /// end of declaration of class GraphInterpolationFunctor

#endif
