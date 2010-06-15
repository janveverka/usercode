/**
  jan.veverka@caltech.edu, 15 June 2010
  based on PhysicsTools/SelectorUtils/interface/MuonVPlusJetsIDSelectionFunctor.h
*/


#ifndef ElectroWeakAnalysis_MultiBosons_interface_VGammaPhotonIDSelectionFunctor_h
#define ElectroWeakAnalysis_MultiBosons_interface_VGammaPhotonIDSelectionFunctor_h

#include "DataFormats/PatCandidates/interface/Photon.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include <iostream>

class VGammaPhotonIDSelectionFunctor : public Selector<pat::Photon> {

public: // interface

  enum Version_t {TEST, SPRING10};

  VGammaPhotonIDSelectionFunctor(edm::ParameterSet const & parameters){
    std::string versionStr = parameters.getParameter<std::string>("version");
    if (versionStr == "TEST") {
      initialize(SPRING10,
                 parameters.getParameter<double>("ecalIsoConstant"),
                 parameters.getParameter<double>("ecalIsoPtSlope"),
                 parameters.getParameter<double>("hadronicOverEM") );
      if (parameters.exists("cutsToIgnore") )
        setIgnoredCuts(parameters.getParameter<std::vector<std::string> >("cutsToIgnore") );
    }
    else if (versionStr == "SPRING10") {
      initialize(SPRING10,
                 parameters.getParameter<double>("ecalIsoConstant"),
                 parameters.getParameter<double>("ecalIsoPtSlope"),
                 parameters.getParameter<double>("hadronicOverEM")
                );
      if (parameters.exists("cutsToIgnore") )
        setIgnoredCuts(parameters.getParameter<std::vector<std::string> >("cutsToIgnore") );
    }
    else {
      throw cms::Exception("InvalidInput") << "Expect version to be one of TEST, SPRING10" << std::endl;
    }
    retInternal_ = getBitTemplate();
  }


  VGammaPhotonIDSelectionFunctor(Version_t version,
                                 double ecalIsoConstant = 4.2,
                                 double ecalIsoPtSlope = 0.004,
                                 double hadronicOverEm = 0.05
                                )
  {
    initialize(version, ecalIsoConstant, ecalIsoPtSlope, hadronicOverEm);
  }


  void initialize(Version_t version,
                  double ecalIsoConstant = 4.2,
                  double ecalIsoPtSlope = 0.004,
                  double hadronicOverEm = 0.05
                 )
  {
    version_ = version;

    push_back("ecalIsoConstant", ecalIsoConstant);
    push_back("ecalIsoPtSlope",  ecalIsoPtSlope);
    push_back("hadronicOverEm",  hadronicOverEm);

    set("ecalIsoConstant");
    set("ecalIsoPtSlope");
    set("hadronicOverEm");

    if ( version_ == TEST ) {
      set("hadronicOverEm", false);
    }

  }

  // Allow for multiple definitions of the cuts.
  bool operator()(const pat::Photon & photon, pat::strbitset & ret)
  {

    if (version_ == SPRING10) return spring10Cuts(photon, ret);
    else if (version_ == TEST) return testCuts(photon, ret);
    else {
      return false;
    }
  }

  using Selector<pat::Photon>::operator();

  // cuts based on spring10 analysis
  bool spring10Cuts(const pat::Photon & photon, pat::strbitset & ret)
  {
    ret.set(false);

    double ecalIso         = photon.ecalRecHitSumEtConeDR04();
    double pt              = photon.pt();
    double ecalIsoConstant = cut("ecalIsoConstant", double());
    double ecalIsoPtSlope  = cut("ecalIsoPtSlope", double());
    double ecalIsoMax      = ecalIsoConstant + ecalIsoPtSlope * pt;

    double hadronicOverEm = photon.hadronicOverEm();

    if (ecalIso < ecalIsoMax ||
        ignoreCut("ecalIsoConstant") ||
        ignoreCut("ecalIsoPtSlope")
       )
    {
      passCut(ret, "ecalIsoConstant");
      passCut(ret, "ecalIsoPtSlope");
    }
    if (hadronicOverEm < cut("hadronicOverEm", double()) ||
        ignoreCut("hadronicOverEm")
       ) passCut(ret, "hadronicOverEm");

    setIgnored(ret);

    return (bool)ret;
  }



  // test cuts
  bool testCuts(const pat::Photon & photon, pat::strbitset & ret)
  {
    ret.set(false);

    double ecalIso         = photon.ecalRecHitSumEtConeDR04();
    double pt              = photon.pt();
    double ecalIsoConstant = cut("ecalIsoConstant", double());
    double ecalIsoPtSlope  = cut("ecalIsoPtSlope", double());
    double ecalIsoMax      = ecalIsoConstant + ecalIsoPtSlope * pt;

    double hadronicOverEm = photon.hadronicOverEm();

    if (ecalIso < ecalIsoMax ||
        ignoreCut("ecalIsoConstant") ||
        ignoreCut("ecalIsoPtSlope")
       )
    {
      passCut(ret, "ecalIsoConstant");
      passCut(ret, "ecalIsoPtSlope");
    }
    if (hadronicOverEm < cut("hadronicOverEm", double()) ||
        ignoreCut("hadronicOverEm")
       ) passCut(ret, "hadronicOverEm");

    setIgnored(ret);

    return (bool)ret;
  }

 private: // member variables

  Version_t version_;

};

#endif
