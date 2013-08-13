# -*- coding: utf-8 -*-
'''
FWLite/Daq/python/plot_rates.py - Plots the results of the Isilon test

USAGE: python -i plot_rates.py

Jan Veverka, MIT, jan.veverka@cern.ch
13 August 2013
'''

import os
import user
import pprint
import ROOT
import FWLite.Tools.canvases as canvases
import FWLite.Tools.cmsstyle as cmsstyle
from FWLite.Tools.legend import Legend

source_dir = os.path.join(os.environ['CMSSW_BASE'], 'src/FWLite/Daq/data')
filename = os.path.join(source_dir, 'rates_6x6_test1.dat')

tree = ROOT.TTree('isilon', 'isilon test data')
tree.ReadFile(filename, 'i/I:time/C:write/F:read:cpu')

graphs = []

#_______________________________________________________________________________
def main():
    '''
    Main entry point of execution.
    '''
    #plot_aggregate_throughput()
    #plot_outbound_throughput()
    #plot_inbound_throughput()
    plot_all_throughputs_overlaid()
    plot_cpu_usage()
    canvases.update()
## End of main()


#_______________________________________________________________________________
def plot_aggregate_throughput():
    canvases.next('Isilon_6x6_Aligned').SetGrid()
    tree.Draw('read + write:5*(i+1)', '', '')
    process_graph(name = 'aggregate',
                  ytitle = 'Aggregate Throughput (Gb/s)')
## End of plot_aggregate_throughput()


#_______________________________________________________________________________
def plot_inbound_throughput():
    canvases.next('Write').SetGrid()
    tree.Draw('write:5*(i+1)', '', '')
    process_graph(name='write',
                  ytitle='Write Throughput (Gb/s)',
                  color=ROOT.kRed)
## End of plot_inbound_throughput()


#_______________________________________________________________________________
def plot_outbound_throughput():
    canvases.next('Read').SetGrid()
    tree.Draw('read:5*(i+1)', '', '')
    process_graph(name = 'read',
                  ytitle = 'Read Throughput (Gb/s)',
                  color = ROOT.kBlue)
## End of plot_outbound_throughput()


#_______________________________________________________________________________
def plot_all_throughputs_overlaid():
    canvases.next('Overlaid').SetGrid()
    tree.Draw('read + write : 5 * (i + 1)')
    graph_total = customize(beautify(get_graph()),
                            ytitle = 'Cluster Filesystem Throughput (Gb/s)',
                            yrange = (0,11))
    tree.Draw('read : 5 * (i + 1)')
    graph_read = customize(beautify(get_graph()), color = ROOT.kBlue)
    tree.Draw('write : 5 * (i + 1)')
    graph_write = customize(beautify(get_graph()), color = ROOT.kRed)
    graph_total.Draw('alp')
    graph_read.Draw('lp')
    graph_write.Draw('lp')
    gstack = [graph_total, graph_write, graph_read]
    titles = ['Aggregate (%.1f #pm %.1f)' % get_mean_rms('read + write'),
              'Reading (%.1f #pm %.1f)' % get_mean_rms('read'),
              'Writing (%.1f #pm %.1f)' % get_mean_rms('write')]
    Legend(gstack, titles, position = (0.5, 0.9, 0.92, 0.7)).draw()
    graphs.extend(gstack)
## End of plot_all_throughputs_overlaid()


#_______________________________________________________________________________
def get_mean_rms(expression):
    '''
    Returns the mean and rms of the given expression.
    '''
    tree.Draw(expression + '>>htemp', '', 'goff')
    htemp = ROOT.gDirectory.Get('htemp')
    result = (htemp.GetMean(), htemp.GetRMS())
    htemp.Delete()
    return result
## End of get_mean_rms(expression)


#_______________________________________________________________________________
def plot_cpu_usage():
    canvases.next('CPU').SetGrid()
    tree.Draw('cpu:5*(i+1)', '', '')
    process_graph(name='cpu',
                  yrange=(0,100),
                  ytitle='Cluster CPU usage (%)')
## End of plot_cpu_usage()


#_______________________________________________________________________________
def process_graph(*args, **kwargs):
    '''
    Processes the graph plotted by the last TTree::Draw call.
    Customizes the given graph, draws it and appends it to a global list to
    prevent garbage collection
    '''
    graph = beautify(get_graph())
    customize(graph, *args, **kwargs)
    graph.Draw('apl')
    graphs.append(graph)
    return graph
## End of process_graph()


##______________________________________________________________________________
def get_graph():
    '''
    Returns the last graph created by a TTree::Draw call.
    '''
    return ROOT.gDirectory.FindObject('Graph').Clone()
## End of get_graph()


##______________________________________________________________________________
def beautify(graph):
    '''
    Beautifies the look and feel of the given graph.
    '''
    graph.SetMarkerStyle(20)
    graph.GetXaxis().SetTitle('Time since beginning (min)')
    graph.GetXaxis().SetRangeUser(0, 60)
    graph.GetYaxis().SetRangeUser(0, 10)
    graph.SetTitle('')
    return graph
## End of customize_graph(graph)


##______________________________________________________________________________
def customize(graph, name = None, yrange = None, ytitle = None, color = None):
    '''
    Customizes the look and feel of the given graph.
    '''
    if name:
        graph.SetName(name)
    if ytitle:
        graph.GetYaxis().SetTitle(ytitle)
    if yrange:
        graph.GetYaxis().SetRangeUser(*yrange)
    if color:
        paint(graph, color)
    return graph
## End of customize(graph)


##______________________________________________________________________________
def paint(graph, color):
    '''
    For the given graph, sets the color of the line and marker to the given one.
    '''
    graph.SetLineColor(color)
    graph.SetMarkerColor(color)
    return graph
## End of customize(graph)


##______________________________________________________________________________
if __name__ == '__main__':
    main()
    #pprint.pprint(graphs)
    canvases.make_plots(['png'])
    canvases.make_pdf_from_eps()
