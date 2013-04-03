from Vgamma.Analysis.records.montecarlosamplerecord import MonteCarloSampleRecord
from Vgamma.Analysis.tools import load_input_files


zmmg = MonteCarloSampleRecord(
    name = 'zmmg',
    title = ('ZGammaToMuMuGamma_2Jet_MG5_TuneZ2 UW Private Sample with Fall11'
        ' Conditions'),
    latex_label = 'Z#gamma#to#mu#mu#gamma',
    source_filenames = load_input_files('MC/zmmg_susy.dat'),
    source_tree       = 'VgAnalyzerKit/EventTree',
    skim_filenames = load_input_files('MC/mmg_zmmg_susy.dat'),
    skim_tree         = 'EventTree',
    tree_version      = 'V15MC',
    total_processed_events = 472380,
    ## AN-11-251 rev 153517, p. 7
    cross_section_in_pb = 45.2,
    )

    
#______________________________________________________________________________
if __name__ == '__main__':
    print zmmg.__repr__()
    import user
