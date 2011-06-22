##
##
## Takes a filename, a tree name, a RooArgSet, and a vector of cuts
## and produces a RooDataset
##
import os
import sys
import ROOT

## Configuration
path = '/raid2/veverka/esTrees'
inputFiles = ['esTree_DYToMuMu_pythia6_AOD-42X-v4_V2.root']
treeName = 'pmvTree/pmv'
variable = ROOT.RooRealVar('s', '100*(1/kRatio-1)', 0, -50, 50, "%")
cuts = [ '87.2 < mmgMass',
         'mmgMass < 95.2',
         'phoIsEB' ]

## Default Categories
## Use negative r9 values for the Endcaps
##    Endcaps  |   Barrel
##  high | low | low | high
##     -0.95   0    0.94
_r9 = ROOT.RooRealVar('r9', '(2*phoIsEB-1)*phoR9', -2, 2)
_r9cat = ROOT.RooThresholdCategory('r9cat', 'photon r9', _r9, 'high' )
_r9cat.addThreshold(-0.95, 'high') ## Endcaps
_r9cat.addThreshold(0.94, 'low')   ## Barrel

_subdet = ROOT.RooCategory('subdet', 'phoIsEB')
_subdet.defineType('Barrel' , 1)
_subdet.defineType('Endcaps', 0)

# categories = [_r9, _subdet]
categories = [_subdet]

## Data attached in the process
dataset = ROOT.RooDataSet()

#------------------------------------------------------------------------------
def setDefault(**kwargs):
    global inputFiles, treeName, variable, cuts, dataset, categories
    for arg in 'inputFiles treeName variable cuts dataset categories'.split():
        if arg in kwargs.keys():
            setattr( sys.modules[__name__], arg, kwargs[arg] )
            del kwargs[arg]
    if kwargs.keys():
        raise RuntimeError, "Unknown argument(s): %s" % repr( kwargs.keys() )
## setDefault

#------------------------------------------------------------------------------
def getDataSet(**kwargs):
    global inputFiles, treeName, variable, cuts, dataset, categories
    setDefault(**kwargs)

    ## Initialize
    varSet = ROOT.RooArgSet( variable, *categories )
    dataset = ROOT.RooDataSet('data', 'data', varSet )

    ## Get the tree / chain
    tree = ROOT.TChain(treeName)
    for f in inputFiles:
        tree.AddFile( os.path.join(path, f) )

    ## Build list expressions for variables
    varExpressions = [ variable.GetTitle() ]

    for cat in categories:
        if type(cat) == type( ROOT.RooThresholdCategory() ):
            varExpressions.append(
                cat.getVariables().createIterator().GetTitle()
                )
        else:
            varExpressions.append( cat.GetTitle() )

    ## Auxiliary function to build the selection string
    andCuts = lambda(cuts): " & ".join( "(%s)" % cut for cut in cuts )
    joinExpressions = lambda(expressions): ":".join( expressions )

    ## Get the data from the tree
    print 'expr = ', joinExpressions(varExpressions)
    print 'cuts = ', andCuts(cuts)
    tree.Draw( joinExpressions(varExpressions), andCuts(cuts), 'goff' )

    ## Fill the data in the dataset
    for i in range( tree.GetSelectedRows() ):
        variable.setVal( tree.GetV1()[i] )
        for icat in range( len(categories) ):
            cat = categories[icat]
            x = tree.GetVal(icat+1)[i]
            if type(cat) == type( ROOT.RooThresholdCategory() ):
                cat.getVariables().createIterator().setVal(x)
            else:
                cat.setIndex( int(x) )
        dataset.addFast( varSet )
    ## Close the file with source tree

    return dataset

#------------------------------------------------------------------------------
def main():
    ## test the getDataSet function
    getDataSet()
    plot = variable.frame()
    dataset.plotOn(plot)
    plot.Draw()



    pass
## main

if __name__ == "__main__":
    main()
    import user