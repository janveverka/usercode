{
gROOT->LoadMacro("../resolutionErrors.C");

// const char *filenameData = "pixelMatch_data_Nov4ReReco_v4.dat";
// const char *filenameMC   = "pixelMatch_Powheg_Fall10_v4.dat";

// const char *path = "/raid2/veverka/PMVTrees_v6/";
const char *path = "/raid2/veverka/pmvTrees/";

/**
    "data": "pmvTree_ZMu_May10ReReco-42X-v3_Plus_PromptSkim-v4_42X-v5_V6.root",

    'w'  : 'pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V6.root',
    'qcd': 'pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V6.root',
    'tt' : 'pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V6.root',
    'z'  : 'pmvTree_DYToMuMu_pythia6_AOD-42X-v4_V6.root',
*/


// const char *filenameData = "pmvTree_ZMu_May10ReReco-42X-v3_Plus_PromptSkim-v4_42X-v5_V6.root";
// const char *filenameMC   = "pmvTree_DYToMuMu_pythia6_AOD-42X-v4_V6.root";
// const char *filenameQCD  = "pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V6.root";
// const char *filenameW    = "pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V6.root";
// const char *filenameTT   = "pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V6.root";


/// results with 499/pb
const char *filenameData = "pmvTree_ZMu-May10ReReco_plus_PromptReco-v4_FNAL_42X-v3_V8.root";
const char *filenameMC   = "pmvTree_DYToMuMu_pythia6_v1_plus_v2_RECO-42X-v4_V8.root";
const char *filenameQCD  = "pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V6.root";
const char *filenameW    = "pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V6.root";
const char *filenameTT   = "pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V6.root";

enum mcSample {z=0, qcd, w, tt};

/// FIXME
/*
cweight = {
    "data": 1.,
    'z'  : 0.17175592557735,
    'tt' : 0.019860956416475,
    'w'  : 0.54974976060237,
    'qcd': 0.27884236321449,
}



*/
double weight[] = {
  0.17175592557735 * 1795714. / 2008540., // z
  0.27884236321449,  // qcd
  0.54974976060237,  // w
  0.019860956416475  // tt
};

TFile dataFile(Form("%s%s", path, filenameData));
TFile mcFile(Form("%s%s", path, filenameMC));
TFile qcdFile(Form("%s%s", path, filenameQCD));
TFile wFile(Form("%s%s", path, filenameW));
TFile ttFile(Form("%s%s", path, filenameTT));

/// Read data set
TTree * tdata  = (TTree*) dataFile.Get("pmvTree/pmv");
TTree * tmc    = (TTree*) mcFile.Get("pmvTree/pmv");
TTree * tqcd   = (TTree*) qcdFile.Get("pmvTree/pmv");
TTree * tw   = (TTree*) wFile.Get("pmvTree/pmv");
TTree * ttt   = (TTree*) ttFile.Get("pmvTree/pmv");

TCut drCut("minDeltaR < 1");
// TCut phoTIsoCut("phoTrackIsoCorr < 2 + 0.001 * phoPt");
// TCut phoEIsoCut("phoEcalIso < 4.2+0.006*phoPt");
// TCut phoHIsoCut("phoHcalIso < 2.2+0.0025*phoPt");
// TCut ebSihihCut("minDTheta<0.05|phoSigmaIetaIeta<0.013");
TCut ebCut("abs(phoEta) < 1.5");
TCut eeCut("abs(phoEta) > 1.5");
TCut signalCut("isFSR");
TCut backgroundCut("!isFSR");
TCut mWindowCut("abs(mmgMass-90) < 15");
TCut ubCut("(minDEta > 0.04 | minDPhi > 0.2)");
TCut vetoCut("phoR9 > 0.94");
// TCut vetoCut("phoDeltaRToTrack > 0.062"); //eb low R9
// TCut vetoCut("!phoHasPixelMatch");
TCut nVtx1to2("nVertices<=2");
TCut phoPt5to10("5 <= phoPt & phoPt < 10");
TCut phoPt10to20("10 <= phoPt & phoPt < 20");
TCut phoPt20up("20 <= phoPt");
TCut ebLowR9("0.36 < phoR9 && phoR9 <= 0.94");
TCut eeLowR9("0.32 < phoR9 && phoR9 <= 0.94");
TCut highR9("0.94 < phoR9");

/*TCut ebSelection("phoIsEB & abs(mmgMass-90)<17.5 & (minDEta > 0.04 | minDPhi > 0.3)");
TCut eeSelection("!phoIsEB & abs(mmgMass-90)<17.5 & (minDEta > 0.08 | minDPhi > 0.3)");*/
TCut ebSelection("phoIsEB & abs(mmgMass-90)<15 & phoPt > 20 && scEt > 10 && phoHoE < 0.5");
TCut eeSelection("!phoIsEB & abs(mmgMass-90)<15 & phoPt > 20 && scEt > 10 && phoHoE < 0.5");

// TCut selection = eeSelection;
// TCut selection = ebSelection && highR9;
// TCut selection = ebSelection && ebLowR9;
// TCut selection = eeSelection && highR9;
TCut selection = ebSelection;
// TCut selection = ebSelection && nVtx1to2;
// TCut selection = ebSelection && !nVtx1to2;
// TCut selection = ebSelection && phoPt5to10;
// TCut selection = ebSelection && phoPt10to20;
// TCut selection = ebSelection && phoPt20up;

// gStyle->SetPadLeftMargin(1.3);
TCanvas * c1 = new TCanvas("c1", "c1", 20, 20, 800, 400);
c1->Divide(2,1);
c1->cd(1);


// Scale all MC such that z has event weight 1 to maintain it's statistical error

// Barrel MC, passing probes
double p_mc = tmc->Draw("mmgMass>>hp_mc(15,75,105)",
                        Form("pileup.weightOOT * %f * (%s)",
                             weight[z],
                             (selection && vetoCut).GetTitle()
                            )
                        );
double pb_mc = tmc->Draw("mmgMass>>hpb_mc(15,75,105)",
                         Form("pileup.weightOOT * %f * (%s)",
                              weight[z],
                              (selection && vetoCut && backgroundCut).GetTitle()
                             )
                        );
double pb_qcd = tqcd->Draw("mmgMass>>hpb_qcd(15,75,105)",
                           Form("pileup.weightOOT * %f * (%s)",
                                 weight[qcd],
                                 (selection && vetoCut).GetTitle()
                                )
                          );
double pb_w = tw->Draw("mmgMass>>hpb_w(15,75,105)",
                       Form("pileup.weightOOT * %f * (%s)",
                             weight[w],
                             (selection && vetoCut).GetTitle()
                            )
                      );
double pb_tt = ttt->Draw("mmgMass>>hpb_tt(15,75,105)",
                         Form("pileup.weightOOT * %f * (%s)",
                               weight[w],
                               (selection && vetoCut).GetTitle()
                              )
                        );
double ps_mc = p_mc - pb_mc;
double eps_mc = sqrt(ps_mc);

// Barrel MC, failing probes
double f_mc = tmc->Draw("mmgMass>>hf_mc(15,75,105)",
                         Form("pileup.weightOOT * %f * (%s)",
                              weight[z],
                              (selection && !vetoCut).GetTitle()
                             )
                        );
double fb_mc = tmc->Draw("mmgMass>>hfb_mc(15,75,105)",
                         Form("pileup.weightOOT * %f * (%s)",
                               weight[z],
                               (selection && !vetoCut && backgroundCut).GetTitle()
                              )
                        );
double fb_qcd = tqcd->Draw("mmgMass>>hfb_qcd(15,75,105)",
                           Form("pileup.weightOOT * %f * (%s)",
                                 weight[qcd],
                                 (selection && !vetoCut).GetTitle()
                                )
                           );
double fb_w = tw->Draw("mmgMass>>hfb_w(15,75,105)",
                        Form("pileup.weightOOT * %f * (%s)",
                              weight[w],
                              (selection && !vetoCut).GetTitle()
                             )
                       );
double fb_tt = ttt->Draw("mmgMass>>hfb_tt(15,75,105)",
                         Form("pileup.weightOOT * %f * (%s)",
                               weight[tt],
                               (selection && !vetoCut).GetTitle()
                             )
                         );

double fs_mc = f_mc - fb_mc;
double efs_mc = sqrt(fs_mc);

// Barrel data
double p = tdata->Draw("mmgMass>>hp(15,75,105)", selection && vetoCut);
double f = tdata->Draw("mmgMass>>hf(15,75,105)", selection && !vetoCut);

double ps = ps_mc * p / (p_mc + pb_qcd + pb_w + pb_tt);
double fs = fs_mc * f / (f_mc + fb_qcd + fb_w + fb_tt);

double pb = p - ps;
double fb = f - fs;

double eps = Oplus(sqrt(p), pb + pb_qcd + pb_w + pb_tt); // 100 % error on bg
double efs = Oplus(sqrt(f), fb + pb_qcd + fb_w + fb_tt); // 100 % error on bg

// Calculate efficiency
double eff = ps / (ps + fs);
double eff_mc = ps_mc / (ps_mc + fs_mc);

// Efficiency error
if (fs < 1.e-5) {
    fs = 1.;
}
double eeff = eff*(1-eff)*Oplus(eps/ps, efs/fs);
double eeff_mc = eff_mc*(1-eff_mc)*Oplus(eps_mc/ps_mc, efs_mc/fs_mc);

cout << "== Normal approx. errors == " << endl;
cout << "veto efficiency in MC: " << eff_mc << " +/- " << eeff_mc << endl;
cout << "veto efficiency in data: " << eff << " +/- " << eeff << endl;

/// CL 1-sigma/68% Bayesian with Beta(1,1) prior with mode of posterior
/// to define the interval

TH1F h_pass("h_pass", "number of passing signal probes", 2, 0, 2);
TH1F h_total("h_total", "number of all signal probes", 2, 0, 2);

h_pass .GetXaxis()->SetBinLabel(1, "data");
h_total.GetXaxis()->SetBinLabel(1, "data");
h_pass .GetXaxis()->SetBinLabel(2, "MC");
h_total.GetXaxis()->SetBinLabel(2, "MC");

h_pass.Fill("data", ps);
h_pass.Fill("MC"  , ps_mc);
h_total.Fill("data", ps + fs);
h_total.Fill("MC"  , ps_mc + fs_mc);

TGraphAsymmErrors g_eff;
g_eff.BayesDivide(&h_pass, &h_total);

// Add systematic error on data in quadrature
// Assume systematic errors = 100% background
double eeff_syst = eff*(1-eff)*Oplus(pb/ps, fb/fs);

cout << "== Bayesian binomial errors == " << endl;

cout << "MC veto efficiency: "
      << g_eff.GetY()[1]
      << " + " << g_eff.GetErrorYhigh(1)
      << " - " << g_eff.GetErrorYlow(1)
      << " (stat.)" << endl;

cout << "Data veto efficiency: "
      << g_eff.GetY()[0]
      << " + " << g_eff.GetErrorYhigh(0)
      << " - " << g_eff.GetErrorYlow(0)
      << " (stat.) "
      << " +/- " << eeff_syst << " (syst.)"
      << endl;

// Draw passing probes TODO: ADD W and ttbar
TH1F *hp = (TH1F*) gDirectory->Get("hp");
TH1F *hp_mc = (TH1F*) gDirectory->Get("hp_mc");
TH1F *hpb_mc = (TH1F*) gDirectory->Get("hpb_mc");
TH1F *hpb_qcd = (TH1F*) gDirectory->Get("hpb_qcd");

// This is black magic
hp_mc->Add(hpb_qcd);
hpb_mc->Add(hpb_qcd);

double scaleFactor = hp->Integral() / hp_mc->Integral();
scaleFactor *= hp->GetBinWidth(1) / hp_mc->GetBinWidth(1);
hp_mc->Scale(scaleFactor);
hpb_mc->Scale(scaleFactor);
hpb_qcd->Scale(scaleFactor);

hp_mc->SetLineColor(kAzure - 9);
hp_mc->SetFillColor(kAzure - 9);
hpb_mc->SetLineColor(kSpring + 5);
hpb_mc->SetFillColor(kSpring + 5);
hpb_qcd->SetLineColor(kYellow - 7); // kOrange-2, kRed-3
hpb_qcd->SetFillColor(kYellow - 7);

hp_mc->SetTitle("R_{9} > 0.94");
hp_mc->GetXaxis()->SetTitle("m(#mu#mu#gamma) (GeV)");
hp_mc->GetYaxis()->SetTitle("Entries / 1 GeV");

hp_mc->SetStats(0);
hpb_mc->SetStats(0);
hpb_qcd->SetStats(0);

hp->SetMarkerStyle(20);

double ymax = TMath::Max(
    hp->GetMaximum() + TMath::Sqrt(hp->GetMaximum()),
    hp_mc->GetMaximum()
);

hp_mc->GetYaxis()->SetRangeUser(0, 1.1*ymax);


c1->cd(1);
hp_mc->Draw();
hpb_mc->Draw("same");
hpb_qcd->Draw("same");
hp->Draw("e0same");
c1->cd(1)->RedrawAxis();


// Draw failing probes
TH1F *hf = (TH1F*) gDirectory->Get("hf");
TH1F *hf_mc = (TH1F*) gDirectory->Get("hf_mc");
TH1F *hfb_mc = (TH1F*) gDirectory->Get("hfb_mc");

double scaleFactor = hf->Integral() / hf_mc->Integral();
scaleFactor *= hf->GetBinWidth(1) / hf_mc->GetBinWidth(1);
hf_mc->Scale(scaleFactor);
hfb_mc->Scale(scaleFactor);

hf_mc->SetLineColor(kAzure - 9);
hf_mc->SetFillColor(kAzure - 9);
hfb_mc->SetLineColor(kSpring + 5);
hfb_mc->SetFillColor(kSpring + 5);

hf_mc->SetTitle("R_{9} < 0.94");
hf_mc->GetXaxis()->SetTitle("m(#mu#mu#gamma) (GeV)");
hf_mc->GetYaxis()->SetTitle("Entries / 5 GeV");

hf_mc->SetStats(0);
hfb_mc->SetStats(0);

hf->SetMarkerStyle(20);

double ymax = TMath::Max(
    hf->GetMaximum() + TMath::Sqrt(hf->GetMaximum()),
    hf_mc->GetMaximum()
);

hf_mc->GetYaxis()->SetRangeUser(0, 1.1*ymax);

c1->cd(2);
hf_mc->Draw();
hfb_mc->Draw("same");
hf->Draw("e0same");
c1->cd(2)->RedrawAxis();

TCanvas *c2 = new TCanvas("c2", "c2", 40, 40 ,400, 400);
c2->SetRightMargin(0.02);
c2->SetLeftMargin(0.12);
TH2F *frame = new TH2F("frame","",2,0,2,1,0,1);
frame->SetStats(0);
frame->GetYaxis()->SetTitleOffset(1.5);
frame->GetYaxis()->SetTitle("Efficiency");
frame->GetXaxis()->SetLabelSize(0.08);
frame->GetXaxis()->SetBinLabel(1,"data");
frame->GetXaxis()->SetBinLabel(2,"MC");
frame->Draw();
g_eff.Draw("p");

c1->Print("m3_x.png");
c2->Print("eff_x.png");
}