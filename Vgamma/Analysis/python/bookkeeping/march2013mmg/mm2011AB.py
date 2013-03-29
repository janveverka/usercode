from Vgamma.Analysis.records.realdatasamplerecord import RealDataSampleRecord
from Vgamma.Analysis.tools import load_input_files

mm2011AB = RealDataSampleRecord(
    name              = 'mm2011AB',
    title             = ('Full DoubleMu 2011A (May10ReReco-v1, '
        '05Aug2011-v1, 03Oct2011-v1, PromptReco-v4) and '
        '2011B (PromptReco-v1) Data'),
    latex_label       = 'Data',
    source_filenames  = load_input_files('RealData/mm2011AB_susy.dat'),
    skim_filenames    = load_input_files('RealData/mmg_mm2011AB_susy.dat'),    
    total_processed_events = 56945243,
    ## AN-11-251 rev 153517, p. 150
    lumi_per_pb       = 4998.9,
    )

    
#______________________________________________________________________________
if __name__ == '__main__':
    print mm2011AB.__repr__()
    import user
