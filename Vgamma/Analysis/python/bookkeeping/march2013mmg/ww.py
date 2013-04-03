from Vgamma.Analysis.records.montecarlosamplerecord import MonteCarloSampleRecord
from Vgamma.Analysis.tools import load_input_files


ww = MonteCarloSampleRecord(
    name = 'ww',
    title = 'WWJetsTo2L2Nu_TuneZ2_Fall11',
    latex_label = 'WW',
    source_filenames = load_input_files('MC/ww_hadoop.dat'),
    source_tree       = 'VgAnalyzerKit/EventTree',
    skim_filenames = load_input_files('MC/mmg_ww_hadoop.dat'),
    skim_tree         = 'EventTree',
    tree_version      = 'V14MC',
    ## AN-11-251 rev 153517, p. 7
    cross_section_in_pb = 5.7,
    )

ww.total_processed_events = 1190173
