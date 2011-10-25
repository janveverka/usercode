//--*-C++-*--
/*
  Author: Jan Veverka

  Calculates the shortest interval (x_lo, x_hi) containing at least the given
  fraction in (0,1] of the given elements [first, last).

*/
#ifndef JPSI_MUMU_MODALINTERVAL_H
#define JPSI_MUMU_MODALINTERVAL_H

#include "TObject.h"

namespace cit {
  class ModalInterval : public TObject {

  public:
    typedef std::vector<double>::const_iterator const_iterator;
    ModalInterval();
    ModalInterval(const_iterator first, const_iterator last, double fraction);
    virtual ~ModalInterval();

    void   getInterval(double& low, double& high);
    double getLowBound();
    double getHighBound();
    double getSize();

    void readData(const_iterator first, const_iterator last);
    void setFraction(double fraction);

  protected:
    /// Calculates the interval.
    void get();
    /// Sets the interval bounds to the left most interval.
    void initBounds();

    /// Interval contains at least fraction_ of the total entries.
    double fraction_;
    /// Has the interval been calculated?
    bool   updated_;
    /// Sorted copy of the input data.
    std::vector<double> x_;
    /// Interval lower und upper bounds as pointers to elements of x_.
    const_iterator first_;
    const_iterator last_;

    ClassDef(ModalInterval,0)

  };
} // end of namespace cit
#endif
