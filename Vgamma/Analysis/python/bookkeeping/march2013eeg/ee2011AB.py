from Vgamma.Analysis.records.realdatasamplerecord import RealDataSampleRecord
from Vgamma.Analysis.tools import load_input_files

ee2011AB = RealDataSampleRecord(
    name              = 'ee2011AB',
    title             = ('Full DoubleElectron 2011A (May10ReReco-v1, '
        '05Aug2011-v1_excTrg_addCSC, 03Oct2011-v1, PromptReco-v4) and '
        '2011B (PromptReco-v1) Data'),
    latex_label       = 'Data',
    source_filenames  = load_input_files('RealData/ee2011AB_susy.dat'),
    #skim_filenames    = load_input_files('RealData/eeg_ee2011AB_susy.dat'),    
    ## AN-11-251 rev 153517, p. 150
    lumi_per_pb       = 4961.1,
    )

    
## Injected automatically by output of 
## Vgamma.Analysis.bookkeeping.processedevents
ee2011AB.total_processed_events = 58582068

