from Vgamma.Analysis.records.montecarlosamplerecord import MonteCarloSampleRecord
from Vgamma.Analysis.tools import load_input_files


ttbar = MonteCarloSampleRecord(
    name = 'ttbar',
    title = 'TTJets_TuneZ2_Madgraph_Fall11',
    latex_label = 't#bar{t}',
    source_filenames = load_input_files('MC/ttbar_hadoop.dat'),
    source_tree       = 'VgAnalyzerKit/EventTree',
    skim_filenames = load_input_files('MC/mmg_ttbar_hadoop.dat'),
    skim_tree         = 'EventTree',
    tree_version      = 'V14MC',
    ## AN-11-251 rev 153517, p. 7
    cross_section_in_pb = 165.,
    )
    
## Generated automatically
ttbar.total_processed_events = 3582450
