#include "JPsi/MuMu/interface/ModalInteval.h"

ClassImp(ModalInteval)

void
ModalInteval::get(InputIterator first, InputIterator last, RealNumber fraction,
                  iterator_traits<InputIterator>::reference low,
                  iterator_traits<InputIterator>::reference high)
{
  /// dummy implementation for now
  low = *first;
  high = *last;
}
