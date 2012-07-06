import ROOT         # allows access to ROOT colors (e.g. ROOT.kRed)

##############################################################################
######## About Config Files ##################################################

## This file can be generated by running 'rootplot --config'

## Options are loaded in the following order:
##   1. from the command line
##   2. from the default configuration file
##   3. from ~/.rootplotrc
##   4. from configuration files specified on the command-line
## This leads to two major points worth understanding:
##   1. you may delete any lines you like in this file and they will still
##      be loaded correctly from the default
##   2. values specified here will superceed the same options from the
##      command-line
## Therefore, you could set, for example, 'xerr = True' in this file,
## and x-errorbars will always be drawn, regardless of whether '--xerr' is
## given on the command-line or not.  You can do this with any of the command-
## line options, but note that dashes are translated to underscores, so
## '--ratio-split=1' becomes 'ratio_split = 1'.

## Most global style options like default line widths can be set through
## a rootlogon.C, as described at:
##    http://root.cern.ch/drupal/content/how-create-or-modify-style

##############################################################################
######## Specifying Files and Targets ########################################

## You can specify the files to run on through the 'filenames' variable rather
## than entering them at the command-line, for example:
filenames = ['vecbos_official.root', 'vecbos_private.root']

## Likewise, you can specify target histograms or directories here rather than 
## on the command-line, for example:
# targets = ['Muons', 'Pileup', 'Photons']

## You might also want to specify fancy labels for the legend here rather 
## than on the command-line:
legend_entries = [r'Official', r'Private']

##############################################################################
######## Different Options for Different Targets #############################

## Leave these lists empty to have them automatically filled according to the
## command-line options.  Any list that is filled must be at least as long
## as the number of targets or it will throw an error.

line_colors = []                # normally filled by options.colors
fill_colors = []                # normally filled by options.colors
marker_colors = []              # normally filled by options.colors
marker_sizes = []         # in pixels
line_styles = []          # 1 (solid), 2 (dashed), 4 (dashdot), 3 (dotted), ...
fill_styles = []          # 0 (hollow), 1001 (solid), 2001 (hatched), ...
draw_commands = []        # a TH1::Draw option, include 'stack' to make stacked

##############################################################################
######## Global Style Options ################################################

## Colors can be specified as (r, g, b) tuples (with range 0. to 1. or range
## 0 to 255), or ROOT color constants (ROOT.kBlue or 600)

colors = [
    ## a default set of contrasting colors the author happens to like
    # ( 82, 124, 219), # blue
    # (212,  58, 143), # red
    (  0, 122, 255), # JV blue
    (225,   7,  40), # JV red      
    (255, 218,  33), # JV yellow
    (231, 139,  77), # orange
    (145,  83, 207), # purple
    # (114, 173, 117), # green
    ( 67,  77,  83), # dark grey
    ]

## Used when --marker_styles is specified; more info available at:
## http://root.cern.ch/root/html/TAttMarker.html
marker_styles = [
     4, # circle
    25, # square
    26, # triangle
     5, # x
    30, # five-pointed star
    27, # diamond
    28, # cross
     3, # asterisk
    ]

#### Styles for --data
data = 2
data_linestyle = 1
data_color = (0,0,0)      # black
# mc_color = (50, 150, 150) # used when there are exactly 2 targets; set to
mc_color = (  0, 122, 255)
                          # None to pick up the normal color
# data_marker = 4           # marker style (circle)
data_marker = 'o'           # mpl marker style (circle)

#### Settings for --ratio-split or --efficiency-split
ratio_split = True
ratio_max  = 2.0
ratio_min  = 0.0
ratio_logy = False
ratio_fraction = 0.3  # Fraction of the canvas that bottom plot occupies
ratio_label = 'Private / Official' # Label for the bottom plot
ratio_grid = True
efficiency_label = 'Efficiency vs. %(ratio_file)s'

#### Titles produced by --area-normalize and --normalize
area_normalized_title = 'Fraction of Events in Bin'
#target_normalized_title = 'Events Normalized to %(norm_file)s'
target_normalized_title = '%(ylabel)s'

