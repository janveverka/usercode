/**
  * Takes ubinned univariate data and calculates bin boundaries and
  * bin medians based on the data such that:
  *   o Number of data entries per bin is in a given range 
  *     [minBinContent, maxBinContent].
  *     5 <= minBinContent is desireable to obtain a chi2 statistic that follows
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

#include "JPsi/MuMu/interface/ModalInterval.h"

// TODO : make this a derived class of the ModalInterval.
namespace cit {
  class DataDrivenBinning : public ModalInterval {

  public:
    DataDrivenBinning();
    DataDrivenBinning(const_iterator first, const_iterator last,
                      size_t minBinContent = 10, size_t maxBinContent = 100);
    DataDrivenBinning(size_t n, double *first,
                      size_t minBinContent = 10, size_t maxBinContent = 100);
    DataDrivenBinning(std::vector<double> const & data,
                      size_t minBinContent = 10, size_t maxBinContent = 100);
    virtual ~DataDrivenBinning();

    std::vector<double> const & binBoundaries();
    std::vector<double> const & binMedians();
    double getNiceBinWidth(double maxBinWidth) const;

  protected:
    void getBinning();
    void getBoundaries();
    void getMedians();
    void initNiceNumbers();

    size_t minBinContent_;
    size_t maxBinContent_;
    std::vector<double> boundaries_;
    std::vector<double> medians_;
    std::vector<double> niceNumbers_;

    /// Make this a ROOT class.
    ClassDef(DataDrivenBinning,0)

  };  /// end of declaration of class DataDrivenBinning
} /// end of namespace cit

#endif
