'''
Holds information about photon ID variables.
Jan Veverka, MIT, jan.veverka@cern.ch
28 July 2013
'''

import sys

#______________________________________________________________________________
class Config:
    '''
    Holds configuration data.
    '''
    def __init__(self, *args, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
## End of class Config


#______________________________________________________________________________
## Shorthand definitions of frequent configuration fragments
bcuts = ['ph1.isbarrel', 'ph2.isbarrel']
ecuts = ['!ph1.isbarrel', '!ph2.isbarrel']
epair = lambda expression: ['ph1.' + expression, 'ph2.' + expression]


#______________________________________________________________________________
configs = [
    Config(name        = 'mass',
           title       = 'Mass',
           unit        = 'GeV',
           expressions = ['mass'],
           binning     = '60,60,120'),
           
    Config(name        = 'pt',
           title       = 'Electron p_{T}',
           unit        = 'GeV',
           expressions = ['ph1.pt', 'ph2.pt'],
           binning     = '200,0,200'),
           
    Config(name        = 'eta',
           title       = 'Electron #eta',
           unit        = 'GeV',
           expressions = ['ph1.eta', 'ph2.eta'],
           binning     = '120,-3,3'),
           
    Config(name        = 'pt1',
           title       = 'Lead Electron p_{T}',
           unit        = 'GeV',
           expressions = ['ph1.pt'],
           binning     = '200,0,200'),
           
    Config(name        = 'pt2',
           title       = 'Sublead Electron p_{T}',
           unit        = 'GeV',
           expressions = ['ph2.pt'],
           binning     = '200,0,200'),
           
    Config(name        = 'eta1',
           title       = 'Lead Electron #eta',
           expressions = ['ph1.eta'],
           binning     = '120,-3,3'),
           
    Config(name        = 'eta2',
           title       = 'Sublead Electron #eta',
           expressions = ['ph2.eta'],
           binning     = '120,-3,3'),

    Config(name        = 'r9b',
           title       = 'Barrel Electron r_{9}',
           expressions = epair('r9'),
           binning     = '110,0.1,1.2',
           selections  = bcuts,
           qqbinning   = '70,0.29,0.99',),
           
    Config(name        = 'r9e',
           title       = 'Endcap Electron r_{9}',
           expressions = epair('r9'),
           binning     = '110,0.1,1.2',
           selections  = ecuts,
           qqbinning   = '60,0.4,1.0',),
           
    Config(name        = 'setab',
           title       = 'Barrel SC #sigma_{#eta} #times 1000',
           expressions = epair('scetawidth * 1000'),
           binning     = '100,0.,0.03',
           selections  = bcuts,
           qqbinning   = '50,6,16',),
           
    Config(name        = 'setae',
           title       = 'Endcap SC #sigma_{#eta} #times 1000',
           expressions = epair('scetawidth * 1000'),
           binning     = '100,0.,0.05',
           selections  = ecuts,
           qqbinning   = '50,10,35',),
           
    Config(name        = 'sphib',
           title       = 'Barrel SC #sigma_{#phi} #times 1000',
           expressions = epair('scphiwidth * 1000'),
           binning     = '100,0.,0.2',
           selections  = bcuts,
           qqbinning   = '50,6,106',),
           
    Config(name        = 'sphie',
           title       = 'Endcap SC #sigma_{#phi} #times 1000',
           expressions = epair('scphiwidth * 1000'),
           binning     = '100,0.,0.2',
           selections  = ecuts,
           qqbinning   = '50,6,106',),
           
    Config(name        = 'sieieb',
           title       = 'Barrel SC #sigma_{i#etai#eta} #times 1000',
           expressions = epair('sigietaieta * 1000'),
           binning     = '130,0.001,0.014',
           selections  = bcuts,
           qqbinning   = '60,6,12',),
           
    Config(name        = 'sieiee',
           title       = 'Endcap SC #sigma_{i#etai#eta} #times 1000',
           expressions = epair('sigietaieta * 1000'),
           binning     = '100,0.01,0.035',
           selections  = ecuts,
           qqbinning   = '60,19,34',),
           
    Config(name        = 'cieipb',
           title       = 'Barrel SC cov(i#eta,i#phi) #times 10^{4}',
           expressions = epair('idmva_CoviEtaiPhi * 1e4'),
           binning     = '200,-2.5,2.5',
           selections  = bcuts,
           qqbinning   = '50,-1,1',),
           
    Config(name        = 'cieipe',
           title       = 'Endcap SC cov(i#eta,i#phi) #times 10^{4}',
           expressions = epair('idmva_CoviEtaiPhi * 1e4'),
           binning     = '100,-10,10',
           selections  = ecuts,
           qqbinning   = '50,-6,4',),
           
    Config(name        = 's4ratiob',
           title       = 'Barrel S_{4} Ratio',
           expressions = epair('idmva_s4ratio'),
           binning     = '160,0.3,1.1',
           selections  = bcuts,
           qqbinning   = '50,0.45,0.95',),
           
    Config(name        = 's4ratioe',
           title       = 'Endcap S_{4} Ratio',
           expressions = epair('idmva_s4ratio'),
           binning     = '160,0.3,1.1',
           selections  = ecuts,
           qqbinning   = '50,0.45,0.95',),
           
]


#______________________________________________________________________________
this_module = sys.modules[__name__]
config_map = {}
for cfg in configs:
    ## Fill in defaults
    if not hasattr(cfg, 'unit'):
        cfg.unit = ''
    if not hasattr(cfg, 'selections'):
        cfg.selections = [''] * len(cfg.expressions)
    if not hasattr(cfg, 'qqbinning'):
        cfg.qqbinning = cfg.binning        
    ## Attach to the module and to a dictionary
    setattr(this_module, cfg.name, cfg)
    config_map[cfg.name] = cfg
  
