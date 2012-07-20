'''
module fitter_test
-------------------

file: Zmmg/FWLite/test/phosphor/fitter_test.py

Tests the PHOSPHOR fitter.

Usage: python -i fitter_test.py

Jan Veverka, Caltech, 12 March 2012
'''

from Zmmg.FWLite.phosphor.fitter import Fitter


cfg_filename = 'test.cfg'
output_filename = 'test.root'


#______________________________________________________________________________
def get_configuration(filename):
    '''
    cfg get_configuration()
    
    Reads the configuration from a the file `filename' and returns it.
    '''
    return {'model': 'dummy cofig', 
            'monte_carlo': 'dummy cfg',
            'real_data': 'dummy cfg'}
## End of get_configuration(..).


#______________________________________________________________________________
def main():
    cfg = get_configuration(cfg_filename)
    
    global fitter
    fitter = Fitter('phosphor')

    fitter.build_model(cfg['model'])
    fitter.validate_model()

    fitter.fit_data(cfg['monte_carlo'])
    fitter.validate_fit(cfg)

    fitter.fit_data(cfg['real_data'])
    fitter.validate_fit(cfg)

    fitter.w.writeToFile(output_filename)
## End of main()


if __name__ == '__main__':
    main()
    import user
