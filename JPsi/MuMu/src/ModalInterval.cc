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
  lower_ = x_.begin();
  upper_ = x_.end() - 1;
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
ModalInterval::ModalInterval(size_t n, double* first, double fraction) :
  fraction_(fraction),
  updated_(false),
  x_(0)
{
  readData(n, first);
}


///----------------------------------------------------------------------------
ModalInterval::ModalInterval(std::vector<double> const& data, double fraction) :
  fraction_(fraction),
  updated_(false),
  x_(0)
{
  readData(data);
}


///----------------------------------------------------------------------------
ModalInterval::~ModalInterval(){}


///----------------------------------------------------------------------------
void
ModalInterval::getInterval(double& lower, double& upper)
{
  get();
  lower = *lower_;
  upper = *upper_;
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
    lower_ = x_.begin();
    upper_  = x_.end() - 1;
    updated_ = true;
    return;
  }

  /// Here comes the meat.

  /// Set the default bounds include the left-most interval.
  initBounds();

  /// Calculate the size of the default interval.
  double dx = *upper_ - *lower_;

  /// Find the smallest interval containing at least fraction of the
  /// total entries. Loop over all intervals.
  for (std::vector<double>::const_iterator first = lower_, last  = upper_;
       last < x_.end(); ++first, ++last)
  {
    /// Compare the size of the defoult interval with the current one.
    if (*last - *first < dx) {
      /// Found new shortest interval.  Store its bounds and size.
      lower_ = first;
      upper_  = last;
      dx = *upper_ - *lower_;
    }
  } /// End of loop over all intervals.

  updated_ = true;
  return;
}


///----------------------------------------------------------------------------
double
ModalInterval::getLowerBound() {
  get();
  return *lower_;
}


///----------------------------------------------------------------------------
double
ModalInterval::getUpperBound() {
  get();
  return *upper_;
}


///----------------------------------------------------------------------------
double
ModalInterval::getSize() {
  get();
  return *upper_ - *lower_;
}


///----------------------------------------------------------------------------
/// Update the default interval boundaries to the left most interval.
void
ModalInterval::initBounds() {
  /// Calculate the number of data entries in the interval
  size_t interval_entries = TMath::Ceil(fraction_ * x_.size());

  /// Update the bounds.
  lower_ = x_.begin();
  upper_  = x_.begin() + interval_entries - 1;

  updated_  = false;
}


///----------------------------------------------------------------------------
void
ModalInterval::readData(size_t n, double* first) {
  readData(first, first + n);
}


///----------------------------------------------------------------------------
void
ModalInterval::readData(std::vector<double> const& data) {
  readData(data.begin(), data.end());
}


///----------------------------------------------------------------------------
void
ModalInterval::setFraction(double fraction) {
  fraction_ = fraction;
  initBounds();
  updated_  = false;
}


///----------------------------------------------------------------------------
/// Set the fraction of the events in terms of nsigma such that it is same as 
/// for a Gaussian distribution in mean +/- nsigma * sigma
void
ModalInterval::setSigmaLevel(double nsigma) {
  fraction_ = 1 - TMath::Prob(nsigma*nsigma, 1);
  initBounds();
  updated_  = false;
}

