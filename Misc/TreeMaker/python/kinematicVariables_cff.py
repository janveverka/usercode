'''
Defines a configuration fragment that can be used as a part of the
variables parameter of the TreeMaker describing basic kinematic variables 
of a generic candidate.

Jan Veverka, Caltech, 6 Aug 2012
'''

import FWCore.ParameterSet.Config as cms
import Misc.TreeMaker.tools as tools

varlist = 'pt eta phi mass charge vx vy vz'.split()
kinematicVariables = tools.get_variables(*varlist)

