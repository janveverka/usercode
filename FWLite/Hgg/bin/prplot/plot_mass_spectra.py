import os
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases


#______________________________________________________________________________
def get_inputs():
    '''
    Opens the input files for 7 and 8 TeV and returns a dictionary of the 
    inputs (period) -> (root file).
    '''
    data_path = '/mnt/hadoop/user/bornheim/hgg/2012/ichep2012/common'
    filenames = {
        '7TeV': 'hgg.inputbkgdata_7TeV.root',
        '8TeV': 'hgg.inputbkgdata_8TeV.root',
        }

    inputs = {}
    for period, filename in filenames.items():
        inputs[period] = ROOT.TFile.Open(os.path.join(data_path, filename))
    return inputs
## End of get_inputs()


#______________________________________________________________________________
def main():
    '''
    Main entry point of execution.
    '''
    inputs = get_inputs()
    print inputs
## End of main


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
