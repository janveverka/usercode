#include "ElectroWeakAnalysis/MultiBosons/bin/MuonHistogrammer.h"

#include <string>

using namespace std;
using namespace edm;
using namespace pat;


MuonHistogrammer::MuonHistogrammer(const ParameterSet & config,
                                   fwlite::TFileService &fs
                                  ) :
    src_(config.getParameter<InputTag>("src") )
{
//   string fileName         = config.getParameter<string>("outputFile");
  string dirName          = config.getParameter<string>("outputDirectory");
  VParameterSet histosCfg = config.getParameter<VParameterSet>("histograms");

  // TODO Check if the rhs can be omitted
//   fwlite::TFileService fs;/* = fwlite::TFileService(fileName);*/
  TFileDirectory dir = fs.mkdir(dirName);


  for (VParameterSet::const_iterator iCfg = histosCfg.begin();
       iCfg != histosCfg.end(); ++iCfg)
  {
    ExpressionHisto<Muon> *hist = new ExpressionHisto<Muon>(*iCfg);
    hist->initialize(dir);
    vhistograms_.push_back(hist);
  }
}


MuonHistogrammer::~MuonHistogrammer()
{
  // delete all histograms and clear the vector of pointers
  vector<ExpressionHisto<Muon>* >::const_iterator hist;
  for (hist = vhistograms_.begin(); hist != vhistograms_.end(); ++hist)
    (*hist)->~ExpressionHisto<Muon>();

  vhistograms_.clear();
}


void
MuonHistogrammer::analyze(const EventBase &iEvent)
{
  Handle<vector<Muon> > collection;
  iEvent.getByLabel(src_, collection);

  analyze(*collection);
}


void
MuonHistogrammer::analyze(const vector<Muon> &collection)
{
  // loop over histograms
  vector<ExpressionHisto<Muon>* >::const_iterator hist;
  for (hist = vhistograms_.begin(); hist != vhistograms_.end(); ++hist)
  {
    // loop over collection
    vector<Muon>::const_iterator element, begin = collection.begin();
    for (element = begin; element != collection.end(); ++element) {
      const double dummyWeight = 1.0;
      if ( !(*hist)->fill(*element, dummyWeight, element-begin) ) break;
    } // loop over collection
  } // loop over histograms
}


void
MuonHistogrammer::analyze(const std::vector<reco::ShallowClonePtrCandidate> &collection)
{
  // loop over histograms
  vector<ExpressionHisto<Muon>* >::const_iterator hist;
  for (hist = vhistograms_.begin(); hist != vhistograms_.end(); ++hist)
  {
    // loop over collection
    std::vector<reco::ShallowClonePtrCandidate>::const_iterator it, begin;
    it = begin = collection.begin();
    for (; it != collection.end(); ++it) {
      // convert the iterator to a pointer to it's master
      reco::CandidatePtr ptr = it->masterClonePtr();
      const Muon * element = dynamic_cast<const Muon*>( ptr.get() );

      const double dummyWeight = 1.0;
      if ( !(*hist)->fill(*element, dummyWeight, it-begin) ) break;
    } // loop over collection
  } // loop over histograms
}

