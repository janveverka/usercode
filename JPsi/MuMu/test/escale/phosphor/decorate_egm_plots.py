import commands
import JPsi.MuMu.escale.egmdecorator as decorator

#decorator.basepath = '/raid2/veverka/jobs/outputs/eg_paper_dr0p1'

plots = []
for name in '''
            egm_mc_EB_pt25to999_yyv3_highR9_evt1of4
            egm_mc_EB_pt25to999_yyv3_evt1of4
            egm_mc_EE_pt25to999_yyv3_evt1of4
            egm_data_EB_pt25to999_yyv3_highR9
            egm_data_EB_pt25to999_yyv3
            egm_data_EE_pt25to999_yyv3
            '''.split():
    plot = decorator.EgmDecorator(name)
    plot.new_canvas.Draw()
    outputname = plot.name.replace('egm', 'egm_phosphor').replace('_yyv3', '')
    plot.new_canvas.Print(outputname + '.eps')
    plot.new_canvas.Print(outputname + '.C')
    plot.new_canvas.Print(outputname + '.png')
    
    command = 'ps2pdf -dEPSCrop ' + outputname + '.eps'
    (exitstatus, outtext) = commands.getstatusoutput(command)
    if  exitstatus != 0:
        raise RuntimeError, '"%s" failed: "%s"!' % (command, outtext)
    
    plots.append(plot)
    
## Print the apparent peak positions
print 'Apparent peak positions (GeV)'
for plot in plots:
    print "%.3f   %s" % (plot.peak_position, plot.name)
