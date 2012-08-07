SOURCE=zg_pick.root
root -l -b << EOF
TFile *_file0 = TFile::Open("$SOURCE")
muonTree->cd()
muons->SetScanField(0)
muons->Scan("id.event:pt:eta:charge:isGlobal:isPF:normChi2:nHit:nMatch:dxy:dz:nPixel:nLayer"); >dump.txt
.q
EOF

sed -i 's/*//g' dump.txt
