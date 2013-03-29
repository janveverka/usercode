from Vgamma.Analysis.records.montecarlosamplerecord import MonteCarloSampleRecord
from Vgamma.Analysis.tools import load_input_files


zz = MonteCarloSampleRecord(
    name = 'zz',
    title = 'ZZ_TuneZ2_Fall11',
    latex_label = 'ZZ',
    source_filenames = load_input_files('MC/zz_hadoop.dat'),
    skim_filenames = load_input_files('MC/mmg_zz_hadoop.dat'),
    ## AN-11-251 rev 153517, p. 7
    cross_section_in_pb = 5.9,
    )

zz.total_processed_events = 4066045
