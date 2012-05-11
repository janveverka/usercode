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
    plot.new_canvas.Print(plot.name + '.eps')
    plot.new_canvas.Print(plot.name + '.C')
    plot.new_canvas.Print(plot.name + '.png')
    plots.append(plot)