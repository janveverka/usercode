import os
import socket
import JPsi.MuMu.common.clusterCorrections as clusterCorrs

from JPsi.MuMu.common.basicRoot import *

_hostname = socket.gethostname()
if (_hostname == 't3-susy.ultralight.org' or 
    ('compute-' in _hostname and '.local' in _hostname)) :
    ## Path for the t3-susy
    _path = '/raid2/veverka/esTrees/'
elif _hostname == 'nbcitjv':
    ## Path for Jan's Dell Inspiron 6000 laptop
    _path = '/home/veverka/Work/data/esTrees'
elif (_hostname == 'eee.home' or
      _hostname == 'Jan-Veverkas-MacBook-Pro.local' or
      (_hostname[:8] == 'pb-d-128' and _hostname[-8:] == '.cern.ch')):
    ## Path for Jan's MacBook Pro
    _path = '/Users/veverka/Work/Data/esTrees'
else:
    raise RuntimeError, "Unknown hostname `%s'" % _hostname

_files = {}
_files['v1'] = {
    'data' : '''
            esTree_ZMu-May10ReReco-42X-v3_V1.root
            esTree_PromptReco-v4_FNAL_42X-v3_V1.root
            '''.split(),
    'z' : ['esTree_DYToMuMu_pythia6_AOD-42X-v4_V1.root'],
}

_files['v2'] = {
    ## pmvTree format
    'data' : '''
            esTree_ZMu-May10ReReco-42X-v3_V2.root
            esTree_PromptReco-v4_FNAL_42X-v3_V2.root
            '''.split(),
    'z' : ['esTree_DYToMuMu_pythia6_AOD-42X-v4_V2.root'],
    'w'    : ['esTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V2.root'],
    'tt'   : ['esTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V2.root'],
    'qcd'  : ['esTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V2.root'],
}

