#include "FWLite/Tools/interface/GraphInterpolationFunctor.h"
/**
  * Implementation of \class GraphInterpolationFunctor
  * Jan Veverka, MIT, 2 August 2013
  */

#include <iostream>

/// Make this a ROOT class
ClassImp(GraphInterpolationFunctor)

///----------------------------------------------------------------------------
/// Constructor
GraphInterpolationFunctor::GraphInterpolationFunctor(const TGraph & graph) :
  graph_(graph)
{}


///----------------------------------------------------------------------------
/// Destructor
GraphInterpolationFunctor::~GraphInterpolationFunctor()
{}


///----------------------------------------------------------------------------
/// Example method. Prints some information about adding new classes to ROOT
/// in the standard output.
Double_t
GraphInterpolationFunctor::operator()(Double_t x)
{
  return graph_.Eval(x);
} /// operator(..)

