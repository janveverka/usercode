{
  gSystem->Load("libJPsiMuMu");
  #include "JPsi/MuMu/interface/ModalInterval.h"
  size_t n = 10000;
  vector<double> data;
  data.reserve(n);
  for (int i=0; i<n; ++i) {
    data.push_back(gRandom->Gaus(0,1));
  }
  cit::ModalInterval mi(data.begin(), data.end(), 1);
  cout << "[" << mi.getLowBound() << ", " << mi.getHighBound() << "]" << endl;
  mi.setFraction(1 - TMath::Prob(pow(0.05,2), 1));
  cout << "[" << mi.getLowBound() << ", " << mi.getHighBound() << "]" << endl;
}