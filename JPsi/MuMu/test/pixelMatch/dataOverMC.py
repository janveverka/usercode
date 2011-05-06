import math

data, dataStatHi, dataStatLo, dataSyst = 86.0, 4.1, 5.0, 2.5
mc, mcStatHi, mcStatLo                 = 89.72, 0.19, 0.19

oplus = lambda x,y: math.sqrt(x*x + y*y)

latex = """  
    & & $97.4 ^{+0.9 }_{-1.2 } \pm 0.5$
    & $97.75^{+0.05}_{-0.05}$
    """

fragments = {
    "EB" : """
              & $97.4 ^{+0.9 }_{-1.2 } \pm 0.5$
              & $97.75^{+0.05}_{-0.05}$
           """,
    "EE" : """
              & $86.0 ^{+4.1 }_{-5.0 } \pm 2.5$
              & $89.72^{+0.19}_{-0.19}$ 
           """,
    
    "nVtx1-2" : """  
                  $97.5 ^{+1.2 }_{-1.7 } \pm 0.5$ &
                  $97.65^{+0.07}_{-0.07}$  \\
                """,
    "nVtx3up" : """
          $98.2 ^{+1.0 }_{-1.6 }\pm 0.6$  &
          $97.84^{+0.06}_{-0.06}$ \\
    
                """,
    "pt5-10" : """
          $99.0 ^{+0.7 }_{-1.4 } \pm 0.7$ &
          $97.93^{+0.07}_{-0.07}$ \\
    
                """,

    "pt10-20" : """
          $94.9 ^{+2.1 }_{-2.9 } \pm 0.4$  &
          $97.90^{+0.07}_{-0.07}$  \\
    
                """,

    "pt20up" : """
          $98.0 ^{+1.4 }_{-2.8 } \pm 0.1$  &
          $97.14^{+0.11}_{-0.12}$ \\
    
                """,
}

def printRatio(latex):
    ## clean up the latex string
    for c in "\n^{}+-&_\\pm$":
        latex = latex.replace(c, " ")
    data, dataStatHi, dataStatLo, dataSyst, mc, mcStatHi, mcStatLo = \
        tuple([float(x) for x in latex.split()])
    ratio = data/mc

    errData = oplus(max(dataStatHi, dataStatLo), dataSyst)
    errMC   = max(mcStatHi, mcStatLo)
    
    err = oplus(errData/data, errMC/mc) * ratio
    
    print "& $%.3f \\pm %.3f $ \\\\" % (ratio, err)
    
if __name__ == "__main__": 
    for name, latex in fragments.items():
        print name,
        printRatio(latex)
    import user