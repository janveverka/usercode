import os
import datetime
import Vgamma.Analysis.bookkeeping.march2013mmg as march2013mmg
import Vgamma.Analysis.bookkeeping.march2013eeg as march2013eeg
import Vgamma.Analysis.bookkeeping.test as test

#______________________________________________________________________________
def main():
    print 'START:', datetime.datetime.now().isoformat()

    to_process = [
        ('EEG', march2013mmg.samples), 
        ('MMG', march2013eeg.samples),
        ('TEST', test.samples)
        ]
        
    for name, samples in to_process:
        ## Give a heads-up
        print '==', name, '=='
        print 'Samples to process:', samples.keys()

        ## Loop over datasets
        for sample in (samples.values())[:]:
            total = sample.get_total_processed_events()
            if total == sample.total_processed_events:
                print sample.name, 'up to date'
            else:
                print sample.name, 'updating total_processed_events',
                print '%d -> %d' % (sample.total_processed_events, total)
                filename = os.path.join(samples.package.__path__[0], 
                                        sample.name + '.py')
                with file(filename, 'a') as pyfile:
                    line = ('%s.total_processed_events = '
                            '%s\n') % (sample.name, total)
                    pyfile.write(line)
        
    print 'FIN:', datetime.datetime.now().isoformat()

#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
