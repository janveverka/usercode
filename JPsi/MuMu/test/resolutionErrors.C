double zMassPdg() { return 91.1876; }

double Oplus(double a, double b) { return TMath::Sqrt(a*a + b*b); }

float muonSigmaPtOverPt(float pt, float eta) {
  /// Muon pt relative error sigma(pt_mu)/pt, see fig. 17 of AN2008_097_v3.pdf
  /// Normalized to 1 for Pt < 10 GeV
  float ptFactor = pt < 10. ? 1 : -5 + 6  * TMath::Log10(pt);

  /// Muon pt relative error as a function of eta
  /// CMS PAS TRK-10-004 eq. (5)
  float b[] = {1.61, 5e-3, 1.9e-2, 1.4e-2, 1.5};
  float etaFactor;
  if (TMath::Abs(eta) < b[0]) {
    float b0MinusB4 = b[0] - b[4];
    float c = b[2] + b[3] + b0MinusB4 * b0MinusB4 - b[1] * b[0] * b[0];
    etaFactor = c + b[1] * eta * eta;
  } else {
    float absEtaMinusB4 = TMath::Abs(eta) - b[4];
    etaFactor = b[2] + b[3] * absEtaMinusB4 * absEtaMinusB4;
  }
  return ptFactor * etaFactor;
}

/// see CMS IN 2000/028 for EE, 2008 JINST 3 S08004 and CMS DN-2007/12 for EB
float photonSigmaEOverE(float E, float eta){
  if (TMath::Abs(eta) < 1.5) {
    float s = 0.035;
    float n = 0.15;
    float c = 0.02;
    float sTerm = s / TMath::Sqrt(E);
    float nTerm = n / E;
    return TMath::Sqrt(sTerm * sTerm + nTerm * nTerm + c * c);
  } else {
    float s = 0.05;
    float n = 0.45;
    float c = 0.06;
    float sTerm = s / TMath::Sqrt(E);
    float nTerm = n / E;
    return TMath::Sqrt(sTerm * sTerm + nTerm * nTerm + c * c);
  }
}

float photonSigmaPtOverPt(float pt, float eta){
  return photonSigmaEOverE(pt * TMath::CosH(eta), eta);
}

float phoEtrue(float mmMass) {
  return 0.5*(zMassPdg()*zMassPdg() - mmMass*mmMass) / mmMass;
}

float phoEmeas(float mmgMass, float mmMass) {
  return 0.5 * (mmgMass*mmgMass - mmMass*mmMass) / mmMass;
}

float kFactor(float mmgMass, float mmMass) {
  return phoEtrue(mmMass) / phoEmeas(mmgMass, mmMass);
}