_files['v3'] = {
    # Results with 715 / pb of June 17 up to run 166861
    'data' : [ 'esTree_V3_ZMu-May10ReReco-42X-v3.root',
               'esTree-V3_PromptReco-v4_FNAL_42X-v3.root', ],
    'z'    : [ 'esTree_V3_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v4'] = {
    'data' : '''
             esTree_V4_Run2010B-ZMu-Apr21ReReco-v1.root
             esTree_V4_PromptReco-v4_FNAL_42X-v3.root
             esTree_V4_ZMu-May10ReReco-42X-v3.root
             '''.split(),
    'z'    : [ 'esTree_V4_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v5'] = {
    'z'    : [ 'esTree_V5_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v6'] = {
    'z'    : [ 'esTree_V6_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v7'] = {
    'data' : '''
             esTree_V7_Run2010B-ZMu-Apr21ReReco-v1.root
             esTree_V7_ZMu-May10ReReco-42X-v3.root
             esTree_V7_PromptReco-v4_FNAL_42X-v3.root
             '''.split(),
    'z'    : [ 'esTree_V7_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v8'] = {
    'data' : '''
             esTree_V8_05Jul2011ReReco-ECAL-v1_condor_Dimuon_RECO-42X-v9_test.root
             esTree_V8_DoubleMu_Dimuon_AOD_Aug5rereco.root
             esTree_V8_DoubleMu_Dimuon_AOD_Prompt_v6.root
             '''.split(),
    'z_test'    : '''
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job5_of40.root
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job16_of40.root
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job20_of40.root
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job31_of40.root
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job39_of40.root
             '''.split(),
    'z'    : '''
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root
             '''.split(),
}

_files['v10'] = {
    'data' : '''
             esTree_V10_DoubleMu_Run2011A-May10ReReco-v1_glite_Dimuon_RECO-42X-v9.root
             esTree_V10_DoubleMu_Run2011A-PromptReco-v4_glite_Dimuon_RECO-42X-v9.root
             '''.split(),
    'z'    : [ 'esTree_V10_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root' ]
}

_files['v11'] = {
    'data' : '''
             esTree_V11_DoubleMu_Run2011A-May10ReReco-v1_glite_Dimuon_RECO-42X-v9.root
             esTree_V11_DoubleMu_Run2011A-PromptReco-v4_glite_Dimuon_RECO-42X-v9.root
             '''.split(),
    'z'    : [ 'esTree_V11_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root' ]
}

## Full 2011 data as used by the Vgamma AN-11-251
_files['v12'] = {
    'data': '''
            esTree_V12_DoubleMu_Run2011A-May10ReReco-v1_glite_Dimuon_RECO-42X-v9.root
            esTree_V12_DoubleMu_Run2011A-PromptReco-v4_glite_Dimuon_RECO-42X-v9.root
            esTree_V12_DoubleMu_Run2011A-05Aug2011-v1_glite_Dimuon_AOD-42X-v9.root
            esTree_V12_DoubleMu_Run2011A-03Oct2011-v1_condor_Dimuon_AOD-42X-v9.root
            esTree_V12_DoubleMu_Run2011B-PromptReco-v1_condor_Dimuon_AOD-42X-v9.root
            '''.split(),
    '2011A': '''
            esTree_V12_DoubleMu_Run2011A-May10ReReco-v1_glite_Dimuon_RECO-42X-v9.root
            esTree_V12_DoubleMu_Run2011A-PromptReco-v4_glite_Dimuon_RECO-42X-v9.root
            esTree_V12_DoubleMu_Run2011A-05Aug2011-v1_glite_Dimuon_AOD-42X-v9.root
            esTree_V12_DoubleMu_Run2011A-03Oct2011-v1_condor_Dimuon_AOD-42X-v9.root
            '''.split(),
    '2011B': '''
            esTree_V12_DoubleMu_Run2011B-PromptReco-v1_condor_Dimuon_AOD-42X-v9.root
            '''.split(),
    }

## Yong's trees with the default CMSSW photon cluster corrections
_files['yyv1'] = {
    'data': [('testSelectionfsr.v3.DoubleMuRun2011AB16Jan2012v1AOD.'
              'muid2.phtid1.phtcorr360.datapu0.mcpu0.r1to129.root')],
    'z'   : [('testSelectionfsr.v3.DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia'
              'Fall11-PU_S6_START42_V14B-v1AODSIM.'
              'muid2.phtid1.phtcorr360.datapu6.mcpu1.r1to50.root')],
    }
    

## Yong's trees with the Caltech photon regression
_files['yyv2'] = {
    'data': [('testSelectionfsr.v3.DoubleMuRun2011AB16Jan2012v1AOD.'
              'muid2.phtid1.phtcorr360.datapu0.mcpu0.r1to129.root')],
    'z'   : [('testSelectionfsr.v3.DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia'
              'Fall11-PU_S6_START42_V14B-v1AODSIM.'
              'muid2.phtid1.phtcorr360.datapu6.mcpu1.r1to50.root')],
    }
    

## Yong's trees with the Hgg photon regression v2
_files['yyv3'] = {
    'data': [('testSelectionfsr.v3.DoubleMuRun2011AB16Jan2012v1AOD.'
              'muid2.phtid1.phtcorr96.datapu0.mcpu0.r1to129.root')],
    'z'   : [('testSelectionfsr.v3.DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia'
              'Fall11-PU_S6_START42_V14B-v1AODSIM.'
              'muid2.phtid1.phtcorr96.datapu6.mcpu1.r1to50.root')],
    }
    
_files['v13'] = {
    'z' : [('esTree_V13_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_'
            'Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb_'
            'batch1of2.root'),
           ('esTree_V13_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_'
            'Fall11-PU_S6_START42_V14B-v1_condor_Dimuon_AOD-42X-v10_10Feb_'
            'batch2of2.root')]
    }

_treeNames = {
    'v1' : 'tree/es',
    'v2' : 'pmvTree/pmv',
    'v3' : 'tree/es',
    'v4' : 'tree/pmv',
    'v5' : 'tree/pmv',
    'v6' : 'tree/pmv',
    'v7' : 'tree/pmv',
    'v8' : 'tree/pmv',
    'v10' : 'tree/pmv',
    'v11' : 'tree/pmv',
    'v12' : 'tree/pmv',
    'v13' : 'tree/pmv',
    'yyv1' : 'Analysis',
    'yyv2' : 'Analysis',    
    'yyv3' : 'Analysis',    
}


def getChains(version='v4'):
    chains = {}
    for name, flist in _files[version].items():
        chains[name] = TChain( _treeNames[version] )
        for f in flist:
            print "Loading ", name, ":", f
            chains[name].Add( os.path.join(_path, f) )

    if version in 'yyv1 yyv2 yyv3'.split():
        ## On each line corresponding to a list item, 
        ## 1st is esTree name, 2nd is YY tree name in Yong's trees.
        es_to_yy_name_map = '''mmMass          mm 
                               phoEta          gameta
                               phoPhi          gamphi
                               phoGenE         gametrue
                               phoIsEB         abs(gamsceta)<1.5
                               phoR9           gamr9
                               mu1Pt           mpt[0]
                               mu2Pt           mpt[1]
                               mu1Eta          meta[0]
                               mu2Eta          meta[1]
                               mu1Phi          mphi[0]
                               mu2Phi          mphi[1]
                               pileup.weight   evtweight
                               isFSR           gametrue>0'''.split('\n')
        if version == 'yyv1':
            ## Use the default CMSSW cluster corrections
            es_to_yy_name_map.extend(
                '''mmgMass         mmg
                  phoPt           gamenergy/cosh(gameta)'''.split('\n')
                  )
        elif version in 'yyv2 yyv3'.split():
            ## Use the regression cluster corrections
            es_to_yy_name_map.extend(
                '''mmgMass         mmgcorr
                   phoPt           gamscenergycorr/cosh(gameta)'''.split('\n')
                   )
        ## Set aliases for Yong's trees so that one can use the same names
        ## as in esTrees
        for ch in chains.values():
            for name_pair in es_to_yy_name_map:
                if len(name_pair.strip()) < 3:
                    raise RuntimeError, 'Illegal name pair %s' % name_pair
                es_name, yy_name = name_pair.split()
                ch.SetAlias(es_name, yy_name)
    
    ## Set aliases
    for ch in chains.values():
        ch.SetAlias( 'phoE', 'phoPt * cosh(phoEta)' )
        ch.SetAlias( 'brem', 'scPhiWidth / scEtaWidth' )
        ch.SetAlias( 'rawE', 'scRawE + preshowerE' )
        ch.SetAlias( 'corrE', 'phoCrackCorr * corrE(rawE, scEta, brem)' )
        ch.SetAlias( 'newCorrE', 'phoCrackCorr * newCorrE(rawE, scEta, brem)' )
        ch.SetAlias( 'corrKRatio', 'phoE * kRatio / corrE' )
        ch.SetAlias( 'newCorrKRatio', 'phoE * kRatio / newCorrE' )
        ch.SetAlias('m1gMass',
                    'sqrt(2*mu1Pt*phoPt*(cosh(mu1Eta - phoEta) - cos(mu1Phi - phoPhi)))')
        ch.SetAlias('m2gMass',
                    'sqrt(2*mu2Pt*phoPt*(cosh(mu2Eta - phoEta) - cos(mu2Phi - phoPhi)))')
        ch.SetAlias('mmGenMass',
                    'sqrt(2*mu1GenPt*mu2GenPt*(cosh(mu1GenEta - mu2GenEta) - '
                                              'cos(mu1GenPhi - mu2GenPhi)))')
        ch.SetAlias('mmgGenMass',
                    'threeBodyMass(mu1GenPt, mu1GenEta, mu1GenPhi, 0.106, '
                                  'mu2GenPt, mu2GenEta, mu2GenPhi, 0.106, '
                                  'phoGenEt, phoGenEta, phoGenPhi, 0)')
                    ## 'sqrt(2*mu1GenPt*mu2GenPt*(cosh(mu1GenEta - mu2GenEta) - '
                    ##                           'cos( mu1GenPhi - mu2GenPhi)) + '
                    ##      '2*mu1GenPt*phoGenEt*(cosh(mu1GenEta - phoGenEta) - '
                    ##                           'cos( mu1GenPhi - phoGenPhi)) + '
                    ##      '2*mu2GenPt*phoGenEt*(cosh(mu2GenEta - phoGenEta) - '
                    ##                           'cos( mu2GenPhi - phoGenPhi)))')
        ch.SetAlias('mmgMassPhoGenE',
                    'threeBodyMass(mu1Pt, mu1Eta, mu1Phi, 0.106, '
                                  'mu2Pt, mu2Eta, mu2Phi, 0.106, '
                                  'phoGenE * phoPt / phoE, phoEta, phoPhi, 0)')
        ch.SetAlias('mmgMassPhoGenEMuGenPt',
                    'threeBodyMass(mu1GenPt, mu1Eta, mu1Phi, 0.106,'
                                  'mu2GenPt, mu2Eta, mu2Phi, 0.106,'
                                  'phoGenE * phoPt / phoE, phoEta, phoPhi, 0)')
        ch.SetAlias('phoERes', 'phoE/phoGenE - 1') 

    return chains

if __name__ == "__main__":
    import user

