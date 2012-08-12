'''
Dumps ASCII outputs for several collections.
USAGE: python dump.py | sh
Jan Veverka, Caltech, 11 August 2012
'''

import commands

#______________________________________________________________________________
def strip_lines(lines):
    '''
    Return a copy of lines with leading and trailing whitespace 
    stripped from each line.
    '''
    return '\n'.join([l.strip() for l in lines.split('\n')])
## End of strip_lines(...)


#______________________________________________________________________________
def dump(source='mc.root', directory = 'mmgAfterDR'):
    '''
    Dumps several variables of a TTree in a root file in an ASCII file
    '''
    
    ## Use a map (directory) -> (tree) to set the tree given a directory
    tree = {
        'muonsAfterVtx'  : 'muons'  ,
        'muonsAfterId'   : 'muons'  ,
        'photonsBeforeId': 'photons',
        'mmgAfterDR'     : 'mmg'    ,
        }[directory]
    
    ## Use a map (tree) -> (variables) to set the variables given a tree
    variables = {
        'muons'  : ('id.run:id.event:pt:eta:charge:isGlobal:isPF:normChi2:'
                    'nHit:nMatch:dxy:dz:nPixel:nLayer:chIso:nhIso:phIso:'
                    'combIso:rho:EA'),
        'photons': ('id.run:id.event:pt:eta:eleVeto:hoe:sihih:'
                    'chIso:nhIso:phIso:rho:chEA:nhEA:phEA'),
        'mmg'    : ('id.run:id.event:mass:mmMass:deltaR1:deltaR2:'
                    'mu1Pt:mu2Pt:phoPt:mu1Q:mu2Q')
        }[tree]
        
    ## Use a map (tree) -> (selection) to set the selection given a tree
    selection = {
        'muons'  : 'n > 0 & pt > 10 & abs(eta) < 2.4',
        'photons': 'n > 0',
        'mmg'    : 'n > 0',
        }[tree]
        
    ## Use a map (source) -> (shortsource) to set the shortsource
    shortsource = {'mc.root': 's12', 'data.root': 'r12'}[source]
    output = 'Caltech_sync2_%(shortsource)s_%(directory)s.txt' % locals()
    
    snippet = '''
    root -l -b <<EOF
    TFile *_file0 = TFile::Open("%(source)s")
    %(directory)s->cd()
    %(tree)s->SetScanField(0)
    %(tree)s->Scan("%(variables)s", "%(selection)s"); >%(output)s
    .q
    EOF

    ## Remove asterisks, empty lines, and the extra message at the end
    sed -i '{s/*//g; /entries/d; /^ *$/d}' %(output)s
    ''' % locals()
    
    snippet = strip_lines(snippet)

    print 'echo Dumping', directory, 'for', source, '...'
    print snippet
    #(exitstatus, outtext) = commands.getstatusoutput(snippet)
    #if  exitstatus != 0:
        #raise RuntimeError, '"%s" failed: "%s"!' % (snippet, outtext)
## End of dump()


#______________________________________________________________________________
def main():
    '''
    Main entry point to execution.
    '''
    dump('mc.root', 'muonsAfterVtx')
    #dump('mc.root', 'muonsAfterId')
    dump('mc.root', 'photonsBeforeId')
    dump('mc.root', 'mmgAfterDR')

    dump('data.root', 'muonsAfterVtx')
    #dump('data.root', 'muonsAfterId')
    dump('data.root', 'photonsBeforeId')
    dump('data.root', 'mmgAfterDR')
## End of main

if __name__ == '__main__':
    main()
    import user
