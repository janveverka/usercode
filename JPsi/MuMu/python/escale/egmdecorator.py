'''
Provides the class EgmDecorator that facilitates the decoration of the PHOSPHOR
fits for the EGM-11-001 paper.
'''

import os
import ROOT

import JPsi.MuMu.tools as tools
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.latex import Latex

## Initial values are set to MC truth for data only
basepath = '/raid2/veverka/jobs/outputs/eg_paper'

## Initial values are set to MC truth for both data and MC
# basepath = '/raid2/veverka/jobs/outputs/eg_paper_v2'

## In addition to eg_paper_v2, us dr > 0.1 to reduce muon bias
# basepath = '/raid2/veverka/jobs/outputs/eg_paper_dr0p1'

###############################################################################
class EgmDecorator:
    #__________________________________________________________________________
    def __init__(self, name='egm_data_EB_pt25to999_yyv3'):
        '''
        Initializes the canvas.
        '''
        self.name = name
                
        ## Open the file
        filename = 'phosphor5_model_and_fit_' + name + '.root'
        filepath = os.path.join(basepath, name, filename)
        rootfile = ROOT.TFile.Open(filepath)
        
        ## Get the workspace from the rootfile and close it again.
        self.workspace = rootfile.Get(name + '_workspace').Clone()
        rootfile.Close()
        
        self.old_canvas = self.get_old_canvas()
        self.new_canvas = self.get_new_canvas()
        self.curve = self.get_curve()
        self.decorate_canvas(self.new_canvas)
    ## End of __init__()
    
    
    #__________________________________________________________________________
    def get_old_canvas(self):
        '''
        Gets the canvas with the fit stored in the workspace.
        '''
        ## Build the name of the canvas depending on whether this is MC or data
        if 'data' in self.name:
            canvas_name = '_'.join(['c', self.name, 'data'])
        else:
            canvas_name = '_'.join(['c', self.name, 'fit'])
        
        ## Retrieve the canvas from the workspace
        return self.workspace.obj(canvas_name)
    ## End of get_old_canvas()
    
    
    #__________________________________________________________________________
    def get_new_canvas(self):
        '''
        Gets the new canvas for the EGM-11-001.
        '''
        ## Clone the old canvas:
        new_canvas = self.get_old_canvas().Clone(self.name + '_' + 'egm')
        
        ## Clean some of the canvas
        for primitive in new_canvas.GetListOfPrimitives():
            ## Remove all the latex
            if primitive.InheritsFrom('TLatex'):
                new_canvas.RecursiveRemove(primitive)
            ## Remove the frame title
            if 'frame' in primitive.GetName():
                primitive.SetTitle('')
        
        ## No Title and Grid
        new_canvas.SetGrid(0, 0)
        
        return new_canvas
    ## End of get_new_canvas()   
    
    #__________________________________________________________________________
    def decorate_canvas(self, canvas):
        '''
        Decorate the new canvas with the results of the fit and other labels.
        '''
        gpad_save = ROOT.gPad
        canvas.cd()
        
        phoScale = self.workspace.var('phoScale')
        phoRes = self.workspace.var('phoRes')
        
        ## Draw fit results:
        Latex([
            'Fit Parameters:',
            '#mu(E_{#gamma}) = %.2f #pm %.2f %%' % (
                phoScale.getVal(), phoScale.getError()
                ),
            '#sigma(E_{#gamma}) = %.2f #pm %.2f %%' % (
                phoRes.getVal(), phoRes.getError()
                ),
            ],
            position=(0.65, 0.8), textsize=22, rowheight=0.0825
            ).draw()
        
        ## CMS Preliminary:
        Latex(['CMS Preliminary 2011,  #sqrt{s} = 7 TeV'], 
              position=(0.17, 0.93), textsize=22).draw()
        

        labels = []
        ## Data or MC
        if 'data' in self.name:
            labels.append('Data, L = 4.89 fb^{-1}')
        else:
            labels.append('Simulation')
            
        ## EB or EE
        if 'EB' in self.name:
            labels.append('ECAL Barrel')
        else:
            labels.append('ECAL Endcaps')
        
        if 'highR9' in self.name:
            labels.append('R_{9} > 0.94')
            
        Latex(labels, position=(0.22, 0.8), textsize=22, 
              rowheight=0.0825
              ).draw()
        
        canvas.Modified()
        canvas.Update()
        
        gpad_save.cd()
    ## End of decorate_new_canvas()
        
    #__________________________________________________________________________
    def get_curve(self):
        '''
        Returns the curve of the model plotted on the old canvas.
        Preconditions: attribute old_canvas has already been defined.
        '''
        name = 'pm_Norm[mmgMass]_Range[plot]_NormRange[plot]'
        return self.old_canvas.GetListOfPrimitives().FindObject(name)
    ## End of get_curve
    
## End of EgmDecorator.


###############################################################################
def main():
    '''
    Tests the EgmDecorator class.
    '''
    print 'Entering EgmDecorator test...'
    global decorator
    decorator = EgmDecorator()
    decorator.old_canvas.Draw()
    decorator.new_canvas.Draw()
    print 'Exiting EgmDecorator test with success!'
## End of main()


if __name__ == '__main__':
    main()
    import user
