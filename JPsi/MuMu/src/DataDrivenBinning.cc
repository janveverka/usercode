/**
  * Jan Veverka, Caltech,  26 October 2011
  */

#include <algorithm>
#include <cmath>
#include <list>

#include "TError.h"
#include "TH1I.h"
#include "TMath.h"

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
DataDrivenBinning::getBoundaries()
{
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

  /// Ancrease the range symmetrically to correspond to an integer number
  /// of bins.
  double margin = nbins * binWidth - (xstop - xstart);
  xstart -= 0.5 * margin;
  xstop  += 0.5 * margin;

  /// TODO: Use the fact that we already have sorted data and
  /// simplify the code bellow so that it doesn't need the TH1F.

  /// Get the bin frequencies for uniform bins.
  TH1I * hist = new TH1I("hist", "hist", nbins, xstart, xstop);
  for (const_iterator ix = x_.begin(); ix != x_.end(); ++ix) {
    hist->Fill(*ix);
  }

  /// Store the bincontents.
  std::vector<double> contents;

  /// Merge bins with low frequencies.  Store bin boundaries.  Loop over 
  /// the uniform bins forward.  
  size_t binContent = 0.;
  for (size_t bin = 1; bin <= nbins; ++bin) {
    binContent += hist->GetBinContent(bin);
    if (binContent >= minBinContent_) {
      double newBoundary = hist->GetBinLowEdge(bin) + binWidth;
      /// Check if the new boundary is already in the vector.
      std::vector<double>::const_iterator it;
      it = std::find(boundaries_.begin(), boundaries_.end(), newBoundary);
      if (it == boundaries_.end()) {
	/// Didn't find the new boundary in the vector. Let's include it.
	boundaries_.push_back(newBoundary);
	contents.push_back(binContent);
	binContent = 0;
      } // End of check whether new boundary is in the vector.
    } // End of check of the bin contents.
  } // End of forward loop over bins

  /// The last bin may have too few entries.  Walk over the boundaries
  /// backward and remove them as needed
  std::vector<double>::const_reverse_iterator content  = contents.rbegin();
  for (binContent = 0; content != contents.rend(); ++content) {
    binContent += *content;
    if (binContent >= minBinContent_) {
      /// We are done!
      break;
    } else {
      /// Remove the boundary
      boundaries_.pop_back();
    }
  } // End of backward loop over the bin contents.  

  /// Add the last upper boundary of the binning.
  boundaries_.push_back(xstop);

  /// Cleanup allocated memory
  delete hist;  
}


///----------------------------------------------------------------------------
void
DataDrivenBinning::getMedians()
{
  std::vector<const_iterator> binsFirstEntries;
  binsFirstEntries.reserve(boundaries_.size() + 1);

  /// The index of the first entry in the first bin is 0.
  binsFirstEntries.push_back(x_.begin());
  /// Loop over the bin boundaries.
  for (const_iterator ib = boundaries_.begin() + 1; 
       ib != boundaries_.end(); ++ib) {
    /// Loop over the data. Find the first entry with x > boundary. 
    for (const_iterator ix = binsFirstEntries.back() + 1; 
	 ix < x_.end(); ++ix) {
      if (*ix < *ib) continue;
      /// ix points to the first entry in bin with low edge *ib.
      binsFirstEntries.push_back(ix);
      break;
    } /// End of loop over data.
  } /// End of loop over boundaries.

  /// Add the end of the data
  binsFirstEntries.push_back(x_.end());

  /// Loop over the first entries per bin calculate the medians
  /// iix is an iterator over iterators!
  medians_.reserve(boundaries_.size());
  std::vector<const_iterator>::const_iterator iix =  binsFirstEntries.begin();
  for (; iix + 1 < binsFirstEntries.end(); ++iix) {
    const_iterator ifirst = *iix;
    const_iterator ilast  = *(iix + 1);
    double median = TMath::Median( ilast - ifirst, &(*ilast) );
    medians_.push_back(median);
  } /// End of loop over the first entries per bin.
} /// End of getMedians(...)



///----------------------------------------------------------------------------
void
DataDrivenBinning::get()
{
  if (updated_) 
    return;

  getBoundaries();
  getMedians();

  updated_ = true;
}


///----------------------------------------------------------------------------
std::vector<double> const & 
DataDrivenBinning::binBoundaries()
{
  get();
  return boundaries_;
}


///----------------------------------------------------------------------------
std::vector<double> const & 
DataDrivenBinning::binMedians()
{
  get();
  return medians_;
}

