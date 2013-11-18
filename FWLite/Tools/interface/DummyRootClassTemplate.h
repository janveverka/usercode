#ifndef FWLite_Tools_DummyRootClassTemplate_h
#define FWLite_Tools_DummyRootClassTemplate_h

#include "TObject.h"

/**
  * This is just a boiler plate for adding new class templates to ROOT and
  * using scram/gcc for compilation.
  * Jan Veverka, MIT,  18 November 2013
  */

namespace fwlite {
  template <class T>
  class DummyRootClassTemplate : public TObject {
  public:
    DummyRootClassTemplate(T iData);
    virtual ~DummyRootClassTemplate();

    /// Print info about this class.
    void printData();

  private:
    T fData;

    /// Make this a ROOT class.
    /// Use 1 as the 2nd arg to store class in a ROOT file.
    ClassDef(DummyRootClassTemplate,0)
  };  /// DummyRootClassTemplate
} /// fwlite
#endif // FWLite_Tools_DummyRootClassTemplate_h
