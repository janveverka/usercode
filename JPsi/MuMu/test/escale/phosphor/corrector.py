'''
Dumps snippet of code for the PhosphoCorrectorFunctor
That gives the results of the scale and resolution
measurements.
'''

##------------------------------------------------------------------------------
def main():
    '''
    Main entry point of execution.  Writes a snippet of c++
    code to STDOUT.
    '''
    dump_scale_snippet();
    dump_resolution_snippet();
## End of main().


##------------------------------------------------------------------------------
def dump_scale_snippet():
    '''
    Writes a snippet of code to STDIN that inicializes the vector scales
    with the measured values of photon energy scale in %.
    '''
    print header('scale')
    ## Loop over categories
    category = 'kMonteCarloBarrelEt12to15'
    value = 0.45
    print '  scales[%s] = %.2f;' % (category, value)
## End of dump_scale_snippet()


##------------------------------------------------------------------------------
def dump_resolution_snippet():
    '''
    Writes a snippet of code to STDIN that inicializes the vector resolutions
    with the measured values of resolution in %.
    '''
    print header('resolution')
    loop_over_categories('resolution')
    ## Loop over the categories
    category = 'kMonteCarloBarrelEt12to15'
    value = 5.32
    print '  resolutions[%s] = %.2f;' % (category, value)

    lines = loop_over_categories('resolution')
    indent(lines, '  ')
    print '\n'.join(lines)
## End of dump_scale_snippet()


##------------------------------------------------------------------------------
def header(varname):
    '''
    Returns the header for both the scale and resolution.
    '''
    return ('  /// Measured values of {x} in (%)\n'
            '  std::vector<double> {x}s(kNumCategories);').format(x=varname)
## End of print_header()


##------------------------------------------------------------------------------
def loop_over_categories(varname):
    '''
    Loops over the photon categories and provides a line for each. Returns
    a string of the lines.
    '''
    if varname == 'scale':
        default_value = 0.0
    else:
        default_value = 1.0

    categories = get_categories()

    lines = []
    for source, subdet, pt in categories:
        name = 'k' + ''.join([source, subdet, pt])
        lines.append('{x}s[{c}] = {v};'.format(x=varname, c=name,
                                               v=default_value))
        if source == 'RealData2011B':
            lines.append('')
    return lines
## End of loop_over_categories.


##------------------------------------------------------------------------------
def get_categories():
    '''
    Returns a list of strings that are the category enumearation variables.
    '''
    categories = []
    for subdet in 'Barrel Endcaps'.split():
        for pt in '12to15 15to20'.split():
            for data in 'MonteCarlo RealData2011A RealData2011B'.split():
                categories.append((data, subdet, 'Et' + pt))
    return categories
## End of get_categories


##------------------------------------------------------------------------------
def indent(lines, prefix):
    '''
    Indents lines with the given prefix.
    '''
    for i, l in enumerate(lines):
        lines[i] = prefix + l
## End of indent.


##------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
    import user
