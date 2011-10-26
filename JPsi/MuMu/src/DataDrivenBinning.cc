/**
  * Jan Veverka, Caltech,  26 October 2011
  */

#include <algorithm>
#include <cmath>
#include <list>
#include "TMath.h"
#include "TError.h"
#include "JPsi/MuMu/interface/DataDrivenBinning.h"

using namespace cit;

/// Make this a ROOT class
ClassImp(DataDrivenBinning)

///----------------------------------------------------------------------------
/// Default constructor
DataDrivenBinning::DataDrivenBinning()
{}


///----------------------------------------------------------------------------
DataDrivenBinning::DataDrivenBinning(const_iterator first, const_iterator last,
                                     size_t minBinContent,
				     size_t maxBinContent) :
  ModalInterval(first, last, 1.), minBinContent_(minBinContent),
  maxBinContent_(maxBinContent), boundaries_(0), medians_(0), niceNumbers_(0)
{
  initNiceNumbers();
}


///----------------------------------------------------------------------------
DataDrivenBinning::DataDrivenBinning(size_t n, double* first,
                                     size_t minBinContent,
				     size_t maxBinContent) :
  ModalInterval(n, first, 1.), minBinContent_(minBinContent),
  maxBinContent_(maxBinContent), boundaries_(0), medians_(0), niceNumbers_(0)
{
  initNiceNumbers();
}


///----------------------------------------------------------------------------
DataDrivenBinning::DataDrivenBinning(std::vector<double> const & data,
                                     size_t minBinContent, 
				     size_t maxBinContent) :
  ModalInterval(data, 1.), minBinContent_(minBinContent),			  maxBinContent_(maxBinContent), boundaries_(0), medians_(0), niceNumbers_(0) 
{
  initNiceNumbers();
}


///----------------------------------------------------------------------------
DataDrivenBinning::~DataDrivenBinning()
{}


///----------------------------------------------------------------------------
void
DataDrivenBinning::initNiceNumbers()
{
  niceNumbers_.push_back(1);
  niceNumbers_.push_back(2);
  niceNumbers_.push_back(2.5);
  niceNumbers_.push_back(5);
  
  std::sort(niceNumbers_.begin(), niceNumbers_.end());
}


///----------------------------------------------------------------------------
double
DataDrivenBinning::getNiceBinWidth(double maxBinWidth) const
{
  /// Find a, n such that maxBinWidth = a * 10^n with a in [1, 10), n integer.
  double n = floor(log10(maxBinWidth));
  double a = maxBinWidth * pow(10, -n);  

  /// Find greatest nice number smaller or equal to a.  Nice numbers are
  /// sorted in ascending order. Loop over them backwards, from the greatest
  /// to the least.
  std::vector<double>::const_reverse_iterator nice = niceNumbers_.rbegin();
  for (; nice != niceNumbers_.rend(); ++nice) {
    if (*nice <= a) {
      /// Found a good nice number.  Retrun the corresponding nice bin width.
      a = *nice;
      return a * pow(10, n);
    }
  } /// End of loop over nice numbers.

  /// This should never happen!
  Warning("getNiceBinWidth", "Failed.");
  return maxBinWidth;
}


///----------------------------------------------------------------------------
/// The MEAT.
void
DataDrivenBinning::get()
{
  /// Store the bin boundaries in a list so that we can easily remove them
  std::list<double> boundaries;

  /// Get a range to caver all data and store it
  ModalInterval::get();
  double xstart = lowerBound();
  double xstop  = upperBound();

  /// Get the maximum bin width given by maxBinContent
  setNumberOfEntriesToCover(maxBinContent_);
  double maxBinWidth = length();

  /// Find the greatest "nice looking" bin width smaller than the max.
  double binWidth = getNiceBinWidth(maxBinWidth);

  /// Get the minimum number of bins given the range of data and maximum
  /// bin content.
  size_t nbins = TMath::Ceil((xstop - xstart) / binWidth);
  
}

