#include <algorithm>
#include <vector>

#include "TMath.h"

#include "JPsi/MuMu/interface/ModalInterval.h"

using namespace cit;

ClassImp(ModalInterval)

///----------------------------------------------------------------------------
/// Default constructor.
ModalInterval::ModalInterval() :
  fraction_(1.),
  updated_(false),
  x_(0)
{
  first_ = x_.begin();
  last_  = x_.end() - 1;
}


///----------------------------------------------------------------------------
ModalInterval::ModalInterval(const_iterator first, const_iterator last,
                             double fraction) :
  fraction_(fraction),
  updated_(false),
  x_(0)
{
  readData(first, last);
}


///----------------------------------------------------------------------------
ModalInterval::~ModalInterval(){}


///----------------------------------------------------------------------------
void
ModalInterval::getInterval(double& low, double& high)
{
  get();
  low  = *first_;
  high = *last_;
  return;
}


///----------------------------------------------------------------------------
void
ModalInterval::get()
{
  /// Check if we need to update the calculation
  if (updated_ == true) {
    /// Cached values are up to date. No need to carry on.
    return;
  }

  /// Check if the fraction is less than unity
  if (fraction_ >= 1.) {
    /// The fraction is greater or equal to one.  We return an interval
    /// containing all the data.
    first_ = x_.begin();
    last_  = x_.end() - 1;
    updated_ = true;
    return;
  }

  /// Here comes the meat.

  /// Set the default bounds include the left-most interval.
  initBounds();

  /// Calculate the size of the default interval.
  double dx = *last_ - *first_;

  /// Find the smallest interval containing at least fraction of the
  /// total entries. Loop over all intervals.
  for (std::vector<double>::const_iterator first = first_, last  = last_;
       last < x_.end(); ++first, ++last)
  {
    /// Compare the size of the defoult interval with the current one.
    if (*last - *first < dx) {
      /// Found new shortest interval.  Store its bounds and size.
      first_ = first;
      last_  = last;
      dx = *last_ - *first_;
    }
  } /// End of loop over all intervals.

  updated_ = true;
  return;
}


///----------------------------------------------------------------------------
double
ModalInterval::getLowBound() {
  get();
  return *first_;
}


///----------------------------------------------------------------------------
double
ModalInterval::getHighBound() {
  get();
  return *last_;
}


///----------------------------------------------------------------------------
double
ModalInterval::getSize() {
  get();
  return *last_ - *first_;
}


///----------------------------------------------------------------------------
/// Update the default interval boundaries to the left most interval.
void
ModalInterval::initBounds() {
  /// Calculate the number of data entries in the interval
  size_t interval_entries = TMath::Ceil(fraction_ * x_.size());

  /// Update the bounds.
  first_ = x_.begin();
  last_  = x_.begin() + interval_entries - 1;

  updated_  = false;
}


///----------------------------------------------------------------------------
void
ModalInterval::setFraction(double fraction) {
  fraction_ = fraction;
  initBounds();
  updated_  = false;
}


///----------------------------------------------------------------------------
void
ModalInterval::readData(const_iterator first, const_iterator last) {
  updated_  = false;

  /// Check if [first, last) is not empty.
  if (first >= last) {
    /// There is no data available.
    x_.resize(0);
    initBounds();
    updated_ = true;
    return;
  }

  x_.resize(last - first);

  /// Set the first and last to include the left-most interval
  initBounds();

  /// Copy the source data to a new vector to sort it
  std::copy(first, last, x_.begin());

  /// Sort the data
  std::sort(x_.begin(), x_.end());
}

