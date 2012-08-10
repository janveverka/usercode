SOURCE=zg.root
#SOURCE=zg_pick.root
root -l -b << EOF
TFile *_file0 = TFile::Open("$SOURCE")
// muonsAfterVtx->cd()
// muonsAfterId->cd()
muonsAfterIso->cd()
muons->SetScanField(0)
muons->Scan(
  "id.event:pt:eta:charge:isGlobal:isPF:normChi2:nHit:nMatch:dxy:dz:nPixel:"
  "nLayer:chIso:nhIso:phIso:combIso:rho:EA"
  ); >dump.txt
.q
EOF

sed -i 's/*//g' dump.txt
