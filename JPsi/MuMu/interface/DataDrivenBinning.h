/**
  * Takes ubinned univariate data and calculates bin boundaries and
  * bin medians based on the data such that:
  *   o Number of data entries per bin is in a given rane [min, max].
  *     5 <= min is desireable to obtain a chi2 statistic that follows
  *     the chi2 PDF and thus can be used to estimate the p-value,
  *     see the PDG review on Statistics. Some maxixmum is desirable
  *     to visualize the details of the shape in the peak area.
  *   o Bins have uniform widths in regions with high densities (peak).
  *     This width is chosen to be a nice number, e.g. 1, 0.5, 0.25, 0.2 etc.
  *   o Bins have non-uniform widths in regions with low densities (tails)
  *     Neighboring bins with few entries are merged to have at least
  *     the given minimum.
  *
  * Jan Veverka, Caltech,  26 October 2011
  */

#ifndef JPSI_MUMU_DATADRIVENBINNING_H
#define JPSI_MUMU_DATADRIVENBINNING_H

#include <vector>
#include <algorithm>

#include "TObject.h"

// TODO : make this a derived class of the ModalInterval.
namespace cit {
  class DataDrivenBinning : public TObject {

  public:
    typedef std::vector<double>::const_iterator const_iterator;
    DataDrivenBinning();
    DataDrivenBinning(const_iterator first, const_iterator last,
                      size_t min = 10, size_t max = 100);
    DataDrivenBinning(size_t n, double *first,
                      size_t min = 10, size_t max = 100);
    DataDrivenBinning(std::vector<double> const & data,
                      size_t min = 10, size_t max = 100);
    virtual ~DataDrivenBinning();

    inline
    std::vector<double> const &
    boundaries() const {return boundaries_;}

    inline
    std::vector<double> const &
    medians() const {return medians_;}

    ///------------------------------------------------------------------------
    template<typename T>
    void
    readData(T first, T last) {
      updated_  = false;

      /// Check if [first, last) is not empty.
      if (first >= last) {
        /// There is no data available.
        x_.resize(0);
        updated_ = true;
        return;
      }

      x_.resize(last - first);

      /// Copy the source data to a new vector to sort it
      std::copy(first, last, x_.begin());

      /// Sort the data
      std::sort(x_.begin(), x_.end());
    } /// end of template<...> readData(...)

    void readData(size_t n, double* first);
    void readData(std::vector<double> const& data);

  protected:
    void get();

    bool updated_;
    std::vector<double> x_;
    size_t min_;
    size_t max_;
    std::vector<double> boundaries_;
    std::vector<double> medians_;

    /// Make this a ROOT class.
    ClassDef(DataDrivenBinning,0)

  };  /// end of declaration of class DataDrivenBinning
} /// end of namespace cit

#endif
