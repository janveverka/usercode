from Vgamma.Analysis.records.montecarlosamplerecord import MonteCarloSampleRecord
from Vgamma.Analysis.tools import load_input_files


qcd20m = MonteCarloSampleRecord(
    name = 'qcd20m',
    title = 'QCD_Pt20_MuEnrichedPt15_TuneZ2_Summer11',
    latex_label = 'QCD',
    source_filenames = load_input_files('MC/qcd20m_hadoop.dat'),
    skim_filenames = load_input_files('MC/mmg_qcd20m_hadoop.dat'),
    ## AN-11-251 rev 153517, p. 7
    cross_section_in_pb = 84679.3,
    )

qcd20m.total_processed_events = 25009714
