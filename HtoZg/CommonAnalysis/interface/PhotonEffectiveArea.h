//-----------------------------------------------------------------------------
// $Id $
//
// PhotonEffectiveArea
//
// Helper Class for storing effective areas
//
// Authors: J. Veverka, Caltech, 11 August 2012
// Inspired by: 
//      UserCode/sixie/Muon/MuonAnalysisTools/interface/MuonEffectiveArea.h
//-----------------------------------------------------------------------------


/// --> NOTE if you want to use this class as standalone without the CMSSW part 
///  you need to uncomment the below line and compile normally with scramv1 b 
///  Then you need just to load it in your root macro the lib with the correct 
///  path
//#define STANDALONE   // <---- this line

#ifndef HtoZg_CommonAnalysis_PhotonEffectiveArea_h
#define HtoZg_CommonAnalysis_PhotonEffectiveArea_h

#ifndef STANDALONE
#endif

using namespace std;

namespace cit {
  namespace hzg {
    class PhotonEffectiveArea{
    public:
      PhotonEffectiveArea();
      ~PhotonEffectiveArea(); 
      
      enum Type {
        kCharged03, 
        kNeutral03, 
        kPhoton03
      };
      
      enum Target {
        kNoCorr,
        kData2011,
        kData2012
      };

      static Double_t get(Type type, Double_t scEta, Target target = kData2011) {
        
        Double_t ea = 0;
        Double_t absEta = fabs(scEta);
        
        if (target == kNoCorr) {
          return 0.0;
        }
        
        //2011 Data Effective Areas
        else if (target == kData2011) {      
          /// Source: https://twiki.cern.ch/twiki/bin/view/CMS/
          ///       CutBasedPhotonID2012#Effective_Areas_for_rho_correcti
          /// Revision: r8
          /// Accessed: 11 August 2012
          /// NOTE: To be used with the rho calculated according to the twiki above
          if (type == kCharged03){
              if (absEta >= 0.0 && absEta < 1.0) ea = 0.012;
              if (absEta >= 1.0 && absEta < 1.5) ea = 0.010;
              if (absEta >= 1.5 && absEta < 2.0) ea = 0.014;
              if (absEta >= 2.0 && absEta < 2.2) ea = 0.012;
              if (absEta >= 2.2 && absEta < 2.3) ea = 0.016;
              if (absEta >= 2.3 && absEta < 2.4) ea = 0.020;
              if (absEta >= 2.4                ) ea = 0.012;
          }
          if (type == kNeutral03){
              if (absEta >= 0.0 && absEta < 1.0) ea = 0.030;
              if (absEta >= 1.0 && absEta < 1.5) ea = 0.057;
              if (absEta >= 1.5 && absEta < 2.0) ea = 0.039;
              if (absEta >= 2.0 && absEta < 2.2) ea = 0.015;
              if (absEta >= 2.2 && absEta < 2.3) ea = 0.024;
              if (absEta >= 2.3 && absEta < 2.4) ea = 0.039;
              if (absEta >= 2.4                ) ea = 0.072;
          }
          if (type == kPhoton03){
              if (absEta >= 0.0 && absEta < 1.0) ea = 0.148;
              if (absEta >= 1.0 && absEta < 1.5) ea = 0.130;
              if (absEta >= 1.5 && absEta < 2.0) ea = 0.112;
              if (absEta >= 2.0 && absEta < 2.2) ea = 0.216;
              if (absEta >= 2.2 && absEta < 2.3) ea = 0.262;
              if (absEta >= 2.3 && absEta < 2.4) ea = 0.260;
              if (absEta >= 2.4                ) ea = 0.266;
          } 
        } // target == kData2011
        
        //2012 Data Effective Areas
        else if (target == kData2012) {
          return get(type, scEta, kData2011);
        }
        
        return ea;  
      } // static Double_t get(...)
    }; // class PhotonEffectiveArea
  } // namespace cit::hzg
} // namespace cit

#endif
