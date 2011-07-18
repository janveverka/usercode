import copy

'''Holds data specifying a plot based on a TTree'''
class PlotData:
    def __init__(self, name, title, source, expression, cuts, labels):
        ## string used as a key in various dictionaries
        self.name = name
        ## string used in human-readable output
        self.title = title
        ## TLaltex string list that is included on the graphics
        self.labels = labels
        ## TTree providing source of data
        self.source = source
        ## TTree::Draw expression string of variable subject to fittin
        self.expression = expression
        ## TTree::Draw selection string applied to data source
        self.cuts = cuts

    def clone(self, **kwargs):
        newPlot = copy.deepcopy(self)
        for argName, argValue in kwargs.items():
            setattr( newPlot, argName, argValue )
        return newPlot