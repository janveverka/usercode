"""
Check the values of EBDetId static methods calculating
various fiducial flags of gaps between modules and super modules:
isNextToEtaBoundary and isNextToPhiBoundary.
"""
import ROOT
print "Loading FWLite library..."
ROOT.gSystem.Load("libFWCoreFWLite")
ROOT.AutoLibraryLoader.enable()
#ROOT.gSystem.Load('libDataFormatsEcalDetId')

def get_tree():
    ROOT.gROOT.ProcessLine(
        "struct FlagVars {"
        "  Int_t ieta, iphi, isEtaGap, isPhiGap, isGap;"
        "};"
        )

    flag_vars = ROOT.FlagVars()
    tree = ROOT.TTree("tree", "EBDetId fiducial flags test")
    tree.Branch("id",
                ROOT.AddressOf(flag_vars, "ieta"),
                "ieta/I:iphi:isEtaGap:isPhiGap:isGap")

    for ieta in range(-100,100):
        for iphi in range(-200,400):
            if not ROOT.EBDetId.validDetId(ieta, iphi):
                continue
            detid = ROOT.EBDetId(ieta,iphi)
            flag_vars.ieta = detid.ieta()
            flag_vars.iphi = detid.iphi()
            flag_vars.isEtaGap = ROOT.EBDetId.isNextToEtaBoundary(detid)
            flag_vars.isPhiGap = ROOT.EBDetId.isNextToPhiBoundary(detid)
            flag_vars.isGap = ROOT.EBDetId.isNextToBoundary(detid)
            tree.Fill()
    return tree

if __name__ == "__main__":
    import user
    tree = get_tree()
    # tree.Print()
    c1 = ROOT.TCanvas()
    tree.Draw("ieta>>h1(181,-90.5,90.5)", "isEtaGap")
    c2 = ROOT.TCanvas()
    tree.Draw('iphi>>h2(371,-5.5,365.5)', 'isPhiGap')
    
