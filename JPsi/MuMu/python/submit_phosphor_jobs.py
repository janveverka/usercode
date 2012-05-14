#!/bin/env python
## Creates PHOSPHOR fit jobs for the OSG.

import os
import commands

# project_name = 'phosphor_baseline_s6mc_v2'
# project_name = 'test6'
project_name = 'eg_paper_dr0p1'

output_base = '/raid2/veverka/jobs/outputs'
template_filename='JPsi/MuMu/scripts/phosphor-job.template'

#______________________________________________________________________________
def get_egpaper_list():
    '''
    Returns a list of job names for plots for the EGM-11-001 paper.
    '''
    job_names = []

    total_sections = 4

    for subdet in 'EB EE'.split():
        for pt in '25to999'.split():
            for version in 'yyv3'.split():
                ## real data inclusive r9 job name
                name = '_'.join(['egm_data', subdet, 'pt'+pt, version])
                job_names.append(name)

                ## real data high r9 job name
                name = '_'.join(['egm_data', subdet, 'pt'+pt, 
                                 version, 'highR9'])
                job_names.append(name)

                ## monte carlo job names - same events of training and fit
                ## inclusive R9
                name = '_'.join(['egm_mc', subdet, 'pt'+pt, version])
                job_names.append(name)

                ## high r9
                name = '_'.join(['egm_mc', subdet, 'pt'+pt, 
                                 version, 'highR9'])
                job_names.append(name)
                
                
    ## Use only subsection of events for the training 
    ## and indepenedent events for MC fit
    for basename in job_names[:]:
        for section in range(1, total_sections + 1):
            part = 'evt%dof%d' % (section, total_sections)
            name = basename + '_' + part
            job_names.append(name)
            
    return job_names
## End of get_egpaper_list()


#______________________________________________________________________________
def get_large_list():
    job_names = []

    total_sections = 4

    for subdet in 'EB EE'.split():
        for r9 in 'highR9 lowR9'.split():
            for pt in '10to12 12to15 15to20 20to25 25to30 30to999'.split():
                for version in 'v13 v14 v15'.split():
                    ## real data job name
                    name = '_'.join(['sgetest_data', subdet, r9, 'pt'+pt,
                                     version])
                    job_names.append(name)

                    ## monte carlo job names
                    for section in range(1, total_sections + 1):
                        part = 'evt%dof%d' % (section, total_sections)
                        name = '_'.join(['sgetest_mc', subdet, r9, 
                                        'pt'+pt, version, part])
                        job_names.append(name)
    return job_names
## End of get_large_list()


#______________________________________________________________________________
def get_baseline_list():
    job_names = []

    total_sections = 4

    for subdet in 'EB EE'.split():
        for pt in '10to12 12to15 15to20 20to999'.split():
            for version in 'v13 v14 v15'.split():
                ## real data job name
                name = '_'.join(['sge_data', subdet, 'pt'+pt, version])
                job_names.append(name)

                ## monte carlo job names
                for section in range(1, total_sections + 1):
                    part = 'evt%dof%d' % (section, total_sections)
                    name = '_'.join(['sge_mc', subdet, 
                                    'pt'+pt, version, part])
                    job_names.append(name)
    return job_names
## End of get_large_list()


job_names = get_egpaper_list()
# job_names = get_baseline_list()
# job_names = get_large_list()

submission_dir = os.path.join(os.curdir, project_name)
output_dir = os.path.join(output_base, project_name)

for dir_path in [submission_dir, output_dir]:
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

template_path = os.path.join(os.environ['CMSSW_BASE'], 'src', 
                             template_filename)

print 'Submitting %d jobs:' % len(job_names)
for j in job_names:
    print j

with open(template_path, 'r') as template_file:
    template = template_file.read()
    for job_name in job_names:
        job_path = os.path.join(submission_dir, job_name + '.job')
        with open(job_path, 'w') as job_file:
            job_file.write(template.format(job_name=job_name,
                                           output_dir=output_dir))
            job_file.close()
            submission_cmd = 'qsub ' + job_path
            status, output = commands.getstatusoutput(submission_cmd)
            print output
            if status != 0:
                sys.exit('%s exited with status %d!' % submission_cmd, status)

print 'Submitted %d jobs with success!' % len(job_names)
