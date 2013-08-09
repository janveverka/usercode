/**
 * \file FWLite/Tools/test/FlatChainSourceTest.cc
 * \class FlatChainSourceTest
 *
 * \brief Unit test of the class FlatChainSource
 *
 * \author Jan Veverka, MIT, jan.veverka@cern.ch
 * \date 9 August 2013
 */

#include <iostream>
#include <boost/filesystem.hpp>
#include <boost/shared_ptr.hpp>
#include <cppunit/extensions/HelperMacros.h>

#include "TChain.h"
#include "TFile.h"
#include "TObject.h" // Provides Form(...)
#include "TTree.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWLite/Tools/interface/FlatChainSource.h"

using namespace ::std;
using ::fwlite::tools::FlatChainSource;


//_____________________________________________________________________________
/**
 * FlatChainSource test fixture
 */
class FlatChainSourceTest : public ::CppUnit::TestFixture {
  CPPUNIT_TEST_SUITE(FlatChainSourceTest);
  CPPUNIT_TEST(testConfig);
  CPPUNIT_TEST(testChain);
  CPPUNIT_TEST(testBadVariable);
  CPPUNIT_TEST_SUITE_END();

public:
  typedef boost::shared_ptr<TTree> TreePtr;
  typedef boost::shared_ptr<TChain> ChainPtr;
  typedef boost::shared_ptr<edm::ParameterSet> PSetPtr;
  enum VariablesType {kGood, kBadFormat, kBadTypeFormat, kBadType};
  void setUp(void);
  void tearDown(void);

protected:
  void testConfig(void);
  void testChain(void);
  void testBadVariable(void);

private:
  /// Auxiliary methods
  void initReferenceObjects();
  void initTestedObjects();
  void initFileNames();
  void initVariables();
  void initTreesAndFiles();
  TreePtr makeTree(const char* name, unsigned index);
  PSetPtr makeParameterSet(VariablesType type = kGood);
  void writeTreeToFile(TreePtr tree, const char* filename);
  ChainPtr makeChain();

  /// Objects used as references in the tests
  string treeName_;
  vector<string> fileNames_;
  vector<string> variables_;
  vector<string> variablesBadFormat_;
  vector<string> variablesBadTypeFormat_;
  vector<string> variablesBadType_;
  Float_t xleaf_;
  Int_t   ileaf_;
  vector<TreePtr> trees_;
  
  /// Tested objects
  FlatChainSource::Configuration *config_;
  FlatChainSource *source_;
}; // class FlatChainSourceTest

//_____________________________________________________________________________
// Register 
CPPUNIT_TEST_SUITE_REGISTRATION(FlatChainSourceTest);

//_____________________________________________________________________________
void
FlatChainSourceTest::setUp(void)
{
  initReferenceObjects();
  initTestedObjects();
} // FlatChainSourceTest::setUp(void)


//_____________________________________________________________________________
void
FlatChainSourceTest::tearDown(void)
{
  delete config_;
  delete source_;
} // FlatChainSourceTest::tearDown(void)


//_____________________________________________________________________________
void
FlatChainSourceTest::testConfig(void)
{
  CPPUNIT_ASSERT_EQUAL(treeName_, config_->treeName());
  CPPUNIT_ASSERT_EQUAL(treeName_, source_->config().treeName());
  for (unsigned i=0; i<fileNames_.size(); ++i) {
    CPPUNIT_ASSERT_EQUAL(fileNames_[i], config_->fileNames()[i]);
    CPPUNIT_ASSERT_EQUAL(fileNames_[i], source_->config().fileNames()[i]);
  }
} //FlatChainSourceTest::testConfig(void)


//_____________________________________________________________________________
void
FlatChainSourceTest::testChain(void)
{
  ChainPtr chain = makeChain();
  chain->SetBranchAddress("xleaf", &xleaf_);
  chain->SetBranchAddress("ileaf", &ileaf_);

  for (unsigned i=0; i<chain->GetEntries(); ++i) {
    chain->GetEntry(i);
    source_->chain().GetEntry(i);
    CPPUNIT_ASSERT_EQUAL(ileaf_, source_->get<Int_t  >("ileaf"));
    CPPUNIT_ASSERT_EQUAL(xleaf_, source_->get<Float_t>("xleaf"));
    CPPUNIT_ASSERT_EQUAL(ileaf_, source_->getI("ileaf"));
    CPPUNIT_ASSERT_EQUAL(xleaf_, source_->getF("xleaf"));
    CPPUNIT_ASSERT_EQUAL(ileaf_, source_->I("ileaf"));
    CPPUNIT_ASSERT_EQUAL(xleaf_, source_->F("xleaf"));
  } // loop over entries
} //FlatChainSourceTest::testChain(void)


//_____________________________________________________________________________
void
FlatChainSourceTest::testBadVariable(void)
{
  CPPUNIT_ASSERT_NO_THROW(FlatChainSource(*makeParameterSet(kGood)));
  CPPUNIT_ASSERT_THROW(FlatChainSource(*makeParameterSet(kBadFormat    )),
                       cms::Exception                                     );
  CPPUNIT_ASSERT_THROW(FlatChainSource(*makeParameterSet(kBadTypeFormat)),
                       cms::Exception                                     );
  CPPUNIT_ASSERT_THROW(FlatChainSource(*makeParameterSet(kBadType      )),
                       cms::Exception                                     );
} //FlatChainSourceTest::testBadVariable(void)


