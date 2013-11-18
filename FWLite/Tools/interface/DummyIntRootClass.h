#ifndef FWLite_Tools_DummyIntRootClass_h
#define FWLite_Tools_DummyIntRootClass_h
#include "FWLite/Tools/interface/DummyRootClassTemplate.h"
namespace fwlite {
  class DummyIntRootClass : public DummyRootClassTemplate<Int_t>
  {
    public:
      DummyIntRootClass(Int_t iData) : DummyRootClassTemplate<Int_t>(iData) {}
      virtual ~DummyIntRootClass() {}
      ClassDef(DummyIntRootClass, 0)
  }; // DummyIntRootClass
}
#endif