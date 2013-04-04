'''
Facilitates the creation and use of multiple canvases.
'''

import commands
import os
import tempfile
import ROOT

canvases = []

xperiod = 30
yperiod = 5
wheight = 500
wwidth = 700

#______________________________________________________________________________
def next(name=None, title=None):
    update()
    i = len(ROOT.gROOT.GetListOfCanvases())
    wtopx = 20 * (i % xperiod)
    wtopy = 20 * (i % yperiod)
    
    if not title:
        title = name
        
    if name:
        if ROOT.gROOT.GetListOfCanvases().FindObject(name):
            i = 0
            while ROOT.gROOT.GetListOfCanvases().FindObject(name + '_%d' % i):
                i += 1
            name = name + '_%d' % i
            if title:
                title = title + ' %d' % i
        c1 = ROOT.TCanvas(name, title)
    else:
        c1 = ROOT.TCanvas()
        if title:
            c1.SetTitle(title)

    c1.SetWindowPosition(wtopx, wtopy)
    c1.SetWindowSize(wwidth, wheight)

    canvases.append(c1)
    return c1
## end of next()


#______________________________________________________________________________
def make_plots(extensions = ['png'], destination = 'plots'):
    if not os.path.isdir(destination):
        os.mkdir(destination)
    for c in canvases:
        if not c:
            continue
        for ext in extensions:
            filename = ''.join([c.GetName(), '.', ext])
            c.Print(os.path.join(destination, filename))
        ## end of loop over graphics_extensions
    ## end of loop over canvases
## end of make_plots()


#______________________________________________________________________________
def make_pdf_from_eps(destination = 'plots'):
    '''
    Creates an eps output and uses GhostScript-based ps2pdf command to convert
    it to a pdf.
    '''
    tmpdir = tempfile.mkdtemp()
    print 'Using', tmpdir, 'for temporary .eps files.'
    for c in canvases:
        if not c:
            continue
        epsname = os.path.join(tmpdir, c.GetName() + '.eps')
        pdfname = os.path.join(destination, c.GetName() + '.pdf')
        c.Print(epsname)
        command = '''ps2pdf -dEPSCrop %(epsname)s %(pdfname)s
                     rm %(epsname)s''' % locals()
        (exitstatus, outtext) = commands.getstatusoutput(command)
        if  exitstatus != 0:
            raise RuntimeError, '"%s" failed: "%s"!' % (command, outtext)
        ## end of loop over canvases
    os.rmdir(tmpdir)
## end of make_pdf_from_eps()


#______________________________________________________________________________
def update():
    for c in canvases:
        if c:
            c.Update()
    ## end of loop over canvases
## end of update()

