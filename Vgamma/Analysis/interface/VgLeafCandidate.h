/**
 * \class VgLeafCandidate
 * \brief Representation of a generic elementary particle.
 * Derives from the VgCandidate class and holds a key under
 * which it is stored in the VgTree array.
 *
 * \author Jan Veverka, Caltech
 * \date 15 September 2012.
 */

#ifndef Vgamma_Analysis_VgLeafCandidate_h
#define Vgamma_Analysis_VgLeafCandidate_h

#include "Vgamma/Analysis/interface/VgCandidate.h"
#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"

namespace cit {
  class VgLeafCandidate;
  typedef std::vector<VgLeafCandidate> VgLeafCandidates;
  
  class VgLeafCandidate : public VgCandidate {
  public:
    /// Ctor and dtor
    VgLeafCandidate(VgAnalyzerTree const &, ParticleType, unsigned);
    VgLeafCandidate(VgLeafCandidate const &);
    VgLeafCandidate();
    ~VgLeafCandidate() {}
    // VgLeafCandidate & operator=(VgLeafCandidate const &);
    /// Accessors
    unsigned key() const {return key_;}
    /// Static data
    static const double kElectronMass;
    static const double kMuonMass;
    static const double kPhotonMass;
  private:
    /// Initialize data members
    void init();
    /// Reference to our tree holding data
    VgAnalyzerTree const * tree_;
    /// Index in the VgTree array. 
    unsigned key_;
  }; /// class VgLeafCandidate
} /// namespace cit

#endif // #define Vgamma_Analysis_VgCandidate_h
