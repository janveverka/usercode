//--*-C++-*--
/*
  Author: Jan Veverka

  Calculates the shortest interval (x_lo, x_hi) containing at least the given
  fraction in (0,1] of the given elements [first, last).

*/
#ifndef JPSI_MUMU_MODALINTERVAL_H
#define JPSI_MUMU_MODALINTERVAL_H

#include <type>

class ModalInterval {
public:
  // ModalInterval() {};
  // inline virtual ~ModalInterval() {};


  template<class InputIterator, typename RealNumber>
  void get(InputIterator first, InputIterator last, RealNumber fraction,
            iterator_traits<InputIterator>::reference low,
            iterator_traits<InputIterator>::reference high);

  ClassDef(ModalInterval,1)
}; // end of declaration class ModalInterval

#endif
