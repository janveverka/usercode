import array
import os
import ROOT
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.roofit as roo
from JPsi.MuMu.common.modalinterval import ModalInterval

basepath = '/home/cmorgoth/scratch/CMSSW_5_2_5/src/UserCode/CPena/src/PhosphorCorrFunctor/SIXIE_LAST_VERSION'

basecuts = [
    'DileptonMass + Mass < 180',
    # '0.1 < MinDeltaR',
    'MinDeltaR < 1.5', 
    'Mu2Pt > 10.5',
    'Mu1Pt > 21', 
    'DileptonMass > 55',
    ]
    
catcuts = [
    'PhotonIsEB',
    'PhotonPt > 25',
    'PhotonR9 > 0.94',
    ]

#==============================================================================
class Source:
    '''
    Facilitates the analysis
    '''    
    ROOT.gROOT.ProcessLine('''
        struct leafs_t {
          UInt_t RunNumber;
          UInt_t EventNumber;
          Float_t Mass;
        };
        '''.replace('\n', '')
        )
    #__________________________________________________________________________
    def __init__(self, name, title, filename, cuts):
        self.name = name
        self.title = title
        self.filename = filename
        self.cuts = cuts
        self.setup_tree()
    
    #__________________________________________________________________________
    def setup_tree(self):
        self.source = ROOT.TFile.Open(self.filename)
        self.tree = self.source.Get('ZmumuGammaEvent')
        self.setbranchstatus(mode='cuts')
        self.tree = self.tree.CopyTree(
            '&'.join(['(%s)' % c for c in self.cuts])
            )
        self.setbranchstatus(mode='brief')
        self.tree = self.tree.CopyTree('1')
        self.tree.BuildIndex('RunNumber', 'EventNumber')
        ## Create leaf buffers
        self.leafs = ROOT.leafs_t()
        for leaf in 'RunNumber EventNumber Mass'.split():
            self.tree.SetBranchAddress(leaf, 
                                       ROOT.AddressOf(self.leafs, leaf))
    #__________________________________________________________________________
    def setbranchstatus(self, mode='cuts'):
        self.tree.SetBranchStatus("*", 0)
        if mode == 'cuts':
            for branch in '''
                          RunNumber
                          EventNumber
                          Mass
                          DileptonMass
                          MinDeltaR
                          Mu1Pt
                          Mu2Pt
                          PhotonIsEB
                          PhotonPt
                          PhotonR9           
                          '''.split():
                self.tree.SetBranchStatus(branch, 1)
        elif mode == 'brief':
            for branch in '''
                          RunNumber
                          EventNumber
                          Mass
                          '''.split():
                self.tree.SetBranchStatus(branch, 1)            
## End of Source



#==============================================================================
class Merger:
    #__________________________________________________________________________
    def __init__(self, source1, source2):
        self.source1 = source1
        self.source2 = source2
        self.tree = ROOT.TTree('merged', 'merged')
        self.merge()
    #__________________________________________________________________________
    def merge(self):
        for src in [self.source1, self.source2]:
            self.tree.Branch(src.name,
                             ROOT.AddressOf(src.leafs, 'Mass'),
                             src.name + '/F')
        for entry in range(self.source1.tree.GetEntries()):
            self.source1.tree.GetEntry(entry)
            run   = self.source1.leafs.RunNumber
            event = self.source1.leafs.EventNumber
            bytes = self.source2.tree.GetEntryWithIndex(run, event)
            if bytes < 0:
                # print 'Run', run, 'Event', event, 'not in', 
                # print self.source2.name
                continue
            self.tree.Fill()
    #__________________________________________________________________________
    def report(self):
        common = self.tree.GetEntries()
        print 'Common events:', common
        for src in [self.source1, self.source2]:
            total = src.tree.GetEntries()
            unique = total - common
            percent = float(unique) / total
            print 'Unique for %s:' % src.name, unique, '(%.2g %%)' % percent
# End of class Merger


#==============================================================================
class Profiler:
    #__________________________________________________________________________
    def __init__(self, data, fractions=[0.1 * i for i in range(1,10)]):
        self.data = data
        self.fractions = fractions
        self.makegraph()
        
    #__________________________________________________________________________
    def makegraph(self):
        row = self.data.get()
        if row.getSize() < 1:
            raise RuntimeError, 'Dataset must contain at least one variable!'
        self.data.tree().Draw(row.first().GetName(), '', 'goff')
        size = self.data.tree().GetSelectedRows()
        first = self.data.tree().GetV1()
        modalinterval = ModalInterval(size, first)
        widths = []
        for x in self.fractions:
            modalinterval.setFraction(x)
            widths.append(modalinterval.length())
        xvalues = array.array('d', self.fractions)
        yvalues = array.array('d', widths)
        self.graph = ROOT.TGraph(len(self.fractions), xvalues, yvalues)
        
## End of class Profiler


regression = Source(
    name = 'regression',
    title = 'Regression',
    filename = os.path.join(
        basepath, 
        'PhotonRegression/ZmumuGammaNtuple_Full2012_MuCorr.root'
        ),
    cuts = basecuts + catcuts,
    )
    
default = Source(
    name = 'default',
    title = 'Default',
    filename = os.path.join(
        basepath, 
        'NoPhotonRegression/ZmumuGammaNtuple_Full2012_MuCorr.root',
        ),
    cuts = basecuts + catcuts,
    )

merger = Merger(default, regression)
merger.report()

common = merger.tree.GetEntries()


w = ROOT.RooWorkspace('w', 'w')
w.factory('regression[60, 120]')
w.factory('default[60, 120]')
data = dataset.get(tree=merger.tree,
                   variables=[w.var(x) for x in 'default regression'.split()])
data.tree().Draw('default:regression', '', 'goff')

data1 = data.reduce(ROOT.RooArgSet(w.var('regression')))
data2 = data.reduce(ROOT.RooArgSet(w.var('default'   )))
granularity = 200
fractions = [1./granularity * i for i in range(1, granularity)]
p1 = Profiler(data1, fractions)
p2 = Profiler(data2, fractions)

p1.graph.SetLineColor(ROOT.kRed)
canvases.next()
p1.graph.Draw('al')
p2.graph.Draw('l')

graph = ROOT.TGraph(p1.graph.GetN())
for i in range(graph.GetN()):
    x = p1.graph.GetX()[i]
    y = p1.graph.GetY()[i] / p2.graph.GetY()[i]
    graph.SetPoint(i, x, y)

canvases.next()
graph.Draw('al')

#modalinterval.length()
#fractions = [0.1 * i for i in range(1, 10)]
#widths = []
#for x in fractions:
    #modalinterval.setFraction(x)
    #widths.append(modalinterval.length())

#xvalues = array.array('d', fractions)
#yvalues = array.array('d', widths)
#graph = ROOT.TGraph(len(fractions), xvalues, yvalues)
#graph.Draw('ap')
#output = ROOT.TFile(outpath, 'RECREATE')
#graph.Write('width')
#output.Write()

if __name__ == '__main__':
    import user
