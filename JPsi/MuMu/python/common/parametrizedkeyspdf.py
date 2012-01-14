"""
parametrizedkeyspdf - The Parametrized KEYS PDF.

This module defines the class ParametrizedKeysPdf which implements a
RooAbsPdf resulting from linear parametrization of the observable
of a RooKeysPdf.

The shape of the PDF is taken from the RooKeysPdf trained on the given
data.  The parametrization introduces dependence on the location
and scale x -> (x-m)/s.  Here, the location and scale parameters are named
m and s.  They are named `mode' and `width' in the code and they
bear the meaning of the mode and effective sigma of the shape.
The effective sigma is defined at the shortes interval containing
68% of the total volume of the observable.  This corresponds to
2*sigma of the normal distribution.

Jan Veverka, Caltech, 17 December 2011
"""

import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.tools as tools


##------------------------------------------------------------------------------
class ParametrizedKeysPdf(ROOT.RooKeysPdf):
    'Introduce location and scale parameters.'

    def __init__(self, name, title, x, mode, width, data,
                 mirror=ROOT.RooKeysPdf.NoMirror, rho=1., forcerange=True):

        self.shape = ROOT.RooKeysPdf(name + '_shape', title + ' shape', x, data,
                                     mirror, rho)
        self.shapewidth = tools.pdf_effsigma(self.shape, x)
        self.shapewidthvar = ROOT.RooRealVar(
            name + '_shapewidthvar',
            name + '_shapewidthvar',
            self.shapewidth
            )
        self.shapemode = tools.pdf_mode(self.shape, x)
        self.shapemodevar = ROOT.RooRealVar(
            name + '_shapemodevar',
            name + '_shapemodevar',
            self.shapemode
            )
        if self.shapewidth <= 0.:
            raise RuntimeError, ('Illegal value of pdf width: %f.' %
                                 self.shapewidth)
        ## Define the transformation of x that introduces the dependence on the
        ## mode and width
        self.xtransform = ROOT.RooFormulaVar(
            x.GetName() + '_linearTransform_' + name,
            x.GetTitle() + ' Linear Transform for Substitution in ' + title,
            "{shapemode} + ({x} - {mode}) * {shapewidth} / {width}".format(
                x=x.GetName(),
                mode=mode.GetName(),
                width=width.GetName(),
                shapemode=self.shapemodevar.GetName(),
                shapewidth=self.shapewidthvar.GetName()
                ),
            ROOT.RooArgList(x, mode, width, self.shapemodevar,
                            self.shapewidthvar)
            )

        ## TODO: Use RooLinearVar for the xtransform along the lines below
        ## Unfortunately, the implementation below doesn't seem to work.
        ## self.xslope = ROOT.RooFormulaVar(
        ##     x.GetName() + '_slope_' + name,
        ##     x.GetTitle() + ' Slope in Linear Transform',
        ##     "{shapewidth} / {width}".format(
        ##         shapewidth=self.shapewidth, width=width.GetName()
        ##         ),
        ##     ROOT.RooArgList(width)
        ##     )
        ## self.xoffset = ROOT.RooFormulaVar(
        ##     x.GetName() + '_offset_' + name,
        ##     x.GetTitle() + ' Offset in Linear Transform',
        ##     "{shapemode} - {mode} * {shapewidth} / {width}".format(
        ##         mode=mode.GetName(), width=width.GetName(), 
        ##         shapemode=self.shapemode, shapewidth=self.shapewidth,
        ##         ),
        ##     ROOT.RooArgList(mode, width)
        ##     )
        ## self.xtransform = ROOT.RooLinearVar(
        ##     x.GetName() + '_linearTransform_' + name,
        ##     x.GetTitle() + ' Linear Transform for Substitution in ' + title,
        ##     x, self.xslope, self.xoffset, x.getUnit()
        ##     )

        if forcerange:
            ## Restrict the allowed tranformed values to the range where the
            ## PDF was trained.
            ## TODO: Use a custom compiled class for this instead of the
            ## interpreted RooFormulaVar.
            self.xtransform_fullrange = self.xtransform
            self.xtransform = ROOT.RooFormulaVar(
                x.GetName() + '_rangedLinearTransform_' + name,
                (x.GetTitle() + ' Lin. Transform constrained to a Range in ' +
                 title),
                ('{lo} * ({x} <= {lo}) + '
                 '{x} * ({lo} < {x} & {x} < {hi}) + '
                 '{hi} * ({hi} <= {x})').format(x=self.xtransform.GetName(),
                                                lo=x.getMin(),
                                                hi=x.getMax()),
                ROOT.RooArgList(self.xtransform_fullrange)
                )

        self.customizer = ROOT.RooCustomizer(self.shape, 'transform')
        self.customizer.replaceArg(x, self.xtransform)

        ROOT.RooKeysPdf.__init__(self, self.customizer.build())
        self.SetName(name)
        self.SetTitle(title)
    ## end of __init__
## end of ParameterizedKeysPdf