#### Overflow and underflow text labels
overflow_text = ' Overflow'
underflow_text = ' Underflow'

#### Define how much headroom to add to the plot
top_padding_factor = 1.2
top_padding_factor_log = 5.    # used when --logy is set

#### Plotting options based on histogram names
## Apply options to histograms whose names match regular expressions
## The tuples are of the form (option_name, value_to_apply, list_of_regexs)
## ex: to rebin by 4 all histograms containing 'pt' or starting with 'eta':
##    ('rebin', 4, ['.*pt.*', 'eta.*'])
options_by_histname = [
    ('area_normalize', True, []),
                       ]

#### Legend
legend_width = 0.38        # Fraction of canvas width
legend_entry_height = 0.05 # Fraction of canvas height
max_legend_height = 0.4    # Fraction of canvas height
legend_left_bound = 0.20   # For left justification
legend_right_bound = 0.95  # For right justification
legend_upper_bound = 0.91  # For top justification
legend_lower_bound = 0.15  # For bottom justification
legend_codes = { 1 : 'upper right',
                 2 : 'upper left',
                 3 : 'lower left',
                 4 : 'lower right',
                 5 : 'right',
                 6 : 'center left',
                 7 : 'center right',
                 8 : 'lower center',
                 9 : 'upper center',
                10 : 'center',
                }

#### Page numbers
numbering_size_root = 0.03  # Fraction of canvas width
numbering_align_root = 33   # Right-top adjusted
numbering_x_root = 0.97     # Fraction of canvas width
numbering_y_root = 0.985    # Fraction of canvas height

#### Draw style for TGraph
draw_graph = 'ap'

#### This code snippet will be executed after the histograms have all
#### been drawn, allowing you to add decorations to the canvas
decoration_root = '''
## Draw a line to indicate a cut
#line = ROOT.TLine(5.,0.,5.,9.e9)
#line.Draw()
## Add a caption
#tt = ROOT.TText()
#tt.DrawTextNDC(0.6, 0.15, "CMS Preliminary")
'''

##############################################################################
######## From the Command Line ###############################################

normalize = 2 
ymin = 0.0 
grid = True


##############################################################################
######## HTML Output #########################################################

#### Number of columns for images in HTML output
ncolumns_html = 2

#### Provide a template for the html index files
html_template=r'''
    <html>
    <head>
    <link rel='shortcut icon' href='http://packages.python.org/rootplot/_static/rootplot.ico'>
    <link href='http://fonts.googleapis.com/css?family=Yanone+Kaffeesatz:bold' rel='stylesheet' type='text/css'>
    <style type='text/css'>
        body { padding: 10px; font-family:Arial, Helvetica, sans-serif;
               font-size:15px; color:#FFF; font-size: large; 
               background-image: url(
                   'http://packages.python.org/rootplot/_static/tile.jpg');}
        img    { border: solid black 1px; margin:10px; }
        object { border: solid black 1px; margin:10px; }
        h1   { text-shadow: 2px 2px 2px #000;
               font-size:105px; color:#fff; border-bottom: solid black 1px;
               font-size: 300%%; font-family: 'Yanone Kaffeesatz'}
        a, a:active, a:visited {
               color:#FADA00; text-decoration:none; }
        a:hover{ color:#FFFF00; text-decoration:none;
                 text-shadow: 0px 0px 5px #fff; }
    </style>
    <title>%(path)s</title>
    </head>
    <body>
    <a style="" href="http://packages.python.org/rootplot/"><img style="position: absolute; top:10 px; right: 10px; border: 0px" src="http://packages.python.org/rootplot/_static/rootplot-logo.png"></a>
    <h1>Navigation</h1>
      %(back_nav)s
      <ul>
          %(forward_nav)s
      </ul>
    <h1>Images</h1>
    %(plots)s
    <p style='font-size: x-small; text-align: center;'>
      <a href='http://www.greepit.com/resume-template/resume.htm'>
        Based on a template by Sarfraz Shoukat</a></p>
    </body>
    </html>
'''
