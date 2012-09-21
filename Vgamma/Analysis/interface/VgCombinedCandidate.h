/**
 * \class VgCombinedCandidate
 * \brief Representation of a generic combined particle candidate.
 * Derives from the VgCandidate class and holds a list
 * of daughters that are of type VgLeafCandidate.
 *
 * \author Jan Veverka, Caltech
 * \date 18 September 2012.
 */

#ifndef Vgamma_Analysis_interface_VgCombinedCandidate_h
#define Vgamma_Analysis_interface_VgCombinedCandidate_h

#include "boost/shared_ptr.hpp"
#include "Vgamma/Analysis/interface/VgCandidate.h"
#include "Vgamma/Analysis/interface/VgLeafCandidate.h"
#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"

namespace cit {
  class VgCombinedCandidate;
  typedef std::vector<VgCombinedCandidate> VgCombinedCandidates;
  
  class VgCombinedCandidate : public VgCandidate {
  public:
    /// Ctors and dtor
    VgCombinedCandidate();
    VgCombinedCandidate(VgCombinedCandidate const &);
    ~VgCombinedCandidate() {}
    void addDaughter(VgCandidate const &);
    void addDaughter(VgLeafCandidate const &);
    void addDaughter(VgCombinedCandidate const &);
    /// Accessors
    VgLeafCandidates const & daughters() const {return daughters_;}
    VgLeafCandidate const & daughter(unsigned i) const {return daughters_[i];}
    unsigned numDaughters() const {return daughters_.size();}
    /// Overloaded the equality operator
    bool operator==(VgCombinedCandidate const & other) const;
    bool operator!=(VgCombinedCandidate const & other) const {
      return !operator==(other);
    }
  private:
    void update();
    VgLeafCandidates daughters_;
  }; /// class VgCombinedCandidate
} /// namespace cit

#endif // #define Vgamma_Analysis_interface_VgCombinedCandidate_h
