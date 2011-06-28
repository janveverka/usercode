#include <string>
#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>

#include "TFile.h"
#include "TH1.h"

#include "DataFormats/Common/interface/Handle.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "Misc/TreeMaker/interface/PileupBranchManager.h"

namespace cit {

  ///--------------------------------------------------------------------------
  PileupBranchManager::PileupBranchManager(const edm::ParameterSet& iConfig) :

    doPileupSummaryInfo_(
      iConfig.existsAs<edm::InputTag>( "pileupInfoSrc", false )
    ),

    doWeights_(
      iConfig.existsAs<edm::ParameterSet>( "lumiReWeighting", false )
    ),

    doRho_(
      iConfig.existsAs<edm::InputTag>( "rhoSrc", false )
    ),

    b_numInteractions_(0),
    b_bunchCrossing_(0)
  {
    using namespace edm;

    if ( doPileupSummaryInfo_ == true )
      pileupInfoSrc_ =
        iConfig.getUntrackedParameter<InputTag>( "pileupInfoSrc" );

    if ( doRho_ == true )
      rhoSrc_ = iConfig.getUntrackedParameter<InputTag>( "rhoSrc" );

    if ( doWeights_ == true ) {
      ParameterSet cfg =
        iConfig.getUntrackedParameter<ParameterSet>( "lumiReWeighting" );

//       std::cout << "LumiReWeighting ctor\n";
      LogDebug("lumi") << "still alive!";


      // Here I would like to do something along these lines:
//       LumiWeights_ = edm::LumiReWeighting(
//         cfg.getParameter<std::string>( "mcFile" ),
//         cfg.getParameter<std::string>( "dataFile" ),
//         cfg.getParameter<std::string>( "mcHist" ),
//         cfg.getParameter<std::string>( "dataHist" )
//       );
      // However, this seems to die with a seg-fault. Trying a workaround.

      /// Start hack to circumvent the LumiReWeighting ctor seg-fault
      std::vector<float> mcDistribution;
      std::vector<float> dataDistribution;

      /// The distribution can be either passed as a vector of doubles
      /// or as a histogram in a root file.
      /// Get the MC distribution. Do we have the vector?
      if ( cfg.existsAs<std::vector<double> >( "mcDistribution", true ) ) {
        /// (casting from doubles to floats)
        copy( cfg.getParameter<std::vector<double> >( "mcDistribution" ),
              mcDistribution );
      } else {
        /// Didn't find the vector of doubles so expect a root file
        FileInPath fileName = cfg.getParameter<FileInPath>( "mcFile" );
        if ( fileName.location() == FileInPath::Unknown )
          throw cms::Exception("Configuration") << "File: "
                                                << fileName.relativePath()
                                                << " does not exist!\n";
        std::string histoName = cfg.getParameter<std::string>( "mcHist" );
        TFile *file = TFile::Open( fileName.fullPath().c_str() );
        TH1* histo = (TH1*) file->Get( histoName.c_str() );
        mcDistribution.reserve( histo->GetXaxis()->GetNbins() );
        mcDistribution.clear();
        for (int npu = 0; npu < histo->GetXaxis()->GetNbins(); ++npu) {
          int bin = histo->GetXaxis()->FindBin( npu );
          mcDistribution.push_back( histo->GetBinContent( bin ) );
        }
        file->Close();
        delete file;
      } /// End of getting the MC distribution.

      /// Now get the data distribution. Do we have the vector?
      if ( cfg.existsAs<std::vector<double> >( "dataDistribution", true ) ) {
        /// (casting from doubles to floats)
        copy( cfg.getParameter<std::vector<double> >( "dataDistribution" ),
              dataDistribution );
      } else {
        /// Didn't find the vector of doubles so expect a root file
        FileInPath fileName = cfg.getParameter<FileInPath>( "dataFile" );
        if ( fileName.location() == FileInPath::Unknown )
          throw cms::Exception("Configuration") << "File: "
                                                << fileName.relativePath()
                                                << " does not exist!\n";
        std::string histoName = cfg.getParameter<std::string>( "dataHist" );
        TFile *file = TFile::Open( fileName.fullPath().c_str() );
        TH1* histo = (TH1*) file->Get( histoName.c_str() );
        dataDistribution.reserve( histo->GetXaxis()->GetNbins() );
        dataDistribution.clear();
        for (int npu = 0; npu < histo->GetXaxis()->GetNbins(); ++npu) {
          int bin = histo->GetXaxis()->FindBin( npu );
          dataDistribution.push_back( histo->GetBinContent( bin ) );
        }
        file->Close();
        delete file;
      } /// End of getting the data distribution.

      LogDebug("lumi") << "still alive!";

      LumiWeights_ = LumiReWeighting( mcDistribution, dataDistribution );

    }  // end if  ( doWeights_ == true )

  } // end of ctor definition


