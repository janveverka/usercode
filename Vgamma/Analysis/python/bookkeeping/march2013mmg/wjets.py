from Vgamma.Analysis.records.montecarlosamplerecord import MonteCarloSampleRecord
from Vgamma.Analysis.tools import load_input_files


wjets = MonteCarloSampleRecord(
    name = 'wjets',
    title = 'WJetsToLNu_TuneZ2_Madgraph_Fall11',
    latex_label = 'W+jets',
    source_filenames = load_input_files('MC/wjets_hadoop.dat'),
    skim_filenames = load_input_files('MC/mmg_wjets_hadoop.dat'),
    ## AN-11-251 rev 153517, p. 7
    cross_section_in_pb = 31314.,
    )

## Injected from processedevents.py
wjets.total_processed_events = 80256027
