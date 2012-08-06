root -l -b << EOF
TFile *_file0 = TFile::Open("zg.root")
muonTree->cd()
muons->SetScanField(0)
muons->Scan("id.event:pt:charge:isGlobal:isPF:normChi2:nHit:nMatch:dxy:dz:nPixel:nLayer"); >Caltech_s12_muons_after_id.txt
.q
EOF

sed -i 's/*//g' Caltech_s12_muons_after_id.txt
