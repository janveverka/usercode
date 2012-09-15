/**
 * \brief Representation of a generic particle.
 * Holds the weigth and the momentum information so
 * that one can apply efficiency scale factors and
 * energy/momentum corrections.
 *
 * Jan Veverka, Caltech, 15 September 2012.
 */

#ifndef Vgamma_Analysis_VgCandidate_h
#define Vgamma_Analysis_VgCandidate_h

#include "TLorentzVector.h"

namespace cit {
  class VgCandidate {
  public:
    enum ParticleType {kMuon, kPhoton, kElectron, kCombined};
    // Ctor and dtor
    VgCandidate();
    virtual ~VgCandidate() {}
    // Accessors
    TLorentzVector const & momentum() const {return momentum_;}
    ParticleType           type()     const {return type_    ;}
    double                 weight()   const {return weight_  ;}
    // Setters
    void setMomentum(TLorentzVector const& momentum) {momentum_ = momentum;}
    void setType(ParticleType type) {type_ = type;}
    void setWeight(double weight) {weight_ = weight;}
    // Indirect setters
    void scaleWeight(double scaleFactor) {weight_ *= scaleFactor;}
  private:
    TLorentzVector momentum_;
    ParticleType   type_    ;
    double         weight_  ;
  }; // class VgCandidate
} // namespace cit

#endif
