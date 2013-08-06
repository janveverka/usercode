/**
 * Implementation of the \class CorrectionApplicator
 * 
 * Jan Veverka, MIT, jan.veverka@cern.ch
 * 04 August 2013.
 */

#include <iostream>
#include "FWCore/Utilities/interface/Exception.h"
#include "FWLite/Hgg/interface/CorrectionApplicator.h"

using namespace std;
using mit::hgg::CorrectionApplicator;
using mit::hgg::correction_applicator::Configuration;
using mit::hgg::correction_applicator::configuration::Inputs;
using mit::hgg::correction_applicator::configuration::MaxEntries;

typedef cms::Exception Bad;

//______________________________________________________________________________
/**
 * Constructor
 */
CorrectionApplicator::CorrectionApplicator(PSetPtr cfg) :
  process_(new Configuration(cfg)),
  ichain_(new TChain("CorrectionApplicatorInputChain")),
  input_(cfg->getParameter<PSet>("inputs"))
{
  initialize();
} // Constructor


//______________________________________________________________________________
/**
 * Destructor
 */
CorrectionApplicator::~CorrectionApplicator()
{
} // Destructor


//______________________________________________________________________________
/**
 * Run the correction application.
 */
void
CorrectionApplicator::run()
{
//   beginRun();
  loopOverEntries();
//   endRun();
} // run()




//==============================================================================
// 2nd  L E V E L   D E C O M P O S I T I O N
//==============================================================================


//___________________________________________________________________________
/**
 * Loops over the entries.
 */
void
CorrectionApplicator::loopOverEntries()
{
  // Long64_t entriesToProcess = ichain_->GetEntries();
  Long64_t entriesToProcess = input_.chain().GetEntries();
  Long64_t maxEntries = process_->maxEntries()->toProcess();
  
  if (maxEntries > 0 && maxEntries < entriesToProcess) {
    entriesToProcess = maxEntries;
  }
  
  for (Long64_t ientry = 0; ientry < entriesToProcess; ++ientry) {
    // if (ichain_->LoadTree(ientry) < 0) break;
    if (input_.chain().LoadTree(ientry) < 0) break;
    reportEntry(ientry, entriesToProcess);
    processEntry();
  }
} // CorrectionApplicator::loopOverEntries()


//==============================================================================
// 3rd  L E V E L   D E C O M P O S I T I O N
//==============================================================================


//______________________________________________________________________________
/**
 * Initializes data members.
 * Parses configuration (in cfg ctor), opens input file, retrieves the input
 * tree, defines variables to be read, sets their addresses, creates the
 * output file and tree, initializes corrections.
 * Pre-conditions: Valid configuration exists.
 * Post-conditions: Input, output and corrector fields are initialized.
 */
void
CorrectionApplicator::initialize()
{
  initializeInputs();
  initializeOutputs();
  initializeCorrectors();
  initializePhotonIdMVAs();
} // CorrectionApplicator::initialize()


//______________________________________________________________________________
/**
 * Initializes the input file and tree.
 * Pre-conditions: Valid configuration exists.
 * Post-conditions: The input tree and branch buffers are initialized and
 *                  the address are set.
 */
void
CorrectionApplicator::initializeInputs()
{
  ichain_->SetName(process_->inputs()->treeName().c_str());

  Inputs::vstring const& fileNames = process_->inputs()->fileNames();
  for (Inputs::vstring::const_iterator fileName = fileNames.begin();
       fileName != fileNames.end(); ++fileName)
  {
    ichain_->Add(fileName->c_str());
  }

} // CorrectionApplicator::initializeInputs()


//______________________________________________________________________________
/**
 * Initializes
 */
void
CorrectionApplicator::initializeOutputs()
{
} // CorrectionApplicator::initializeOutputs()


//______________________________________________________________________________
/**
 *
 */
void
CorrectionApplicator::initializeCorrectors()
{
} // CorrectionApplicator::initializeCorrectors()


//______________________________________________________________________________
/**
 *
 */
void
CorrectionApplicator::initializePhotonIdMVAs()
{
} // CorrectionApplicator::initializePhotonIdMVAs()


//___________________________________________________________________________
/**
 * Processes the current entry.
 */
void
CorrectionApplicator::processEntry()
{
} // CorrectionApplicator::processEntry()


//___________________________________________________________________________
/**
 * Reports the current entry.
 */
void
CorrectionApplicator::reportEntry(Long64_t ientry, Long64_t entriesToProcess)
{
  if (ientry % process_->maxEntries()->reportEvery() == 0) {
    std::cout << "Processing entry " << ientry << std::endl;
  }
} // CorrectionApplicator::reportEntry()


// Method boiler plate
// //___________________________________________________________________________
// /**
//  *
//  */
// void
// CorrectionApplicator::()
// {
// } // CorrectionApplicator::()




//==============================================================================
/// Implementation of \class Configuration
//==============================================================================


//______________________________________________________________________________
/**
 * Configuration Ctor
 */
Configuration::Configuration(PSetPtr source) :
  source_(source),
  inputs_(new Inputs(source->getParameter<PSet>("inputs"))),
  maxEntries_(new MaxEntries(/* toProcess   default */ -1,
                             /* reportEvery default */  1))
{
  initialize();
} // Configuration::Configuration()


//___________________________________________________________________________
/**
 * Initialize configuration
 */
void
Configuration::initialize()
{
  if (source_->existsAs<PSet>("maxEntries")) {
    maxEntries_->parse(source_->getParameter<PSet>("maxEntries"));
  }
} // Configuration::initialize()


// Method boiler plate
// //___________________________________________________________________________
// /**
//  *
//  */
// void
// Configuration::()
// {
// } // Configuration::()




//==============================================================================
/// Implementation of \class Inputs
//==============================================================================


//___________________________________________________________________________
/**
 * Ctor
 */
Inputs::Inputs(PSet const& cfg) :
  fileNames_(cfg.getParameter<vstring>("fileNames")),
  treeName_(cfg.getParameter<std::string>("treeName"))
{
} // Inputs::Inputs()


// //___________________________________________________________________________
// /**
//  *
//  */
// void
// Inputs::()
// {
// } // Inputs::()




//==============================================================================
/// Implementation of \class MaxEntries
//==============================================================================


//___________________________________________________________________________
/**
 * Ctor
 */
MaxEntries::MaxEntries(Long64_t toProcess, Long64_t reportEvery) :
  toProcess_  (toProcess  ),
  reportEvery_(reportEvery)
{} // MaxEntries::MaxEntries()


//___________________________________________________________________________
/**
 * Parses the given parameter set and updates the values of entries to
 * process and to report.
 */
void
MaxEntries::parse(PSet const& cfg)
{
  toProcess_   = cfg.getUntrackedParameter<Long64_t>("toProcess"  ,
                                                      toProcess_  );
  reportEvery_ = cfg.getUntrackedParameter<Long64_t>("reportEvery",
                                                      reportEvery_);
} // MaxEntries::parse()


// //___________________________________________________________________________
// /**
//  *
//  */
// void
// MaxEntries::()
// {
// } // MaxEntries::()


