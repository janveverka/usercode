'''
This example demonstrates the use of the module FWLite.Tools.canvases.
It produces a couple of canvases and writes them as graphics files
in the directory plots under cwd, see
http://www.hep.caltech.edu/~veverka/plots/2013/13-04-04/plots/

Jan Veverka, Caltech, 4 April 2013

USAGE: python -i canvases_example.py
'''
import pprint
import ROOT
import FWLite.Tools.canvases as canvases


#______________________________________________________________________________
def main():
    '''
    Main entry point of execution.
    '''
    hist = get_gaussian_histogram()
    make_canvases(hist)
    make_more_canvases(hist)

    ## Make output graphics in different formats using ROOT for the conversions
    canvases.make_plots('png C root eps'.split())

    ## Store canvases as pdf by creating eps and then using ps2pdf to convert
    ## them.
    canvases.make_pdf_from_eps()

    ## The module holds references to the created canvases.
    ## Note that they did not get killed even though we do not
    ## explicitly keep references to them.  They still show up on the screen.
    ## You can access them like this:
    print 'List of canvases:'
    pprint.pprint(canvases.canvases)
## End of main()


#______________________________________________________________________________
def get_gaussian_histogram(entries=1000, mean=0, sigma=1):
    '''
    Returns a histogram filled with normally distributed entries with the
    given number of entries, mean and sigma.
    '''
    hist = ROOT.TH1F('gauss', 'Gauss', 100, -5*sigma, 5*sigma)
    for i in range(entries):
        hist.Fill(ROOT.gRandom.Gaus(mean, sigma))
    hist.SetLineWidth(3)
    return hist
## End of get_gaussian_histogram


#______________________________________________________________________________
def make_canvases(hist):
    '''
    Creates a couple of example canvases and draws the given histogram on them.
    '''
    ## The function next(name=None, title=None) creates a new canvas
    canvases.next(name='gauss', title='Normal Distribution')
    hist.DrawCopy()

    ## Overloaded canvas names are automatically modified by appending "_<number>"
    ## Both name and title are optional. The title defaults to name if not given.
    canvases.next('gauss')
    hist.Draw()

    ## next returns the newly created histogram, so that you can customize it.
    canvases.next('gauss_logy').SetLogy()
    hist.DrawCopy()

    ## Or you can name the new canvas to use it later.
    canvas = canvases.next('gauss_logy_grid')
    canvas.SetLogy()
    canvas.SetGrid()
    hist.DrawCopy()

    ## You can customize the default canvas window width and height
    canvases.wwidth = 600
    canvases.wheight = 600
    canvases.next('gauss_square')
    hist.DrawCopy()
    
    ## Note that the canvas windows are staggered on the screen in x and y
    ## with defualt periods of xperiod=30 in x and yperiod=5 in y.  This
    ## is the 6th canvas, first in this yperiod, so it will be on the
    ## top of the screen again.
    canvases.next('gauss_topscreen')
    hist.DrawCopy()
## End of make_more_canvases()


#______________________________________________________________________________
def make_more_canvases(hist):    
    '''
    Creates more of example canvases and draws the given histogram on them.
    '''
    
    ## You can customize this behavior like this:
    canvases.yperiod = 1
    ## Now, all the canvases will be rendered at the top of the screen
    ## since they all start in the y-period
    canvases.next(title='Red at the top of the display')
    hist.SetLineColor(ROOT.kRed)  ## Just for fun
    hist.DrawCopy()
    
    ## The same for the position of the canvas window on the display along
    ## the x-direction (left-right)
    canvases.xperiod = len(canvases.canvases)
    canvases.next(title='Blue at the left side of the display')
    hist.SetLineColor(ROOT.kBlue)  ## Just for fun
    hist.DrawCopy()
## End of make_more_canvases()


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
