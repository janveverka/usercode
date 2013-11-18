#ifndef FWLite_Tools_DummyRootClassTemplate_tpp
#define FWLite_Tools_DummyRootClassTemplate_tpp

#include "FWLite/Tools/interface/DummyRootClassTemplate.h"
/**
  * Implementation of \class DummyRootClassTemplate
  * Jan Veverka, MIT, 18 November 2008
  */

#include <iostream>       // std::cout and std::endl
#include <typeinfo>       // operator typeid

/// Make this a ROOT class
templateClassImp(fwlite::DummyRootClassTemplate)


///----------------------------------------------------------------------------
template <class T>
fwlite::DummyRootClassTemplate<T>::DummyRootClassTemplate(T iData) :
  fData(iData)
{}


///----------------------------------------------------------------------------
template <class T>
fwlite::DummyRootClassTemplate<T>::~DummyRootClassTemplate()
{}


///----------------------------------------------------------------------------
template <class T>
void
fwlite::DummyRootClassTemplate<T>::printData()
{
  std::cout << "fwlite::DummyRootClassTemplate<" << typeid(T).name()
            << ">::printData(): data: " << fData << std::endl;
}

#endif