//_____________________________________________________________________________
/**
 * Initializes objects that are used as reference for testing.
 * Pre-condition:  None.
 * Post-condition: treeName_, fileNames_, trees_ are initialized and
 *                 corresponding root files exist.
 */
void
FlatChainSourceTest::initReferenceObjects()
{
  treeName_ = "tree";
  initFileNames();
  initVariables();
  initTreesAndFiles();
} // FlatChainSourceTest::initReferenceObjects()


//_____________________________________________________________________________
/**
 * Initializes objects to be tested.
 * Pre-condition:  Reference objects have been initialized.
 * Post-condition: source_ has been initialized.
 */
void
FlatChainSourceTest::initTestedObjects()
{
  config_ = new FlatChainSource::Configuration(*makeParameterSet());
  source_ = new FlatChainSource(*makeParameterSet());
} // FlatChainSourceTest::initReferenceObjects()


//_____________________________________________________________________________
/**
 * Pre-condition: CMSSW_BASE environment variable is set
 * Post-condition: fileNames_ is initialized
 */
void
FlatChainSourceTest::initFileNames()
{
  const char *dir = Form("%s/%s", getenv("CMSSW_BASE"),
                         "src/FWLite/Tools/data");

  fileNames_.push_back(Form("%s/%s", dir, "FlatChainSourceTest0.root"));
  fileNames_.push_back(Form("%s/%s", dir, "FlatChainSourceTest1.root"));
} // FlatChainSourceTest::initFileNames()


//_____________________________________________________________________________
/**
 * Initializes variables_ describing what leaves should be buffered.
 */
void
FlatChainSourceTest::initVariables()
{
  variables_.push_back("xleaf/F");
  variables_.push_back("ileaf/I");
  variablesBadFormat_.push_back("a/b/c");
  variablesBadType_.push_back("x/x");
  variablesBadTypeFormat_.push_back("x/xx");
} // FlatChainSourceTest::initVariables()


//_____________________________________________________________________________
void
/**
 * Pre-condition: treeName_ and fileNames_ are initialized
 * Post-condition: trees_ are initilized and files with trees exist.
 */
FlatChainSourceTest::initTreesAndFiles()
{
  for (unsigned i=0; i<fileNames_.size(); ++i) {
    TreePtr tree = makeTree(treeName_.c_str(), i);
    trees_.push_back(tree);
    if (not boost::filesystem::exists(fileNames_[i])) {
      writeTreeToFile(tree, fileNames_[i].c_str());
    }
  }
} // FlatChainSourceTest::initTreesAndFiles()


//_____________________________________________________________________________
/**
 * Creates and returns a dummy tree of the given name. Uses the given
 * index to calculate the leaf values, so that they differ for trees
 * with a different index.
 */
FlatChainSourceTest::TreePtr
FlatChainSourceTest::makeTree(const char *name, unsigned index)
{
  const unsigned kMaxEntries = 2;

  TreePtr tree(new TTree(name, name));
  tree->Branch("xleaf", &xleaf_, "xleaf/F");
  tree->Branch("ileaf", &ileaf_, "ileaf/I");

  for (unsigned j=0; j < kMaxEntries; ++j) {
    xleaf_ = 1. + 10 * index + j;
    ileaf_ = -1 - 10 * index - j;
    tree->Fill();
  }

  return tree;
} // FlatChainSourceTest::makeTree(unsigned i)


//_____________________________________________________________________________
/**
 * Writes the given tree to a root file of the given filename.
 */
void
FlatChainSourceTest::writeTreeToFile(TreePtr tree, const char *filename)
{
  TFile * file = TFile::Open(filename, "RECREATE");
  tree->CopyTree("")->SetDirectory(file);
  file->Write();
  file->Close();
  delete file;
} // FlatChainSourceTest::writeTreeToFile(TreePtr tree, const char *filename)


//_____________________________________________________________________________
/**
 * Returns a shared pointer to a ParameterSet with a dummy configuration
 * based on treeName_ and fileNames_.
 *
 * Pre-condition: treeName_ and fileNames_ have been initialized
 */
FlatChainSourceTest::PSetPtr
FlatChainSourceTest::makeParameterSet(VariablesType type)
{
  vector<string> variables;
  switch (type) {
    case kGood         : variables = variables_             ; break;
    case kBadType      : variables = variablesBadType_      ; break;
    case kBadTypeFormat: variables = variablesBadTypeFormat_; break;
    case kBadFormat    : variables = variablesBadFormat_    ; break;
  } // switch (type)

  PSetPtr pset(new edm::ParameterSet());
  pset->addParameter("treeName" , treeName_);
  pset->addParameter("fileNames", fileNames_);
  pset->addParameter("variables", variables);
  pset->registerIt();
  return pset;
} // FlatChainSourceTest::makeParameterSet()


//_____________________________________________________________________________
/**
 * Returns a shared pointer to the chain used as a reference in the test.
 *
 * Pre-condition: treeName_ and fileNames_ have been initialized and
 *                files with trees exist
 */
FlatChainSourceTest::ChainPtr
FlatChainSourceTest::makeChain()
{
  ChainPtr chain(new TChain(treeName_.c_str()));
  for (vector<string>::const_iterator file = fileNames_.begin();
       file != fileNames_.end(); ++file) {
    chain->Add(file->c_str());
  }
  return chain;
} // FlatChainSourceTest::makeParameterSet()
