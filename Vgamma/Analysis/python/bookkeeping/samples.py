'''
Register of samples used in the analysis

Jan Veverka, Caltech, 27 March 2013.
'''

from Vgamma.Analysis.bookkeeping.sampleregister import SampleRegister

register = SampleRegister()

## AN-11-251 rev 153517, p. 150
register.data(
    name = 'mm2011AB',
    lumi = 4998.9,
    )

register.data(
    name = "ee2011AB", 
    lumi = 4961.1
    )

## AN-11-251 rev 153517, p. 7
register.mc(
    name = "zmmg", 
    cross_section = 45.2
    )
    
register.mc(
    "zjets", 
    cross_section = 3048.
    )
    
register.mc(
    "ttbar", 
    cross_section = 165.
    )
    
register.mc(
    "wjets", 
    cross_section = 31314
    )    
    
register.mc(
    "qcd20m", 
    cross_section = 84679.3
    )
    
register.mc(
    "ww", 
    cross_section = 5.7
    )
    
register.mc(
    "wz", 
    cross_section = 18.2
    )
    
register.mc(
    "zz", 
    cross_section = 5.9
    )
    