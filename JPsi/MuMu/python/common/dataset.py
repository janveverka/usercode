'''Utility to extract RooDataSet from a TTree.

Data:
  - tree: source TTree
  - variable: RooRealVar in dataset rows defined by TTree.Draw expression
              in it's title.
  - weight: RooRealVar defining dataset weights
  - categories: RooCategory list included in dataset.
                Expression evaluating to index is defined by their titles.
  - cuts: List of strings defining cuts that extracted rows pass.
  - dataset: RooDataSet extracted after call to dataset.get()
  (- canvases: optional auxiliary TCanvas list used for testing)

Functions:
  - set: Set data values. Helper function of get.
  - get: Takes optional tree, variable, categories, cuts.
         Updates data with given args using set and extracts dataset from tree
         given configuration held in variable, categories and cuts.
         Updates dataset data and returns it.
  - plot: Plot the dataset on variable's frame.
  - main:
Takes a tree, a RooRealVar variable, a list of categories and a list of cuts.
Returns a RooDataSet extracted from the tree given the expressions in
variable and categories titles.
'''

import os
import sys
import ROOT

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *

## Configuration
tree = TTree()
variable = RooRealVar( 'x', 'dummy x variable', 0, -10, 10)
weight = RooRealVar( 'w', 'dummy weight', 1 )

## Default/example categories
categories = []

cuts = []

dataset = RooDataSet()

#------------------------------------------------------------------------------
def set(**kwargs):
    global tree, variable, weight, cuts, categories, dataset
    for arg in 'tree variable weight cuts categories dataset'.split():
        if arg in kwargs.keys():
            setattr( sys.modules[__name__], arg, kwargs[arg] )
            del kwargs[arg]
    if kwargs.keys():
        raise RuntimeError, "Unknown argument(s): %s" % repr( kwargs.keys() )
## set

#------------------------------------------------------------------------------
def get(**kwargs):
    global tree, variable, weight, cuts, categories, dataset

    ## Initialize
    set(**kwargs)
    varSet = RooArgSet( variable, weight, *categories )
    dataset = RooDataSet( 'data', 'data', varSet, WeightVar( weight.GetName() ) )
    #dataset.setWeightVar( weight )
    #dataset = RooDataSet('data', 'data', varSet )

    ## Build list expressions for variables
    varExpressions = [ variable.GetTitle(), weight.GetTitle() ]

    for cat in categories:
        varExpressions.append( cat.GetTitle() )

    ## Auxiliary function to build the selection string
    andCuts = lambda(cuts): " & ".join( "(%s)" % cut for cut in cuts )
    joinExpressions = lambda(expressions): ":".join( expressions )

    ## Set the title for the dataset
    dataset.SetTitle( '%s for %s' % ( joinExpressions(varExpressions),
                                      andCuts(cuts)                    ) )
    ## Select only events within the range of variable.
    ## This is needed to exclude underflows and overflows.
    cuts.append('%f<%s & %s<%f' % (variable.getMin(), variable.GetTitle(),
                                   variable.GetTitle(), variable.getMax()))
    ## Get the data from the tree
    tree.Draw( joinExpressions(varExpressions), andCuts(cuts), 'goff para' )

    ## Fill the dataset
    for i in range( tree.GetSelectedRows() ):
        variable.setVal( tree.GetV1()[i] )
        weight.setVal( tree.GetV2()[i] )
        for icat in range( len(categories) ):
            cat = categories[icat]
            x = tree.GetVal(icat+2)[i]
            cat.setIndex( int(x) )
        dataset.add( varSet, weight.getVal() )
    ## Close the file with source tree

    return dataset
## get

#------------------------------------------------------------------------------
def plot():
    frame = variable.frame()
    dataset.plotOn(frame)
    frame.Draw()
    return frame
# plot

#------------------------------------------------------------------------------
def main():
    'test the get function'
    global canvases
    canvases = []

    #gROOT.Set

    get()
    canvases.append( TCanvas('s', 's') )
    plot()

    get( variable = RooRealVar('k', 'kRatio', 0.5, 1.5) )
    canvases.append( TCanvas('k_noweights', 'k_noweights') )
    frame = plot()
    dataset.plotOn( frame, Cut('subdet==subdet::Barrel'), MarkerColor(kBlue),
                    LineColor(kBlue) )
    dataset.plotOn( frame, Cut('subdet==subdet::Endcaps'), MarkerColor(kRed),
                    LineColor(kRed) )
    frame.Draw()

    canvases.append( TCanvas('k_withweights', 'k_withweights') )
    frame = plot()
    dataset.plotOn( frame, Cut('subdet==subdet::Barrel'), MarkerColor(kBlue),
                    LineColor(kBlue), DataError(RooAbsData.SumW2) )
    dataset.plotOn( frame, Cut('subdet==subdet::Endcaps'), MarkerColor(kRed),
                    LineColor(kRed) )
    frame.Draw()

    get( variable = RooRealVar('logik', '-log(kRatio)', -0.5, 0.5) )
    canvases.append( TCanvas() )
    frame = plot()
    dataset.plotOn( frame, Cut('r9==r9::High'), MarkerColor(kBlue),
                    LineColor(kBlue) )
    dataset.plotOn( frame, Cut('r9==r9::Low'), MarkerColor(kRed),
                    LineColor(kRed) )
    frame.Draw()
## main

if __name__ == "__main__":
    main()
    import user
