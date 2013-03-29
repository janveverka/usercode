from Vgamma.Analysis.records.montecarlosamplerecord import MonteCarloSampleRecord
from Vgamma.Analysis.tools import load_input_files


zjets = MonteCarloSampleRecord(
    name = 'zjets',
    title = 'DYJetsToLL_TuneZ2_M50_Madgraph_Fall11',
    latex_label = 'Z+jets',
    source_filenames = load_input_files('MC/zjets_hadoop.dat'),
    # skim_filenames = load_input_files('MC/eeg_zjets_hadoop.dat'),
    ## AN-11-251 rev 153517, p. 7
    cross_section_in_pb = 3048.,
    )

## Injected automatically by output of 
## Vgamma.Analysis.bookkeeping.processedevents
zjets.total_processed_events = 34576856

