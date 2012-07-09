'''
Provides core tools facilitating analysis on the grid.
Jan Veverka, Caltech, 9 July 2012
'''

#______________________________________________________________________________
def expand_crab_job_list(job_list):
    '''
    Takes a string specifying a list of jobs in CRAB notation, expands
    it to a python's list of integers and returns that list.
    Example:
    job_list = "1-35,42,153-160"
    retuns: [1, 2, 3, ..., 35, 42, 153, 154, 155, ..., 160]
    '''
    new_job_list = []
    ## Loop over the ranges (for example 3 items: "1-35", "42", and "153-160")
    for job_range in job_list.split(','):
        try:
            ## Check if there is more than one item in this range:
            if '-' not in job_range:
                ## This is a single job, e.g. "42", include it directly:
                new_job_list.append(int(job_range))
                continue
            else:
                ## This is a range of jobs. Extract the first
                ## and last jobs, e.g. 1 and 35 for "1-35".
                first_job, last_job = map(int, job_range.split('-'))
                ## Loop over all jobs in the range, e.g. 1, 2, ..., 35:
                for job in range(first_job, last_job + 1):
                    new_job_list.append(job)
        except ValueError:
            raise RuntimeError(
                "Don't understand %s in %s!" % (job_range, job_list)
                )
    return new_job_list
## End of expand_crab_job_list(...)


#______________________________________________________________________________
def test_expand_crab_job_list(verbosity = 0):
    '''
    Tests the expand_crab_job_list() function.
    '''
    list_in = '1-35,42,153-160'
    list_should = range(1,36) + [42] + range(153, 161)
    list_out = expand_crab_job_list(list_in)

    if verbosity > 0:
        print 'expand_crab_job_list(%s):' % list_in, list_out

    if (not len(list_out) == len(list_should) or 
        not all(x == y for (x, y) in zip(list_out, list_should))):
          raise RuntimeError(
              'Failed test expand_crab_job_list("%s")' % list_in
              )
## End of test_expand_crab_job_list(...)


#______________________________________________________________________________
if __name__ == '__main__':
    test_expand_crab_job_list(1)
    import user