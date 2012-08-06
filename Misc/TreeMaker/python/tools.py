import FWCore.ParameterSet.Config as cms


#______________________________________________________________________________
def get_variables_from_map(name_expression_map):
    '''
    Takes a dictionary of {name1 -> expression1, name2 -> expression2} or 
    a list of pairs [(name1, expression1), (name2, expression2)]
    and builds a VPSet configuration fragment that can be used to
    extend the TreeMaker parameter variables.
    '''
    variables = cms.VPSet()
    items = []
    if type(name_expression_map) == dict:
        items.extend(name_expression_map.items())
    else:
        items.extend(name_expression_map)
    for name, expression in items:
        variables.append(cms.PSet(tag      = cms.untracked.string(name),
                                  quantity = cms.untracked.string(expression)))
    return variables
## End of get_variables_from_map


#______________________________________________________________________________
def get_variables(*args, **kwargs):
    '''
    Takes input arguments arg1, arg2, ..., and keyword arguments k1=a1, 
    k2=a2, ... etc., and builds a VPSet configuration fragment that 
    extends the parameter variables. The arguments arg1, arg2, ..., etc.
    are interpreted as both the variable tag and quantity. The key=value
    pairs of the keyword arguments k1=a1, k2=a2 etc. are interpreted
    as the variable tag and quantity, respectively:
    cms.VPSet(
        cms.PSet(tag      = cms.untracked.string(arg1), 
                 quantity = cms.untracked.string(arg1)),
        cms.PSet(tag      = cms.untracked.string(arg2), 
                 quantity = cms.untracked.string(arg2)),
        ...
        cms.PSet(tag      = cms.untracked.string(k1), 
                 quantity = cms.untracked.string(a1)),
        cms.PSet(tag      = cms.untracked.string(k2), 
                 quantity = cms.untracked.string(a2)),
        ...
        )
    '''
    argmap = [(arg, arg) for arg in args]
    
    return get_variables_from_map(argmap + kwargs.items())
## End of get_variables(..)
