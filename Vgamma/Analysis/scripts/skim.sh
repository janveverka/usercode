skim VgAnalyzerKit/EventTree \
    ZGammaToMuMuGamma_2Jet_MG5_TuneZ2_mmgSkim.root \
    ZGammaToMuMuGamma_2Jet_MG5_TuneZ2.root \
    -c'Sum$(muPt > 10) > 1 & nPho > 0' \
    -e1000 -v
