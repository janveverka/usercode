/**
 * \file FWLite/Tools/test/ChainSourceTest.cc
 * \class ChainSourceTest
 *
 * \brief Unit test of the class ChainSource
 *
 * \author Jan Veverka, MIT, jan.veverka@cern.ch
 * \date 8 August 2013
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
#include "FWLite/Tools/interface/ChainSource.h"

using namespace ::std;
using ::fwlite::tools::ChainSource;


//_____________________________________________________________________________
/**
 * ChainSource test fixture
 */
class ChainSourceTest : public ::CppUnit::TestFixture {
  CPPUNIT_TEST_SUITE(ChainSourceTest);
  CPPUNIT_TEST(testConfig);
  CPPUNIT_TEST(testChain);
  CPPUNIT_TEST_SUITE_END();

public:
  typedef boost::shared_ptr<TTree> TreePtr;
  typedef boost::shared_ptr<TChain> ChainPtr;
  typedef boost::shared_ptr<edm::ParameterSet> PSetPtr;
  void setUp(void);
  void tearDown(void);

protected:
  void testConfig(void);
  void testChain(void);

private:
  /// Auxiliary methods
  void initReferenceObjects();
  void initTestedObjects();
  void initFileNames();
  void initTreesAndFiles();
  TreePtr makeTree(const char* name, unsigned index);
  PSetPtr makeParameterSet();
  void writeTreeToFile(TreePtr tree, const char* filename);
  ChainPtr makeChain();

  /// Objects used as references in the tests
  string treeName_;
  vector<std::string> fileNames_;
  Float_t xleaf_;
  Int_t   ileaf_;
  vector<TreePtr> trees_;
  
  /// Tested objects
  ChainSource::Configuration *config_;
  ChainSource *source_;
}; // class ChainSourceTest

//_____________________________________________________________________________
// Register 
CPPUNIT_TEST_SUITE_REGISTRATION(ChainSourceTest);

//_____________________________________________________________________________
void
ChainSourceTest::setUp(void)
{
  initReferenceObjects();
  initTestedObjects();
} // ChainSourceTest::setUp(void)


//_____________________________________________________________________________
void
ChainSourceTest::tearDown(void)
{
  delete config_;
  delete source_;
} // ChainSourceTest::tearDown(void)


//_____________________________________________________________________________
void
ChainSourceTest::testConfig(void)
{
  CPPUNIT_ASSERT_EQUAL(treeName_, config_->treeName());
  CPPUNIT_ASSERT_EQUAL(treeName_, source_->config().treeName());
  for (unsigned i=0; i<fileNames_.size(); ++i) {
    CPPUNIT_ASSERT_EQUAL(fileNames_[i], config_->fileNames()[i]);
    CPPUNIT_ASSERT_EQUAL(fileNames_[i], source_->config().fileNames()[i]);
  }
} //ChainSourceTest::testConfig(void)


//_____________________________________________________________________________
void
ChainSourceTest::testChain(void)
{
  ChainPtr chain = makeChain();
  chain->SetBranchAddress("xleaf", &xleaf_);
  chain->SetBranchAddress("ileaf", &ileaf_);

  Float_t xleaf;
  Int_t ileaf;
  source_->chain().SetBranchAddress("xleaf", &xleaf);
  source_->chain().SetBranchAddress("ileaf", &ileaf);

  for (unsigned i=0; i<chain->GetEntries(); ++i) {
    chain->GetEntry(i);
    source_->chain().GetEntry(i);
    CPPUNIT_ASSERT_EQUAL(ileaf_, ileaf);
    CPPUNIT_ASSERT_EQUAL(xleaf_, xleaf);
  } // loop over entries
} //ChainSourceTest::testChain(void)


//_____________________________________________________________________________
/**
 * Initializes objects that are used as reference for testing.
 * Pre-condition:  None.
 * Post-condition: treeName_, fileNames_, trees_ are initialized and
 *                 corresponding root files exist.
 */
void
ChainSourceTest::initReferenceObjects()
{
  treeName_ = "tree";
  initFileNames();
  initTreesAndFiles();
} // ChainSourceTest::initReferenceObjects()


//_____________________________________________________________________________
/**
 * Initializes objects to be tested.
 * Pre-condition:  Reference objects have been initialized.
 * Post-condition: source_ has been initialized.
 */
void
ChainSourceTest::initTestedObjects()
{
  config_ = new ChainSource::Configuration(*makeParameterSet());
  source_ = new ChainSource(*makeParameterSet());
} // ChainSourceTest::initReferenceObjects()


//_____________________________________________________________________________
/**
 * Pre-condition: CMSSW_BASE environment variable is set
 * Post-condition: fileNames_ is initialized
 */
void
ChainSourceTest::initFileNames()
{
  const char *dir = Form("%s/%s", getenv("CMSSW_BASE"),
                         "src/FWLite/Tools/data");

  fileNames_.push_back(Form("%s/%s", dir, "ChainSourceTest0.root"));
  fileNames_.push_back(Form("%s/%s", dir, "ChainSourceTest1.root"));
} // ChainSourceTest::initFileNames()


//_____________________________________________________________________________
void
/**
 * Pre-condition: treeName_ and fileNames_ are initialized
 * Post-condition: trees_ are initilized and files with trees exist.
 */
ChainSourceTest::initTreesAndFiles()
{
  for (unsigned i=0; i<fileNames_.size(); ++i) {
    TreePtr tree = makeTree(treeName_.c_str(), i);
    trees_.push_back(tree);
    if (not boost::filesystem::exists(fileNames_[i])) {
      writeTreeToFile(tree, fileNames_[i].c_str());
    }
  }
} // ChainSourceTest::initTreesAndFiles()


//_____________________________________________________________________________
/**
 * Creates and returns a dummy tree of the given name. Uses the given
 * index to calculate the leaf values, so that they differ for trees
 * with a different index.
 */
ChainSourceTest::TreePtr
ChainSourceTest::makeTree(const char *name, unsigned index)
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
} // ChainSourceTest::makeTree(unsigned i)


//_____________________________________________________________________________
/**
 * Writes the given tree to a root file of the given filename.
 */
void
ChainSourceTest::writeTreeToFile(TreePtr tree, const char *filename)
{
  TFile * file = TFile::Open(filename, "RECREATE");
  tree->CopyTree("")->SetDirectory(file);
  file->Write();
  file->Close();
  delete file;
} // ChainSourceTest::writeTreeToFile(TreePtr tree, const char *filename)


//_____________________________________________________________________________
/**
 * Returns a shared pointer to a ParameterSet with a dummy configuration
 * based on treeName_ and fileNames_.
 *
 * Pre-condition: treeName_ and fileNames_ have been initialized
 */
ChainSourceTest::PSetPtr
ChainSourceTest::makeParameterSet()
{
  PSetPtr pset(new edm::ParameterSet());
  pset->addParameter("treeName" , treeName_);
  pset->addParameter("fileNames", fileNames_);
  pset->registerIt();
  return pset;
} // ChainSourceTest::makeParameterSet()


//_____________________________________________________________________________
/**
 * Returns a shared pointer to the chain used as a reference in the test.
 *
 * Pre-condition: treeName_ and fileNames_ have been initialized and
 *                files with trees exist
 */
ChainSourceTest::ChainPtr
ChainSourceTest::makeChain()
{
  ChainPtr chain(new TChain(treeName_.c_str()));
  for (vector<string>::const_iterator file = fileNames_.begin();
       file != fileNames_.end(); ++file) {
    chain->Add(file->c_str());
  }
  return chain;
} // ChainSourceTest::makeParameterSet()
