SOURCE=zg.root
#SOURCE=zg_pick.root
root -l -b << EOF
TFile *_file0 = TFile::Open("$SOURCE")

// muonsAfterVtx->cd()
// muonsAfterId->cd()

// muons->SetScanField(0)
// muons->Scan(
//  "id.event:pt:eta:charge:isGlobal:isPF:normChi2:nHit:nMatch:dxy:dz:nPixel:"
//  "nLayer:chIso:nhIso:phIso:combIso:rho:EA"
//  ); >dump.txt

// photonsBeforeId->cd()
// photons->SetScanField(0)
// photons->Scan(
//   "id.event:pt:eta:eleVeto:hoe:sihih:"
//   "chIso:nhIso:phIso:rho:chEA:nhEA:phEA", "n > 0"
//  ); >dump.txt

mmgAfterDR->cd()
mmg->SetScanField(0)
mmg->Scan(
  "id.run:id.event:mass:mmMass:deltaR1:deltaR2:"
  "mu1Pt:mu2Pt:phoPt:mu1Q:mu2Q", "n > 0"
  ); >dump.txt

.q
EOF

## Remove asterisks, extra message and empty lines
sed -i '{s/*//g; /entries/d; /^ *$/d}' dump.txt