  ///--------------------------------------------------------------------------
  void
  PileupBranchManager::init(TTree & tree)
  {

    std::string prefix = "pileup.";
    std::string sizeName = prefix + "size";
    std::string leafList, branchName;

    /// Book the branches

    /// Do we want to store the pile-up info?
    if ( doPileupSummaryInfo_ == true ) {
      leafList = sizeName + "/I";
      tree.Branch( sizeName.c_str(), &size_, leafList.c_str() );

      branchName = prefix + "numInteractions";
      leafList = prefix + "numInteractions[" + sizeName + "]/i";
      b_numInteractions_ = tree.Branch( branchName.c_str(),
                                        &(numInteractions_[0]),
                                        leafList.c_str() );

      branchName = prefix + "bunchCrossing";
      leafList = prefix + "bunchCrossing[" + sizeName + "]/I";
      b_bunchCrossing_ = tree.Branch( branchName.c_str(),
                                      &(bunchCrossing_[0]),
                                      leafList.c_str() );
    }

    /// Do we want to store the event weight?
    if ( doWeights_ == true ) {
      branchName = prefix + "weight";
      leafList = prefix + "weight/F";
      tree.Branch( branchName.c_str(), &weight_, leafList.c_str() );

      branchName = prefix + "weightOOT";
      leafList = prefix + "weightOOT/F";
      tree.Branch( branchName.c_str(), &weightOOT_, leafList.c_str() );
    } // doWeights_ == true

    /// Do we want to store rho from FastJet for pileup subtraction?
    if ( doRho_ == true ) {
      branchName = prefix + "rho";
      leafList = prefix + "rho/F";
      tree.Branch( branchName.c_str(), &rho_, leafList.c_str() );
    } // doRho_ == true

  } // end of PileupBranchManager::init(TTree & tree) definition


  ///--------------------------------------------------------------------------
  void
  PileupBranchManager::getData( const edm::Event& iEvent,
                                const edm::EventSetup& iSetup )
  {
    /// Do we want to store the pile-up info?
    if (doPileupSummaryInfo_ == true) {
      edm::Handle<std::vector< PileupSummaryInfo > >  pileupInfo;
      iEvent.getByLabel( pileupInfoSrc_, pileupInfo );

      size_ = pileupInfo->size();

      numInteractions_.clear();
      bunchCrossing_  .clear();

      numInteractions_.reserve( size_ );
      bunchCrossing_  .reserve( size_ );

      /// Loop over pileup bunch crossings.
      for(std::vector<PileupSummaryInfo>::const_iterator
          pu = pileupInfo->begin();
          pu != pileupInfo->end(); ++pu) {
        numInteractions_.push_back( pu->getPU_NumInteractions() );
        bunchCrossing_  .push_back( pu->getBunchCrossing()      );
      } // end of loop over pileup bunch crossings

      // Reset the branch addresses, the vectors may have been reallocated.
      if (b_numInteractions_ != 0)
        b_numInteractions_->SetAddress( &(numInteractions_[0]) );
      if (b_bunchCrossing_ != 0)
        b_bunchCrossing_->SetAddress( &(bunchCrossing_[0]) );

    } // end of pileup

    /// Do we want to store the pile-up event weight?
//     std::cout << "LumiReWeighting weight\n";
    if ( doWeights_ == true ) {
      weight_    = LumiWeights_.weight   ( iEvent );
      weightOOT_ = LumiWeights_.weightOOT( iEvent );
    }

    if ( doRho_ == true ) {
      edm::Handle<double>  rho;
      iEvent.getByLabel( rhoSrc_, rho);
      rho_    = *rho;
    }


  } // end of PileupBranchManager::getData(...) definition

  ///--------------------------------------------------------------------------
  void
  PileupBranchManager::copy( const std::vector<double> & from,
                             std::vector<float> & to  )
  {
    to.clear();
    to.reserve( from.size() );
    for ( std::vector<double>::const_iterator x = from.begin();
          x < from.end(); ++x )
      to.push_back( static_cast<float>( *x ) );
  } // end of copy

} // end of namespace cit
