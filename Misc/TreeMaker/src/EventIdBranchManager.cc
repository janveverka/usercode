#include <string>
#include <iostream>

#include "DataFormats/Common/interface/Handle.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "Misc/TreeMaker/interface/EventIdBranchManager.h"

namespace cit {

  EventIdBranchManager::EventIdBranchManager(const edm::ParameterSet& iConfig) :
      eventInfo_( iConfig.getUntrackedParameter<bool>( "eventInfo", true ) ),
//       pileupInfo_( iConfig.existsAs<edm::InputTag>( "pileupInfoSrc", false ) ),
//       doPileupWeight_( iConfig.existsAs<edm::ParameterSet>( "lumiReWeighting",
//                                                            false ) ),
      id_()
  {
//     if ( pileupInfo_ == true )
//       pileupInfoSrc_ = iConfig.getUntrackedParameter<edm::InputTag>(
//                          "pileupInfoSrc"
//                        ) ;
// 
//     if ( doPileupWeight_ == true ) {
// 
//       edm::ParameterSet cfg = iConfig.getUntrackedParameter<
//                                 edm::ParameterSet
//                               >( "lumiReWeighting" );

//       std::cout << "LumiReWeighting ctor\n";
      LogDebug("lumi") << "still alive!";

//       float GJetsLumi_f[21] = {
//         257141., 295755., 263008., 286909., 282291., 281067.,
//         295777., 297075., 250569., 299795., 256528., 248686.,
//         203484., 137833., 117686., 76877., 62815., 35462.,
//         8381., 10012., 4233.
//       };
// 
//       float TrueDist2011_f[51] = {
//         3.6124e+06, 5.7606e+06, 1.3047e+07, 2.12065e+07, 2.71345e+07, 2.89995e+07,
//         2.68765e+07, 2.21641e+07, 1.65695e+07, 1.13875e+07, 7.27332e+06, 4.35533e+06,
//         2.46294e+06, 1.32354e+06, 679618, 335115, 159402, 73447,
//         32906.5, 14384.3, 6152.9, 2581.8, 1064.77, 432.206,
//         172.826, 68.1079, 26.4529, 10.1234, 3.81552, 1.4155,
//         0.51655, 0.185307, 0.0653117, 0.0226036, 0.00767821, 0.00255903,
//         0.000836568, 0.000268193, 8.43057e-05, 2.59835e-05, 7.85175e-06, 2.32636e-06,
//         6.75872e-07, 1.92565e-07, 5.3812e-08, 1.47516e-08, 3.96773e-09, 1.0473e-09,
//         2.71346e-10, 5.26651e-08, 0.
//       };
//       LogDebug("lumi") << "still alive!";
// 
//       std::vector< float > TrueDist2011;
//       std::vector< float > GJetsLumi;
//     
//       for( int i=0; i<21; ++i) {
//         TrueDist2011.push_back(TrueDist2011_f[i]);
//         GJetsLumi   .push_back(GJetsLumi_f[i]);
//       }
//       LogDebug("lumi") << "still alive!";
//       LumiWeights_ = edm::LumiReWeighting(GJetsLumi, TrueDist2011);

//       LumiWeights_ = edm::LumiReWeighting(
//         cfg.getParameter<std::string>( "mcFile" ),
//         cfg.getParameter<std::string>( "dataFile" ),
//         cfg.getParameter<std::string>( "mcHist" ),
//         cfg.getParameter<std::string>( "dataHist" )
//       );

//     }  // end if  ( doPileupWeight_ == true )

  } // end of ctor definition


  void
  EventIdBranchManager::init(TTree & tree)
  {
    /// Book the branches
    /// Do we want to safe the event ID data?
    if ( eventInfo_ == true )
      tree.Branch("id", &id_, "run/i:luminosityBlock:event");

    /// Do we want to store the pile-up info?
//     if ( pileupInfo_ == true ) {
//       tree.Branch( "numPileup", &numPileup_, "numPileup/i" );
//     }

//       std::cout << "LumiReWeighting branches\n";
    /// Do we want to store the event weight?
//     if ( doPileupWeight_ == true ) {
//       tree.Branch( "puWeight"    , &puWeight_    , "puWeight/F"     );
//       tree.Branch( "puWeightOOT" , &puWeightOOT_ , "puWeightOOT/F"  );
//     }

  } // end of EventIdBranchManager::init(TTree & tree) definition


  void
  EventIdBranchManager::getData( const edm::Event& iEvent,
                                 const edm::EventSetup& iSetup )
  {
    /// Do we want to safe the event ID data?
    if (eventInfo_ == true)
      /// Use the EventIdData ctor to get the event ID data.
      id_ = EventIdData( iEvent.id() );

    /// Do we want to store the pile-up info?
//     if (pileupInfo_ == true) {
//       edm::Handle<std::vector< PileupSummaryInfo > >  pileupInfo;
//       iEvent.getByLabel(pileupInfoSrc_, pileupInfo);
//       /// Loop over pileup bunch crossings.
//       numPileup_ = 0;
//       for(std::vector<PileupSummaryInfo>::const_iterator
//           bunchXing = pileupInfo->begin();
//           bunchXing != pileupInfo->end(); ++bunchXing) {
//         if ( bunchXing->getBunchCrossing() == 0 ) 
//           /// This is the in-time pile-up
//           numPileup_ = bunchXing->getPU_NumInteractions();
//       } // end of loop over pileup bunch crossings
//     } // end of pileup

    /// Do we want to store the pile-up event weight?
//     std::cout << "LumiReWeighting weight\n";
//     if ( doPileupWeight_ == true ) {
//       puWeight_    = LumiWeights_.weight   ( iEvent );
//       puWeightOOT_ = LumiWeights_.weightOOT( iEvent );
//     }
  } // end of EventIdBranchManager::getData(...) definition

} // end of namespace cit