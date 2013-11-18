#include "FWLite/Tools/interface/DummyRootClassTemplate.h"
/**
  * Implementation of \class DummyRootClassTemplate
  * Jan Veverka, MIT, 18 November 2008
  */

#include <iostream>

/// Make this a ROOT class
templateClassImp(DummyRootClassTemplate)


///----------------------------------------------------------------------------
template <class T>
DummyRootClassTemplate<T>::DummyRootClassTemplate(T const & iData) :
  fData(iData)
{}


///----------------------------------------------------------------------------
template <class T>
DummyRootClassTemplate<T>::~DummyRootClassTemplate()
{}


///----------------------------------------------------------------------------
template <class T>
void
DummyRootClassTemplate<T>::print()
{
  std::cout << "DummyRootClassTemplate<T>::print(): data: "
            << fData << std::endl;
}
