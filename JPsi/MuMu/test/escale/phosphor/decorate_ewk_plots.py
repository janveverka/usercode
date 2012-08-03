import commands
import JPsi.MuMu.escale.vgammadecorator as decorator

plots = []
for name in '''
            sge_data_EB_pt15to20_v13
            '''.split():
    plot = decorator.Decorator(name)
    plot.new_canvas.Draw()
    outputname = plot.name.replace('sge', 'PHOSPHOR_Fit').replace('_v13', '')
    plot.new_canvas.Print(outputname + '.eps')
    plot.new_canvas.Print(outputname + '.C')
    plot.new_canvas.Print(outputname + '.png')
    
    command = 'ps2pdf -dEPSCrop ' + outputname + '.eps'
    (exitstatus, outtext) = commands.getstatusoutput(command)
    if  exitstatus != 0:
        raise RuntimeError, '"%s" failed: "%s"!' % (command, outtext)
    
    plots.append(plot)
